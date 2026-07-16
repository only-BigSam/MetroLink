import requests

from config import BASE_URL


class APIClient:

    def __init__(self):

        self.token = None

    def login(self, email, password):

        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:

            data = response.json()

            self.token = data["access_token"]

        return response

    def get(self, endpoint):

        headers = {}

        if self.token:

            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers
        )

        return response