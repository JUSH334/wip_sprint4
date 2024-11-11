# BaseGameMode class for common game functionalities
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
        """Attempt a move in the base mode, overridden in child classes if needed."""
        if self.board[row][col] != ' ':
            return False  # Invalid move if cell is already occupied
        self.board[row][col] = character
        return True

    def end_game(self):
        """Ends the game, to be customized in each game mode."""
        self.is_game_active = False


# SimpleGameMode for "first SOS wins" mode
class SimpleGameMode(BaseGameMode):
    """Implements the simple game mode where the first SOS wins."""

    def make_move(self, row, col, character):
        """Place a character and check if it leads to a win."""
        if super().make_move(row, col, character):
            self.game_manager.gui.board.update_button(row, col, character)

            # Check for SOS pattern immediately after each move
            if self.check_sos(row, col):
                self.end_game_with_winner()
                return {"result": "win", "winner": self.game_manager.current_player}
            elif self.game_manager.is_board_full():
                self.end_game_with_draw()
                return {"result": "draw"}
            else:
                return {"result": "next_turn"}  # Indicates to switch turns
        return False

    def check_sos(self, row, col):
        """Checks if an SOS pattern is created around the given row, col position."""
        # Define all directions for SOS checking: horizontal, vertical, and diagonals
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal top-left to bottom-right
            (1, -1)  # Diagonal top-right to bottom-left
        ]

        for dx, dy in directions:
            # Check backward: positions (row - 2dx, col - 2dy), (row - dx, col - dy), (row, col)
            if self.is_sos_sequence(row - 2 * dx, col - 2 * dy, row - dx, col - dy, row, col):
                return True

            # Check centered: positions (row - dx, col - dy), (row, col), (row + dx, col + dy)
            if self.is_sos_sequence(row - dx, col - dy, row, col, row + dx, col + dy):
                return True

            # Check forward: positions (row, col), (row + dx, col + dy), (row + 2dx, col + 2dy)
            if self.is_sos_sequence(row, col, row + dx, col + dy, row + 2 * dx, col + 2 * dy):
                return True

        print("No SOS pattern detected.")
        return False

    def is_sos_sequence(self, x1, y1, x2, y2, x3, y3):
        """Helper method to check for 'S-O-S' sequence in given positions."""
        if (self.is_valid_position(x1, y1) and self.is_valid_position(x2, y2) and self.is_valid_position(x3, y3)):
            if (self.board[x1][y1] == 'S' and
                    self.board[x2][y2] == 'O' and
                    self.board[x3][y3] == 'S'):
                print(f"SOS pattern detected: ({x1}, {y1}) -> ({x2}, {y2}) -> ({x3}, {y3})")
                return True
        return False

    def is_valid_position(self, row, col):
        """Checks if the given position is within the board boundaries."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def end_game_with_winner(self):
        """Declare the current player as winner and end the game."""
        winner = self.game_manager.current_player
        self.game_manager.gui.turn_label.config(text=f"{winner} wins!")
        self.game_manager.end_game()

    def end_game_with_draw(self):
        """Handle game draw scenario in Simple Game Mode."""
        self.game_manager.gui.turn_label.config(text="The game is a draw! No SOS was created.")
        self.game_manager.end_game()


# GeneralGameMode for "SOS count determines the winner" mode
class GeneralGameMode(BaseGameMode):
    """Implements the general game mode where SOS counts determine the winner."""

    def __init__(self, board_size, game_manager):
        super().__init__(board_size, game_manager)
        self.sos_count = {"Blue": 0, "Red": 0}

    def make_move(self, row, col, character):
        """Place a character and check for SOS patterns and if the board is full."""
        if super().make_move(row, col, character):
            self.game_manager.gui.board.update_button(row, col, character)

            # Check for SOS patterns and update sos_count
            sos_formed = self.check_sos(row, col)
            if sos_formed > 0:
                current_player = self.game_manager.current_player
                self.sos_count[current_player] += sos_formed

                # Update the SOS count labels
                if current_player == "Blue":
                    self.game_manager.gui.blue_score_label.config(text=f"Blue SOS: {self.sos_count['Blue']}")
                else:
                    self.game_manager.gui.red_score_label.config(text=f"Red SOS: {self.sos_count['Red']}")

                # Check if the board is now full after forming SOS
                if self.game_manager.is_board_full():
                    self.end_game_based_on_score()
                    return {"result": "end"}  # End game as board is full

                # If board is not full, grant an extra turn for forming an SOS
                self.handle_extra_turn(sos_formed)
                return {"result": "extra_turn"}

            # If no SOS is formed, check if the board is full
            if self.game_manager.is_board_full():
                self.end_game_based_on_score()
                return {"result": "end"}  # End game as board is full

            # If no SOS is formed and the board is not full, switch turns
            return {"result": "next_turn"}

        return False

    def check_sos(self, row, col):
        """Counts the number of SOS patterns created around the given row, col position."""
        # Define all directions for SOS checking: horizontal, vertical, and diagonals
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal top-left to bottom-right
            (1, -1)   # Diagonal top-right to bottom-left
        ]

        sos_count = 0  # Count the number of SOS patterns formed

        for dx, dy in directions:
            # Check backward: positions (row - 2dx, col - 2dy), (row - dx, col - dy), (row, col)
            sos_count += self.is_sos_sequence(row - 2*dx, col - 2*dy, row - dx, col - dy, row, col)

            # Check centered: positions (row - dx, col - dy), (row, col), (row + dx, col + dy)
            sos_count += self.is_sos_sequence(row - dx, col - dy, row, col, row + dx, col + dy)

            # Check forward: positions (row, col), (row + dx, col + dy), (row + 2dx, col + 2dy)
            sos_count += self.is_sos_sequence(row, col, row + dx, col + dy, row + 2*dx, col + 2*dy)

        if sos_count > 0:
            print(f"SOS patterns detected: {sos_count}")
        else:
            print("No SOS pattern detected.")
        return sos_count

    def is_sos_sequence(self, x1, y1, x2, y2, x3, y3):
        """Helper method to check for 'S-O-S' sequence in given positions."""
        if (self.is_valid_position(x1, y1) and
            self.is_valid_position(x2, y2) and
            self.is_valid_position(x3, y3)):
            if (self.board[x1][y1] == 'S' and
                self.board[x2][y2] == 'O' and
                self.board[x3][y3] == 'S'):
                print(f"SOS pattern detected: ({x1}, {y1}) -> ({x2}, {y2}) -> ({x3}, {y3})")
                return 1
        return 0

    def is_valid_position(self, row, col):
        """Checks if the given position is within the board boundaries."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def handle_extra_turn(self, sos_formed):
        """Handle extra turn in General Game Mode if SOS is created."""
        current_player = self.game_manager.current_player
        self.game_manager.gui.turn_label.config(
            text=f"{current_player} formed {sos_formed} SOS! They get an extra turn!"
        )

    def end_game_based_on_score(self):
        """Determine the winner based on SOS counts and end the game."""
        blue_score = self.sos_count["Blue"]
        red_score = self.sos_count["Red"]

        if blue_score > red_score:
            self.game_manager.gui.turn_label.config(text="Blue wins!")
        elif red_score > blue_score:
            self.game_manager.gui.turn_label.config(text="Red wins!")
        else:
            self.game_manager.gui.turn_label.config(text="The game is a draw!")

        # End the game by disabling the board and stopping further moves
        self.game_manager.end_game()

    def reset_game(self, board_size):
        """Resets the board, game state, and player scores."""
        super().reset_game(board_size)
        self.sos_count = {"Blue": 0, "Red": 0}  # Reset SOS counts for both players

        # Update the score labels in the GUI
        self.game_manager.gui.blue_score_label.config(text="Blue SOS: 0")
        self.game_manager.gui.red_score_label.config(text="Red SOS: 0")


