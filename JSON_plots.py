import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import exact_solver

def plot_json(file, fig):
    #data = json.load(file)
    #results = json.loads(data.get('data'))
    #print(results)
    results = file
    size = [x.get('size') for x in results]
    max_size = size[-1]
    score = [json.loads(x.get('score'))[0] for x in results]
    time = [x.get('time') for x in results]
    length = max_size-size[0]+1
    cumulative_time = [0]*length

    for key in time[0].keys():
        if key != 'WALLTIME' and key != 'CONNECTION':
            for x in time:
                x['WALLTIME'] -= x[key]
                x['CONNECTION'] -= x[key]
    for x in time:
        x['WALLTIME'] -= x['CONNECTION']
    for key in time[0].keys():
        cumulative_time = [cumulative_time[y] + [x.get(key) for x in time][y] for y in range(length)]
        plt.plot(size[0:18], cumulative_time[0:18], label=key)

def plot_all_perc(file):
    #data = json.load(file)
    #results = json.loads(data.get('data'))
    results = file
    size = [x.get('size') for x in results]
    max_size = size[-1]
    score = [json.loads(x.get('score'))[0] for x in results]
    time = [x.get('time') for x in results]
    length = max_size - size[0] + 1
    cumulative_time = [0]*length

    for key in time[0].keys():
        if key != 'WALLTIME' and key != 'CONNECTION':
            for x in time:
                x['WALLTIME'] -= x[key]
                x['CONNECTION'] -= x[key]
    for x in time:
        x['WALLTIME'] -= x['CONNECTION']
    for key in time[0].keys():
        cumulative_time = [cumulative_time[y] + [x.get(key) for x in time][y] for y in range(length)]
        cumulative_time = [cumulative_time[y]/time[y].get('WALLTIME') for y in range(length)]
        plt.plot(size, cumulative_time, label=key)

def plot_single_perc(file, fig):
    data = json.load(file)
    results = json.loads(data.get('data'))
    time = results[0].get('time')
    print(time)

    for key in time.keys():
        if key != 'WALLTIME' and key != 'CONNECTION':
            time['CONNECTION'] -= time[key]
    for key in time.keys():
        time[key] = time[key]/time['WALLTIME']
        print(time[key])
    for key in time.keys():
        if key != 'WALLTIME' and key != 'CONNECTION':
            time['WALLTIME'] -= time[key]
    time['CLASSIC'] = time.pop('WALLTIME')
    ax = fig.add_subplot(111)
    ax.bar(time.keys(), time.values())
    ax.set_xticklabels(time.keys(), rotation=35)
    plt.ylabel('fraction runtime')

def plot_score_dsp(file):
    fig, ax = plt.subplots()
    data = json.load(file)
    results = json.loads(data.get('data'))
    #results = file
    score = [json.loads(x.get('score'))[0] for x in results]
    size = [x.get('size') for x in results]
    best_score = exact_solver.dsp_score(size[-1])
    plt.plot(size, score, label='measured score')
    plt.plot(size, best_score, label='optimal score')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel("graph size [nodes]")
    plt.ylabel("score")
    plt.legend()

def plot_score_mcp(file):
    fig, ax = plt.subplots()
    results = file
    score = [json.loads(x.get('score'))[0] for x in results]
    size = [x.get('size') for x in results]
    #best_score = exact_solver.mcp_score(size[-1])
    best_score = [6.0, 8.0, 10.0, 12.0, 12.0, 14.0, 16.0, 18.0, 18.0, 20.0, 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 30.0, 32.0, 34.0, 36.0]
    plt.plot(size, score, label='measured score')
    plt.plot(size, best_score[0:len(size)], label='optimal score')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel("graph size [nodes]")
    plt.ylabel("score")
    plt.legend()

