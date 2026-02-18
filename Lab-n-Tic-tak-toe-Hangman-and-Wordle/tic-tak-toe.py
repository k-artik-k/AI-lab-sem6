import tkinter as tk
from tkinter import messagebox
import random
import math

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Tic Tac Toe - AI")

        self.board = [" "] * 9
        self.human = "X"
        self.ai = "O"
        self.current_turn = "X"

        self.difficulty = "Hard"

        self.human_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.create_ui()

    # ================= UI =================

    def create_ui(self):

        top_frame = tk.Frame(self.root)
        top_frame.pack()

        self.status_label = tk.Label(top_frame, text="Your Turn",
                                     font=("Arial", 14))
        self.status_label.pack()

        self.score_label = tk.Label(top_frame,
                                    text="Human: 0   AI: 0   Draws: 0",
                                    font=("Arial", 12))
        self.score_label.pack()

        level_frame = tk.Frame(self.root)
        level_frame.pack(pady=5)

        tk.Label(level_frame, text="Difficulty: ").pack(side=tk.LEFT)

        self.level_var = tk.StringVar(value="Hard")

        tk.OptionMenu(level_frame, self.level_var,
                      "Easy", "Medium", "Hard").pack(side=tk.LEFT)

        self.buttons = []
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for i in range(9):
            btn = tk.Button(board_frame,
                            text=" ",
                            font=("Arial", 24),
                            width=5,
                            height=2,
                            bg="lightgray",
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        tk.Button(self.root, text="Restart",
                  command=self.reset_game,
                  bg="orange").pack(pady=5)

    # ================= GAME LOGIC =================

    def player_move(self, index):
        if self.board[index] == " " and self.current_turn == self.human:
            self.make_move(index, self.human)

            if not self.check_game_over():
                self.current_turn = self.ai
                self.root.after(400, self.ai_move)

    def ai_move(self):
        self.difficulty = self.level_var.get()

        if self.difficulty == "Easy":
            move = self.random_move()

        elif self.difficulty == "Medium":
            if random.random() < 0.4:
                move = self.random_move()
            else:
                move = self.best_move(depth_limit=3)

        else:  # Hard
            move = self.best_move(depth_limit=None)

        self.make_move(move, self.ai)

        if not self.check_game_over():
            self.current_turn = self.human
            self.status_label.config(text="Your Turn")

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player,
                                   bg="#90EE90" if player == "X" else "#FFB6C1")

    def random_move(self):
        empty = [i for i in range(9) if self.board[i] == " "]
        return random.choice(empty)

    # ================= MINIMAX =================

    def best_move(self, depth_limit):
        best_score = -math.inf
        moves = []

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.ai
                score = self.minimax(0, False, -math.inf, math.inf, depth_limit)
                self.board[i] = " "

                if score > best_score:
                    best_score = score
                    moves = [i]
                elif score == best_score:
                    moves.append(i)

        return random.choice(moves)

    def minimax(self, depth, is_max, alpha, beta, depth_limit):

        winner = self.check_winner()

        if winner == self.ai:
            return 10 - depth
        elif winner == self.human:
            return depth - 10
        elif " " not in self.board:
            return 0

        if depth_limit is not None and depth >= depth_limit:
            return 0

        if is_max:
            max_eval = -math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = self.ai
                    eval = self.minimax(depth+1, False, alpha, beta, depth_limit)
                    self.board[i] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = self.human
                    eval = self.minimax(depth+1, True, alpha, beta, depth_limit)
                    self.board[i] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    # ================= WIN CHECK =================

    def check_winner(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for combo in combos:
            if self.board[combo[0]] != " " and \
               self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                return self.board[combo[0]]
        return None

    def check_game_over(self):
        winner = self.check_winner()

        if winner:
            if winner == self.human:
                self.human_score += 1
                messagebox.showinfo("Game Over", "You Win!")
            else:
                self.ai_score += 1
                messagebox.showinfo("Game Over", "AI Wins!")

            self.update_score()
            self.reset_game()
            return True

        elif " " not in self.board:
            self.draw_score += 1
            messagebox.showinfo("Game Over", "Draw!")
            self.update_score()
            self.reset_game()
            return True

        return False

    def update_score(self):
        self.score_label.config(
            text=f"Human: {self.human_score}   AI: {self.ai_score}   Draws: {self.draw_score}"
        )

    def reset_game(self):
        self.board = [" "] * 9
        self.current_turn = self.human
        self.status_label.config(text="Your Turn")
        for btn in self.buttons:
            btn.config(text=" ", bg="lightgray")


# ================= MAIN =================

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
