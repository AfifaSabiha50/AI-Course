def dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()  
    
    if start_node not in visited:
        print(start_node, end=' ')  # present node print
        visited.add(start_node)     # visited list e add
        
        for neighbor in sorted(graph[start_node]):  # Sorted neighbor
            dfs(graph, neighbor, visited)


# ----- User Input -----
graph = {}
num_nodes = int(input("Enter number of nodes: "))
num_edges = int(input("Enter number of edges: "))

# Node input
for i in range(num_nodes):
    node = input(f"Enter name of node {i+1}: ")
    graph[node] = []

# Edge গুলো ইনপুট
print("\nEnter edges (node1 node2):")
for _ in range(num_edges):
    u, v = input().split()
    graph[u].append(v)
    graph[v].append(u)  # Undirected Graph

# Adjacency List প্রিন্ট
print("\nGraph Adjacency List:")
for node in graph:
    print(f"{node}: {graph[node]}")

# DFS চালানো
start_node = input("\nEnter starting node for DFS: ")
g= input("\n goal node:")
if start_node in graph:
    print("\nDFS Traversal:")
    dfs(graph, start_node)
else:
    print("Start node not found in graph.")
