"""Demo runner for ECC-HISE batch envelope."""

import os

from prototype.ecc_hise.envelope import ECC_HISE_Receiver, ECC_HISE_Sender


def main() -> None:
    mk = os.urandom(32)
    sender = ECC_HISE_Sender(mk)
    receiver = ECC_HISE_Receiver(mk)
    records = [f"settlement-record-{i:04d}".encode() for i in range(10)]
    batch = sender.build_batch(records, batch_id="BATCH-2026-001", domain_id="settlement")
    recovered = receiver.verify_and_decrypt(batch, sender.public_key)
    assert recovered == records
    print("ECC-HISE batch OK")
    print(f"Records: {len(records)}")
    print(f"Total batch size: {batch.total_bytes} bytes")
    print(f"Merkle root: {batch.header.merkle_root.hex()[:32]}...")


if __name__ == "__main__":
    main()
