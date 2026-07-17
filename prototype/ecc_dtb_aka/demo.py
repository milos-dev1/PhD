"""Demo runner for ECC-DTB-AKA handshake."""

from prototype.common.crypto_utils import random_nonce
from prototype.ecc_dtb_aka.protocol import ECCDTBAKAClient, ECCDTBAKAServer, run_handshake


def main() -> None:
    device = b"demo-device-uuid-001"
    client = ECCDTBAKAClient(device)
    server = ECCDTBAKAServer({client.pk_client_bytes: client.pk_client})
    txn = random_nonce()
    state = run_handshake(client, server, txn)
    tbk = client.derive_tbk(txn)
    print("Handshake successful")
    print(f"MSK length: {len(state.msk)} bytes")
    print(f"TBK length: {len(tbk)} bytes")
    print(f"Device FP: {state.device_fp.hex()}")


if __name__ == "__main__":
    main()
