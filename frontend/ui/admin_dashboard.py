import customtkinter as ctk
from services.api import APIClient
from config import BACKGROUND, PRIMARY, PRIMARY_HOVER


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

        response = self.api.get("/users")

        if response.status_code != 200:

            error = ctk.CTkLabel(
                self.content,
                text="Unable to load users.",
                text_color="red",
                font=("Arial", 16)
            )

            error.pack(
                anchor="nw",
                padx=30
            )

            return

        users = response.json()

        for user in users:

            row = ctk.CTkFrame(
                self.content
            )

            row.pack(
                fill="x",
                padx=30,
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=f"{user['id']}"
            ).pack(
                side="left",
                padx=10
            )

            ctk.CTkLabel(
                row,
                text=user["name"]
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkLabel(
                row,
                text=user["email"]
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkLabel(
                row,
                text=user["role"]
            ).pack(
                side="right",
                padx=20
            )

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
            pady=30
        )

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
            pady=30
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
            pady=30
        )

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
            pady=30
        )

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
            pady=30
        )