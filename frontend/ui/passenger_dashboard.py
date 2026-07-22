import customtkinter as ctk
from tkinter import messagebox


class PassengerDashboard(ctk.CTkFrame):

    def __init__(self, parent, api):

        super().__init__(parent)

        self.root = parent
        self.api = api

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
            text="Passenger",
            font=("Arial", 28, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.sidebar,
            text="Available Trips",
            command=self.show_trips
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="My Bookings",
            command=self.show_bookings
        ).pack(fill="x", padx=15, pady=5)

        self.content = ctk.CTkFrame(self)

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_trips()

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

        for i, text in enumerate(headers):

            ctk.CTkLabel(
                self.table,
                text=text,
                font=("Arial", 14, "bold")
            ).grid(
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

    def show_trips(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Available Trips",
            font=("Arial", 30, "bold")
        ).pack(anchor="nw", padx=20, pady=20)

        self.create_table(
            [
                "ID",
                "Route",
                "Vehicle",
                "Departure",
                "Arrival",
                "Action"
            ]
        )

        response = self.api.get_trips()

        if response.status_code != 200:

            messagebox.showerror(
                "Error",
                "Unable to load trips."
            )
            return

        trips = response.json()

        for trip in trips:

            if trip["status"] != "SCHEDULED":
                continue

            self.add_row(
                [
                    trip["id"],
                    trip["route"],
                    trip["vehicle"],
                    trip["departure_time"],
                    trip["arrival_time"]
                ],
                button_text="Book",
                button_command=lambda t=trip: self.book_trip(t)
            )

    def book_trip(self, trip):

        dialog = ctk.CTkInputDialog(
            text="Number of seats:",
            title="Book Trip"
        )

        seats = dialog.get_input()

        if not seats:
            return

        response = self.api.book_trip(
            trip["id"],
            int(seats)
        )

        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Trip booked successfully."
            )

            self.show_trips()

        else:

            messagebox.showerror(
                "Error",
                response.json()["detail"]
            )

    def show_bookings(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="My Bookings",
            font=("Arial", 30, "bold")
        ).pack(anchor="nw", padx=20, pady=20)

        self.create_table(
            [
                "ID",
                "Route",
                "Seats",
                "Status",
                "Action"
            ]
        )

        response = self.api.get_my_bookings()

        if response.status_code != 200:
            return

        bookings = response.json()

        for booking in bookings:

            self.add_row(
                [
                    booking["id"],
                    booking["route_name"],
                    booking["seats_booked"],
                    booking["status"]
                ],
                button_text="Cancel",
                button_command=lambda b=booking: self.cancel_booking(b)
            )

    def cancel_booking(self, booking):

        confirm = messagebox.askyesno(
            "Cancel Booking",
            "Are you sure you want to cancel this booking?"
        )

        if not confirm:
            return

        response = self.api.cancel_my_booking(
            booking["id"]
        )

        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Booking cancelled successfully."
            )

            self.show_bookings()

        else:

            messagebox.showerror(
                "Error",
                response.json()["detail"]
            )