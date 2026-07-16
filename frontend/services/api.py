import requests

from config import BASE_URL


class APIClient:

    def login(self, email, password):

        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        return response