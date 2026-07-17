"""Shared cryptographic utilities for thesis prototypes."""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

CURVE = ec.SECP256R1()
PROTOCOL_LABEL = b"ECC-DTB-AKA-v1"
TBK_LABEL = b"TBK"
CONFIRM_LABEL = b"confirm"
KEY_SIZE = 32


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def device_fingerprint(attributes: bytes) -> bytes:
    return sha256(attributes)[:16]


def hkdf_derive(ikm: bytes, salt: bytes, info: bytes, length: int = KEY_SIZE) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        info=info,
    ).derive(ikm)


def generate_ec_keypair() -> ec.EllipticCurvePrivateKey:
    return ec.generate_private_key(CURVE)


def ecdh_shared_secret(private_key: ec.EllipticCurvePrivateKey, peer_public: ec.EllipticCurvePublicKey) -> bytes:
    return private_key.exchange(ec.ECDH(), peer_public)


def sign(private_key: ec.EllipticCurvePrivateKey, message: bytes) -> bytes:
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))


def verify(public_key: ec.EllipticCurvePublicKey, message: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False


def public_key_bytes(public_key: ec.EllipticCurvePublicKey) -> bytes:
    return public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )


def load_public_key(data: bytes) -> ec.EllipticCurvePublicKey:
    return ec.EllipticCurvePublicKey.from_encoded_point(CURVE, data)


def compute_msk(shared: bytes, device_fp: bytes, nonce_c: bytes, nonce_s: bytes) -> bytes:
    salt = device_fp + nonce_c + nonce_s
    return hkdf_derive(shared, salt, PROTOCOL_LABEL, KEY_SIZE)


def derive_transaction_key(msk: bytes, txn_nonce: bytes) -> bytes:
    return hkdf_derive(msk, txn_nonce, TBK_LABEL, KEY_SIZE)


def hmac_tag(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def random_nonce(length: int = 16) -> bytes:
    return os.urandom(length)
