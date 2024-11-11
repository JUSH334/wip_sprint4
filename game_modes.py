# game_modes.py

class BaseGameMode:
    """Base class for common game mode functionality."""

    def __init__(self, board_size, game_manager):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.game_manager = game_manager
        self.is_game_active = False

    def reset_game(self, board_size):
        """Resets the board and game state."""
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.is_game_active = True

    def make_move(self, row, col, character):
        """Attempt a move in the base mode."""
        if self.board[row][col] != ' ':
            return False  # Invalid move if cell is already occupied
        self.board[row][col] = character
        return True

    def check_sos(self, row, col):
        """Counts the number of SOS patterns created around the given row, col position."""
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal top-left to bottom-right
            (1, -1)  # Diagonal top-right to bottom-left
        ]

        sos_count = 0
        for dx, dy in directions:
            sos_count += self.is_sos_sequence(row - 2 * dx, col - 2 * dy, row - dx, col - dy, row, col)
            sos_count += self.is_sos_sequence(row - dx, col - dy, row, col, row + dx, col + dy)
            sos_count += self.is_sos_sequence(row, col, row + dx, col + dy, row + 2 * dx, col + 2 * dy)
        return sos_count

    def is_sos_sequence(self, x1, y1, x2, y2, x3, y3):
        """Helper method to check for 'S-O-S' sequence in given positions."""
        if self.is_valid_position(x1, y1) and self.is_valid_position(x2, y2) and self.is_valid_position(x3, y3):
            if self.board[x1][y1] == 'S' and self.board[x2][y2] == 'O' and self.board[x3][y3] == 'S':
                return 1
        return 0

    def is_valid_position(self, row, col):
        """Checks if the given position is within the board boundaries."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def end_game_with_draw(self):
        """Handle game draw scenario."""
        self.game_manager.gui.turn_label.config(text="The game is a draw!")
        self.game_manager.end_game()

class SimpleGameMode(BaseGameMode):
    """Implements the simple game mode where the first SOS wins."""

    def make_move(self, row, col, character):
        if not super().make_move(row, col, character):
            # Invalid move feedback
            self.game_manager.gui.turn_label.config(text="Invalid move. Try again.")
            return

        # Update the board display
        self.game_manager.gui.board.update_button(row, col, character)

        # Check for win or draw conditions
        if self.check_sos(row, col) > 0:
            self.end_game_with_winner()
        elif self.game_manager.is_board_full():
            self.end_game_with_draw()
        else:
            # Switch turn for next player
            self.game_manager.switch_turn()

    def end_game_with_winner(self):
        """Declare the current player as winner and end the game."""
        self.game_manager.gui.turn_label.config(text=f"{self.game_manager.current_player} wins!")
        self.game_manager.end_game()

    def end_game_with_draw(self):
        """Handle game draw scenario."""
        self.game_manager.gui.turn_label.config(text="The game is a draw! No SOS was created.")
        self.game_manager.end_game()


class GeneralGameMode(BaseGameMode):
    """Implements the general game mode where SOS counts determine the winner."""

    def __init__(self, board_size, game_manager):
        super().__init__(board_size, game_manager)
        self.sos_count = {"Blue": 0, "Red": 0}

    def reset_game(self, board_size):
        """Resets the board, game state, and scores."""
        super().reset_game(board_size)
        # Reset SOS count for both players
        self.sos_count = {"Blue": 0, "Red": 0}
        self.update_score_display()

    def update_score_display(self):
        """Updates the SOS count labels."""
        self.game_manager.gui.blue_score_label.config(text=f"Blue SOS: {self.sos_count['Blue']}")
        self.game_manager.gui.red_score_label.config(text=f"Red SOS: {self.sos_count['Red']}")

    def make_move(self, row, col, character):
        if not super().make_move(row, col, character):
            # Invalid move feedback
            self.game_manager.gui.turn_label.config(text="Invalid move. Try again.")
            return

        # Update the board display
        self.game_manager.gui.board.update_button(row, col, character)

        # Check for SOS formations
        sos_formed = self.check_sos(row, col)
        if sos_formed > 0:
            # Update SOS count and display
            self.sos_count[self.game_manager.current_player] += sos_formed
            self.update_score_display()

            # Handle extra turn if the board isn't full
            if not self.game_manager.is_board_full():
                self.handle_extra_turn(sos_formed)
                return

        # Check for game end conditions
        if self.game_manager.is_board_full():
            self.end_game_based_on_score()
        else:
            # Switch turn for next player
            self.game_manager.switch_turn()

    def update_score_display(self):
        """Updates the SOS count labels."""
        self.game_manager.gui.blue_score_label.config(text=f"Blue SOS: {self.sos_count['Blue']}")
        self.game_manager.gui.red_score_label.config(text=f"Red SOS: {self.sos_count['Red']}")

    def handle_extra_turn(self, sos_formed):
        """Notify player of an extra turn for forming SOS."""
        self.game_manager.gui.turn_label.config(
            text=f"{self.game_manager.current_player} formed {sos_formed} SOS! They get an extra turn!"
        )

    def end_game_based_on_score(self):
        """Determine winner based on SOS count or declare a draw."""
        blue_score, red_score = self.sos_count["Blue"], self.sos_count["Red"]
        if blue_score > red_score:
            self.game_manager.gui.turn_label.config(text="Blue wins!")
        elif red_score > blue_score:
            self.game_manager.gui.turn_label.config(text="Red wins!")
        else:
            self.end_game_with_draw()  # Draw handled in BaseGameMode
        self.game_manager.end_game()

