# game_manager.py
from game_modes import SimpleGameMode, GeneralGameMode

# game_manager.py
class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple", gui=None):
        self.board_size = board_size
        self.current_player = "Blue"
        self.gui = gui
        self.is_game_active = True
        self.set_game_mode(game_mode)

    def set_game_mode(self, game_mode):
        """Sets the game mode and initializes the appropriate game mode class."""
        self.game_mode = game_mode
        if game_mode == "Simple":
            self.mode = SimpleGameMode(self.board_size, self)
            # Hide SOS score labels in Simple mode
            if self.gui:
                self.gui.blue_score_label.grid_remove()
                self.gui.red_score_label.grid_remove()
        elif game_mode == "General":
            self.mode = GeneralGameMode(self.board_size, self)
            # Show SOS score labels in General mode
            if self.gui:
                self.gui.blue_score_label.grid()
                self.gui.red_score_label.grid()

    def on_board_click(self, row, col):
        """Handles a click on the board and delegates the move to the active game mode."""
        character_choice = (self.gui.blue_controls.get_choice()
                            if self.current_player == "Blue"
                            else self.gui.red_controls.get_choice())

        # Delegate to game mode for all processing
        self.make_move(row, col, character_choice)

    def reset_game(self, board_size, game_mode):
        """Resets the game with a new board size and game mode."""
        self.board_size = board_size
        self.set_game_mode(game_mode)
        self.mode.reset_game(board_size)  # Reset the game mode-specific logic
        self.current_player = "Blue"  # Reset to starting player

    def make_move(self, row, col, character):
        """Makes a move in the game via the selected game mode."""
        return self.mode.make_move(row, col, character)

    def switch_turn(self):
        """Switches the turn between players and updates the GUI."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"
        self.gui.turn_label.config(text=f"Current turn: {self.current_player}")

    def end_game(self):
        """Ends the game by disabling interactions and setting the game state."""
        self.is_game_active = False
        self.mode.is_game_active = False
        self.gui.board.disable_buttons()

    def is_board_full(self):
        """Checks if the entire board is filled."""
        return all(cell != ' ' for row in self.mode.board for cell in row)

    def get_current_player(self):
        """Returns the current player."""
        return self.current_player
