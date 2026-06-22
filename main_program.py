from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as sampler

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from matplotlib import pyplot as plt
import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
token= 0 #mettre login IBM quantum
, instance="crn:v1:bluemix:public:quantum-computing:us-east:a/33e6f8e03ed64b2b80accee6243f7c5c:76fc4509-57b2-403d-a0a8-fd1f3b5e77ae::", overwrite=True, # Optional
)

# Load saved credentials
service = QiskitRuntimeService()
 
# Circuit
qc = QuantumCircuit(2)


# Porte d'Hadamard pour avoir une "équiprobabilité" au départ
qc.h(0)
 
# une porte NOT
qc.cx(0, 1)


backend = service.least_busy(
    operational=True, simulator=True
)

observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
# isa_circuit.draw("mpl", idle_wires=False)  # Commentez cette ligne pour ne pas afficher le circuit transpilé

# "J'arrondi" les probabilités avec estimator qui est l'espérance 

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 5000

mapped_observables = [
    observable.apply_layout(isa_circuit.layout) for observable in observables
]

job = estimator.run([(isa_circuit, mapped_observables)])


pub_result = job.result()[0]


errors = pub_result.data.stds

#Machine de turing


n = 20
tab_ruban = np.array([None] * n)

Instruction = ["ALLER"]*(n-2) + ["ARRET"] + ["ARRET"]
tab_ruban[0]=("B", ">", Instruction[0])
tab_ruban[n-1] = ("X", ">", Instruction[n-1])


l = 0
thr = tab_ruban[l]

k = 0
while (thr[2]!="ARRET"):
    k = k + 1
    thr = tab_ruban[l]
    if thr[2] == "ALLER" :
        if errors < 0.1 :  # peu d'erreur 
            tab_ruban[l+1] = (thr[0], ">", Instruction[l])
            l = l + 1
        else :
            tab_ruban[l-1] = (thr[0], "<", Instruction[l])
            l = l - 1


print(k)     # nombre de tour de la machine