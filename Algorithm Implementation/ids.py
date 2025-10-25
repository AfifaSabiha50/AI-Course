def depth_limited_search(graph, start, goal, limit, visited=None):
    if visited is None:
        visited = set()
    if limit < 0:
        return None
    print(f"Visiting: {start}, Remaining depth: {limit}")
    if start == goal:
        return [start]
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            path = depth_limited_search(graph, neighbor, goal, limit - 1, visited)
            if path:
                return [start] + path
    visited.remove(start)
    return None

def iterative_deepening_search(graph, start, goal, max_depth):
    for depth in range(max_depth + 1):
        print(f"\n--- Searching with depth limit = {depth} ---")
        path = depth_limited_search(graph, start, goal, depth)
        if path:
            return path
    return None

# -------- User Input --------
graph = {}
num_nodes = int(input("Enter number of nodes: "))
num_edges = int(input("Enter number of edges: "))

for _ in range(num_nodes):
    node = input("Enter node name: ")
    graph[node] = []

print("\nEnter edges (node1 node2):")
for _ in range(num_edges):
    u, v = input().split()
    graph[u].append(v)
    graph[v].append(u)

start_node = input("\nEnter start node: ")
goal_node = input("Enter goal node: ")
max_depth = int(input("Enter maximum depth limit: "))

path = iterative_deepening_search(graph, start_node, goal_node, max_depth)

if path:
    print("\nPath found:")
    print(" -> ".join(path))
else:
    print("\nNo path found within max depth limit")
