# game_manager.py

from game_modes import SimpleGameMode, GeneralGameMode
from player import HumanPlayer, ComputerPlayer


class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple", gui=None):
        self.board_size = board_size
        self.gui = gui
        self.is_game_active = True
        self.players = {"Blue": None, "Red": None}  # Stores player instances
        self.set_game_mode(game_mode)

    def initialize_players(self, blue_type="Human", red_type="Human"):
        """Initialize players as human or computer based on GUI selection."""
        blue_controls = self.gui.blue_controls if blue_type == "Human" else None
        red_controls = self.gui.red_controls if red_type == "Human" else None

        # Create HumanPlayer or ComputerPlayer based on type
        self.players["Blue"] = HumanPlayer("Blue", "Blue", blue_controls) if blue_type == "Human" else ComputerPlayer(
            "Blue", "Blue")
        self.players["Red"] = HumanPlayer("Red", "Red", red_controls) if red_type == "Human" else ComputerPlayer("Red",
                                                                                                                 "Red")

        self.current_player = self.players["Blue"]  # Start with Blue player

    def set_game_mode(self, game_mode):
        """Sets the game mode and initializes the appropriate game mode class."""
        self.game_mode = game_mode
        if game_mode == "Simple":
            self.mode = SimpleGameMode(self.board_size, self)
            if self.gui:
                self.gui.blue_score_label.grid_remove()
                self.gui.red_score_label.grid_remove()
        elif game_mode == "General":
            self.mode = GeneralGameMode(self.board_size, self)
            if self.gui:
                self.gui.blue_score_label.grid()
                self.gui.red_score_label.grid()

    def on_board_click(self, row, col):
        """Handles a click on the board for a human player's move."""
        if isinstance(self.current_player, HumanPlayer):
            self.current_player.make_move(self.mode, row, col)  # Delegates move to game mode

    def make_move(self, row, col, character):
        """Delegates the move to the game mode and processes the result."""
        result = self.mode.make_move(row, col, character)

        # Handle the outcome based on game mode result
        if result:
            if result["result"] == "win":
                self.gui.turn_label.config(text=f"{self.current_player.color} wins!")
                self.end_game()
            elif result["result"] == "draw":
                self.gui.turn_label.config(text="The game is a draw! No SOS was created.")
                self.end_game()
            elif result["result"] == "next_turn":
                self.switch_turn()
            elif result["result"] == "extra_turn":
                self.gui.turn_label.config(text=f"{self.current_player.color} gets another turn!")

    def switch_turn(self):
        """Switches the turn between players and updates the GUI."""
        self.current_player = self.players["Red"] if self.current_player == self.players["Blue"] else self.players[
            "Blue"]
        self.gui.turn_label.config(text=f"Current turn: {self.current_player.color}")

        if isinstance(self.current_player, ComputerPlayer):
            self.gui.root.after(1000, lambda: self.current_player.make_move(self.mode))

    def reset_game(self, board_size, game_mode, blue_type="Human", red_type="Human"):
        """Resets the game with a new board size, game mode, and player types."""
        self.board_size = board_size
        self.set_game_mode(game_mode)
        self.initialize_players(blue_type, red_type)  # Initialize players based on GUI selection
        self.mode.reset_game(board_size)  # Reset the game mode-specific logic
        self.current_player = self.players["Blue"]  # Start with Blue player

    def end_game(self):
        """Ends the game by disabling interactions and setting the game state."""
        self.is_game_active = False
        self.mode.is_game_active = False
        self.gui.board.disable_buttons()

    def is_board_full(self):
        """Checks if the entire board is filled."""
        return all(cell != ' ' for row in self.mode.board for cell in row)


