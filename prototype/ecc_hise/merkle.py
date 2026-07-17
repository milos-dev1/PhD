"""Merkle tree utilities for ECC-HISE audit chains."""

from __future__ import annotations

import hashlib
from typing import List, Tuple


def _hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def merkle_root(leaves: List[bytes]) -> bytes:
    if not leaves:
        return _hash(b"")
    layer = list(leaves)
    while len(layer) > 1:
        nxt: list[bytes] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(_hash(left + right))
        layer = nxt
    return layer[0]


def merkle_proof(leaves: List[bytes], index: int) -> List[Tuple[bytes, str]]:
    if index < 0 or index >= len(leaves):
        raise IndexError("leaf index out of range")
    proof: List[Tuple[bytes, str]] = []
    layer = list(leaves)
    idx = index
    while len(layer) > 1:
        sib_idx = idx - 1 if idx % 2 == 1 else idx + 1
        if sib_idx < len(layer):
            pos = "L" if sib_idx < idx else "R"
            proof.append((layer[sib_idx], pos))
        elif len(layer) % 2 == 1 and idx == len(layer) - 1:
            # Odd layer: last node pairs with itself
            proof.append((layer[idx], "R"))
        nxt: list[bytes] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(_hash(left + right))
        idx //= 2
        layer = nxt
    return proof


def verify_merkle_proof(leaf: bytes, root: bytes, proof: List[Tuple[bytes, str]]) -> bool:
    h = leaf
    for sibling, pos in proof:
        h = _hash(sibling + h) if pos == "L" else _hash(h + sibling)
    return h == root
