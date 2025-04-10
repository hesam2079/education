from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption,
)

# 1. تولید کلید خصوصی و عمومی
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# تابعی برای امضای پیام
def sign_message(message: str, private_key):
    # تبدیل پیام به بایت‌ها
    message_bytes = message.encode('utf-8')
    # امضای پیام
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

# تابعی برای تأیید امضای پیام
def verify_signature(message: str, signature, public_key):
    message_bytes = message.encode('utf-8')
    try:
        # تأیید امضا
        public_key.verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False

# 2. ارسال پیام با امضا
message = "Hello, this is a secure message."
signature = sign_message(message, private_key)

print("Message:", message)
print("Signature:", signature.hex())

# 3. تأیید امضا در سمت دریافت‌کننده
is_valid = verify_signature(message, signature, public_key)

if is_valid:
    print("The signature is valid.")
else:
    print("The signature is NOT valid.")
