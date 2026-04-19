# generate_keys.py
from Crypto.PublicKey import RSA

def main():
    key = RSA.generate(4096)
    with open("shark_private.pem", "wb") as f:
        f.write(key.export_key())
    with open("shark_public.pem", "wb") as f:
        f.write(key.publickey().export_key())
    print("[+] Keys generated successfully")
    print(f"[+] Public key:\n{key.publickey().export_key().decode()}")

if __name__ == "__main__":
    main()