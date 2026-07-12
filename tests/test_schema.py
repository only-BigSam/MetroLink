from backend.schemas.user import UserRegister

user = UserRegister(
    name="Samuel Daniel",
    email="samuel@example.com",
    password="password123"
)

print(user)