def plot_accuracy(file, fig, ax):
    data = json.load(file)
    results = json.loads(data.get('data'))
    score = [json.loads(x.get('score'))[0] for x in results]
    print(score)
    size = [x.get('size') for x in results]
    print(size)
    #best_score = exact_solver.dsp_score(size[-1])

    best_score = [9, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 28, 30, 32, 34, 36, 37, 39, 41]
    accuracy = [score[i]/best_score[i] for i in range(len(score))]
    print(accuracy)
    plt.plot(size, accuracy, label='measured outcome accuracy')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel("graph size [nodes]")
    plt.ylabel("outcome accuracy")



#######################SCORE IBM QASM + MONTEAL########################################
#file = open('log_montreal/ibmq_nairobi_mcp.json')
#plot_score_mcp(file)
#plt.title('Score MCP on Nairobi')
#plt.savefig('score_nairobi_mcp.pdf')
#plt.show()
#fig, ax = plt.subplots()

#data = [0]*20
#with open('log_montreal/mcp_ibmq_montreal_5_to_24', 'rt') as file:
#    i = 0
#    for line in file:
#        data[i] = json.loads(line)
#        i += 1

#plot_score_mcp(data)
#plt.title('score MCP on IBM Montreal')
#plt.savefig('score_montreal_mcp.pdf')
#plt.show()
#results = data
#score = [json.loads(x.get('score'))[0] for x in results]
#size = [x.get('size') for x in results]
# best_score = exact_solver.mcp_score(size[-1])
#best_score = [6.0, 8.0, 10.0, 12.0, 12.0, 14.0, 16.0, 18.0, 18.0, 20.0, 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 30.0, 32.0,
#              34.0, 36.0]
#plt.plot(size, score, label='measured score IBM Montreal')
#plt.plot(size, best_score, label='optimal score')


#file = open('log_qasm_sim/log_qiskit_mcp_long.json')
#data2 = json.load(file)
#results2 = json.loads(data2.get('data'))

#score = [json.loads(x.get('score'))[0] for x in results2]
#size = [x.get('size') for x in results2]
#plt.plot(size, score, label='measured score IBM QASM simulator')


#ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
#plt.xlabel("graph size [nodes]")
#plt.ylabel("score cost function")
#plt.legend()
#plt.title('Score MCP on IBM QASM simulator and IBM Montreal')
#plt.savefig('score_mcp_qasm_montreal.pdf')
#plt.show()
###########################################################################################################
#######################SCORE IBM QASM + MONTEAL ACCURACY########################################
#file = open('log_montreal/ibmq_nairobi_mcp.json')
#plot_score_mcp(file)
#plt.title('Score MCP on Nairobi')
#plt.savefig('score_nairobi_mcp.pdf')
#plt.show()
#fig, ax = plt.subplots()

#data = [0]*20
#with open('log_montreal/mcp_ibmq_montreal_5_to_24', 'rt') as file:
#    i = 0
#    for line in file:
#        data[i] = json.loads(line)
#        i += 1

#results = data
#score = [json.loads(x.get('score'))[0] for x in results]
#size = [x.get('size') for x in results]

#best_score = exact_solver.mcp_score(size[-1])
#best_score = [6.0, 8.0, 10.0, 12.0, 12.0, 14.0, 16.0, 18.0, 18.0, 20.0, 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 30.0, 32.0,
#              34.0, 36.0]
#accuracy = [score[i] / best_score[i] for i in range(len(score))]
#plt.plot(size, accuracy, label='measured outcome accuracy IBM Montreal')

#file = open('log_qasm_sim/log_qiskit_mcp_long.json')
#data2 = json.load(file)
#results2 = json.loads(data2.get('data'))

#score = [json.loads(x.get('score'))[0] for x in results2]
#size = [x.get('size') for x in results2]
#accuracy = [score[i] / best_score[i] for i in range(len(score))]
#plt.plot(size, accuracy, label='measured outcome accuracy IBM QASM simulator')
#plt.plot(size, score, label='measured score IBM QASM simulator')


#ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
#plt.xlabel("graph size [nodes]")
#plt.ylabel("outcome accuracy")
#plt.legend()
#plt.title('outcome accuracy MCP on IBM QASM simulator and IBM Montreal')
#plt.savefig('accuracy_mcp_qasm_montreal.pdf')
#plt.show()
###########################################################################################################
#########################SCORE MCP NAIROBI################################################################
#fig, ax = plt.subplots()

#file = open('log_montreal/ibmq_nairobi_reg_mcp.json')
#data = json.load(file)
#results1 = json.loads(data.get('data'))
#score = [json.loads(x.get('score'))[0] for x in results1]
#size = [x.get('size') for x in results1]
#plt.plot(size, score, label='measured score IBM Nairobi')



#file = open('log_montreal/ibmq_nairobi_mcp.json')
#data2 = json.load(file)
#results2 = json.loads(data2.get('data'))
#score = [json.loads(x.get('score'))[0] for x in results2]
#size = [x.get('size') for x in results2]
#plt.plot(size, score, label='Measured score for MCP on IBM Nairobi (runtime)')

#best_score = [6.0, 8.0, 10.0, 12.0, 12.0, 14.0, 16.0, 18.0, 18.0, 20.0, 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 30.0, 32.0,
#              34.0, 36.0]
#plt.plot(size, best_score[0:len(size)], label='optimal score')

#ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
#plt.xlabel("graph size [nodes]")
#plt.ylabel("score cost function")
#plt.legend(loc='upper left')
#plt.title('Score MCP on IBM Nairobi')

#plt.savefig('score_MCP_Nairobi_both.pdf')
#plt.show()
#################################################################################################################

#########################ACCURACY MCP NAIROBI################################################################
#fig, ax = plt.subplots()

#file = open('log_montreal/ibmq_nairobi_reg_mcp.json')
#data = json.load(file)
##results1 = json.loads(data.get('data'))
#score = [json.loads(x.get('score'))[0] for x in results1]
#size = [x.get('size') for x in results1]
#best_score = [6.0, 8.0, 10.0, 12.0, 12.0, 14.0, 16.0, 18.0, 18.0, 20.0, 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 30.0, 32.0,
#             34.0, 36.0]
#accuracy = [score[i] / best_score[i] for i in range(len(score))]
#plt.plot(size, accuracy, label='measured outcome accuracy IBM Nairobi')
#plt.plot(size, score, label='measured score IBM Nairobi')



#file = open('log_montreal/ibmq_nairobi_mcp.json')
#data2 = json.load(file)
#results2 = json.loads(data2.get('data'))
##score = [json.loads(x.get('score'))[0] for x in results2]
#size = [x.get('size') for x in results2]
#accuracy = [score[i] / best_score[i] for i in range(len(score))]
#plt.plot(size, accuracy, label='measured outcome accuracy for MCP on IBM Nairobi (runtime)')
#plt.plot(size, score, label='Measured score for MCP on IBM Nairobi (runtime)')


#plt.plot(size, best_score[0:len(size)], label='optimal score')

#ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
####plt.xlabel("graph size [nodes]")
#plt.ylabel("outcome accuracy")
#plt.legend(loc='upper left')
#plt.title('Outcome accuracy MCP on IBM Nairobi')

##plt.savefig('accuracy_MCP_Nairobi_both.pdf')
#plt.show()
#################################################################################################################

###########SCORE DSP QASM MONTREAL############################################################################

fig, ax = plt.subplots()

file = open('log_montreal/ibmq_montreal_dsp.json')
data = json.load(file)
results1 = json.loads(data.get('data'))
score = [json.loads(x.get('score'))[0] for x in results1]
size = [x.get('size') for x in results1]

#plt.plot(size, score, label='Measured score for DSP on IBM Montreal')


#best_score = exact_solver.dsp_score(size[-1]+1)
#print(best_score)
best_score = [9, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 28, 30, 32, 34, 36, 37, 39, 41]

#plt.plot(size, best_score, label='optimal score')
accuracy = [score[i] / best_score[i] for i in range(len(score))]
print(size, accuracy)
plt.plot(size, accuracy, label='measured outcome accuracy for DSP on IBM Montreal')

