import customtkinter as ctk

from ui.login import LoginPage


class MetroLinkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MetroLink")
        self.geometry("1000x650")
        self.resizable(True, True)

        ctk.set_appearance_mode("Light")

        self.configure(
            fg_color="#FFFFFF"
        )

        LoginPage(self)


if __name__ == "__main__":
    app = MetroLinkApp()
    app.mainloop()