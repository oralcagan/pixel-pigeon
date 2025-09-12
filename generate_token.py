# Generate a secure token for your email service
import secrets

# Generate a secure 32-byte token
token = secrets.token_hex(32)
print(f"Generated token: {token}")

# You can also generate multiple tokens
print("\nGenerated tokens:")
for i in range(3):
    print(f"Token {i+1}: {secrets.token_hex(32)}")