import customtkinter as ctk


class RoleDialog(ctk.CTkToplevel):

    def __init__(self, parent, user, callback):

        super().__init__(parent)

        self.user = user
        self.callback = callback

        self.title("Change User Role")
        self.geometry("350x220")
        self.resizable(False, False)

        title = ctk.CTkLabel(
            self,
            text=f"Change role for\n{user['name']}",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=(20, 15))

        self.role_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "admin",
                "driver",
                "passenger"
            ]
        )

        self.role_menu.set(user["role"])

        self.role_menu.pack(pady=10)

        save = ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        )

        save.pack(pady=(20, 10))

    def save(self):

        self.callback(
            self.user,
            self.role_menu.get()
        )

        self.destroy()