#!/usr/bin/env python
import generate_graph as gg

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def mcp_solver(g):
    result = 0
    size, edges = g
    for n in range(2**(size-1)):
        node_array = bitfield(n)
        node_array.extend([0]*(size-len(node_array)))
        node_array = [-1 if x == 0 else 1 for x in node_array]
        c = 0
        for e in edges:
            c += 0.5 * (1 - int(node_array[e[0]]) * int(node_array[e[1]]))
        if c >= result:
            result = c
    return result

def mcp_score(max_size):
    opt_results = [0] * (max_size - 4)
    for i in range(5, max_size+1):
        print(i)
        graph = gg.regular_graph(i)
        opt_results[i - 5] = mcp_solver(graph)
        print(opt_results)
    return opt_results


def dsp_score(max_size):
    opt_results = [0] * (max_size - 4)
    for i in range(5, max_size + 1):
        print(i)
        result = 0
        c = 0
        size, edges = gg.regular_graph(i)
        connections = []
        for k in range(size):
            connections.append([k])
        for t in edges:
            connections[t[0]].append(t[1])
            connections[t[1]].append(t[0])
        for n in range(2 ** size):
            node_array = bitfield(n)
            node_array.extend([0] * (size - len(node_array)))
            T = 0
            for con in connections:
                tmp = 0
                for k in con:
                    tmp = tmp or node_array[k]
                    if tmp:
                        T += 1
                        break
            D = 0
            for j in range(size):
                D += 1 - node_array[j]
            c = (T + D)
            if c >= result:
                result = c
        opt_results[i - 5] = result
    return opt_results

def tsp_score(max_size):
    opt_results = [0]*(max_size-4)
    for n in range(5, max_size+1):
        size, A, D = gg.tsp_problem_set(n, gg.regular_graph)
        cost = 0
        coupling = []
        result = 10**8
        for i in range(size):
            for j in range(i):
                if i != j:
                    coupling.append([i + j * size, j + i * size])
        print("evaluating all possible configurations, this might take a while.")
        for k in range(2 ** (size**2)):
            cost = 0
            node_array = bitfield(k)
            node_array.extend([0] * (size**2 - len(node_array)))
            for i in range(0, size):
                for j in range(i, size):
                    cost += D[i + size * j] * node_array[i + size * j]
            for j in coupling:
                cost += -5 * (1 - 2 * node_array[j[0]]) * (1 - 2 * node_array[j[1]])
            if cost <= result:
                print(cost)
                print(node_array)
                result = cost
        opt_results[n-5] = result
    return opt_results


#max_size = 50
#opt_results = [0]*(max_size-4)
#for i in range(4, max_size+1):
#    graph = gg.regular_graph(i)
#    opt_results[i-5] = mcp_solver(graph)
#print(opt_results)
