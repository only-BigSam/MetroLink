import customtkinter as ctk


class EditDriverDialog(ctk.CTkToplevel):

    def __init__(self, parent, driver, callback):

        super().__init__(parent)

        self.driver = driver
        self.callback = callback

        self.title("Edit Driver")
        self.geometry("350x260")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Edit Driver",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 20))

        self.license = ctk.CTkEntry(self)

        self.license.insert(
            0,
            driver["license_number"]
        )

        self.license.pack(
            fill="x",
            padx=30,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(
            pady=20
        )

    def save(self):

        self.callback(
            self.driver["id"],
            {
                "license_number": self.license.get()
            }
        )

        self.destroy()