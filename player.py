# player.py

class Player:
    """Base class for a player in the SOS game."""

    def __init__(self, name, choice="S"):
        self.name = name
        self.choice = choice

    def make_move(self, game_manager, row=None, col=None):
        """Makes a move in the game. Implemented specifically in subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_choice(self):
        """Returns the player's current choice ('S' or 'O')."""
        return self.choice


class HumanPlayer(Player):
    """Represents a human player."""

    def __init__(self, name, controls):
        super().__init__(name)
        self.controls = controls

    def make_move(self, game_manager, row, col):
        """Makes a move for the human player based on GUI input."""
        self.choice = self.controls.get_choice()  # Gets choice ('S' or 'O') from GUI controls
        game_manager.make_move(row, col, self.choice)


class ComputerPlayer(Player):
    """Represents a computer player with basic strategy."""

    def make_move(self, game_manager):
        """Computes a move and makes it automatically."""
        # Basic AI move logic (can be enhanced with strategies)
        empty_cells = [
            (r, c) for r in range(game_manager.board_size)
            for c in range(game_manager.board_size)
            if game_manager.mode.board[r][c] == ' '
        ]

        if empty_cells:
            row, col = random.choice(empty_cells)  # Randomly select an empty cell
            self.choice = random.choice(["S", "O"])  # Randomly select 'S' or 'O'
            game_manager.make_move(row, col, self.choice)
