import customtkinter as ctk
from config import PRIMARY, PRIMARY_HOVER


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color="white",
            corner_radius=10,
            height=45,
            font=("Arial", 15, "bold"),
            **kwargs
        )