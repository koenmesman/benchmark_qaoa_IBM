#!/usr/bin/env python
from Benchmark import Benchmark

#MCP benchmark
mcp = Benchmark('mcp')
mcp.set_lim(20)
mcp.run()
#print(mcp.stream)

#DSP benchmark
#dsp = Benchmark('dsp')
#dsp.set_lim(20)
#dsp.run()

#TSP benchmark
#tsp = Benchmark('tsp')
#tsp.run()
#print(tsp.max_size)


# ToDo
#   verify results --> score
#   set result threshold / measure fidelity (quantum simulator?)
#   measure time
#   measure memory usage
#   define output format (JSON)
#       {problem, best, {size, p, score, time, memory usage}}
#   create output file