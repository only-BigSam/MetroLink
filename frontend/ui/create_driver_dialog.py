import customtkinter as ctk


class CreateDriverDialog(ctk.CTkToplevel):

    def __init__(self, parent, callback):

        super().__init__(parent)

        self.callback = callback

        self.title("Create Driver")
        self.geometry("350x320")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Create Driver",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 20))

        self.user_id = ctk.CTkEntry(
            self,
            placeholder_text="User ID"
        )

        self.user_id.pack(
            padx=30,
            fill="x",
            pady=8
        )

        self.license = ctk.CTkEntry(
            self,
            placeholder_text="License Number"
        )

        self.license.pack(
            padx=30,
            fill="x",
            pady=8
        )

        self.phone = ctk.CTkEntry(
            self,
            placeholder_text="Phone Number"
        )

        self.phone.pack(
            padx=30,
            fill="x",
            pady=8
        )

        ctk.CTkButton(
            self,
            text="Create",
            command=self.create
        ).pack(
            pady=25
        )

    def create(self):

        self.callback(
            {
                "user_id": int(self.user_id.get()),
                "license_number": self.license.get(),
                "phone_number": self.phone.get()
            }
        )

        self.destroy()