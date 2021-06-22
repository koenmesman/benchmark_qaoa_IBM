import generate_graph as gg
import Classic_opt as opt
import time
import json
import datetime
import traceback

global BENCHMARK_TIMES


#Workflow qaoa instance:
#   define problem size (qubits), optionally adjust for TSP (though strangeworks does not support >9 qubits)
#   create graph instance from 'generate_graph.py'
#   you can change the initial parameters for [beta, gamma], iterations p and the nr. of quantum circuit repetitions
#   define [beta, gamma] as [beta[0], beta[1], ..., beta[p-1], gamma[0], ... , gamma[p-1]]
#   the qaoa optimizer reads this as beta =  param[0:p], gamma = [p:2p]
#   (rep = 100 is more realistic, but for testing purposes use a small number)
#   define q_func as either "mcp" (max-cut), "tsp" (traveling salesman) or "dsp" (dominating set)
#   result format is: [best_solution_result, [best_beta, best_gamma]]


class Benchmark:
    def __init__(self, func):
        self.init_param = [0,0]
        self.p = 1
        self.rep = 10
        self.q_func = func
        self.max_size = []
        self.qvm = ""
        self.lim = 10
        #zero_time = datetime.timedelta()
        global BENCHMARK_TIMES
        #BENCHMARK_TIMES = {'CREATING': zero_time, 'VALIDATING': zero_time, 'QUEUED': zero_time, 'RUNNING': zero_time,
        #                   'OTHER': zero_time}
        BENCHMARK_TIMES = {'CREATING': 0, 'VALIDATING': 0, 'QUEUED': 0, 'RUNNING': 0,
                           'OTHER': 0, 'CONNECTION': 0}

    def __qubit_select(self, func):
        self._qbits = {
            'mcp': self._problem_size,
            'dsp': self._problem_size + 10,
            'tsp': self._problem_size**2
        }
        return self._qbits.get(func)

    def update_p(self, new_p):
        self.p = new_p

    def set_lim(self, lim):
        self.lim = lim+1

    def run(self):
        self._problem_size = 12
        out = []
        keys = ['size', 'p', 'score', 'time']
        global BENCHMARK_TIMES
        while self._problem_size < self.lim:
            self.qubits = self.__qubit_select(self.q_func)

            try:
                self.graph = gg.regular_graph(self._problem_size)
                self.results = 0
                print('start', self.q_func, self._problem_size)
                self._start = time.time()
                self._results = opt.nm(self.init_param, self.graph, self.p, self.q_func)
                self._time = time.time() - self._start
                print('finished')
                print(BENCHMARK_TIMES)
                self._results[1] = list(self._results[1])
                self._time_dict = BENCHMARK_TIMES
                self._time_dict['WALLTIME'] = self._time
                res = dict(zip(keys, [self._problem_size, self.p, json.dumps(self._results), self._time_dict]))
                out.append(res)
                BENCHMARK_TIMES = {'CREATING': 0, 'VALIDATING': 0, 'QUEUED': 0, 'RUNNING': 0,
                                   'OTHER': 0}
                self._problem_size += 1
            except Exception as e:
                print(e)
                traceback.print_exc()
                self._problem_size -= 1
                break
        list_out = json.dumps(out)        
        self.stream = {'qfunc' : self.q_func, 'size' : self._problem_size, 'data' : list_out}
        outfile = open('log_qiskit_'+ self.q_func +'.json', 'r')
        data = json.load(outfile)
        try:
            outfile = open('log_qiskit_'+ self.q_func +'.json', 'w')
            data.update(self.stream)
            outfile.seek(0)
            json.dump(data, outfile, indent=6)
        except:
            print('could not load saved file')
            #json.dump(self.stream, outfile, indent=6)
            #with open('log_qiskit.txt', 'w') as outfile:
            #    json.dump(self.stream, outfile)
            #print('new file created')
        finally:
            outfile.close()
        return self.stream


def get_times(job, wall):
    print(job)
    create = job.get('CREATED')-job.get('CREATING')
    validate = job.get('VALIDATED') - job.get('VALIDATING')
    if job.get('RUNNING'): # and job.get('QUEUED'):
        queue = job.get('RUNNING') - job.get('QUEUED')
    else:
        queue = datetime.timedelta()

    if job.get('RUNNING'):
        runtime = job.get('COMPLETED') - job.get('RUNNING')
    else:
        runtime = datetime.timedelta()

    other = job.get('COMPLETED') - job.get('CREATING') - create - validate - queue - runtime
    total = job.get('COMPLETED') - job.get('CREATING')
    out_dict = {'CREATING': create, 'VALIDATING': validate, 'QUEUED': queue, 'RUNNING': runtime, 'OTHER': other, 'CONNECTION': total}
    for key, val in out_dict.items():
        out_dict[key] = val.total_seconds()
    out_dict['CONNECTION'] -= wall
    return out_dict

def merge_times(old_times, new_times):
    for key, old_val in old_times.items():
        old_times[key] = old_val + new_times[key]
    return old_times
