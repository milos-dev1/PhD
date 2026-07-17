"""ECC-DTB-AKA protocol implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from cryptography.hazmat.primitives.asymmetric import ec

from prototype.common.crypto_utils import (
    CONFIRM_LABEL,
    compute_msk,
    derive_transaction_key,
    device_fingerprint,
    generate_ec_keypair,
    hmac_tag,
    load_public_key,
    public_key_bytes,
    random_nonce,
    sha256,
    sign,
    verify,
)


@dataclass
class ClientInit:
    ek_public: bytes
    pk_client: bytes
    device_fp: bytes
    nonce_c: bytes
    signature: bytes

    @property
    def message_size(self) -> int:
        return len(self.ek_public) + len(self.pk_client) + len(self.device_fp) + len(self.nonce_c) + len(self.signature)


@dataclass
class ServerResponse:
    ek_public: bytes
    nonce_s: bytes
    cert_server: bytes
    signature: bytes

    @property
    def message_size(self) -> int:
        return len(self.ek_public) + len(self.nonce_s) + len(self.cert_server) + len(self.signature)


@dataclass
class ClientConfirm:
    txn_mac: bytes
    txn_nonce: bytes
    signature: bytes

    @property
    def message_size(self) -> int:
        return len(self.txn_mac) + len(self.txn_nonce) + len(self.signature)


@dataclass
class SessionState:
    msk: bytes
    device_fp: bytes
    nonce_c: bytes
    nonce_s: bytes


@dataclass
class ServerSession:
    msk: bytes
    init: ClientInit
    response: ServerResponse


class ECCDTBAKAClient:
    def __init__(self, device_attributes: bytes):
        self.long_term_key = generate_ec_keypair()
        self.pk_client = self.long_term_key.public_key()
        self.pk_client_bytes = public_key_bytes(self.pk_client)
        self.device_fp = device_fingerprint(device_attributes)
        self._eph_private: Optional[ec.EllipticCurvePrivateKey] = None
        self._nonce_c: Optional[bytes] = None
        self.session: Optional[SessionState] = None

    def create_init(self) -> ClientInit:
        self._eph_private = generate_ec_keypair()
        ek_public = public_key_bytes(self._eph_private.public_key())
        self._nonce_c = random_nonce()
        transcript = ek_public + self.pk_client_bytes + self.device_fp + self._nonce_c
        sig = sign(self.long_term_key, sha256(transcript))
        return ClientInit(ek_public, self.pk_client_bytes, self.device_fp, self._nonce_c, sig)

    def process_response(self, init: ClientInit, response: ServerResponse, txn_nonce: bytes) -> ClientConfirm:
        if not self._eph_private or not self._nonce_c:
            raise ValueError("Client handshake not started")
        ek_server = load_public_key(response.ek_public)
        shared = self._eph_private.exchange(ec.ECDH(), ek_server)
        msk = compute_msk(shared, init.device_fp, init.nonce_c, response.nonce_s)
        server_pk = load_public_key(response.cert_server)
        verify_data = response.ek_public + response.nonce_s + msk
        if not verify(server_pk, sha256(verify_data), response.signature):
            raise ValueError("Invalid server signature")
        self.session = SessionState(msk, init.device_fp, init.nonce_c, response.nonce_s)
        tbk = derive_transaction_key(msk, txn_nonce)
        return ClientConfirm(hmac_tag(tbk, txn_nonce), txn_nonce, sign(self.long_term_key, sha256(msk + CONFIRM_LABEL)))

    def derive_tbk(self, txn_nonce: bytes) -> bytes:
        if not self.session:
            raise ValueError("No active session")
        return derive_transaction_key(self.session.msk, txn_nonce)


class ECCDTBAKAServer:
    def __init__(self, registered_clients: dict[bytes, ec.EllipticCurvePublicKey]):
        self.long_term_key = generate_ec_keypair()
        self.pk_server_bytes = public_key_bytes(self.long_term_key.public_key())
        self.registered_clients = registered_clients
        self._pending: dict[bytes, ServerSession] = {}

    def process_init(self, init: ClientInit) -> ServerResponse:
        if init.pk_client not in self.registered_clients:
            raise ValueError("Unregistered client")
        pk_client = self.registered_clients[init.pk_client]
        transcript = init.ek_public + init.pk_client + init.device_fp + init.nonce_c
        if not verify(pk_client, sha256(transcript), init.signature):
            raise ValueError("Invalid client signature")
        eph_private = generate_ec_keypair()
        ek_server_bytes = public_key_bytes(eph_private.public_key())
        ek_client = load_public_key(init.ek_public)
        shared = eph_private.exchange(ec.ECDH(), ek_client)
        nonce_s = random_nonce()
        msk = compute_msk(shared, init.device_fp, init.nonce_c, nonce_s)
        sig = sign(self.long_term_key, sha256(ek_server_bytes + nonce_s + msk))
        response = ServerResponse(ek_server_bytes, nonce_s, self.pk_server_bytes, sig)
        session_key = init.nonce_c + nonce_s
        self._pending[session_key] = ServerSession(msk, init, response)
        return response

    def verify_confirm(self, init: ClientInit, response: ServerResponse, confirm: ClientConfirm) -> SessionState:
        session_key = init.nonce_c + response.nonce_s
        pending = self._pending.pop(session_key, None)
        if not pending:
            raise ValueError("Unknown session")
        pk_client = self.registered_clients[init.pk_client]
        if not verify(pk_client, sha256(pending.msk + CONFIRM_LABEL), confirm.signature):
            raise ValueError("Invalid client confirm signature")
        tbk = derive_transaction_key(pending.msk, confirm.txn_nonce)
        if not hmac_tag(tbk, confirm.txn_nonce) == confirm.txn_mac:
            raise ValueError("Invalid transaction MAC")
        return SessionState(pending.msk, init.device_fp, init.nonce_c, response.nonce_s)


def run_handshake(client: ECCDTBAKAClient, server: ECCDTBAKAServer, txn_nonce: bytes | None = None) -> SessionState:
    txn_nonce = txn_nonce or random_nonce()
    init = client.create_init()
    response = server.process_init(init)
    confirm = client.process_response(init, response, txn_nonce)
    return server.verify_confirm(init, response, confirm)
