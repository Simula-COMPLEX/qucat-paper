import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import linecache
from programs import AS, BV, CE, IQFT, QRAM, SM
import os
from rpy2 import robjects as robjects

K = 500


def dec2bin(n, bit):
    a = 1
    list = []
    while a > 0:
        a, b = divmod(n, 2)
        list.append(str(b))
        n = a
    s = ""
    for i in range(len(list) - 1, -1, -1):
        s += str(list[i])
    s = s.zfill(bit)
    return s


def wrong_output(i, right_output):
    set_output = set(right_output)
    if i not in set_output:
        return True  # existing wrong output
    return False


def calculate_fail_number_GA(input, mutant, program):
    pvalue = '-'
    count_times = 0
    right_output = []
    p = []  # probability
    wrong = 0
    flag_wrong = False
    fre = []
    flag_fail = False
    print(input)

    if program == 'AS':
        bit_i = 6
        bit = 6
        pt = AS.probabilityComputing(input)

    elif program == 'BV':
        bit_i = 7
        bit = 7
        pt = BV.probabilityComputing(input)
    elif program == 'CE':
        bit_i = 11
        bit = 12
        pt = CE.probabilityComputing(input)
    elif program == 'SM':
        bit_i = 5
        bit = 5
        pt = SM.probabilityComputing(input)
    elif program == 'IQFT':
        bit_i = 10
        bit = 10
        pt = IQFT.probabilityComputing(input)
    elif program == 'QRAM':
        bit_i = 9
        bit = 4
        pt = QRAM.probabilityComputing(input)
    for i in range(len(pt)):
        if pt[i] > 1e-3:
            count_times += 1
            right_output.append(i)
            p.append(pt[i])

    if program == 'AS':
        if mutant == 'M1':
            cal = AS.AS_M1(input, count_times)
        elif mutant == 'M2':
            cal = AS.AS_M2(input, count_times)
        elif mutant == 'M3':
            cal = AS.AS_M3(input, count_times)

    elif program == 'BV':
        if mutant == 'M1':
            cal = BV.BV_M1(input, count_times)
        elif mutant == 'M2':
            cal = BV.BV_M2(input, count_times)
        elif mutant == 'M3':
            cal = BV.BV_M3(input, count_times)


    elif program == 'CE':
        if mutant == 'M1':
            cal = CE.CE_M1(input, count_times)
        elif mutant == 'M2':
            cal = CE.CE_M2(input, count_times)
        elif mutant == 'M3':
            cal = CE.CE_M3(input, count_times)

    elif program == 'SM':
        if mutant == 'M1':
            cal = SM.SM_M1(input, count_times)
        elif mutant == 'M2':
            cal = SM.SM_M2(input, count_times)
        elif mutant == 'M3':
            cal = SM.SM_M3(input, count_times)

    elif program == 'IQFT':
        if mutant == 'M1':
            cal = IQFT.IQFT_M1(input, count_times)
        elif mutant == 'M2':
            cal = IQFT.IQFT_M2(input, count_times)
        elif mutant == 'M3':
            cal = IQFT.IQFT_M3(input, count_times)

    elif program == 'QRAM':
        if mutant == 'M1':
            cal = QRAM.QRAM_M1(input, count_times)
        elif mutant == 'M2':
            cal = QRAM.QRAM_M2(input, count_times)
        elif mutant == 'M3':
            cal = QRAM.QRAM_M3(input, count_times)

    # judge wrong outputs
    for j in range(len(pt)):
        j_s = dec2bin(j, bit)
        if j_s in cal:
            if wrong_output(j, right_output) == True:
                flag_fail = True
                flag_wrong = True
                wrong += cal[j_s]
    #
    # chi test
    if flag_wrong == False:  # no wrong output
        if count_times == 1:  # only one output
            pvalue = 1
        else:
            for j in range(len(p)):
                j_s = dec2bin(right_output[j], bit)
                if j_s in cal:
                    fre.append(cal[j_s])
                else:
                    fre.append(0)
            p = np.array(p)
            fre = np.array(fre)
            p = robjects.FloatVector(p)
            fre = robjects.FloatVector(fre)
            robjects.r('''
                    chitest<-function(observed,theoretical){
                        test_result <- chisq.test(x = observed,p = theoretical)
                        pvalue = test_result$p.value
                        return (pvalue)
                    }
            ''')
            t = robjects.r['chitest'](fre, p)
            pvalue = t[0]
            # print('no wrong output')
    else:
        pvalue = 0
    # print(pvalue)
    if pvalue < 0.01:
        flag_fail = True

    return flag_fail


