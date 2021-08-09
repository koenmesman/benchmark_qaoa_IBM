import json
#import sys
#sys.path.insert(0, '..') # Add qiskit_runtime directory to the path

import IBM_runtime_QAOA
from qiskit import Aer
from qiskit.providers.ibmq.runtime.utils import RuntimeEncoder, RuntimeDecoder
from qiskit.providers.ibmq.runtime import UserMessenger
from qiskit import IBMQ

inputs = {"iterations": 1, "p": 1}

IBMQ.enable_account('')
provider = IBMQ.get_provider(hub='strangeworks-hub', group='science-team', project='science-test')
backend = provider.get_backend("ibm_nairobi") #, account_id="koenmesman")

user_messenger = UserMessenger()
serialized_inputs = json.dumps(inputs, cls=RuntimeEncoder)
unserialized_inputs = json.loads(serialized_inputs, cls=RuntimeDecoder)

IBM_runtime_QAOA.main(backend, user_messenger, **unserialized_inputs)

