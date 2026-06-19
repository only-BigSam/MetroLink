from core.security import (
    hash_password,
    verify_password
)

password = "mypassword123"

hashed = hash_password(password)

print("Hashed:", hashed)

print(
    verify_password(
        "mypassword123",
        hashed
    )
)