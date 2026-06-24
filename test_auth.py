from core.auth import (
    create_access_token,
    verify_access_token
)

token = create_access_token(
    {
        "sub": "john@example.com"
    }
)

print("TOKEN:")
print(token)

payload = verify_access_token(token)

print("\nPAYLOAD:")
print(payload)