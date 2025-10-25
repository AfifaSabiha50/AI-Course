import math
t = 0
def alphabeta(depth, index, is_max, scores, alpha, beta, max_depth):
    global t
    if depth == max_depth:
        return scores[index]

    if is_max:
        best = -math.inf
        for i in range(2):  
            val = alphabeta(depth+1, index*2+i, False, scores, alpha, beta, max_depth)
            best = max(best, val)
            alpha = max(alpha, best)

            
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for i in range(2):
            val = alphabeta(depth+1, index*2+i, True, scores, alpha, beta, max_depth)
            best = min(best, val)
            beta = min(beta, best)

            if beta <= alpha:
                t+=1
                break
        return best
    
n = int(input("Enter number of leaf nodes (power of 2): "))

scores = [int(x) for x in input("Enter leaf values: ").split()]

if len(scores) != n:
    print("Number of scores must match leaf nodes")
else:
    max_depth = int(math.log2(n))
    result = alphabeta(0, 0, True, scores, -math.inf, math.inf, max_depth)

    print("\n===== RESULT =====")
    print("Leaf nodes:", scores)
    print("Optimal value:", result) 
    print("Prune node", t)
