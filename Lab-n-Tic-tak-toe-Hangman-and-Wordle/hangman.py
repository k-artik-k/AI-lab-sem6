import tkinter as tk
from tkinter import messagebox
import random
import time

class Hangman:
    def __init__(self, root):
        self.root = root
        self.root.title("HANGMAN")
        self.root.configure(bg="#121213")
        self.root.resizable(False, False)

        self.words = [
            "PYTHON", "HANGMAN", "COMPUTER", "PROGRAM", "ALGORITHM",
            "VARIABLE", "FUNCTION", "STRING", "INTEGER", "RANDOM"
        ]

        # Game variables
        self.max_tries = 6
        self.reset_game()

        # UI
        self.create_ui()

    def reset_game(self):
        self.word = random.choice(self.words).upper()
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.display_word = ["_" if c.isalpha() else c for c in self.word]
        self.game_over = False

    def create_ui(self):
        # Title
        self.title_label = tk.Label(self.root, text="HANGMAN", font=("Helvetica", 32, "bold"),
                                    fg="white", bg="#121213")
        self.title_label.pack(pady=10)

        # Canvas for hangman drawing
        self.canvas = tk.Canvas(self.root, width=300, height=400, bg="#121213", highlightthickness=0)
        self.canvas.pack()

        # Display word
        self.word_label = tk.Label(self.root, text=" ".join(self.display_word),
                                   font=("Helvetica", 24, "bold"), fg="white", bg="#121213")
        self.word_label.pack(pady=20)

        # Keyboard
        self.keyboard_frame = tk.Frame(self.root, bg="#121213")
        self.keyboard_frame.pack(pady=10)

        self.keyboard_buttons = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, bg="#818384",
                            fg="white", command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i//9, column=i%9, padx=3, pady=3)
            self.keyboard_buttons[letter] = btn

        # New game button
        self.new_game_btn = tk.Button(self.root, text="NEW GAME", bg="#538d4e", fg="white", width=12,
                                      command=self.start_new_game)
        self.new_game_btn.pack(pady=10)

        # Draw initial gallows
        self.draw_gallows()

    def start_new_game(self):
        self.reset_game()
        self.word_label.config(text=" ".join(self.display_word))
        for btn in self.keyboard_buttons.values():
            btn.config(state=tk.NORMAL, bg="#818384")
        self.canvas.delete("hangman")
        self.draw_gallows()

    def guess_letter(self, letter):
        if self.game_over:
            return
        self.keyboard_buttons[letter].config(state=tk.DISABLED)
        if letter in self.word:
            self.keyboard_buttons[letter].config(bg="#538d4e")  # green for correct
            for i, c in enumerate(self.word):
                if c == letter:
                    self.display_word[i] = letter
            self.word_label.config(text=" ".join(self.display_word))
            if "_" not in self.display_word:
                self.game_over = True
                messagebox.showinfo("HANGMAN", "You Won! ")
        else:
            self.keyboard_buttons[letter].config(bg="#b59f3b")  # yellow/orange for wrong
            self.wrong_guesses += 1
            self.draw_hangman_part(self.wrong_guesses)
            if self.wrong_guesses >= self.max_tries:
                self.game_over = True
                messagebox.showinfo("HANGMAN", f"You Lost! The word was: {self.word}")

    # Draw gallows
    def draw_gallows(self):
        self.canvas.create_line(50, 350, 250, 350, fill="white", width=4)  # base
        self.canvas.create_line(100, 350, 100, 50, fill="white", width=4)  # pole
        self.canvas.create_line(100, 50, 200, 50, fill="white", width=4)   # top beam
        self.canvas.create_line(200, 50, 200, 80, fill="white", width=4)   # rope

    # Draw hangman parts with animation
    def draw_hangman_part(self, step):
        # step 1 = head, 2 = body, 3 = left arm, 4 = right arm, 5 = left leg, 6 = right leg
        if step == 1:
            self.canvas.create_oval(175, 80, 225, 130, outline="white", width=4, tags="hangman")  # head
        elif step == 2:
            self.canvas.create_line(200, 130, 200, 230, fill="white", width=4, tags="hangman")  # body
        elif step == 3:
            self.canvas.create_line(200, 150, 160, 190, fill="white", width=4, tags="hangman")  # left arm
        elif step == 4:
            self.canvas.create_line(200, 150, 240, 190, fill="white", width=4, tags="hangman")  # right arm
        elif step == 5:
            self.canvas.create_line(200, 230, 170, 280, fill="white", width=4, tags="hangman")  # left leg
        elif step == 6:
            self.canvas.create_line(200, 230, 230, 280, fill="white", width=4, tags="hangman")  # right leg
# Main
if __name__ == "__main__":
    root = tk.Tk()
    hangman = Hangman(root)
    root.mainloop()