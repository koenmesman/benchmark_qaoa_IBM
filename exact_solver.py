import generate_graph as gg

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def mcp_solver(g):
    result = 0
    size, edges = g
    for n in range(size**2):
        node_array = bitfield(n)
        node_array.extend([0]*(size-len(node_array)))
        node_array = [-1 if x == 0 else 1 for x in node_array]
        c = 0
        for e in edges:
            c += 0.5 * (1 - int(node_array[e[0]]) * int(node_array[e[1]]))
        if c >= result:
            result = c
    return result


max_size = 50
opt_results = [0]*(max_size-4)
for i in range(4, max_size+1):
    graph = gg.regular_graph(i)
    opt_results[i-5] = mcp_solver(graph)
print(opt_results)
