import customtkinter as ctk
from tkinter import messagebox

from services.api import APIClient


class DriverDashboard(ctk.CTkFrame):

    def __init__(self, parent, api):

        super().__init__(parent)

        self.api = api
        self.root = parent

        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Driver",
            font=("Arial", 28, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.sidebar,
            text="My Trips",
            command=self.show_my_trips
        ).pack(fill="x", padx=15, pady=5)

        self.content = ctk.CTkFrame(self)

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_my_trips()

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def create_table(self, headers):

        self.table = ctk.CTkFrame(self.content)

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.headers = headers

        for i, text in enumerate(headers):

            label = ctk.CTkLabel(
                self.table,
                text=text,
                font=("Arial", 14, "bold")
            )

            label.grid(
                row=0,
                column=i,
                padx=10,
                pady=10,
                sticky="w"
            )

        self.current_row = 1

    def add_row(self, values, button_text=None, button_command=None):

        row = self.current_row

        for column, value in enumerate(values):

            ctk.CTkLabel(
                self.table,
                text=str(value)
            ).grid(
                row=row,
                column=column,
                padx=10,
                pady=8,
                sticky="w"
            )

        if button_text:

            ctk.CTkButton(
                self.table,
                text=button_text,
                width=90,
                command=button_command
            ).grid(
                row=row,
                column=len(values),
                padx=10
            )

        self.current_row += 1

    def show_my_trips(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="My Trips",
            font=("Arial", 30, "bold")
        ).pack(anchor="nw", padx=20, pady=20)

        self.create_table(
            [
                "Route",
                "Departure",
                "Arrival",
                "Vehicle",
                "Status",
                "Action"
            ]
        )

        response = self.api.get_my_trips()

        print(response.status_code)

        if response.status_code != 200:
            print(response.text)

        if response.status_code == 200:

            trips = response.json()

            for trip in trips:

                self.add_row(
                    [
                        trip["route_name"],
                        trip["departure_time"],
                        trip["arrival_time"],
                        trip["vehicle_number"],
                        trip["trip_status"]
                    ],
                    button_text="Manage",
                    button_command=lambda t=trip: self.manage_trip(t)
                )

    def manage_trip(self, trip):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Manage Trip",
            font=("Arial", 30, "bold")
        ).pack(anchor="nw", padx=20, pady=20)

        info = ctk.CTkFrame(self.content)

        info.pack(
            fill="x",
            padx=20,
            pady=20
        )

        details = [
            ("Route", trip["route_name"]),
            ("Vehicle", trip["vehicle_number"]),
            ("Departure", trip["departure_time"]),
            ("Arrival", trip["arrival_time"]),
            ("Status", trip["trip_status"])
        ]

        for label, value in details:

            ctk.CTkLabel(
                info,
                text=f"{label}: {value}",
                anchor="w",
                font=("Arial", 15)
            ).pack(anchor="w", pady=5)

        buttons = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        buttons.pack(pady=25)

        ctk.CTkButton(
            buttons,
            text="Start Trip",
            command=lambda: self.start_trip(trip)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="Complete Trip",
            command=lambda: self.complete_trip(trip)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="Passengers",
            command=lambda: self.show_passengers(trip)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.content,
            text="← Back",
            command=self.show_my_trips
        ).pack(pady=20)

    def start_trip(self, trip):

        response = self.api.start_trip(trip["trip_id"])

        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Trip started successfully."
            )

            self.show_my_trips()

        else:

            try:
                message = response.json()["detail"]
            except Exception:
                message = "Unable to start trip."

            messagebox.showerror(
                "Error",
                message
            )

    def complete_trip(self, trip):

        response = self.api.complete_trip(trip["trip_id"])

        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Trip completed successfully."
            )

            self.show_my_trips()

        else:

            try:
                message = response.json()["detail"]
            except Exception:
                message = "Unable to complete trip."

            messagebox.showerror(
                "Error",
                message
            )

    def show_passengers(self, trip):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Passengers",
            font=("Arial", 30, "bold")
        ).pack(anchor="nw", padx=20, pady=20)

        self.create_table(
            [
                "Name",
                "Email",
                "Seats"
            ]
        )

        response = self.api.get_trip_passengers(
            trip["trip_id"]
        )

        if response.status_code == 200:

            passengers = response.json()

            for passenger in passengers:

                self.add_row(
                    [
                        passenger["passenger_name"],
                        passenger["passenger_email"],
                        passenger["seats_booked"]
                    ]
                )

        else:

            try:
                message = response.json()["detail"]
            except Exception:
                message = "Unable to load passengers."

            messagebox.showerror(
                "Error",
                message)

        ctk.CTkButton(
            self.content,
            text="← Back",
            command=lambda: self.manage_trip(trip)
        ).pack(pady=20)