"""A sample runtime program that submits random circuits for user-specified iterations."""

from qiskit import transpile, ClassicalRegister, QuantumRegister, QuantumCircuit
import scipy.optimize as opt
import numpy as np

def regular_graph(n):
    edges = []
    for i in range(n-1):
        edges.append([i, i+1])
    edges.append([0, n-1])
    for i in range(n-2):
        edges.append([i, i+2])
    edges.append([0, n-2])
    edges.append([1, n-1])
    return [n, edges]


def eval_cost(out_state, graph):
    # evaluate Max-Cut
    v = graph[0]
    edges = graph[1]
    c = 0
    bin_len = "{0:0" + str(v) + "b}"  # string required for binary formatting
    bin_val = [int(i) for i in list(out_state)]
    bin_val = [-1 if x == 0 else 1 for x in bin_val]
    for e in edges:
        c += 0.5 * (1 - int(bin_val[e[0]]) * int(bin_val[e[1]]))
    return c


def prepare_circuits(backend, params, graph, p):
    """Generate a QAOA Max-Cut problem circuit.

    Args:
        backend: Backend used for transpilation.
        params: Parameters beta and gamma used in QAOA.
        graph: Graph of the target problem.
        p: Number of QAOA iterations.

    Returns:
        Generated circuit.
    """
    beta = params[0:p]
    gamma = params[p:2*p]

    v, edge_list = graph
    vertice_list = list(range(0, v, 1))

    c = ClassicalRegister(v)
    q = QuantumRegister(v)
    qc = QuantumCircuit(q, c)
    for qubit in range(v):
        qc.h(qubit)
    for iteration in range(p):
        for e in edge_list:
            qc.cnot(e[0], e[1])
            qc.rz(-gamma[p-1], e[1])
            qc.cnot(e[0], e[1])
        for qb in vertice_list:
            qc.rx(2*beta[p-1], qb)
    qc.measure(q, c)

    return transpile(qc, backend)


def mcp(params, size, p, iterations, backend):
    """Run and evaluate the QAOA MaxCut problem.

    Args:
        backend: Backend used for transpilation.
        params: Parameters beta and gamma used in QAOA.
        size: Problem size.
        p: Number of QAOA iterations.

    Returns:
        Generated circuit.
    """
    graph = regular_graph(size)
    qc = prepare_circuits(backend, params, graph, p)
    job = backend.run(qc, shots=iterations)
    result = job.result()
    #time_res = job.time_per_step()
    out_state = result.get_counts()

    prob = list(out_state.values())
    states = list(out_state.keys())
    exp = 0
    for k in range(len(states)):
        exp += eval_cost(states[k], graph) * prob[k]

    return -exp/iterations

def main(backend, user_messenger, **kwargs):
    """Main entry point of the program.

    Args:
        backend: Backend to submit the circuits to.
        user_messenger: Used to communicate with the program consumer.
        kwargs: User inputs.
    """
    iterations = kwargs.pop('iterations', 5)
    p = kwargs.pop('p')
    params = np.zeros(2*p)
    size = 5
    shots = 10000
    for it in range(iterations):
        size += it
        result = opt.minimize(mcp, params, args=(size, p, shots, backend), method='nelder-mead',
                       options={'ftol': 1e-2, 'maxfev': 1000, 'disp': False})
        #result = mcp(params, size, p, backend)
        user_messenger.publish({"iteration": it, "results": result})

    user_messenger.publish("All done!", final=True)