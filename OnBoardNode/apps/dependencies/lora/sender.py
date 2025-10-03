# OnBoardNode/apps/dependencies/lora/sender.py
# Simule le drone : construit une trame chiffrée AES-GCM et (plus tard) l’enverra en LoRa.
import json, time, secrets, struct, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DEV_ID   = int(os.getenv("DEV_ID", "7"))
KEY_HEX  = os.getenv("KEY_HEX", "00112233445566778899aabbccddeeff")  # clé de test
CTR      = int(os.getenv("CTR", "1"))          # compteur paramétrable
JSON_ONLY = os.getenv("JSON_ONLY") == "1"      # n'imprimer que le JSON (pour pipeline)

def build_frame(dev_id: int, ctr: int, lat: float, lng: float):
    key = bytes.fromhex(KEY_HEX)
    aes = AESGCM(key)
    header = struct.pack(">B I I", 1, dev_id, ctr)                     # VER=1
    nonce  = struct.pack(">I I I", dev_id, ctr, secrets.randbits(32))  # 12 octets
    payload = {"ts": int(time.time()), "lat": lat, "lng": lng}
    ct = aes.encrypt(nonce, json.dumps(payload).encode("utf-8"), header)  # ct||tag
    return {"header": header.hex(), "nonce": nonce.hex(), "ciphertext_tag": ct.hex()}

def try_send_over_lora(frame_json: str) -> bool:
    try:
        import sx126x  # TODO: remplacer par le vrai driver LoRa sur le Pi
        # Exemple côté Pi :
        # sx = sx126x.SX126x(...); sx.send(frame_json.encode("utf-8"))
        if not JSON_ONLY:
            print("[HARDWARE] Would send via SX126x (stub).")
        return True
    except Exception:
        if not JSON_ONLY:
            print("[DRY-RUN] No LoRa driver available. Frame will be printed:")
        print(frame_json)  # toujours imprimer la trame JSON
        return False

if __name__ == "__main__":
    frame = build_frame(DEV_ID, ctr=CTR, lat=45.4215, lng=-75.6972)
    try_send_over_lora(json.dumps(frame))