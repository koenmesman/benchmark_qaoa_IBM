import json
import matplotlib.pyplot as plt
import numpy as np

def plot_json(file, fig):
    data = json.load(file)
    results = json.loads(data.get('data'))
    #max_size = data.get('size')
    size = [x.get('size') for x in results]
    max_size = size[-1]
    score = [json.loads(x.get('score'))[0] for x in results]
    time = [x.get('time') for x in results]

    length = max_size-size[0]+1
    print(length)
    print(size)

    cumulative_time = [0]*length

    for key in time[0].keys():
        if key != 'WALLTIME':
            for x in time:
                if key == 'CONNECTION':
                    if not x.get(key):
                        x['CONNECTION'] = 0
                x['WALLTIME'] -= x[key]

        cumulative_time = [cumulative_time[y] + [x.get(key) for x in time][y] for y in range(length)]
        plt.plot(size, cumulative_time, label=key)


fig1 = plt.figure()
file = open('log_qasm_sim/log_qiskit_mcp.json')
plot_json(file, fig1)
plt.legend()
plt.show()

fig2 = plt.figure()
file = open('log_qiskit_mcp.json')
plot_json(file, fig2)
plt.legend()
plt.show()
