"""ECC-HISE secure envelope for server-server batch transfer."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from prototype.common.crypto_utils import hkdf_derive, sha256
from prototype.ecc_hise.hierarchy import KeyHierarchy
from prototype.ecc_hise.merkle import merkle_proof, merkle_root, verify_merkle_proof


@dataclass
class RecordEnvelope:
    index: int
    ciphertext: bytes
    iv: bytes
    signature: bytes
    metadata: bytes
    leaf_hash: bytes


@dataclass
class BatchHeader:
    batch_id: str
    epoch: int
    domain_id: str
    merkle_root: bytes
    sender_pk: bytes
    header_signature: bytes
    timestamp: float
    record_count: int


@dataclass
class SecureBatch:
    header: BatchHeader
    records: List[RecordEnvelope] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        h = self.header
        base = len(h.batch_id) + len(h.merkle_root) + len(h.sender_pk) + len(h.header_signature)
        rec_bytes = sum(len(r.ciphertext) + len(r.iv) + len(r.signature) + len(r.metadata) for r in self.records)
        return base + rec_bytes


class ECC_HISE_Sender:
    def __init__(self, master_key: bytes, signing_key: ed25519.Ed25519PrivateKey | None = None):
        self.master_key = master_key
        self.signing_key = signing_key or ed25519.Ed25519PrivateKey.generate()

    def build_batch(
        self,
        records: List[bytes],
        batch_id: str,
        domain_id: str,
        epoch: int | None = None,
    ) -> SecureBatch:
        epoch = epoch or int(time.time())
        hierarchy = KeyHierarchy(self.master_key, domain_id)
        sk_batch = hierarchy.session_key(batch_id, epoch)

        envelopes: list[RecordEnvelope] = []
        leaves: list[bytes] = []

        for idx, record in enumerate(records):
            k_enc = hkdf_derive(sk_batch, str(idx).encode(), b"ECC-HISE-AES", 32)
            iv = os.urandom(12)
            aad = batch_id.encode()
            ct = AESGCM(k_enc).encrypt(iv, record, aad)
            meta = json.dumps({"idx": idx, "batch": batch_id}).encode()
            sig_payload = sha256(ct + aad + str(idx).encode())
            sig = self.signing_key.sign(sig_payload)
            leaf = sha256(ct + sig + meta)
            leaves.append(leaf)
            envelopes.append(RecordEnvelope(idx, ct, iv, sig, meta, leaf))

        root = merkle_root(leaves)
        header_payload = batch_id.encode() + str(epoch).encode() + root
        header_sig = self.signing_key.sign(header_payload)
        header = BatchHeader(
            batch_id=batch_id,
            epoch=epoch,
            domain_id=domain_id,
            merkle_root=root,
            sender_pk=self.signing_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            ),
            header_signature=header_sig,
            timestamp=time.time(),
            record_count=len(records),
        )
        return SecureBatch(header, envelopes)

    @property
    def public_key(self) -> ed25519.Ed25519PublicKey:
        return self.signing_key.public_key()


class ECC_HISE_Receiver:
    def __init__(self, master_key: bytes):
        self.master_key = master_key

    def verify_and_decrypt(
        self,
        batch: SecureBatch,
        sender_public_key: ed25519.Ed25519PublicKey,
    ) -> List[bytes]:
        header = batch.header
        header_payload = header.batch_id.encode() + str(header.epoch).encode() + header.merkle_root
        sender_public_key.verify(header.header_signature, header_payload)

        hierarchy = KeyHierarchy(self.master_key, header.domain_id)
        sk_batch = hierarchy.session_key(header.batch_id, header.epoch)

        leaves = [r.leaf_hash for r in batch.records]
        if merkle_root(leaves) != header.merkle_root:
            raise ValueError("Merkle root mismatch")

        plaintexts: list[bytes] = []
        for rec in batch.records:
            aad = header.batch_id.encode()
            sig_payload = sha256(rec.ciphertext + aad + str(rec.index).encode())
            sender_public_key.verify(rec.signature, sig_payload)
            k_enc = hkdf_derive(sk_batch, str(rec.index).encode(), b"ECC-HISE-AES", 32)
            pt = AESGCM(k_enc).decrypt(rec.iv, rec.ciphertext, aad)
            plaintexts.append(pt)
            proof = merkle_proof(leaves, rec.index)
            if not verify_merkle_proof(rec.leaf_hash, header.merkle_root, proof):
                raise ValueError(f"Merkle proof failed for record {rec.index}")
        return plaintexts
