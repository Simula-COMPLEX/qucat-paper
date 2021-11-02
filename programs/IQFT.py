from qiskit import (
    #IBMQ,
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
)
from math import pi
from qiskit.tools.visualization import circuit_drawer

def dec2bin(n):
    a = 1
    list = []
    while a > 0:
        a, b = divmod(n, 2)
        list.append(str(b))
        n = a
    s = ""
    for i in range(len(list) - 1, -1, -1):
        s += str(list[i])
    s = s.zfill(10)#input的位数
    return s

def mch(qc, c_q, t_q):
    qc.ry(pi/4,t_q)
    qc.mct(c_q,t_q)
    qc.ry(-pi/4,t_q)
    return qc

def inverse(s):
    s_list = list(s)
    for i in range(len(s_list)):
        if s_list[i] == '0':
            s_list[i] = '1'
        else:
            s_list[i] ='0'
    s = "".join(s_list)
    return s

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft_rotations(circuit, qubit, p):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    for j in range(qubit + 1, 10):
        circuit.cu1(pi/2**(p), qubit, j)
        p += 1
    circuit.barrier()
    return circuit

def IQFT(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    q = QuantumRegister(10)
    c = ClassicalRegister(10)

    qc = QuantumCircuit(q,c)

    input_string = dec2bin(input)
    for i in range(10):
        if input_string[9-i] == '1':
            qc.x(q[i])

    qc.barrier()

    swap_registers(qc,10)
    #qft_rotations(qc,10)
    for qubit in range(10):
        qc.h(qubit)
        p = 1
        qft_rotations(qc,qubit,p)

    qc.barrier()

    qc.measure(q,c)

    #circuit_drawer(qc, filename='IQFT_circuit/IQFT_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def IQFT_M1(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    q = QuantumRegister(10)
    c = ClassicalRegister(10)

    qc = QuantumCircuit(q,c)
    input_string = dec2bin(input)
    print(input_string)
    for i in range(10):
        if input_string[9-i] == '1':
            qc.x(q[i])

    mch(qc,[q[0],q[4]],q[7])#M1

    qc.barrier()

    swap_registers(qc,10)
    #qft_rotations(qc,10)
    for qubit in range(10):
        qc.h(qubit)
        p = 1
        qft_rotations(qc,qubit,p)

    qc.barrier()

    qc.measure(q,c)

    #circuit_drawer(qc, filename='./IQFT_test.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def IQFT_M2(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    q = QuantumRegister(10)
    c = ClassicalRegister(10)

    qc = QuantumCircuit(q, c)

    input_string = dec2bin(input)
    for i in range(10):
        if input_string[9 - i] == '1':
            qc.x(q[i])

    mch(qc, [q[0], q[4],q[6]], q[7])  # M2

    qc.barrier()

    swap_registers(qc, 10)
    # qft_rotations(qc,10)
    for qubit in range(10):
        qc.h(qubit)
        p = 1
        qft_rotations(qc, qubit, p)

    qc.barrier()

    qc.measure(q, c)

    #circuit_drawer(qc, filename='IQFT_circuit/IQFT_M2_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def IQFT_M3(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    q = QuantumRegister(10)
    c = ClassicalRegister(10)

    qc = QuantumCircuit(q, c)

    input_string = dec2bin(input)
    for i in range(10):
        if input_string[9 - i] == '1':
            qc.x(q[i])

    mch(qc, [q[0], q[2],q[4],q[6]], q[7])  # M3

    qc.barrier()

    swap_registers(qc, 10)
    # qft_rotations(qc,10)
    for qubit in range(10):
        qc.h(qubit)
        p = 1
        qft_rotations(qc, qubit, p)

    qc.barrier()

    qc.measure(q, c)

    #circuit_drawer(qc, filename='IQFT_circuit/IQFT_M3_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def IQFT_specification(input):
    simulator = Aer.get_backend('statevector_simulator')
    q = QuantumRegister(10)
    c = ClassicalRegister(10)

    qc = QuantumCircuit(q,c)

    input_string = dec2bin(input)
    for i in range(10):
        if input_string[9-i] == '1':
            qc.x(q[i])

    qc.barrier()

    swap_registers(qc,10)
    #qft_rotations(qc,10)
    for qubit in range(10):
        qc.h(qubit)
        p = 1
        qft_rotations(qc,qubit,p)

    qc.barrier()

    #circuit_drawer(qc, filename='./IQFT_circuit')

    vector = execute(qc, simulator).result().get_statevector()

    return vector

def probabilityComputing(input):
    pt = []
    t = IQFT_specification(input)
    for i in range(1024):
        pt.append(abs(t[i])**2)
    return pt

if __name__ == '__main__':
    # print(IQFT(0,1024))
    print(IQFT_M1(311, 1024))
    # print(IQFT_M2(0, 1024))
    # print(IQFT_M3(0, 1024))