# chess_procedural.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import chess
import math

# -----------------------------
# CONFIG
# -----------------------------
AI_DEPTH = 2                 # increase to 3 for stronger but slower AI
SQUARE_SIZE = 72
SELECT_COLOR = "#FFD54F"
LEGAL_MOVE_COLOR = "#90CAF9"
LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
FONT_FAMILY = "Segoe UI Symbol"   # change if your system lacks it
FONT_SIZE = 40

# -----------------------------
# EVALUATION / AI (Minimax + Alpha-Beta)
# -----------------------------
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board):
    """
    Evaluation from AI (Black) perspective:
    Positive -> good for BLACK (AI)
    Negative -> good for WHITE (human)
    """
    score = 0
    for pt, val in piece_values.items():
        score += val * len(board.pieces(pt, chess.BLACK))
        score -= val * len(board.pieces(pt, chess.WHITE))
    return score

def evaluate_terminal(board, depth):
    """
    If terminal, return big score according to winner.
    Depth used to prefer quicker mate.
    """
    if board.is_checkmate():
        # If it's side-to-move and they are checkmated -> winner is opposite side
        # board.turn is side to move (and getting checkmated)
        winner_is_black = (board.turn == chess.WHITE)
        if winner_is_black:
            return 100000 - depth   # big positive -> good for BLACK
        else:
            return -100000 + depth  # big negative -> good for WHITE
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
        return 0
    return None

def minimax(board, depth, alpha, beta, maximizing_player):
    term = evaluate_terminal(board, depth)
    if term is not None:
        return term
    if depth == 0:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        for mv in board.legal_moves:
            board.push(mv)
            val = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            if val > max_eval:
                max_eval = val
            if val > alpha:
                alpha = val
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for mv in board.legal_moves:
            board.push(mv)
            val = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            if val < min_eval:
                min_eval = val
            if val < beta:
                beta = val
            if beta <= alpha:
                break
        return min_eval

def best_move_for_ai(board, depth=AI_DEPTH):
    """
    Choose best move for BLACK (AI). AI is maximizing player.
    """
    best_mv = None
    best_score = -math.inf
    for mv in board.legal_moves:
        board.push(mv)
        score = minimax(board, depth-1, -math.inf, math.inf, False)
        board.pop()
        if score > best_score:
            best_score = score
            best_mv = mv
    return best_mv

# -----------------------------
# GLOBAL STATE (procedural style)
# -----------------------------
board = chess.Board()
selected_square = None
legal_destinations = []

# Tkinter setup
root = tk.Tk()
root.title("Human vs AI Chess (procedural)")
canvas = tk.Canvas(root, width=8*SQUARE_SIZE, height=8*SQUARE_SIZE, highlightthickness=0)
canvas.pack()
status_lbl = tk.Label(root, text="You: White  —  AI: Black", font=("Arial", 12))
status_lbl.pack(fill="x")

# piece symbols
piece_symbols = {
    chess.PAWN: ('♙','♟'),
    chess.KNIGHT: ('♘','♞'),
    chess.BISHOP: ('♗','♝'),
    chess.ROOK: ('♖','♜'),
    chess.QUEEN: ('♕','♛'),
    chess.KING: ('♔','♚')
}

# -----------------------------
# Drawing & coordinate helpers
# -----------------------------
def coord_to_square(x, y):
    col = x // SQUARE_SIZE
    row_from_top = y // SQUARE_SIZE
    row = 7 - row_from_top
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, row)
    return None

def draw_board():
    canvas.delete("all")
    for r in range(8):
        for c in range(8):
            sq = chess.square(c, 7-r)
            x1 = c * SQUARE_SIZE
            y1 = r * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
            if selected_square == sq:
                color = SELECT_COLOR
            elif sq in legal_destinations:
                color = LEGAL_MOVE_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            piece = board.piece_at(sq)
            if piece:
                sym = piece_symbols[piece.piece_type][0 if piece.color == chess.WHITE else 1]
                fillcol = "black" if (r + c) % 2 == 0 else "white"
                canvas.create_text(x1 + SQUARE_SIZE//2, y1 + SQUARE_SIZE//2,
                                   text=sym, font=(FONT_FAMILY, FONT_SIZE), fill=fillcol)

    # optional: file letters (a-h) at bottom
    for i, ch in enumerate("abcdefgh"):
        x = i * SQUARE_SIZE + 4
        y = 8 * SQUARE_SIZE - 14
        canvas.create_text(x, y, text=ch, anchor="w", font=("Arial", 9))

# -----------------------------
# Result display
# -----------------------------
def show_result():
    res = board.result(claim_draw=True)
    if board.is_checkmate():
        # board.turn is the side to move (who got checkmated)
        winner = "Black (AI)" if board.turn == chess.WHITE else "White (You)"
        messagebox.showinfo("Game Over", f"Checkmate! Winner: {winner}")
    elif board.is_stalemate():
        messagebox.showinfo("Game Over", "Stalemate — Draw.")
    elif board.is_insufficient_material():
        messagebox.showinfo("Game Over", "Draw — insufficient material.")
    else:
        messagebox.showinfo("Game Over", f"Game over: {res}")

# -----------------------------
# Click handler & moves
# -----------------------------
def on_click(event):
    global selected_square, legal_destinations
    sq = coord_to_square(event.x, event.y)
    if sq is None:
        return

    # select a white piece if none selected
    if selected_square is None:
        piece = board.piece_at(sq)
        if piece and piece.color == chess.WHITE:
            selected_square = sq
            # gather legal destinations for highlight
            legal_destinations = [mv.to_square for mv in board.legal_moves if mv.from_square == sq]
            draw_board()
    else:
        # attempt move selected_square -> sq (handle promotion)
        mv = None
        sel_piece = board.piece_at(selected_square)
        if sel_piece and sel_piece.piece_type == chess.PAWN and chess.square_rank(sq) in (0, 7):
            # ask for promotion
            promo = simpledialog.askstring("Promotion", "Promote to (q/r/b/n):", parent=root)
            if promo and promo.lower() in ("q", "r", "b", "n"):
                promo_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
                mv = chess.Move(selected_square, sq, promotion=promo_map[promo.lower()])
        else:
            mv = chess.Move(selected_square, sq)

        if mv in board.legal_moves:
            board.push(mv)
            # reset selection
            selected_square = None
            legal_destinations = []
            draw_board()
            root.update_idletasks()
            # check game over after human move
            if board.is_game_over():
                show_result()
                return
            # AI move
            root.after(120, do_ai_move)
        else:
            # cancel selection
            selected_square = None
            legal_destinations = []
            draw_board()

# -----------------------------
# AI move
# -----------------------------
def do_ai_move():
    global board
    if board.is_game_over():
        show_result()
        return
    mv = best_move_for_ai(board, depth=AI_DEPTH)
    if mv:
        board.push(mv)
        draw_board()
        if board.is_game_over():
            show_result()
    else:
        show_result()

# -----------------------------
# Bind & Start
# -----------------------------
canvas.bind("<Button-1>", on_click)
draw_board()
root.mainloop()
