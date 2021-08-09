"""A sample runtime program that submits random circuits for user-specified iterations."""

from qiskit import transpile, ClassicalRegister, QuantumRegister, QuantumCircuit
import scipy.optimize as opt
import numpy as np
import time
from numpy import pi
import datetime

global BENCHMARK_TIMES

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


def shgo_fun(init_param, graph, p, q_func, backend):  # simplicial homology global optimization
    bounds = [(0, pi), (0, 2 * pi)]
    res = []
    if q_func == 'mcp':
        min_func = max_cut_norm
        v, e = graph
        res = opt.shgo(min_func, bounds, args=(v, e, p, backend),
                       options={'ftol': 1e-10})  # perhaps v, e can be replaced with graph


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


def mcp_shgo(params, size, p, iterations, backend):
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
    print(result)
    time_res = job.time_per_step()

    times = get_times(time_res)
    global BENCHMARK_TIMES
    BENCHMARK_TIMES = merge_times(BENCHMARK_TIMES, times)
    print(time_res)
    out_state = result.get_counts()

    prob = list(out_state.values())
    states = list(out_state.keys())
    exp = 0
    for k in range(len(states)):
        exp += eval_cost(states[k], graph) * prob[k]

    return exp/iterations

def merge_times(old_times, new_times):
    for key, new_val in new_times.items():
        if old_times[key] and new_times[key]:
            new_times[key] = new_val + old_times[key]
    return new_times

def get_times(job):
    create = job.get('CREATED')-job.get('CREATING')
    validate = job.get('VALIDATED') - job.get('VALIDATING')
    if isinstance(job.get('RUNNING'), datetime.datetime) and isinstance(job.get('QUEUED'), datetime.datetime):
        queue = job.get('RUNNING') - job.get('QUEUED')
    else:
        queue = datetime.timedelta()

    if isinstance(job.get('RUNNING'), datetime.datetime):
        runtime = job.get('COMPLETED') - job.get('RUNNING')
    else:
        runtime = datetime.timedelta()

    other = job.get('COMPLETED') - job.get('CREATING') - create - validate - queue - runtime
    total = job.get('COMPLETED') - job.get('CREATING')
    out_dict = {'CREATING': create, 'VALIDATING': validate, 'QUEUED': queue, 'RUNNING': runtime, 'OTHER': other, 'CONNECTION': total}
    for key, val in out_dict.items():
        out_dict[key] = val.total_seconds()

    return out_dict

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
    shots = 1000
    bounds = [(0, pi), (0, 2 * pi)]
    for it in range(iterations):
        zero_time = datetime.timedelta()
        global BENCHMARK_TIMES
        BENCHMARK_TIMES = {'CREATING': zero_time, 'VALIDATING': zero_time, 'QUEUED': zero_time, 'RUNNING': zero_time,
                           'OTHER': zero_time, 'CONNECTION': 0, 'WALLTIME': zero_time}
        size += it
        print(it)
        #result = opt.minimize(mcp, params, args=(size, p, shots, backend), method='nelder-mead',
        #               options={'ftol': 1e-2, 'maxfev': 10, 'disp': False})
        start = time.time()
        result = opt.shgo(mcp_shgo, bounds, args=(size, p, shots, backend),
                       options={'ftol': 1e-10, 'maxfev': 1000}) 
        end = time.time() - start
        BENCHMARK_TIMES['WALLTIME'] = end
        print(BENCHMARK_TIMES)
        #result = mcp(params, size, p, backend)
        user_messenger.publish({"iteration": it, "results": result, "time": end})

    user_messenger.publish("All done!", final=True)