def comb_gen(program, mutant):
    '''
    :param program: program name
    :param mutant: faulty version of a program
    '''
    first_root = './result/results_' + str(K) + '/' + program + '/' + 'scenario2' + '/'
    if not os.path.exists(first_root):
        os.makedirs(first_root)
    file_first = open(first_root + program + '_' + mutant + '_c' + '.txt', 'a')
    o = 2
    for i in range(K):
        c = 0
        flag_stop = False
        while o <= 4:
            dir_root = './inputs_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) + '/'
            input_file = open(dir_root + 'input_' + program + '_' + mutant + '_' + str(i) + '.txt', 'r')
            input_file.readline()
            input_str = input_file.readline().replace('\n', '').replace('\t', '')
            while input_str != "":
                c += 1
                input = int(input_str, 2)
                flag = calculate_fail_number_GA(input, mutant, program)
                if flag == True:
                    file_first.write(str(c) + '\n')
                    flag_stop = True
                    break
                input_str = input_file.readline().replace('\n', '').replace('\t', '')
            if flag_stop == True:
                break


def random_gen(program, mutant):
    '''
    :param program: program name
    :param mutant: faulty version of a program
    '''
    first_root = './result/results_' + str(K) + '/' + program + '/' + 'scenario2' + '/'
    if not os.path.exists(first_root):
        os.makedirs(first_root)
    file_first = open(first_root + program + '_' + mutant + '_r' + '.txt', 'a')
    for i in range(500):
        c = 0
        if program == 'AS':
            n = 6
        elif program == 'BV':
            n = 7
        elif program == 'CE':
            n = 11
        elif program == 'SM':
            n = 5
        elif program == 'IQFT':
            n = 10
        elif program == 'QRAM':
            n = 9
        while True:
            c += 1
            input_str = ''
            for i in range(n):
                bit = random.randint(0, 1)
                input_str += str(bit)
            input = int(input_str, 2)
            flag = calculate_fail_number_GA(input, mutant, program)
            if flag == True:
                file_first.write(str(c) + '\n')
                break


if __name__ == '__main__':
    # combinatorial testing
    comb_gen('AS', 'M1')
    comb_gen('AS', 'M2')
    comb_gen('AS', 'M3')

    comb_gen('BV', 'M1')
    comb_gen('BV', 'M2')
    comb_gen('BV', 'M3')

    comb_gen('CE', 'M1')
    comb_gen('CE', 'M2')
    comb_gen('CE', 'M3')

    comb_gen('IQFT', 'M1')
    comb_gen('IQFT', 'M2')
    comb_gen('IQFT', 'M3')

    comb_gen('QRAM', 'M1')
    comb_gen('QRAM', 'M2')
    comb_gen('QRAM', 'M3')

    comb_gen('SM', 'M1')
    comb_gen('SM', 'M2')
    comb_gen('SM', 'M3')

    # random testing
    random_gen('AS', 'M1')
    random_gen('AS', 'M2')
    random_gen('AS', 'M3')

    random_gen('BV', 'M1')
    random_gen('BV', 'M2')
    random_gen('BV', 'M3')

    random_gen('CE', 'M1')
    random_gen('CE', 'M2')
    random_gen('CE', 'M3')

    random_gen('IQFT', 'M1')
    random_gen('IQFT', 'M2')
    random_gen('IQFT', 'M3')

    random_gen('QRAM', 'M1')
    random_gen('QRAM', 'M2')
    random_gen('QRAM', 'M3')

    random_gen('SM', 'M1')
    random_gen('SM', 'M2')
    random_gen('SM', 'M3')









