"""Benchmark ECC-DTB-AKA against baseline approaches."""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ec

from prototype.common.crypto_utils import (
    compute_msk,
    device_fingerprint,
    generate_ec_keypair,
    public_key_bytes,
    random_nonce,
)
from prototype.ecc_dtb_aka.protocol import ECCDTBAKAClient, ECCDTBAKAServer, run_handshake

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "thesis" / "benchmarks"
ITERATIONS = 200


def bench_dtb_aka() -> dict:
    device_attrs = b"mobile-ios-17-uuid-abc123"
    client = ECCDTBAKAClient(device_attrs)
    server = ECCDTBAKAServer({client.pk_client_bytes: client.pk_client})

    latencies = []
    msg_sizes = []
    for _ in range(ITERATIONS):
        c = ECCDTBAKAClient(device_attrs)
        s = ECCDTBAKAServer({c.pk_client_bytes: c.pk_client})
        txn = random_nonce()
        t0 = time.perf_counter()
        init = c.create_init()
        resp = s.process_init(init)
        confirm = c.process_response(init, resp, txn)
        state = s.verify_confirm(init, resp, confirm)
        latencies.append((time.perf_counter() - t0) * 1000)
        msg_sizes.append(init.message_size + resp.message_size + confirm.message_size)

    return {
        "scheme": "ECC-DTB-AKA",
        "round_trips": 3,
        "auth_latency_ms_mean": round(statistics.mean(latencies), 2),
        "auth_latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "total_message_bytes_mean": round(statistics.mean(msg_sizes)),
        "device_binding": True,
        "transaction_binding": True,
        "forward_secrecy": True,
        "mutual_auth": True,
    }


def bench_standard_ecdh() -> dict:
    latencies = []
    msg_sizes = []
    for _ in range(ITERATIONS):
        c_priv = generate_ec_keypair()
        s_priv = generate_ec_keypair()
        c_pub = c_priv.public_key()
        s_pub = s_priv.public_key()
        t0 = time.perf_counter()
        shared_c = c_priv.exchange(ec.ECDH(), s_pub)
        shared_s = s_priv.exchange(ec.ECDH(), c_pub)
        msk = compute_msk(shared_c, b"\x00" * 16, random_nonce(), random_nonce())
        latencies.append((time.perf_counter() - t0) * 1000)
        msg_sizes.append(len(public_key_bytes(c_pub)) + len(public_key_bytes(s_pub)))
    return {
        "scheme": "Standard ECDH",
        "round_trips": 2,
        "auth_latency_ms_mean": round(statistics.mean(latencies), 2),
        "auth_latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "total_message_bytes_mean": round(statistics.mean(msg_sizes)),
        "device_binding": False,
        "transaction_binding": False,
        "forward_secrecy": True,
        "mutual_auth": False,
    }


def bench_tls13_estimated() -> dict:
    # TLS 1.3 1-RTT handshake crypto core (ECDH + cert verify) without network I/O
    latencies = []
    for _ in range(ITERATIONS):
        c_priv = generate_ec_keypair()
        s_priv = generate_ec_keypair()
        s_lt = generate_ec_keypair()
        t0 = time.perf_counter()
        _ = c_priv.exchange(ec.ECDH(), s_priv.public_key())
        _ = s_priv.exchange(ec.ECDH(), c_priv.public_key())
        # Simulated certificate signature verification cost
        from prototype.common.crypto_utils import sha256, sign, verify

        msg = random_nonce(32)
        sig = sign(s_lt, sha256(msg))
        verify(s_lt.public_key(), sha256(msg), sig)
        latencies.append((time.perf_counter() - t0) * 1000)
    return {
        "scheme": "TLS 1.3 (crypto core)",
        "round_trips": 1,
        "auth_latency_ms_mean": round(statistics.mean(latencies), 2),
        "auth_latency_ms_stdev": round(statistics.stdev(latencies), 2),
        "total_message_bytes_mean": 2800,
        "device_binding": False,
        "transaction_binding": False,
        "forward_secrecy": True,
        "mutual_auth": "server_only",
    }


def main() -> None:
    results = [bench_dtb_aka(), bench_standard_ecdh(), bench_tls13_estimated()]
    OUT.mkdir(parents=True, exist_ok=True)
    out_file = OUT / "chapter2_benchmarks.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
