"""Integrated e-banking security API (ECC-DTB-AKA + ECC-HISE)."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prototype.common.crypto_utils import random_nonce
from prototype.ecc_dtb_aka.protocol import (
    ClientConfirm,
    ClientInit,
    ECCDTBAKAClient,
    ECCDTBAKAServer,
    ServerResponse,
    run_handshake,
)
from prototype.ecc_hise.envelope import ECC_HISE_Receiver, ECC_HISE_Sender

app = FastAPI(title="E-Banking Security Prototype", version="1.0.0")

# In-memory demo state
MASTER_KEY = os.urandom(32)
_clients: dict[str, ECCDTBAKAClient] = {}
_servers: dict[str, ECCDTBAKAServer] = {}
_pending_inits: dict[str, tuple[ClientInit, ServerResponse]] = {}


class RegisterRequest(BaseModel):
    device_id: str


class HandshakeInitResponse(BaseModel):
    session_id: str
    init: dict[str, str]


class HandshakeCompleteRequest(BaseModel):
    session_id: str
    txn_nonce_hex: str


class SettlementBatchRequest(BaseModel):
    batch_id: str
    domain_id: str = "settlement"
    records: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "schemes": "ECC-DTB-AKA, ECC-HISE"}


@app.post("/auth/register")
def register_client(req: RegisterRequest) -> dict[str, str]:
    client = ECCDTBAKAClient(req.device_id.encode())
    server = ECCDTBAKAServer({client.pk_client_bytes: client.pk_client})
    _clients[req.device_id] = client
    _servers[req.device_id] = server
    return {"device_id": req.device_id, "registered": "true"}


@app.post("/auth/handshake/init")
def handshake_init(req: RegisterRequest) -> HandshakeInitResponse:
    if req.device_id not in _clients:
        raise HTTPException(404, "Device not registered")
    client = _clients[req.device_id]
    server = _servers[req.device_id]
    init = client.create_init()
    response = server.process_init(init)
    session_id = init.nonce_c.hex()
    _pending_inits[session_id] = (init, response)
    return HandshakeInitResponse(
        session_id=session_id,
        init={
            "ek_public": init.ek_public.hex(),
            "pk_client": init.pk_client.hex(),
            "device_fp": init.device_fp.hex(),
            "nonce_c": init.nonce_c.hex(),
            "signature": init.signature.hex(),
            "server_ek": response.ek_public.hex(),
            "server_nonce": response.nonce_s.hex(),
        },
    )


@app.post("/auth/handshake/complete")
def handshake_complete(req: HandshakeCompleteRequest) -> dict[str, Any]:
    pending = _pending_inits.pop(req.session_id, None)
    if not pending:
        raise HTTPException(404, "Session not found")
    init, response = pending
    device_id = next(iter(_clients))
    client = _clients[device_id]
    server = _servers[device_id]
    txn_nonce = bytes.fromhex(req.txn_nonce_hex)
    confirm = client.process_response(init, response, txn_nonce)
    state = server.verify_confirm(init, response, confirm)
    return {
        "authenticated": True,
        "msk_length": len(state.msk),
        "device_fp": state.device_fp.hex(),
    }


@app.post("/settlement/submit-batch")
def submit_batch(req: SettlementBatchRequest) -> dict[str, Any]:
    sender = ECC_HISE_Sender(MASTER_KEY)
    receiver = ECC_HISE_Receiver(MASTER_KEY)
    records = [r.encode() for r in req.records]
    batch = sender.build_batch(records, req.batch_id, req.domain_id)
    recovered = receiver.verify_and_decrypt(batch, sender.public_key)
    if recovered != records:
        raise HTTPException(500, "Batch verification failed")
    return {
        "batch_id": req.batch_id,
        "record_count": len(records),
        "merkle_root": batch.header.merkle_root.hex(),
        "total_bytes": batch.total_bytes,
        "verified": True,
    }


def create_app() -> FastAPI:
    return app
