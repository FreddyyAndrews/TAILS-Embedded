import json, time, secrets, struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DEV_ID = 7                   # doit exister dans gateway/keys.json
CTR = 1                      # incremente à chaque message
KEY_HEX = "00112233445566778899aabbccddeeff"  # même que keys.json

def make_frame(dev_id: int, ctr: int, lat: float, lng: float):
    key = bytes.fromhex(KEY_HEX)
    aes = AESGCM(key)

    header = struct.pack(">B I I", 1, dev_id, ctr)                    # VER=1
    nonce  = struct.pack(">I I I", dev_id, ctr, secrets.randbits(32)) # 12B

    payload = {"ts": int(time.time()), "lat": lat, "lng": lng}
    plaintext = json.dumps(payload).encode("utf-8")

    ct = aes.encrypt(nonce, plaintext, header)  # ciphertext + tag (16B)
    return header, nonce, ct

if __name__ == "__main__":
    h, n, c = make_frame(DEV_ID, CTR, 45.4215, -75.6972)
    print(json.dumps({
        "header": h.hex(),
        "nonce": n.hex(),
        "ciphertext_tag": c.hex()
    }, indent=2))