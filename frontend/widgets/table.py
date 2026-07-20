import customtkinter as ctk


class DataTable(ctk.CTkFrame):

    def __init__(self, parent, columns):

        super().__init__(parent)

        self.columns = columns
        self.row_count = 0

        self.build_table()

    def build_table(self):

        self.header = ctk.CTkFrame(
            self,
            fg_color="#EAEAEA"
        )

        self.header.pack(
            fill="x"
        )

        for column in self.columns:

            label = ctk.CTkLabel(
                self.header,
                text=column,
                font=("Arial", 14, "bold"),
                width=150,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=10,
                pady=10
            )

        self.body = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.body.pack(
            fill="both",
            expand=True
        )

    def add_row(self, values, action=None):

        row = ctk.CTkFrame(
            self.body,
            fg_color="#FFFFFF" if self.row_count % 2 == 0 else "#EFEFEF"
        )

        row.pack(
            fill="x",
            pady=2
        )

        for value in values:

            label = ctk.CTkLabel(
                row,
                text=str(value),
                width=150,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=10,
                pady=8
            )

        if action:

            button = ctk.CTkButton(
                row,
                text="Edit",
                width=70,
                command=action
            )

            button.pack(
                side="left",
                padx=10
            )

        self.row_count += 1