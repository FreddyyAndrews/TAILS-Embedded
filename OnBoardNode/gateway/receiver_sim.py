import json, sys
from crypto import decrypt_frame
from replay_guard import check_and_update

if __name__ == "__main__":
    raw = sys.stdin.read()
    obj = json.loads(raw)
    data = decrypt_frame(obj["header"], obj["nonce"], obj["ciphertext_tag"])
    if not check_and_update(data["dev_id"], data["ctr"]):
        print("REJECTED: replay detected (CTR not increasing).")
        sys.exit(1)
    print("ACCEPTED:", json.dumps(data, indent=2))