def best_first_search(graph, start, goal, heuristic):
    OPEN = [(heuristic[start], start)]  
    path = []

    while len(OPEN) > 0:
        print("OPEN:", OPEN)     

        OPEN = sorted(OPEN)
        cost,node = OPEN[0]
        OPEN = OPEN[1:]

        print("Visiting:", node)
        path.append(node)

        if node == goal:
            print("Goal found:", node)
            print("Path:", " -> ".join(path))
            return

        for neigh in graph[node]:
            if neigh not in path:   
                OPEN.append((heuristic[neigh], neigh))

graph = {}    
heuristic = {}

n = int(input("How many nodes? "))

for i in range(n):
    node = input("Node name: ")
    h = int(input("Heuristic of " + node + ": "))
    heuristic[node] = h
    neighbors = input("Neighbors of " + node + ": " ).split()
    graph[node] = neighbors

start = input("Start node: ")
goal = input("Goal node: ")

best_first_search(graph, start, goal, heuristic)

