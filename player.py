# player.py

import random

class BasePlayer:
    """Base class for a player in the SOS game."""

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.choice = "S"  # Default choice

    def get_choice(self):
        """Returns the current choice ('S' or 'O')."""
        return self.choice

    def make_move(self, game_mode, row=None, col=None):
        """Method to make a move. Specific to each subclass."""
        raise NotImplementedError("Subclasses should implement this method.")


class HumanPlayer(BasePlayer):
    """Represents a human player."""

    def __init__(self, name, color, controls):
        super().__init__(name, color)
        self.controls = controls  # GUI control for choosing 'S' or 'O'

    def make_move(self, game_mode, row, col):
        """Make a move in the game mode based on player input from GUI controls."""
        self.choice = self.controls.get_choice()  # Fetch selected 'S' or 'O' from controls
        game_mode.make_move(row, col, self.choice)


class ComputerPlayer(BasePlayer):
    """Represents a computer player with basic move logic."""

    def __init__(self, name, color):
        super().__init__(name, color)

    def make_move(self, game_mode):
        """Automatically make a move using a basic strategy."""
        # Simple strategy: fill an empty spot or attempt to complete an SOS pattern if possible
        empty_cells = [
            (r, c) for r in range(game_mode.board_size)
            for c in range(game_mode.board_size)
            if game_mode.board[r][c] == ' '
        ]

        if empty_cells:
            # Randomly select an empty cell for simplicity
            row, col = random.choice(empty_cells)
            self.choice = "S" if random.choice([True, False]) else "O"  # Randomly choose S or O
            game_mode.make_move(row, col, self.choice)
