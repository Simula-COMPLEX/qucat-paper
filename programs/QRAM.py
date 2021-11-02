import numpy as np
from qiskit import (
    #IBMQ,
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
)
from math import pi
from qiskit.visualization import plot_histogram
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
    s = s.zfill(9)#input的位数
    return s

def inverse(s):
    s_list = list(s)
    for i in range(len(s_list)):
        if s_list[i] == '0':
            s_list[i] = '1'
        else:
            s_list[i] ='0'
    s = "".join(s_list)
    return s

def QRAM(input,count_times):
    simulator = Aer.get_backend('qasm_simulator')
    qreg = QuantumRegister(4)
    addr = QuantumRegister(1)
    qram0 = QuantumRegister(4)
    qram1 = QuantumRegister(4)
    c = ClassicalRegister(4)

    qc = QuantumCircuit(qreg, addr, qram0, qram1, c)

    input_string = dec2bin(input)
    #print('input:'+str(input_string))
    if input_string[8] == '1':
        qc.x(addr[0])
    for i in range(4):
        if input_string[7-i] == '1':
            #print('input '+ str(7-i) + '=1')
            qc.x(qram0[i])
    for i in range(4):
        if input_string[3-i] == '1':
            #print('input ' + str(3 - i) + '=1')
            qc.x(qram1[i])

    qc.barrier()

    qc.h(addr[0])
    qc.p(pi/3,addr[0])
    qc.h(addr[0])

    for i in range(4):
        qc.cswap(addr[0],qram0[i],qram1[i])

    qc.barrier()


    for i in range(4):
        qc.swap(qreg[i],qram0[i])

    qc.barrier()


    for i in range(3):
        control = []
        for j in range(3-i):
            control.append(qreg[j])
        qc.mcx(control, qreg[3-i])
    qc.x(qreg[0])

    qc.barrier()

    qc.measure(qreg,c)


    #circuit_drawer(qc, filename='QRAM_circuit/QRAM_circuit_i7.txt')

    job = execute(qc,simulator,shots = count_times*100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def QRAM_M1(input,count_times):
    simulator = Aer.get_backend('qasm_simulator')
    qreg = QuantumRegister(4)
    addr = QuantumRegister(1)
    qram0 = QuantumRegister(4)
    qram1 = QuantumRegister(4)
    c = ClassicalRegister(4)

    qc = QuantumCircuit(qreg, addr, qram0, qram1, c)

    input_string = dec2bin(input)
    #print('input:'+str(input_string))
    if input_string[8] == '1':
        qc.x(addr[0])
    for i in range(4):
        if input_string[7-i] == '1':
            #print('input '+ str(7-i) + '=1')
            qc.x(qram0[i])
    for i in range(4):
        if input_string[3-i] == '1':
            #print('input ' + str(3 - i) + '=1')
            qc.x(qram1[i])

    qc.barrier()

    qc.h(addr[0])
    qc.p(pi/3,addr[0])
    qc.mct([qram0[0],qram1[0]],qram1[3])#M1
    qc.h(addr[0])

    for i in range(4):
        qc.cswap(addr[0],qram0[i],qram1[i])

    qc.barrier()


    for i in range(4):
        qc.swap(qreg[i],qram0[i])

    qc.barrier()


    for i in range(3):
        control = []
        for j in range(3-i):
            control.append(qreg[j])
        qc.mcx(control, qreg[3-i])
    qc.x(qreg[0])

    qc.barrier()

    qc.measure(qreg,c)


    #circuit_drawer(qc, filename='QRAM_circuit/QRAM_M1_circuit.txt')

    job = execute(qc,simulator,shots = count_times*100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

def QRAM_M2(input,count_times):
    simulator = Aer.get_backend('qasm_simulator')
    qreg = QuantumRegister(4)
    addr = QuantumRegister(1)
    qram0 = QuantumRegister(4)
    qram1 = QuantumRegister(4)
    c = ClassicalRegister(4)

    qc = QuantumCircuit(qreg, addr, qram0, qram1, c)

    input_string = dec2bin(input)
    #print('input:'+str(input_string))
    if input_string[8] == '1':
        qc.x(addr[0])
    for i in range(4):
        if input_string[7-i] == '1':
            #print('input '+ str(7-i) + '=1')
            qc.x(qram0[i])
    for i in range(4):
        if input_string[3-i] == '1':
            #print('input ' + str(3 - i) + '=1')
            qc.x(qram1[i])

    qc.barrier()

    qc.h(addr[0])
    qc.p(pi/3,addr[0])
    qc.mct([qram0[0], qram1[2], qram1[1]], qram1[3])  # M2
    qc.h(addr[0])

    for i in range(4):
        qc.cswap(addr[0],qram0[i],qram1[i])

    qc.barrier()


    for i in range(4):
        qc.swap(qreg[i],qram0[i])

    qc.barrier()


    for i in range(3):
        control = []
        for j in range(3-i):
            control.append(qreg[j])
        qc.mcx(control, qreg[3-i])
    qc.x(qreg[0])

    qc.barrier()

    qc.measure(qreg,c)


    #circuit_drawer(qc, filename='QRAM_circuit/QRAM_M2_circuit.txt')

    job = execute(qc,simulator,shots = count_times*100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts

#qc.mcp(pi / 3, [qram0[0],qram0[2], qram1[1], qram1[3]], addr[0])  # M3
def QRAM_M3(input,count_times):
    simulator = Aer.get_backend('qasm_simulator')
    qreg = QuantumRegister(4)
    addr = QuantumRegister(1)
    qram0 = QuantumRegister(4)
    qram1 = QuantumRegister(4)
    c = ClassicalRegister(4)

    qc = QuantumCircuit(qreg, addr, qram0, qram1, c)

    input_string = dec2bin(input)
    #print('input:'+str(input_string))
    if input_string[8] == '1':
        qc.x(addr[0])
    for i in range(4):
        if input_string[7-i] == '1':
            #print('input '+ str(7-i) + '=1')
            qc.x(qram0[i])
    for i in range(4):
        if input_string[3-i] == '1':
            #print('input ' + str(3 - i) + '=1')
            qc.x(qram1[i])

    qc.barrier()

    qc.h(addr[0])
    qc.p(pi/3,addr[0])
    qc.mct([qram0[0], qram0[2], qram1[0], qram1[2]], qram1[3])  # M3
    qc.h(addr[0])

    for i in range(4):
        qc.cswap(addr[0],qram0[i],qram1[i])

    qc.barrier()


    for i in range(4):
        qc.swap(qreg[i],qram0[i])

    qc.barrier()


    for i in range(3):
        control = []
        for j in range(3-i):
            control.append(qreg[j])
        qc.mcx(control, qreg[3-i])
    qc.x(qreg[0])

    qc.barrier()

    qc.measure(qreg,c)


    #circuit_drawer(qc, filename='QRAM_circuit/QRAM_M3_circuit.txt')

    job = execute(qc,simulator,shots = count_times*100)
    result = job.result()
    counts = result.get_counts(qc)

    return counts
    #
    # simulator = Aer.get_backend('qasm_simulator')
    # qreg = QuantumRegister(4)
    # addr = QuantumRegister(1)
    # qram0 = QuantumRegister(4)
    # qram1 = QuantumRegister(4)
    # c = ClassicalRegister(4)
    #
    # qc = QuantumCircuit(qreg, addr, qram0, qram1, c)
    #
    # input_string = dec2bin(input)
    # #print('input:'+str(input_string))
    # if input_string[8] == '1':
    #     qc.x(addr[0])
    # for i in range(4):
    #     if input_string[7-i] == '1':
    #         #print('input '+ str(7-i) + '=1')
    #         qc.x(qram0[i])
    # for i in range(4):
    #     if input_string[3-i] == '1':
    #         #print('input ' + str(3 - i) + '=1')
    #         qc.x(qram1[i])
    #
    # qc.barrier()
    #
    #
    # qc.h(addr[0])
    # qc.p(pi/3,addr[0])
    # #qc.mcp(pi / 3, [qram0[0],qram0[3], qram1[1], qram1[3]], addr[0])  # M3
    # qc.h(addr[0])
    #
    # qc.cx(qram0[1],addr[0])#M3
    #
    # for i in range(4):
    #     qc.cswap(addr[0],qram0[i],qram1[i])
    #
    # qc.barrier()
    #
    #
    # for i in range(4):
    #     qc.swap(qreg[i],qram0[i])
    #
    # qc.barrier()
    #
    #
    # for i in range(3):
    #     control = []
    #     for j in range(3-i):
    #         control.append(qreg[j])
    #     qc.mcx(control, qreg[3-i])
    # qc.x(qreg[0])
    #
    # qc.barrier()
    #
    # qc.measure(qreg,c)
    #
    #
    # #circuit_drawer(qc, filename='QRAM_circuit/QRAM_M3_circuit_i7.txt')
    #
    # job = execute(qc,simulator,shots = count_times*100)
    # result = job.result()
    # counts = result.get_counts(qc)
    #
    # return counts

def QRAM_specification(input):
    simulator = Aer.get_backend('statevector_simulator')
    qreg = QuantumRegister(4)
    addr = QuantumRegister(1)
    qram0 = QuantumRegister(4)
    qram1 = QuantumRegister(4)
    c = ClassicalRegister(4)

    qc = QuantumCircuit(qreg, addr, qram0, qram1, c)

    input_string = dec2bin(input)
    if input_string[8] == '1':
        qc.x(addr[0])
    for i in range(4):
        if input_string[7-i] == '1':
            qc.x(qram0[i])
    for i in range(4):
        if input_string[3-i] == '1':
            qc.x(qram1[i])

    qc.barrier()

    qc.h(addr[0])
    qc.p(pi/3,addr[0])
    qc.h(addr[0])

    for i in range(4):
        qc.cswap(addr[0],qram0[i],qram1[i])

    qc.barrier()


    for i in range(4):
        qc.swap(qreg[i],qram0[i])

    qc.barrier()


    for i in range(3):
        control = []
        for j in range(3-i):
            control.append(qreg[j])
        qc.mcx(control, qreg[3-i])
    qc.x(qreg[0])

    qc.barrier()

    vector = execute(qc, simulator).result().get_statevector()

    return vector




def probabilityComputing(input):
    pt = []
    t = QRAM_specification(input)
    for i in range(16):
        temp = 0
        for j in range(512):
            temp += abs(t[j*16+i])**2
        pt.append(temp)
    return pt


if __name__ == '__main__':
    #print(probabilityComputing(7))
    print(QRAM(0,2))
    print(QRAM_M1(0, 2))
    print(QRAM_M2(0, 2))
    print(QRAM_M3(0, 2))
