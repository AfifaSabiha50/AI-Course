## AI Games Collection
---
Welcome to the AI Games Collection!
This repository contains three interactive games developed in Python (using Tkinter GUI), each featuring an AI opponent that makes intelligent moves using algorithms like Minimax and Alpha-Beta pruning.

## Included Games
---
## Tic Tac Toe (AI - Minimax)
---

A classic 3x3 board game where you play as ‘X’ against an AI opponent (‘O’) powered by the Minimax algorithm.
The AI always plays optimally — your goal is to either win or at least force a draw!

---
## Chess (Human vs AI)
---

A simplified chess game built with the python-chess library and Tkinter GUI.
You play as White, and the AI (Black) uses the Minimax algorithm with Alpha-Beta pruning for decision-making.
It includes checkmate, stalemate, and draw detection just like a real chess engine!

---
## Subtraction Game (AI - Minimax)
---

A mathematical game starting with 25 stones.
Each player (you and the AI) can remove 1, 2, or 3 stones per turn.
The player who removes the last stone wins!
The AI uses the Minimax algorithm to plan its moves perfectly — can you outsmart it? 

---
Technologies Used
---

. Python 3.x

. Tkinter (for GUI)

. python-chess (only for Chess game)

. Math library (for AI calculations)

---
Features
---

1.  User-friendly GUI for all games
2.  AI opponent with Minimax or Alpha-Beta pruning
3.  Real-time interaction and visual feedback
4.  Simple to run and play — perfect for beginners exploring game AI

---
Folder Structure 
---

AI-Games/
 TicTacToe/
│   ├── tic_tac_toe.py
│   ├── Screenshot/
│   │   └── tic-tac-toe.png
│   └── README.md
│
├── Chess/
│   ├── chess_procedural.py
│   ├── Screenshot/
│   │   └── chess.png
│   └── README.md
│
├── SubtractionGame/
│   ├── subtraction_game.py
│   ├── Screenshot/
│   │   └── subtraction.png
│   └── README.md
│
└── README.md  ← (this file)

---
Algorithm Summary
---

| Game             | Algorithm Used                   | Purpose                      |
| ---------------- | -------------------------------- | ---------------------------- |
| Tic Tac Toe      | **Minimax**                      | Optimal move prediction      |
| Chess            | **Minimax + Alpha-Beta Pruning** | Efficient AI decision-making |
| Subtraction Game | **Minimax**                      | Winning strategy computation |

---
Getting Started
---

To run any game:

1. Ensure Python 3.x is installed.

2. Run the corresponding .py file using:
   
     python filename.py
   
4. Enjoy playing against your AI opponent!

