from collections import deque

def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])

    print("\nBFS Traversal:")
    while queue:
        current = queue.popleft()
        if current not in visited:
            print(current, end=' ')
            visited.add(current)
            queue.extend(neighbor for neighbor in graph[current] if neighbor not in visited)
           
# ----- User Input -----
graph = {}
num_nodes = int(input("Enter number of nodes: "))
num_edges = int(input("Enter number of edges: "))

# Initialize graph with empty adjacency list
for i in range(num_nodes):
    node = input(f"Enter name of node {i+1}: ")
    graph[node] = []

# Take input for edges
print("\nEnter edges (node1 node2):")
for _ in range(num_edges):
    u, v = input().split()
    graph[u].append(v)
    graph[v].append(u)  # For undirected graph

# Show graph structure (optional)
print("\nGraph Adjacency List:")
for node in graph:
    print(f"{node}: {graph[node]}")

# BFS Execution
start_node = input("\nEnter starting node for BFS: ")
if start_node in graph:
    bfs(graph, start_node)
else:
    print("Start node not found in graph.")