file = open('log_qasm_sim/log_qiskit_dsp.json')
data = json.load(file)
results = json.loads(data.get('data'))
score1 = [json.loads(x.get('score'))[0] for x in results]
size1 = [x.get('size') for x in results]

file = open('log_qasm_sim/log_qiskit_dsp_2.json')
data = json.load(file)
results = json.loads(data.get('data'))
score2 = [json.loads(x.get('score'))[0] for x in results]
size2 = [x.get('size') for x in results]

score = score1 + score2
size = size1 + size2
#plt.plot(size, score, label='Measured score for DSP on IBM QASM simulator')
accuracy = [score[i] / best_score[i] for i in range(len(score))]
plt.plot(size, accuracy, label='measured outcome accuracy for DSP on IBM QASM simulator')

ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.xlabel("graph size [nodes]")
plt.ylabel("score cost function")
plt.ylim([0.73, 0.9])
plt.legend(loc='lower left')
plt.title('Score DSP on IBM QASM simulator and IBM Montreal')

plt.savefig('acc_DSP_QASM_Montreal.pdf')
plt.show()
#################################################################################################################











#fig1, ax = plt.subplots()
#file = open('log_montreal/ibmq_nairobi_reg_mcp.json')
#plot_json(file, fig1)
#plt.ylabel("time [s]")
#plt.xlabel("graph size [nodes]")
#ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
#plt.legend()
#plt.title("mcp 5-7 IBM Nairobi")
#plt.savefig('ibmq_nairobi_7.pdf')
#plt.show()

#fig1, ax = plt.subplots()
#data = [0]*20
#with open('log_montreal/mcp_ibmq_montreal_5_to_24', 'rt') as file:
#    i = 0
#    for line in file:
#        data[i] = json.loads(line)
#        i += 1
#plot_json(data, fig1)
#plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=3)
#plt.xlabel("graph size [nodes]")
#plt.ylabel("time [s]")
#ax.xaxis.set_major_locator(plt.MaxNLocator(21, integer=True))
#plt.savefig('mcp_ibmq_montreal_5_to_22.pdf')
#plt.show()

#file = open('log_montreal/ibmq_nairobi_reg_mcp.json')
#plot_score_mcp(file)
#plt.title('Score MCP on IBM Nairobi')
#plt.savefig('score_nairobi_mcp.pdf')
#plt.show()
#############################################################################################


#file = open('log_qasm_sim/log_qiskit_mcp_long.json')
#plot_accuracy(file)
#plot_score_mcp(file)
#plt.title('Measured outcome accuracy for MCP on IBM qasm simulator')
#plt.savefig('qasm_acccuracy_mcp.pdf')
#plt.show()

#data = [0]*20
#with open('log_montreal/mcp_ibmq_montreal_5_to_24', 'rt') as file:
#    i = 0
#    for line in file:
#        data[i] = json.loads(line)
#        i += 1
#plot_accuracy(data)
#plt.title('Measured outcome accuracy for MCP on IBM Montreal')
#plt.savefig('montreal_accuracy_mcp.pdf')
#plt.show()

#file = open('log_montreal/ibmq_nairobi_mcp.json')
#plot_accuracy(file)
#plt.title('Measured outcome accuracy for MCP on IBM Nairobi (runtime)')
#plt.savefig('nairobi_runtime_accuracy_mcp.pdf')
#plt.show()


#file = open('log_montreal/ibmq_montreal_dsp.json')

#plot_accuracy(file)
#plt.title('Measured outcome accuracy for DSP on IBM montreal')
#plt.savefig('montreal_accuracy_dsp.pdf')
#plt.show()


#print(data)
#run = 0
#wall = 0
#times = []
#i = 0
#perc = 0
#for x in data:
#    times.append(x.get('time'))
#for x in times:
#    i+= 1
#    print(i)
#    perc += x.get('RUNNING')/x.get('WALLTIME')
#    print(perc)
#perc = run/wall
#print(perc/i)