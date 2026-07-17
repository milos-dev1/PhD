"""End-to-end integration demo for both security schemes."""

from prototype.api.app import app
from prototype.common.crypto_utils import random_nonce
from fastapi.testclient import TestClient


def main() -> None:
    client = TestClient(app)
    assert client.get("/health").json()["status"] == "ok"

    device_id = "mobile-device-001"
    client.post("/auth/register", json={"device_id": device_id})
    init_resp = client.post("/auth/handshake/init", json={"device_id": device_id})
    session_id = init_resp.json()["session_id"]
    complete = client.post(
        "/auth/handshake/complete",
        json={"session_id": session_id, "txn_nonce_hex": random_nonce().hex()},
    )
    assert complete.json()["authenticated"] is True

    batch = client.post(
        "/settlement/submit-batch",
        json={
            "batch_id": "BATCH-DEMO-001",
            "records": ["payment-001", "payment-002", "payment-003"],
        },
    )
    data = batch.json()
    assert data["verified"] is True
    print("Integration demo OK")
    print(f"Auth MSK length: {complete.json()['msk_length']}")
    print(f"Batch records: {data['record_count']}, root: {data['merkle_root'][:32]}...")


if __name__ == "__main__":
    main()
