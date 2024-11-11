import tkinter as tk

class PlayerControls:
    def __init__(self, parent, player_name, default_choice="S"):
        self.parent = parent
        self.player_name = player_name
        self.choice = tk.StringVar(value=default_choice)
        self.create_controls()

    def create_controls(self):
        label = tk.Label(self.parent, text=f"{self.player_name} player")
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        s_button = tk.Radiobutton(self.parent, text="S", variable=self.choice, value="S")
        s_button.grid(row=1, column=0, padx=5, pady=5)

        o_button = tk.Radiobutton(self.parent, text="O", variable=self.choice, value="O")
        o_button.grid(row=2, column=0, padx=5, pady=5)

    def get_choice(self):
        return self.choice.get()
