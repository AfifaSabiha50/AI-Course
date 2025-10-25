def minimax(depth, node_index, is_max, scores, max_depth):
    if depth == max_depth:
        return scores[node_index]

    if is_max:
        left = minimax(depth+1, node_index*2, False, scores, max_depth)
        right = minimax(depth+1, node_index*2+1, False, scores, max_depth)
        return max(left, right)
    else:
        left = minimax(depth+1, node_index*2, True, scores, max_depth)
        right = minimax(depth+1, node_index*2+1, True, scores, max_depth)
        return min(left, right)



scores = input("Enter leaf node scores: ").split()
scores = [int(x) for x in scores]

import math
max_depth = int(math.log(len(scores), 2))

print("Optimal value (Minimax):", minimax(0, 0, True, scores, max_depth))

