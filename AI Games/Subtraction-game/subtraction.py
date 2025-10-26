import tkinter as tk
from tkinter import messagebox
import math

# ----------------- Minimax Algorithm -----------------
def minimax(stones, is_maximizing):
    # Base case: No stones left
    if stones == 0:
        if is_maximizing:
            return -1   # AI turn: means AI lost
        else:
            return 1    # Player turn: means AI won

    scores = []  # store all possible outcomes for this state

    for move in [1, 2, 3]:
        if stones - move >= 0:
            next_score = minimax(stones - move, not is_maximizing)
            scores.append(next_score)

    # Instead of best_score = ... return ..., we use simpler logic:
    return max(scores) if is_maximizing else min(scores)

def ai_move(stones):
    best_score = -math.inf
    best_move = 1

    for move in [1, 2, 3]:
        if stones - move >= 0:
            score = minimax(stones - move, False)
            if score > best_score:
                best_score = score
                best_move = move

    return best_move
# ----------------- Game Logic -----------------
stones = 25  # Initial number of stones

def update_stones_display():
    canvas.delete("all")
    for i in range(stones):
        x = 20 + (i % 5) * 60
        y = 20 + (i // 5) * 60
        color = "#FF6F61" if i % 2 == 0 else "#6B5B95"
        canvas.create_oval(x, y, x + 50, y + 50, fill=color, outline="#333", width=2)
        canvas.create_text(x + 25, y + 25, text=str(stones - i), fill="white", font=("Helvetica", 14, "bold"))

def player_move(move):
    global stones
    if move > stones:
        messagebox.showwarning("Invalid Move", "Not enough stones!")
        return

    stones -= move
    update_stones_display()

    if stones == 0:
        messagebox.showinfo("Game Over", "You win! 🎉")
        root.destroy()
        return

    root.after(500, ai_turn)

def ai_turn():
    global stones
    move = ai_move(stones)
    stones -= move
    update_stones_display()
    ai_label.config(text=f"AI removed {move} stone{'s' if move > 1 else ''}")

    if stones == 0:
        messagebox.showinfo("Game Over", "AI wins! 🤖")
        root.destroy()
        return
# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("Subtraction Game")
root.configure(bg="#2C3E50")

title_label = tk.Label(root, text="Subtraction Game", font=("Helvetica", 24, "bold"), fg="white", bg="#2C3E50")
title_label.pack(pady=20)

canvas = tk.Canvas(root, width=350, height=200, bg="#34495E", highlightthickness=0)
canvas.pack(pady=20)
update_stones_display()

ai_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="#F1C40F", bg="#2C3E50")
ai_label.pack(pady=5)

buttons_frame = tk.Frame(root, bg="#2C3E50")
buttons_frame.pack(pady=10)

btn_style = {"font": ("Helvetica", 16, "bold"), "bg": "#1ABC9C", "fg": "white", "width": 10, "height": 2, "bd": 0, "activebackground": "#16A085"}

for i in [1, 2, 3]:
    btn = tk.Button(buttons_frame, text=f"Remove {i}", **btn_style, command=lambda x=i: player_move(x))
    btn.grid(row=0, column=i - 1, padx=15, pady=10)

root.mainloop()
