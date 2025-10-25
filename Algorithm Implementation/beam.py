def beam_search(graph, start, goal, heuristic, beam_width):
    OPEN = [(start, start)]  
    
    while len(OPEN) > 0:

        next_level = [] 

        for node, path in OPEN:
            if node == goal:
                print("Goal reached:", node)
                print("Path:", path)
                return

            for neigh in graph[node]:
                if neigh not in [n for n, _ in next_level] : 
                    new_path = path + " -> " + neigh
                    next_level.append((neigh, new_path))

        
        temp = []
        for neigh, path in next_level:
            temp.append((heuristic[neigh], neigh, path))  

        temp.sort() 

        next_level = []
        for i in range(min(beam_width, len(temp))):
            next_level.append((temp[i][1], temp[i][2]))  
        OPEN = next_level
        
graph = {}
heuristic = {}

n = int(input("How many nodes? "))

for i in range(n):
    node = input("Node name : ")
    h = int(input("Heuristic of " + node + ": "))
    heuristic[node] = h
    neighbors = input("Neighbors of " + node + ": ").split()
    graph[node] = neighbors

start = input("Start node: ")
goal = input("Goal node: ")
beam_width = int(input("Beam width: "))

beam_search(graph, start, goal, heuristic, beam_width)