# GameManager to initialize and control the appropriate game mode
class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple", gui=None):
        self.board_size = board_size
        self.current_player = "Blue"
        self.gui = gui
        self.set_game_mode(game_mode)

    def set_game_mode(self, game_mode):
        """Sets the game mode and initializes the appropriate game mode class."""
        self.game_mode = game_mode
        if game_mode == "Simple":
            self.mode = SimpleGameMode(self.board_size, self)
            # Hide SOS score labels in Simple mode
            self.gui.blue_score_label.grid_remove()
            self.gui.red_score_label.grid_remove()
        elif game_mode == "General":
            self.mode = GeneralGameMode(self.board_size, self)
            # Show SOS score labels in General mode
            self.gui.blue_score_label.grid()
            self.gui.red_score_label.grid()

    def on_board_click(self, row, col):
        """Handles a click on the board and delegates the move to the active game mode."""
        # Determine the character based on the current player's selection
        character_choice = (self.gui.blue_controls.get_choice()
                            if self.current_player == "Blue"
                            else self.gui.red_controls.get_choice())

        # Make the move through the current game mode
        result = self.make_move(row, col, character_choice)

        # Process the result
        if result:
            if result["result"] == "win":
                self.gui.turn_label.config(text=f"{result['winner']} wins!")
                self.end_game()
            elif result["result"] == "draw":
                self.gui.turn_label.config(text="The game is a draw! No SOS was created.")
                self.end_game()
            elif result["result"] == "next_turn":
                self.switch_turn()
            elif result["result"] == "continue":
                # In GeneralGameMode, if an SOS is created, the player gets an extra turn
                self.gui.turn_label.config(text=f"{self.current_player} gets another turn!")

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

    def is_board_full(self):
        """Checks if the entire board is filled."""
        return all(cell != ' ' for row in self.mode.board for cell in row)


