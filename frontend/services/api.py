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
    
    def patch(self, endpoint, data):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.patch(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=headers
        )

        return response
    
    def get_drivers(self):

        return self.get("/drivers/")


    def create_driver(self, data):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.post(
            f"{BASE_URL}/drivers/",
            json=data,
            headers=headers
        )


    def get_vehicles(self):

        return self.get("/vehicles")


    def create_vehicle(self, data):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.post(
            f"{BASE_URL}/vehicles",
            json=data,
            headers=headers
        )


    def update_vehicle_status(self, vehicle_id, status):

        return self.patch(
            f"/vehicles/{vehicle_id}/status",
            {
                "status": status
            }
        )
    
    def get_routes(self):

        return self.get("/routes")


    def create_route(self, data):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.post(
            f"{BASE_URL}/routes",
            json=data,
            headers=headers
        )
    
    def get_trips(self):

        return self.get("/trips")


    def create_trip(self, data):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.post(
            f"{BASE_URL}/trips",
            json=data,
            headers=headers
        )


    def update_trip_status(self, trip_id, status):

        return self.patch(
            f"/trips/{trip_id}/status",
            {
                "status": status
            }
        )
    
    def get_bookings(self):

        return self.get("/bookings/")


    def cancel_booking(self, booking_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/bookings/{booking_id}/cancel",
            headers=headers
        )

    def get_my_trips(self):

        return self.get("/drivers/me/trips")


    def start_trip(self, trip_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/drivers/{trip_id}/start",
            headers=headers
        )


    def complete_trip(self, trip_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/drivers/{trip_id}/complete",
            headers=headers
        )


    def get_trip_passengers(self, trip_id):

        return self.get(
            f"/drivers/{trip_id}/passengers"
        )

    def start_trip(self, trip_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/drivers/{trip_id}/start",
            headers=headers
        )


    def complete_trip(self, trip_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/drivers/{trip_id}/complete",
            headers=headers
        )

    def book_trip(self, trip_id, seats):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.post(
            f"{BASE_URL}/bookings",
            json={
                "trip_id": trip_id,
                "seats_booked": seats
            },
            headers=headers
        )

    def get_trips(self):
    
        return self.get("/trips/available")

    def get_my_bookings(self):
        return self.get("/bookings/me")

    def cancel_my_booking(self, booking_id):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        return requests.patch(
            f"{BASE_URL}/bookings/{booking_id}/cancel-me",
            headers=headers
        )