import customtkinter as ctk

from config import BACKGROUND, FRAME, TEXT, PRIMARY


class AdminDashboard:

    def __init__(self, root):

        self.root = root

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
            "Dashboard",
            "Users",
            "Drivers",
            "Vehicles",
            "Routes",
            "Trips",
            "Bookings"
        ]

        for item in menu_items:

            button = ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#D96D00",
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

        heading = ctk.CTkLabel(
            self.content,
            text="Admin Dashboard",
            font=("Arial", 30, "bold"),
            text_color=TEXT
        )

        heading.pack(
            anchor="nw",
            padx=30,
            pady=30
        )