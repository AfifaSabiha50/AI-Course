def depth_limited_search(graph, start, goal, limit):
    def recursive_dls(node, goal, limit, visited):
        print(f"Visiting: {node}, Remaining depth: {limit}")
        if node == goal:
            return [node]  # Goal পাওয়া গেছে, path return করো
        
        if limit <= 0:
            return None  # Depth limit শেষ, আর নিচে যাবে না
        
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                path = recursive_dls(neighbor, goal, limit - 1, visited)
                if path:
                    return [node] + path
        
        return None  # Goal না পাওয়া গেলে None

    return recursive_dls(start, goal, limit, set())


# -------- User Input -------
graph = {}
num_nodes = int(input("Enter number of nodes: "))
num_edges = int(input("Enter number of edges: "))

# Nodes
for _ in range(num_nodes):
    node = input("Enter node name: ")
    graph[node] = []

# Edges (Undirected)
print("\nEnter edges (node1 node2):")
for _ in range(num_edges):
    u, v = input().split()
    graph[u].append(v)
    graph[v].append(u)

start_node = input("\nEnter start node: ")
goal_node = input("Enter goal node: ")
depth_limit = int(input("Enter depth limit: "))

# Run DLS
path = depth_limited_search(graph, start_node, goal_node, depth_limit)

if path:
    print("\nPath found:")
    print(" -> ".join(path))
else:
    print("\nNo path found within depth limit")
