"""Hierarchical ECC key derivation for ECC-HISE."""

from __future__ import annotations

from dataclasses import dataclass

from prototype.common.crypto_utils import hkdf_derive, sha256

DK_LABEL = b"ECC-HISE-DK"
SK_LABEL = b"ECC-HISE-SK"


@dataclass
class KeyHierarchy:
    master_key: bytes
    domain_id: str

    def domain_key(self) -> bytes:
        salt = sha256(self.master_key + self.domain_id.encode())
        return hkdf_derive(self.master_key, salt, DK_LABEL, 32)

    def session_key(self, batch_id: str, epoch: int) -> bytes:
        dk = self.domain_key()
        info = f"{batch_id}:{epoch}".encode()
        return hkdf_derive(dk, info, SK_LABEL, 32)
