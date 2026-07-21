import customtkinter as ctk
from tkinter import messagebox
from services.api import APIClient
from config import BACKGROUND, PRIMARY, PRIMARY_HOVER
from ui.role_dialog import RoleDialog
from ui.create_driver_dialog import CreateDriverDialog
from ui.edit_driver_dialog import EditDriverDialog

class AdminDashboard:

    def __init__(self, root, api):

        self.root = root
        self.api = api
        self.build_ui()

    def build_ui(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.container = ctk.CTkFrame(
            self.root,
            fg_color=BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.sidebar = ctk.CTkFrame(
            self.container,
            width=220,
            fg_color=PRIMARY,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.content = ctk.CTkFrame(
            self.container,
            fg_color=BACKGROUND
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="MetroLink",
            font=("Arial", 26, "bold"),
            text_color="white"
        )

        title.pack(
            pady=(30, 40)
        )

        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Users", self.show_users),
            ("Drivers", self.show_drivers),
            ("Vehicles", self.show_vehicles),
            ("Routes", self.show_routes),
            ("Trips", self.show_trips),
            ("Bookings", self.show_bookings)
        ]

        for text, command in menu_items:

            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color=PRIMARY_HOVER,
                anchor="w"
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )

        logout = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#B22222",
            hover_color="#8B1A1A"
        )

        logout.pack(
            side="bottom",
            padx=20,
            pady=25,
            fill="x"
        )

        self.show_dashboard()

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def create_table(self, headers):

        self.table_container = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.table_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 20)
        )

        self.header_frame = ctk.CTkFrame(
            self.table_container,
            fg_color="#EAEAEA"
        )

        self.header_frame.pack(fill="x")

        widths = {
            "ID": 60,
            "Name": 180,
            "Email": 250,
            "Role": 120,
            "License": 180,
            "Plate": 120,
            "Capacity": 100,
            "Status": 120,
            "Origin": 170,
            "Destination": 170,
            "Distance": 100,
            "Fare": 100,
            "Route": 220,
            "Driver": 180,
            "Vehicle": 120,
            "Departure": 170,
            "Arrival": 170,
            "Action": 100
        }

        for text in headers:

            label = ctk.CTkLabel(
                self.header_frame,
                text=text,
                width=widths.get(text, 150),
                anchor="w",
                font=("Arial", 14, "bold")
            )

            label.pack(
                side="left",
                padx=5,
                pady=10
            )

        self.rows_frame = ctk.CTkScrollableFrame(
            self.table_container,
            fg_color="transparent"
        )

        self.rows_frame.pack(
            fill="both",
            expand=True
        )

        self.row_count = 0

    def add_table_row(self, values, button_text=None, command=None):

        bg = "#FFFFFF"

        if self.row_count % 2:
            bg = "#F6F6F6"

        row = ctk.CTkFrame(
            self.rows_frame,
            fg_color=bg
        )

        row.pack(
            fill="x",
            pady=2
        )

        widths = {
            0: 60,
            1: 220,
            2: 180,
            3: 120,
            4: 120,
            5: 170,
            6: 170
        }

        for i, value in enumerate(values):

            label = ctk.CTkLabel(
                row,
                text=str(value),
                width=widths.get(i, 120),
                anchor="w"
            )

            label.pack(
                side="left",
                padx=5,
                pady=8
            )

        if button_text:

            action_frame = ctk.CTkFrame(
                row,
                fg_color="transparent",
                width=100
            )

            action_frame.pack(
                side="left",
                padx=5
            )

            button = ctk.CTkButton(
                action_frame,
                text=button_text,
                width=80,
                command=command
            )

            button.pack()

        self.row_count += 1

    def clear_table(self):

        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        self.row_count = 0

    def show_dashboard(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Admin Dashboard",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=30
        )

    def show_users(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Users",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30, 15)
        )

        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_users
        )

        refresh.pack(
            side="left"
        )

        self.create_table(
            [
                "ID",
                "Name",
                "Email",
                "Role",
                "Action"
            ]
        )

        response = self.api.get("/users")

        if response.status_code == 200:

            users = response.json()

            for user in users:

                self.add_table_row(
                    [
                        user["id"],
                        user["name"],
                        user["email"],
                        user["role"]
                    ],
                    button_text="Edit",
                    command=lambda u=user: self.edit_user_role(u)
                )

    def populate_users(self, users):

        self.table.clear()

        for user in users:

            self.table.add_row(
                [
                    user["id"],
                    user["name"],
                    user["email"],
                    user["role"]
                ],
                button_text="Edit",
                button_command=lambda u=user: self.edit_user_role(u)
            )
        
    def populate_drivers(self, drivers):

        self.driver_table.clear()

        for driver in drivers:

            self.driver_table.add_row(
                [
                    driver["id"],
                    driver["name"],
                    driver["email"],
                    driver["license_number"]
                ],
                button_text="Edit",
                button_command=lambda d=driver: self.edit_driver(d)
            )


    def edit_driver(self, driver):

        EditDriverDialog(
            self.root,
            driver,
            self.save_driver_changes
        )

    def save_driver_changes(self, driver_id, data):

        print(driver_id)
        print(data)

    def edit_user_role(self, user):

        RoleDialog(
            self.root,
            user,
            self.save_user_role
        )

    def save_user_role(self, user, new_role):

        response = self.api.patch(
            f"/users/{user['id']}/role",
            {
                "role": new_role.upper()
            }
        )

        if response.status_code == 200:

            self.show_users()

        else:

            print(response.text)

    def filter_users(self, event=None):

        search = self.search_entry.get().lower()

        filtered = []

        for user in self.users:

            if (
                search in user["name"].lower()
                or search in user["email"].lower()
                or search in user["role"].lower()
            ):
                filtered.append(user)

        self.populate_users(filtered)

    def filter_drivers(self, event=None):

        search = self.driver_search.get().lower()

        filtered = []

        for driver in self.drivers:

            if (
                search in str(driver["id"]).lower()
                or search in driver["name"].lower()
                or search in driver["email"].lower()
                or search in driver["license_number"].lower()
            ):
                filtered.append(driver)

        self.populate_drivers(filtered)

    def create_driver(self):

        CreateDriverDialog(
            self.root,
            self.save_driver
        )

    def save_driver(self, data):

        response = self.api.create_driver(data)

        print(response.status_code)

        try:
            print(response.json())
        except Exception:
            print(response.text)

        if response.status_code == 200:

            self.show_drivers()

    def show_drivers(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Drivers",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30, 15)
        )

        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_drivers
        )

        refresh.pack(
            side="left"
        )

        create = ctk.CTkButton(
            controls,
            text="+ New Driver",
            command=self.create_driver
        )

        create.pack(
            side="left",
            padx=10
        )

        self.create_table(
            [
                "ID",
                "Name",
                "Email",
                "License",
                "Action"
            ]
        )

        response = self.api.get_drivers()

        if response.status_code == 200:

            drivers = response.json()

            for driver in drivers:

                self.add_table_row(
                    [
                        driver["id"],
                        driver["name"],
                        driver["email"],
                        driver["license_number"]
                    ],
                    button_text="Edit",
                    command=lambda d=driver: self.edit_driver(d)
                )

    def create_vehicle(self):
        print("Create Vehicle")


    def edit_vehicle(self, vehicle):
        print(vehicle)

    def show_vehicles(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Vehicles",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30, 15)
        )

        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_vehicles
        )

        refresh.pack(side="left")

        create = ctk.CTkButton(
            controls,
            text="+ New Vehicle",
            command=self.create_vehicle
        )

        create.pack(
            side="left",
            padx=10
        )

        self.create_table(
            [
                "ID",
                "Plate Number",
                "Capacity",
                "Status",
                "Action"
            ]
        )

        response = self.api.get_vehicles()

        if response.status_code == 200:

            vehicles = response.json()

            for vehicle in vehicles:

                self.add_table_row(
                    [
                        vehicle["id"],
                        vehicle["plate_number"],
                        vehicle["capacity"],
                        vehicle["status"]
                    ],
                    button_text="Edit",
                    command=lambda v=vehicle: self.edit_vehicle(v)
                )

    def show_routes(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Routes",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30, 15)
        )


        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0,15)
        )


        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_routes
        )

        refresh.pack(
            side="left"
        )


        create = ctk.CTkButton(
            controls,
            text="+ New Route",
            command=self.create_route
        )

        create.pack(
            side="left",
            padx=10
        )


        self.create_table(
            [
                "ID",
                "Origin",
                "Destination",
                "Distance",
                "Action"
            ]
        )


        response = self.api.get_routes()


        if response.status_code == 200:

            routes = response.json()


            for route in routes:

                self.add_table_row(
                    [
                        route["id"],
                        route["origin"],
                        route["destination"],
                        route["distance"]
                    ],
                    button_text="Edit",
                    command=lambda r=route: self.edit_route(r)
                )

    def create_route(self):

        print("Create Route")


    def edit_route(self, route):

        print(route)

    

    def show_trips(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Trips",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30,15)
        )

        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0,15)
        )

        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_trips
        )

        refresh.pack(side="left")

        create = ctk.CTkButton(
            controls,
            text="+ New Trip",
            command=self.create_trip
        )

        create.pack(
            side="left",
            padx=10
        )

        self.create_table(
            [
                "ID",
                "Route",
                "Driver",
                "Vehicle",
                "Status",
                "Action"
            ]
        )

        response = self.api.get_trips()

        if response.status_code == 200:

            trips = response.json()

            for trip in trips:

                self.add_table_row(
                    [
                        trip["id"],
                        trip["route"],
                        trip["driver"],
                        trip["vehicle"],
                        trip["status"]
                    ],
                    button_text="Edit",
                    command=lambda t=trip: self.edit_trip(t)
                )

    def create_trip(self):

        print("Create Trip")


    def edit_trip(self, trip):

        print(trip)

    def show_bookings(self):

        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Bookings",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="nw",
            padx=30,
            pady=(30,15)
        )

        controls = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        controls.pack(
            fill="x",
            padx=30,
            pady=(0,15)
        )

        refresh = ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.show_bookings
        )

        refresh.pack(side="left")

        self.create_table(
            [
                "ID",
                "Passenger",
                "Route",
                "Seats",
                "Status",
                "Action"
            ]
        )

        response = self.api.get_bookings()

        if response.status_code == 200:

            bookings = response.json()

            for booking in bookings:

                self.add_table_row(
                    [
                        booking["id"],
                        booking["passenger_name"],
                        booking["route_name"],
                        booking["seats_booked"],
                        booking["booking_status"]
                    ],
                    button_text="Cancel",
                    command=lambda b=booking: self.cancel_booking(b)
                )

    def cancel_booking(self, booking):

        result = messagebox.askyesno(
            "Cancel Booking",
            f"Cancel booking #{booking['id']}?"
        )

        if not result:
            return

        response = self.api.cancel_booking(
            booking["id"]
        )

        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Booking cancelled."
            )

            self.show_bookings()

        else:

            messagebox.showerror(
                "Error",
                response.json()["detail"]
            )