import json
#import sys
#sys.path.insert(0, '..') # Add qiskit_runtime directory to the path

import IBM_runtime_QAOA
from qiskit import Aer
from qiskit.providers.ibmq.runtime.utils import RuntimeEncoder, RuntimeDecoder
from qiskit.providers.ibmq.runtime import UserMessenger

inputs = {"iterations": 3, "p": 1}

backend = Aer.get_backend('qasm_simulator')
user_messenger = UserMessenger()
serialized_inputs = json.dumps(inputs, cls=RuntimeEncoder)
unserialized_inputs = json.loads(serialized_inputs, cls=RuntimeDecoder)

IBM_runtime.main(backend, user_messenger, **unserialized_inputs)

