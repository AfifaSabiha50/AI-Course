import tkinter as tk
from tkinter import messagebox
import math

# Initialize main window
root = tk.Tk()
root.title("Tic Tac Toe (AI - Minimax)")
root.geometry("400x450")
root.config(bg="#f0f0f0")

# Initialize board
board = [" " for _ in range(9)]
buttons = []

# Check for winner
def check_winner(player):
    win_combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def is_draw():
    return " " not in board

def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    elif check_winner("X"):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"
    buttons[move].config(text="O", state="disabled", disabledforeground="red")
    check_game_over()

def check_game_over():
    if check_winner("X"):
        messagebox.showinfo("Result", "🎉 You Win!")
        reset_game()
    elif check_winner("O"):
        messagebox.showinfo("Result", "😈 AI Wins!")
        reset_game()
    elif is_draw():
        messagebox.showinfo("Result", "It's a Draw!")
        reset_game()

def player_move(index):
    if board[index] == " ":
        board[index] = "X"
        buttons[index].config(text="X", state="disabled", disabledforeground="blue")
        check_game_over()
        if not check_winner("X") and not is_draw():
            ai_move()

def reset_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", state="normal")

# UI Layout
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

for i in range(9):
    btn = tk.Button(frame, text=" ", font=("Arial", 24, "bold"), width=5, height=2,
                    command=lambda i=i: player_move(i), bg="#fff", relief="ridge")
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

reset_btn = tk.Button(root, text="Reset", font=("Arial", 14, "bold"),
                      bg="#007BFF", fg="white", width=10, command=reset_game)
reset_btn.pack(pady=10)

root.mainloop()
