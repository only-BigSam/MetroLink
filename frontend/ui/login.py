import os
import customtkinter as ctk
from PIL import Image
from services.api import APIClient
from widgets.buttons import PrimaryButton
from widgets.entries import InputField
from ui.admin_dashboard import AdminDashboard

from config import (
    BACKGROUND,
    FRAME,
    TEXT,
    SECONDARY_TEXT,
)


class LoginPage:

    def __init__(self, root):
        self.root = root
        self.api = APIClient()
        self.build_ui()

    def build_ui(self):

        self.container = ctk.CTkFrame(
            self.root,
            fg_color=BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self.container,
            text="MetroLink",
            font=("Arial", 38, "bold"),
            text_color=TEXT
        )

        title.pack(
            pady=(40, 0)
        )

        subtitle = ctk.CTkLabel(
            self.container,
            text="Sign in to continue",
            font=("Arial", 18),
            text_color=SECONDARY_TEXT
        )

        subtitle.pack(
            pady=(5, 40)
        )

        self.center_frame = ctk.CTkFrame(
            self.container,
            fg_color=FRAME,
            width=430,
            height=330,
            corner_radius=15
        )

        self.center_frame.place(
            relx=0.5,
            rely=0.45,
            anchor="center"
        )

        self.email_entry = InputField(
            self.center_frame,
            placeholder="Email",
            width=300
        )

        self.email_entry.pack(
            pady=(40, 15)
        )

        self.password_entry = InputField(
            self.center_frame,
            placeholder="Password",
            show="*",
            width=300
        )

        self.password_entry.pack(
            pady=15
        )

        self.login_button = PrimaryButton(
            self.center_frame,
            text="Login",
            command=self.login,
            width=300
        )

        self.login_button.pack(
            pady=(25, 20)
        )

        self.message_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            font=("Arial", 13)
        )

        self.message_label.pack(pady=(5, 0))

        footer = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        footer.pack(
            side="bottom",
            anchor="w",
            padx=30,
            pady=20
        )

        sponsor = ctk.CTkLabel(
            footer,
            text="Brought to you by",
            text_color=SECONDARY_TEXT,
            font=("Arial", 13)
        )

        sponsor.pack(
            anchor="w"
        )

        logo_path = "assets/sponsor_logo.png"

        if os.path.exists(logo_path):

            image = Image.open(logo_path)

            logo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(160, 100)
            )

            company_logo = ctk.CTkLabel(
                footer,
                image=logo,
                text=""
            )

            company_logo.image = logo

            company_logo.pack(
                anchor="w",
                pady=(5, 8)
            )

        links = ctk.CTkLabel(
            footer,
            text="About   |   Contact Us   |   Privacy Policy   |   Terms",
            text_color=SECONDARY_TEXT,
            font=("Arial", 12)
        )

        links.pack(
            anchor="w"
        )

    def login(self):

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:

            self.message_label.configure(
                text="Please fill in all fields.",
                text_color="red"
            )

            return

        response = self.api.login(email, password)

        if response.status_code == 200:

            self.message_label.configure(
                text="Login successful!",
                text_color="green"
            )

            AdminDashboard(
                self.root,
                self.api
            )

        else:

            try:
                message = response.json().get(
                    "detail",
                    "Login failed."
                )

            except Exception:

                message = "Unable to contact server."

            self.message_label.configure(
                text=message,
                text_color="red"
            )