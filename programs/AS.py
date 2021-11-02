import math

from qiskit import (
    # IBMQ,
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
)
from qiskit.tools.visualization import circuit_drawer
from math import pi


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
    s = s.zfill(6)
    return s

def mch(qc, c_q, t_q):
    qc.ry(pi/4,t_q)
    qc.mct(c_q,t_q)
    qc.ry(-pi/4,t_q)
    return qc


def AS(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(6)
    b = QuantumRegister(2)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(a, b, c)

    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[5 - i] == '1':
            qc.x(a[i])

    qc.barrier(a)

    qc.h(a[2])
    qc.p(math.pi / 4, a[2])

    qc.x(b[0])
    qc.h(b[1])
    qc.p(math.pi / 2, b[1])

    for i in range(5):
        control = []
        control.append(b[0])
        for j in range(5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[0], a[0])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(3):
        control = []
        control.append(b[1])
        for j in range(2, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[1], a[2])

    qc.barrier(a)

    qc.measure(a, c)

    #circuit_drawer(qc, filename='AS_circuit/AS_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def AS_M1(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(6)
    b = QuantumRegister(2)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(a, b, c)

    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[5 - i] == '1':
            qc.x(a[i])

    qc.barrier(a)

    qc.mct([a[1],a[3]],a[5])#M1

    qc.h(a[2])
    qc.p(math.pi / 4, a[2])

    qc.x(b[0])
    qc.h(b[1])
    qc.p(math.pi / 2, b[1])

    for i in range(5):
        control = []
        control.append(b[0])
        for j in range(5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[0], a[0])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(3):
        control = []
        control.append(b[1])
        for j in range(2, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[1], a[2])

    qc.barrier(a)

    qc.measure(a, c)

    #circuit_drawer(qc, filename='AS_circuit/AS_M1_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def AS_M2(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(6)
    b = QuantumRegister(2)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(a, b, c)

    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[5 - i] == '1':
            qc.x(a[i])

    qc.barrier(a)
    qc.mct([a[0],a[2],a[3]],a[5])#M2

    qc.h(a[2])
    qc.p(math.pi / 4, a[2])

    qc.x(b[0])
    qc.h(b[1])
    qc.p(math.pi / 2, b[1])

    for i in range(5):
        control = []
        control.append(b[0])
        for j in range(5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[0], a[0])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(3):
        control = []
        control.append(b[1])
        for j in range(2, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[1], a[2])

    qc.barrier(a)

    qc.measure(a, c)
    #circuit_drawer(qc, filename='AS_circuit/AS_M2_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def AS_M3(input, count_times):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(6)
    b = QuantumRegister(2)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(a, b, c)

    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[5 - i] == '1':
            qc.x(a[i])

    qc.barrier(a)
    qc.mct([a[0],a[2],a[3],a[4]],a[5])#M3

    qc.h(a[2])
    qc.p(math.pi / 4, a[2])

    qc.x(b[0])
    qc.h(b[1])
    qc.p(math.pi / 2, b[1])

    for i in range(5):
        control = []
        control.append(b[0])
        for j in range(5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[0], a[0])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(3):
        control = []
        control.append(b[1])
        for j in range(2, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[1], a[2])

    qc.barrier(a)

    qc.measure(a, c)
    #circuit_drawer(qc, filename='AS_circuit/AS_M3_circuit.txt')

    job = execute(qc, simulator, shots=count_times * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def AS_specification(input):
    simulator = Aer.get_backend('statevector_simulator')
    a = QuantumRegister(6)
    b = QuantumRegister(2)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(a, b, c)

    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[5 - i] == '1':
            qc.x(a[i])

    qc.barrier(a)

    qc.h(a[2])
    qc.p(math.pi / 4, a[2])

    qc.x(b[0])
    qc.h(b[1])
    qc.p(math.pi / 2, b[1])

    for i in range(5):
        control = []
        control.append(b[0])
        for j in range(5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[0], a[0])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(4):
        control = []
        control.append(b[0])
        control.append(b[1])
        for j in range(1, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.ccx(b[0], b[1], a[1])

    qc.barrier(a)

    for i in range(3):
        control = []
        control.append(b[1])
        for j in range(2, 5 - i):
            control.append(a[j])
        qc.mct(control, a[5 - i])
    qc.cnot(b[1], a[2])


    vector = execute(qc, simulator).result().get_statevector()
    #circuit_drawer(qc, filename='./AS_circuit')

    return vector


def probabilityComputing(input):
    pt = []
    t = AS_specification(input)
    for i in range(64):
        temp = 0
        for j in range(4):
            temp += abs(t[j * 64 + i]) ** 2
        pt.append(temp)
    return pt
if __name__ == '__main__':
    print(AS(0,1))
    print(AS_M1(0,1))
    print(AS_M2(0,1))
    print(AS_M3(0,1))