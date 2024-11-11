import tkinter as tk
from game_manager import GameManager
from player_controls import PlayerControls
from game_board import GameBoard


class SOSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Application")
        self.board_size = 3
        self.game_mode = "Simple"
        self.is_game_active = False
        self.board = None  # Initialize board as None to avoid AttributeError
        self.blue_score_label = tk.Label(self.root, text="Blue SOS: 0")
        self.red_score_label = tk.Label(self.root, text="Red SOS: 0")
        self.game_manager = GameManager(self.board_size, self.game_mode, self)  # Pass self as the GUI reference
        self.create_ui()

    def create_ui(self):
        """Sets up the main layout for the game."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)

        # Top Frame for mode and size selection
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Set up the game controls (mode and board size)
        self.setup_game_controls(self.top_frame)

        # Player control frames on the left and right
        self.blue_frame = tk.Frame(self.main_frame)
        self.blue_controls = PlayerControls(self.blue_frame, "Blue")
        self.blue_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.red_frame = tk.Frame(self.main_frame)
        self.red_controls = PlayerControls(self.red_frame, "Red")
        self.red_frame.grid(row=1, column=2, padx=20, pady=10, sticky="n")

        # Game board frame in the center
        self.create_scrollable_board_frame()

        # Bottom Frame for the Start/End button and Current Turn label
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=1, padx=20, pady=20)

        # Set up the start/end button and current turn label in the bottom frame
        self.setup_bottom_controls(self.bottom_frame)

        # Initial state: Only game mode and board size options enabled
        self.enable_start_options()

        # Add player score labels to show SOS count in General Game mode
        self.blue_score_label = tk.Label(self.main_frame, text="Blue SOS: 0")
        self.blue_score_label.grid(row=3, column=0, padx=10, pady=5)

        self.red_score_label = tk.Label(self.main_frame, text="Red SOS: 0")
        self.red_score_label.grid(row=3, column=2, padx=10, pady=5)

    def setup_game_controls(self, parent):
        label = tk.Label(parent, text="SOS")
        label.grid(row=0, column=0, padx=5, pady=1, sticky="w")
        self.radio_var = tk.StringVar(value="Simple Game")

        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=0, column=1, padx=10, pady=1, sticky="w")

        tk.Radiobutton(radio_frame, text="Simple game", variable=self.radio_var, value="Simple Game").grid(row=0,
                                                                                                           column=0)
        tk.Radiobutton(radio_frame, text="General game", variable=self.radio_var, value="General Game").grid(row=0,
                                                                                                             column=1)

        board_size_label = tk.Label(parent, text="Board size")
        board_size_label.grid(row=0, column=2, padx=5, pady=1, sticky="w")
        self.board_size_var = tk.IntVar(value=3)
        vcmd = (self.root.register(self.validate_board_size), '%P')
        self.board_size_spinbox = tk.Spinbox(parent, from_=3, to=20, textvariable=self.board_size_var,
                                             validate="key", validatecommand=vcmd, width=3)
        self.board_size_spinbox.grid(row=0, column=3, padx=5, pady=1, sticky="w")

    def setup_bottom_controls(self, parent):
        """Sets up the bottom controls like Start/End game button and Current Turn label."""
        self.start_button = tk.Button(parent, text="Start Game", command=self.toggle_game)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.turn_label = tk.Label(parent, text="Current turn: Blue")
        self.turn_label.grid(row=1, column=0, padx=10, pady=5)
        self.turn_label.grid_remove()  # Hide initially until game starts

    def create_scrollable_board_frame(self):
        """Sets up the frame that will hold the game board."""
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=1, column=1, padx=20, pady=10)

    def toggle_game(self):
        if self.start_button["text"] == "Start Game":
            self.start_game()
            self.start_button.config(text="End Game")
        else:
            self.end_game()
            self.start_button.config(text="Start Game")

    def start_game(self):
        self.is_game_active = True
        selected_mode = self.radio_var.get().split()[0]  # "Simple" or "General"
        self.board_size = self.board_size_var.get()

        # Set the game mode in GameManager based on selection
        self.game_manager.reset_game(self.board_size, selected_mode)

        # Display the chosen game mode and board size
        self.turn_label.config(text=f"Game Mode: {selected_mode}, Board Size: {self.board_size}x{self.board_size}")

        # Adjust the window size and initialize the game board UI
        self.adjust_window_size(self.board_size)
        self.board = GameBoard(self.board_frame, self.board_size, self.on_board_click)
        self.board.create_board()

        # Enable gameplay controls and disable start options
        self.enable_gameplay_controls()

        # Update turn label to show initial player turn after mode and size
        initial_turn = self.game_manager.get_current_player()
        self.turn_label.config(
            text=f"Game Mode: {selected_mode}, Board Size: {self.board_size}x{self.board_size}\nCurrent turn: {initial_turn}")
        self.turn_label.grid()

    def end_game(self):
        self.is_game_active = False
        self.game_manager.end_game()
        self.board.disable_buttons()
        self.turn_label.grid_remove()

        # Re-enable start options and disable gameplay controls
        self.enable_start_options()

    def enable_start_options(self):
        """Enables game mode selection and board size options; disables other controls."""
        # Enable game mode and board size controls
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, (tk.Radiobutton, tk.Spinbox)):
                widget.config(state="normal")

        # Disable player controls and board
        for widget in self.blue_frame.winfo_children() + self.red_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="disabled")
        if self.board:
            self.board.disable_buttons()

        # Enable the Start button
        self.start_button.config(state="normal")

    def enable_gameplay_controls(self):
        """Enables gameplay controls and disables game mode and board size options."""
        # Disable game mode and board size controls
        for widget in self.top_frame.winfo_children():
            if isinstance(widget, (tk.Radiobutton, tk.Spinbox)):
                widget.config(state="disabled")

        # Enable player controls
        for widget in self.blue_frame.winfo_children() + self.red_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="normal")

        # Enable the board buttons
        if self.board:
            for row in self.board.board_buttons:
                for button in row:
                    button.config(state="normal")

        # Enable the Start/End button
        self.start_button.config(state="normal")

    def on_board_click(self, row, col):
        """Delegates board click handling to the GameManager."""
        if not self.is_game_active:
            return

        # Delegate the click to the GameManager
        self.game_manager.on_board_click(row, col)

    def validate_board_size(self, new_value):
        if new_value.isdigit():
            return 3 <= int(new_value) <= 20
        return False

    def adjust_window_size(self, board_size):
        """Adjusts the window size based on the board size."""
        cell_size = 50
        board_pixel_size = board_size * cell_size
        max_window_size = 600
        self.root.geometry(
            f"{min(board_pixel_size + 100, max_window_size)}x{min(board_pixel_size + 100, max_window_size)}")


def main():
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
