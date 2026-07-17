"""Benchmark ECC-HISE against baseline data-protection approaches."""

from __future__ import annotations

import json
import os
import statistics
import time
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from prototype.common.crypto_utils import hkdf_derive
from prototype.ecc_hise.envelope import ECC_HISE_Receiver, ECC_HISE_Sender

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "thesis" / "benchmarks"
RECORD_COUNTS = [10, 100, 500]
ITERATIONS = 50


def bench_hise(n_records: int) -> dict:
    mk = os.urandom(32)
    records = [os.urandom(256) for _ in range(n_records)]
    latencies = []
    sizes = []
    for _ in range(ITERATIONS):
        sender = ECC_HISE_Sender(mk)
        receiver = ECC_HISE_Receiver(mk)
        t0 = time.perf_counter()
        batch = sender.build_batch(records, f"B-{n_records}", "settlement")
        _ = receiver.verify_and_decrypt(batch, sender.public_key)
        latencies.append((time.perf_counter() - t0) * 1000)
        sizes.append(batch.total_bytes)
    return {
        "scheme": "ECC-HISE",
        "records": n_records,
        "latency_ms_mean": round(statistics.mean(latencies), 2),
        "latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "batch_bytes_mean": round(statistics.mean(sizes)),
        "merkle_audit": True,
        "hierarchical_keys": True,
        "per_record_signatures": True,
    }


def bench_static_aes(n_records: int) -> dict:
    key = os.urandom(32)
    records = [os.urandom(256) for _ in range(n_records)]
    latencies = []
    sizes = []
    for _ in range(ITERATIONS):
        t0 = time.perf_counter()
        total = 0
        for i, rec in enumerate(records):
            iv = os.urandom(12)
            ct = AESGCM(key).encrypt(iv, rec, b"static")
            total += len(ct) + len(iv)
        latencies.append((time.perf_counter() - t0) * 1000)
        sizes.append(total)
    return {
        "scheme": "Static AES-GCM PSK",
        "records": n_records,
        "latency_ms_mean": round(statistics.mean(latencies), 2),
        "latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "batch_bytes_mean": round(statistics.mean(sizes)),
        "merkle_audit": False,
        "hierarchical_keys": False,
        "per_record_signatures": False,
    }


def bench_tls_like(n_records: int) -> dict:
    """TLS record layer only — encrypt without audit/signatures."""
    key = os.urandom(32)
    records = [os.urandom(256) for _ in range(n_records)]
    latencies = []
    sizes = []
    for _ in range(ITERATIONS):
        t0 = time.perf_counter()
        total = 5  # simulated TLS record framing overhead per record
        for rec in records:
            iv = os.urandom(12)
            ct = AESGCM(key).encrypt(iv, rec, b"tls")
            total += len(ct) + len(iv) + 5
        latencies.append((time.perf_counter() - t0) * 1000)
        sizes.append(total)
    return {
        "scheme": "TLS record layer only",
        "records": n_records,
        "latency_ms_mean": round(statistics.mean(latencies), 2),
        "latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "batch_bytes_mean": round(statistics.mean(sizes)),
        "merkle_audit": False,
        "hierarchical_keys": False,
        "per_record_signatures": False,
    }


def main() -> None:
    results = []
    for n in RECORD_COUNTS:
        results.extend([bench_hise(n), bench_static_aes(n), bench_tls_like(n)])
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "chapter3_benchmarks.json"
    path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
