def a_star_search(graph, start, goal, heuristic, cost):
    queue = [(heuristic[start], 0, start, start)] 
    while len(queue) > 0:
        queue = sorted(queue)
        f, g, node, path = queue[0]
        queue = queue[1:]
        
        if node == goal:
            print("Goal found. Path :", path, "Cost:", g)
            return

        for neigh in graph[node]:
            if neigh not in path:
                new_g = g + cost[(node, neigh)]
                new_f = new_g + heuristic[neigh]
                queue.append((new_f, new_g, neigh, path + " " + neigh))

graph = {}
heuristic = {}
cost = {}

n = int(input("How many nodes? "))

for i in range(n):
    node = input("Node name : ")
    h = int(input("Heuristic of " + node + ": "))
    heuristic[node] = h
    neighbors = input("Neighbors of " + node + ": ").split()
    graph[node] = neighbors
    for neigh in neighbors:
        c = int(input("Cost from " + node + " to " + neigh + ": "))
        cost[(node, neigh)] = c

start = input("Start node: ")
goal = input("Goal node: ")

a_star_search(graph, start, goal, heuristic, cost)

