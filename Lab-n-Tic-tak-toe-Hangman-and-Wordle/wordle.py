import tkinter as tk
from tkinter import messagebox
import random

class Wordle:
    def __init__(self, root):
        self.root = root
        self.root.title("WORDLE")
        self.root.configure(bg="#121213")
        self.root.resizable(False, False)

        # Load words
        self.load_words()

        # Stats
        self.wins = 0
        self.streak = 0
        self.games = 0

        # UI
        self.create_ui()
        self.new_game()

    # ======= Load words =======
    def load_words(self):
        try:
            with open("words.txt", "r") as f:
                text = f.read().upper()
            raw_words = text.replace(",", " ").split()
            self.words = [w.strip() for w in raw_words if len(w.strip()) == 5 and w.isalpha()]
            if not self.words:
                raise ValueError("No valid words found")
        except Exception:
            messagebox.showwarning("Warning", "words.txt missing or invalid. Using default words.")
            self.words = ["APPLE", "GRAPE", "HOUSE", "PLANT", "BRAIN", "LIGHT"]

    # ======= New game =======
    def new_game(self):
        self.target = random.choice(self.words)
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.board = [["" for _ in range(5)] for _ in range(6)]
        for row in self.tiles:
            for tile in row:
                tile.config(text="", bg="#121213")
        for key in self.keyboard_buttons.values():
            key.config(bg="#818384")

    # ======= UI =======
    def create_ui(self):
        title = tk.Label(self.root, text="WORDLE", font=("Helvetica", 28, "bold"), fg="white", bg="#121213")
        title.pack(pady=10)

        self.stats_label = tk.Label(self.root, text="Wins: 0  |  Streak: 0", fg="white", bg="#121213")
        self.stats_label.pack()

        board_frame = tk.Frame(self.root, bg="#121213")
        board_frame.pack(pady=10)
        self.tiles = []
        for r in range(6):
            row_tiles = []
            for c in range(5):
                tile = tk.Label(board_frame, text="", width=4, height=2, font=("Helvetica", 24, "bold"),
                                bg="#121213", fg="white", relief="solid", bd=2)
                tile.grid(row=r, column=c, padx=5, pady=5)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

        # Keyboard
        keyboard_frame = tk.Frame(self.root, bg="#121213")
        keyboard_frame.pack()
        self.keyboard_buttons = {}
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        for row in rows:
            frame = tk.Frame(keyboard_frame, bg="#121213")
            frame.pack()
            for letter in row:
                btn = tk.Button(frame, text=letter, width=4, height=2, bg="#818384", fg="white",
                                command=lambda l=letter: self.handle_letter(l))
                btn.pack(side=tk.LEFT, padx=3, pady=3)
                self.keyboard_buttons[letter] = btn

        control_frame = tk.Frame(self.root, bg="#121213")
        control_frame.pack(pady=5)
        tk.Button(control_frame, text="ENTER", width=8, bg="#3a3a3c", fg="white", command=self.submit_guess).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="DELETE", width=8, bg="#3a3a3c", fg="white", command=self.delete_letter).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="NEW GAME", width=10, bg="#538d4e", fg="white", command=self.new_game).pack(side=tk.LEFT, padx=5)

        self.root.bind("<Key>", self.key_press)

    # ======= Input handling =======
    def key_press(self, event):
        if self.game_over:
            return
        key = event.char.upper()
        if key.isalpha() and len(key) == 1:
            self.handle_letter(key)
        elif event.keysym == "Return":
            self.submit_guess()
        elif event.keysym == "BackSpace":
            self.delete_letter()

    def handle_letter(self, letter):
        if self.current_col < 5 and not self.game_over:
            self.board[self.current_row][self.current_col] = letter
            self.tiles[self.current_row][self.current_col].config(text=letter)
            self.current_col += 1

    def delete_letter(self):
        if self.current_col > 0 and not self.game_over:
            self.current_col -= 1
            self.board[self.current_row][self.current_col] = ""
            self.tiles[self.current_row][self.current_col].config(text="")

    # ======= Wordle logic =======
    def submit_guess(self):
        if self.current_col != 5 or self.game_over:
            return
        guess = "".join(self.board[self.current_row])
        if guess not in self.words:
            messagebox.showwarning("Invalid Word", "Not in word list")
            return
        colors = ["#3a3a3c"] * 5
        target_copy = list(self.target)
        for i in range(5):  # Green
            if guess[i] == self.target[i]:
                colors[i] = "#538d4e"
                target_copy[i] = None
        for i in range(5):  # Yellow
            if colors[i] == "#3a3a3c" and guess[i] in target_copy:
                colors[i] = "#b59f3b"
                target_copy[target_copy.index(guess[i])] = None
        for i in range(5):
            self.tiles[self.current_row][i].config(bg=colors[i])
            self.update_keyboard_color(guess[i], colors[i])
        if guess == self.target:
            self.wins += 1
            self.streak += 1
            self.games += 1
            self.update_stats()
            self.game_over = True
            messagebox.showinfo("WORDLE", "You Won!")
            return
        self.current_row += 1
        self.current_col = 0
        if self.current_row == 6:
            self.games += 1
            self.streak = 0
            self.update_stats()
            self.game_over = True
            messagebox.showinfo("WORDLE", f"You Lost!\nWord was {self.target}")

    def update_keyboard_color(self, letter, color):
        current = self.keyboard_buttons[letter].cget("bg")
        priority = {"#538d4e": 3, "#b59f3b": 2, "#3a3a3c": 1, "#818384": 0}
        if priority[color] > priority.get(current, 0):
            self.keyboard_buttons[letter].config(bg=color)

    def update_stats(self):
        self.stats_label.config(text=f"Wins: {self.wins}  |  Streak: {self.streak}")

# ======= MAIN =======
if __name__ == "__main__":
    root = tk.Tk()
    game = Wordle(root)
    root.mainloop()
