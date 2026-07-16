import customtkinter as ctk


class InputField(ctk.CTkEntry):
    def __init__(self, master, placeholder="", show=None, **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            show=show,
            height=45,
            corner_radius=10,
            font=("Arial", 14),
            **kwargs
        )