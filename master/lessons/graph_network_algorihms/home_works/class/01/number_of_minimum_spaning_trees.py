def is_connected(adj_matrix):
    n = len(adj_matrix)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in range(n):
            if adj_matrix[u][v] == 1 and not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited)

def contract_edge(adj_matrix, u, v):
    n = len(adj_matrix)
    new_adj = [row[:] for row in adj_matrix]
    new_adj[u][v] = 0
    new_adj[v][u] = 0
    for i in range(n):
        if new_adj[v][i] == 1 and i != u:
            new_adj[u][i] = 1
            new_adj[i][u] = 1
        new_adj[v][i] = 0
        new_adj[i][v] = 0
    new_adj.pop(v)
    for row in new_adj:
        row.pop(v)
    return new_adj

def delete_edge(adj_matrix, u, v):
    new_adj = [row[:] for row in adj_matrix]
    new_adj[u][v] = 0
    new_adj[v][u] = 0
    return new_adj

def spanning_trees(adj_matrix):
    n = len(adj_matrix)
    if n == 1:
        return 1
    if not is_connected(adj_matrix):
        return 0
    
    for u in range(n):
        for v in range(u + 1, n):
            if adj_matrix[u][v] == 1:
                adj_minus_e = delete_edge(adj_matrix, u, v)
                t_minus_e = spanning_trees(adj_minus_e)
                adj_contract_e = contract_edge(adj_matrix, u, v)
                t_contract_e = spanning_trees(adj_contract_e)
                return t_minus_e + t_contract_e
    return 1 if n == 1 else 0


test_cases = {
    "K2": [[0, 1], [1, 0]],  
    "P3": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],  
    "K3": [[0, 1, 1], [1, 0, 1], [1, 1, 0]],  
    "K4": [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]  
}

for name, adj_matrix in test_cases.items():
    result = spanning_trees(adj_matrix)
    print(f"تعداد درخت‌های پوشا برای {name}: {result}")
