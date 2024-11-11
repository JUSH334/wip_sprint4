import tkinter as tk

class GameBoard:
    def __init__(self, parent, board_size, on_click_callback):
        self.parent = parent
        self.board_size = board_size
        self.on_click_callback = on_click_callback
        self.board_buttons = []
        self.create_board()

    def create_board(self):
        """Creates the game board dynamically with better spacing."""
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.board_buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(
                    self.parent, text=' ', width=5, height=2,
                    command=lambda r=i, c=j: self.on_click_callback(r, c)
                )
                # Adjust padding to add more space around each button
                button.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

        # Make the grid cells expand proportionally
        for i in range(self.board_size):
            self.parent.grid_rowconfigure(i, weight=1)
            self.parent.grid_columnconfigure(i, weight=1)

    def update_button(self, row, col, text):
        self.board_buttons[row][col].config(text=text)

    def disable_buttons(self):
        for row in self.board_buttons:
            for button in row:
                button.config(state="disabled")
