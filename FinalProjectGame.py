import tkinter as tk
from tkinter import font, simpledialog
import json
import os

SCORES_FILE = "scores.json"

class TicTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self.current_player = "X"
        self.players = {"X": None, "O": None}
        self.scores = self._load_scores()

        self._prompt_usernames()
        self._create_board_display()
        self._create_board_grid()

    def _prompt_usernames(self):
        # Get player names
        player1 = simpledialog.askstring("Player 1", "Enter username for Player X:")
        player2 = simpledialog.askstring("Player 2", "Enter username for Player O:")

        if not player1 or not player2:
            self.quit()

        self.players["X"] = player1
        self.players["O"] = player2

        for player in [player1, player2]:
            if player not in self.scores:
                self.scores[player] = {"wins": 0}
        self._save_scores()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)

        self.display = tk.Label(
            master=display_frame,
            text=f"{self.players['X']} (X) vs {self.players['O']} (O) — {self.players['X']}'s Turn",
            font=font.Font(size=18, weight="bold"),
        )
        self.display.pack()

        self.score_label = tk.Label(
            master=display_frame,
            text=self._get_score_text(),
            font=font.Font(size=14)
        )
        self.score_label.pack()

    def _get_score_text(self):
        p1 = self.players["X"]
        p2 = self.players["O"]
        return f"{p1}'s Wins: {self.scores[p1]['wins']}    |    {p2}'s Wins: {self.scores[p2]['wins']}"

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue"
                )
                button.config(command=lambda b=button: self._handle_click(b))
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        restart_button = tk.Button(
            master=self,
            text="Restart",
            font=font.Font(size=16, weight="bold"),
            bg="green",
            fg="white",
            command=self._restart_game
        )
        restart_button.pack(pady=10)

    def _handle_click(self, clicked_button):
        if clicked_button["text"] == "":
            clicked_button["text"] = self.current_player
            clicked_button["fg"] = "crimson" if self.current_player == "X" else "blue"

            if self._check_winner(self.current_player):
                winner_name = self.players[self.current_player]
                self.display["text"] = f"{winner_name} ({self.current_player}) wins!"
                self._disable_all_buttons()
                self._update_score(winner_name)
            elif self._is_draw():
                self.display["text"] = "It's a draw!"
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                next_player_name = self.players[self.current_player]
                self.display["text"] = f"{next_player_name}'s Turn ({self.current_player})"

    def _check_winner(self, player):
        board = [["" for _ in range(3)] for _ in range(3)]
        for button, (row, col) in self._cells.items():
            board[row][col] = button["text"]
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def _is_draw(self):
        return all(button["text"] != "" for button in self._cells)

    def _disable_all_buttons(self):
        for button in self._cells:
            button.config(state="disabled")

    def _restart_game(self):
        for button in self._cells:
            button.config(text="", state="normal", fg="black")
        self.current_player = "X"
        self.display["text"] = f"{self.players['X']}'s Turn (X)"
        self.score_label["text"] = self._get_score_text()

    def _update_score(self, winner_name):
        self.scores[winner_name]["wins"] += 1
        self._save_scores()
        self.score_label["text"] = self._get_score_text()

    def _load_scores(self):
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as file:
                return json.load(file)
        return {}

    def _save_scores(self):
        with open(SCORES_FILE, "w") as file:
            json.dump(self.scores, file, indent=4)

# Run the app
if __name__ == "__main__":
    app = TicTacToeBoard()
    app.mainloop()
