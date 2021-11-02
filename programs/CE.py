import math

from qiskit import (
    # IBMQ,
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
    s = s.zfill(11)
    return s

def mch(qc, c_q, t_q):
    qc.ry(pi/4,t_q)
    qc.mct(c_q,t_q)
    qc.ry(-pi/4,t_q)
    return qc


def CE(input, count_number):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(3)
    b = QuantumRegister(12)
    c = ClassicalRegister(12)
    qc = QuantumCircuit(a, b, c)

    # a
    qc.x(a[0])
    qc.h(a[2])

    qc.barrier(a)

    # b
    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[10 - i] == '1':
            qc.x(b[i])
    qc.h(b[1])
    qc.p(math.pi / 4, b[1])
    qc.barrier(b)

    # a-=3
    qc.x(a[1])
    qc.cx(a[1], a[2])
    qc.x(a[0])
    qc.cx(a[0], a[1])
    qc.mct([a[0], a[1]], a[2])
    qc.barrier(a)

    # if a<0, b++
    for i in range(12):
        control = []
        control.append(a[2])
        if i < 11:
            for j in range(11 - i):
                control.append(b[j])
        qc.mct(control, b[11 - i])

    qc.barrier(a)

    # a+=3
    qc.mct([a[0], a[1]], a[2])
    qc.cx(a[0], a[1])
    qc.x(a[0])
    qc.cx(a[1], a[2])
    qc.x(a[1])
    qc.barrier(b)

    qc.measure(b, c)

    #circuit_drawer(qc, filename='CE_circuit/CE_circuit.txt')

    job = execute(qc, simulator, shots=count_number * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def CE_M1(input, count_number):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(3)
    b = QuantumRegister(12)
    c = ClassicalRegister(12)
    qc = QuantumCircuit(a, b, c)

    # a
    qc.x(a[0])
    qc.h(a[2])

    qc.barrier(a)

    # b
    input_string = dec2bin(input)
    # print(input)
    # print(input_string)
    for i in range(len(input_string)):
        if input_string[10 - i] == '1':
            qc.x(b[i])
    qc.h(b[1])
    qc.p(math.pi / 4, b[1])
    qc.barrier(b)

    mch(qc,[b[2],b[5]],b[1])#M1

    # a-=3
    qc.x(a[1])
    qc.cx(a[1], a[2])
    qc.x(a[0])
    qc.cx(a[0], a[1])
    qc.mct([a[0], a[1]], a[2])
    qc.barrier(a)

    # if a<0, b++
    for i in range(12):
        control = []
        control.append(a[2])
        if i < 11:
            for j in range(11 - i):
                control.append(b[j])
        qc.mct(control, b[11 - i])

    qc.barrier(a)

    # a+=3
    qc.mct([a[0], a[1]], a[2])
    qc.cx(a[0], a[1])
    qc.x(a[0])
    qc.cx(a[1], a[2])
    qc.x(a[1])
    qc.barrier(b)

    qc.measure(b, c)

    #circuit_drawer(qc, filename='CE_circuit/CE_circuit_M1.txt')

    job = execute(qc, simulator, shots=count_number * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def CE_M2(input, count_number):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(3)
    b = QuantumRegister(12)
    c = ClassicalRegister(12)
    qc = QuantumCircuit(a, b, c)

    # a
    qc.x(a[0])
    qc.h(a[2])

    qc.barrier(a)

    # b
    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[10 - i] == '1':
            qc.x(b[i])
    qc.h(b[1])
    qc.p(math.pi / 4, b[1])
    qc.barrier(b)

    mch(qc, [b[2], b[5], b[7]], b[1])  # M2

    # a-=3
    qc.x(a[1])
    qc.cx(a[1], a[2])
    qc.x(a[0])
    qc.cx(a[0], a[1])
    qc.mct([a[0], a[1]], a[2])
    qc.barrier(a)

    # if a<0, b++
    for i in range(12):
        control = []
        control.append(a[2])
        if i < 11:
            for j in range(11 - i):
                control.append(b[j])
        qc.mct(control, b[11 - i])

    qc.barrier(a)

    # a+=3
    qc.mct([a[0], a[1]], a[2])
    qc.cx(a[0], a[1])
    qc.x(a[0])
    qc.cx(a[1], a[2])
    qc.x(a[1])
    qc.barrier(b)

    qc.measure(b, c)

    #circuit_drawer(qc, filename='CE_circuit/CE_circuit_M2.txt')

    job = execute(qc, simulator, shots=count_number * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts


def CE_M3(input, count_number):
    simulator = Aer.get_backend('qasm_simulator')
    a = QuantumRegister(3)
    b = QuantumRegister(12)
    c = ClassicalRegister(12)
    qc = QuantumCircuit(a, b, c)

    # a
    qc.x(a[0])
    qc.h(a[2])

    qc.barrier(a)

    # b
    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[10 - i] == '1':
            qc.x(b[i])

    qc.mct([b[0],b[3],b[6],b[8]],b[10])#M3

    qc.h(b[1])
    qc.p(math.pi / 4, b[1])
    qc.barrier(b)

    # a-=3
    qc.x(a[1])
    qc.cx(a[1], a[2])
    qc.x(a[0])
    qc.cx(a[0], a[1])
    qc.mct([a[0], a[1]], a[2])
    qc.barrier(a)

    # if a<0, b++
    for i in range(12):
        control = []
        control.append(a[2])
        if i < 11:
            for j in range(11 - i):
                control.append(b[j])
        qc.mct(control, b[11 - i])

    qc.barrier(a)

    # a+=3
    qc.mct([a[0], a[1]], a[2])
    qc.cx(a[0], a[1])
    qc.x(a[0])
    qc.cx(a[1], a[2])
    qc.x(a[1])
    qc.barrier(b)

    qc.measure(b, c)

    #circuit_drawer(qc, filename='CE_circuit/CE_circuit_M3.txt')

    job = execute(qc, simulator, shots=count_number * 100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def CE_specification(input):
    simulator = Aer.get_backend('statevector_simulator')
    a = QuantumRegister(3)
    b = QuantumRegister(12)
    c = ClassicalRegister(12)
    qc = QuantumCircuit(a, b, c)

    # a
    qc.x(a[0])
    qc.h(a[2])

    qc.barrier(a)

    # b
    input_string = dec2bin(input)
    for i in range(len(input_string)):
        if input_string[10 - i] == '1':
            qc.x(b[i])

    qc.h(b[1])
    qc.p(math.pi / 4, b[1])
    qc.barrier(b)

    # a-=3
    qc.x(a[1])
    qc.cx(a[1], a[2])
    qc.x(a[0])
    qc.cx(a[0], a[1])
    qc.mct([a[0], a[1]], a[2])
    qc.barrier(a)

    # if a<0, b++
    for i in range(12):
        control = []
        control.append(a[2])
        if i < 11:
            for j in range(11 - i):
                control.append(b[j])
        qc.mct(control, b[11 - i])

    qc.barrier(a)

    # a+=3
    qc.mct([a[0], a[1]], a[2])
    qc.cx(a[0], a[1])
    qc.x(a[0])
    qc.cx(a[1], a[2])
    qc.x(a[1])
    qc.barrier(b)

    vector = execute(qc, simulator).result().get_statevector()

    #circuit_drawer(qc, filename='./CE_circuit')

    return vector


def probabilityComputing(input):
    pt = []
    t = CE_specification(input)
    for i in range(4096):
        temp = 0
        for j in range(8):
            temp += abs(t[i * 8 + j]) ** 2
        pt.append(temp)
    return pt

if __name__ == '__main__':
    # print(CE(0,1))
    print(CE_M1(2047,1))
    print(probabilityComputing(2047))
    print(sum(probabilityComputing(2047)))
    # print(CE_M2(0,1))
    # print(CE_M3(0,1))