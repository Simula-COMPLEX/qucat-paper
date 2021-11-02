import os
import numpy as np
import subprocess
from programs import  AS, BV, CE, SM, IQFT, QRAM
import rpy2.robjects as robjects
import random

K = 500  # 500
Seed_N = 0


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


# generating test suites
def gen_test_suites(n, o, mutant, program):
    '''
    :param n: number of input qubits
    :param o: strength:
    :param mutant: faulty program version
    :param program: program name
    '''
    global Seed_N
    folderGenerating = './inputs_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) + '/'
    if not os.path.exists(folderGenerating):
        os.makedirs(folderGenerating)
    print(folderGenerating)
    '''
    command-line of running PICT from line 56
    pict ModelFile.txt /o:N /r:SeedN> OutputFile.txt
    ModelFile.txt: We name each model file as p'n'.txt, 'n' is the number of input qubits
    N: Strength for combinatorial testing
    OuputFile.txt: The file of the generated test suite 
    '''
    for i in range(K):
        Seed_N = random.randint(0,65535)
        p = subprocess.Popen(
            "pict p"+str(n)+".txt /o:" + str(o) + " /r:" + str(Seed_N) + "> D:\WXY\Quantum_Comb_testing\inputs_" + str(
                K) + "\\" + program + "\\" + mutant + "_o" + str(
                o) + "\input_" + program + "_" + mutant + '_' + str(i) + ".txt", shell=True, stdout=subprocess.PIPE,
            cwd="D:\Download\PICT")

def calculate_fail_number_GA(input, mutant, algorithm, program, o):
    pvalue = '-'
    count_times = 0
    right_output = []
    p = []  # probability
    wrong = 0
    flag_wrong = False
    fre = []
    flag_fail = False

    folderGenerating = './result/results_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) + '/'
    if not os.path.exists(folderGenerating):
        os.makedirs(folderGenerating)

    f = open(folderGenerating + program + '_' + mutant + '_' + algorithm + '_o' + str(o) + '.txt', 'a')

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
        thre = 1e-3
        if program == 'QRAM':
            thre = 1e-4
        if pt[i] > thre:
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

    if flag_wrong == True:
      pvalue = '-'

    # write in file
    f.write(str(dec2bin(input,bit_i)))
    f.write('\t')
    f.write(str(wrong) + ' / ' + str(count_times * 100))
    f.write('\t')
    # pvalue = ('%.6f'%pvalue)
    #pvalue = (pvalue)
    f.write(str(pvalue))
    f.write('\t')
    if flag_fail == False:
        f.write('pass')
    else:
        f.write('fail')
    f.write('\n')
    # f.write(str(cal))
    # f.write('\n')
    return flag_fail, f

# doing testing
def comb_testing(mutant, program, o):
    '''
    :param mutant: faulty version of the program
    :param program: program name
    :param o: strength
    :return: the list of number of test cases in each test suite
    '''
    #open the input files
    dir_root = './inputs_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) +'/'
    folder_analyzing = './result/results_' + str(K) + '/' + program + '/' + 'scenario1' + '/' + mutant + '_o' + str(o) +'/'
    #summary_comb = './result/results_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) +'/' + program + '_' + mutant + '_' + 'o' + str(o) + '_comb_summary.txt'
    if not os.path.exists(folder_analyzing):
        os.makedirs(folder_analyzing)
    summary_comb = open(folder_analyzing + program + '_' + mutant + '_' + 'o' + str(o) + '_comb_summary.txt','w')

    # input_file = open('./inputs/'+'input_'+program+"_"+mutant+".txt")
    count_list = []  # the list of test cases in different test suites
    fail_list = []  # the list of test cases that fail in different test suites
    fail_suite_count = 0
    for i in range(K):
        input_file = open(dir_root + 'input_' + program + '_' + mutant + '_' + str(i) + '.txt')
        count = 0  # the number of test cases in one test suite
        count_fail = 0  # the number of test cases that fail in one test suite
        #get the input
        input_file.readline()
        input_str = input_file.readline().replace('\n', '').replace('\t', '')
        while input_str != "":
            count += 1
            input = int(input_str, 2)
            flag_fail, f = calculate_fail_number_GA(input, mutant, 'Comb', program, o)
            input_str = input_file.readline().replace('\n', '').replace('\t', '')
            if flag_fail == True:
                count_fail += 1
        print("comb "+str(i)+" "+str(count_fail))
        # f = open('./results/'+program+'/' + program + '_' + mutant + '_' + 'Comb' + '.txt', 'a')
        f.write('fail / total :' + str(count_fail) + ' / ' + str(count))
        f.write('\n')
        if count_fail > 0:
            fail_suite_count += 1
            summary_comb.write('1')
            summary_comb.write('\n')
        else:
            summary_comb.write('0')
            summary_comb.write('\n')
        fail_list.append(count_fail)
        count_list.append(count)
    f.write('\n')
    for i in range(K):
        f.write(str(fail_list[i]) + ' / ' + str(count_list[i]))
        f.write('\t')
    f.write('\n')
    f.write('number of fail suites / total number of suites : ' + str(fail_suite_count) + '/' + str(len(count_list)))
    f.write('\n')
    f.write('number of fail cases / total number of cases : ' + str(sum(fail_list)) + ' / ' + str(sum(count_list)))
    f.write('\n')

    return count_list

# Random
def random_testing(mutant, program, count_list, n, o):
    '''
    :param mutant: faulty version of the program
    :param program:program name
    :param count_list: the list of number of test cases in each test suite in corresponding combinatorial testing
    :param n: number of input qubits
    :param o: strength
    '''
    folder_analyzing = './result/results_' + str(K) + '/' + program + '/' + 'scenario1' + '/' + mutant + '_o' + str(o) +'/'
    if not os.path.exists(folder_analyzing):
        os.makedirs(folder_analyzing)
    summary_random = open(folder_analyzing + program + '_' + mutant + '_' + 'o' + str(o) + '_random_summary.txt','w')

    count_list_r = count_list[:]
    fail_list = []
    fail_suite_count = 0
    for i in range(len(count_list)):
        count_fail = 0
        while count_list[i] != 0:
            input_str = ''
            for j in range(n):
                bit = random.randint(0, 1)
                input_str += str(bit)
            input = int(input_str, 2)
            flag_fail, f = calculate_fail_number_GA(input, mutant, 'Random', program, o)
            count_list[i] = count_list[i] - 1
            if flag_fail == True:
                count_fail += 1
        print("random " + str(i) + " " + str(count_fail))
        # f = open('./results/' + program + '/' + program + '_' + mutant + '_' + 'Random' + '.txt', 'a')
        f.write('fail / total :' + str(count_fail) + ' / ' + str(count_list_r[i]))
        f.write('\n')
        if count_fail > 0:
            fail_suite_count += 1
            summary_random.write('1')
            summary_random.write('\n')
        else:
            summary_random.write('0')
            summary_random.write('\n')
        fail_list.append(count_fail)
    f.write('\n')
    for i in range(K):
        f.write(str(fail_list[i]) + ' / ' + str(count_list_r[i]))
        f.write('\t')
    f.write('\n')
    f.write('number of fail suites / total number of suites : ' + str(fail_suite_count) + '/' + str(len(count_list_r)))
    f.write('\n')
    f.write('number of fail cases / total number of cases : ' + str(sum(fail_list)) + ' / ' + str(sum(count_list_r)))
    f.write('\n')


if __name__ == '__main__':
    #generating inputs
    gen_test_suites(6, 2, 'M1', 'AS')
    gen_test_suites(6, 3, 'M1', 'AS')
    gen_test_suites(6, 4, 'M1', 'AS')
    gen_test_suites(6, 2, 'M2', 'AS')
    gen_test_suites(6, 3, 'M2', 'AS')
    gen_test_suites(6, 4, 'M2', 'AS')
    gen_test_suites(6, 2, 'M3', 'AS')
    gen_test_suites(6, 3, 'M3', 'AS')
    gen_test_suites(6, 4, 'M3', 'AS')

    gen_test_suites(9, 2, 'M1', 'AS_9')
    gen_test_suites(9, 3, 'M1', 'AS_9')
    gen_test_suites(9, 4, 'M1', 'AS_9')
    gen_test_suites(9, 2, 'M2', 'AS_9')
    gen_test_suites(9, 3, 'M2', 'AS_9')
    gen_test_suites(9, 4, 'M2', 'AS_9')
    gen_test_suites(9, 2, 'M3', 'AS_9')
    gen_test_suites(9, 3, 'M3', 'AS_9')
    gen_test_suites(9, 4, 'M3', 'AS_9')

    gen_test_suites(7, 2, 'M1', 'BV')
    gen_test_suites(7, 3, 'M1', 'BV')
    gen_test_suites(7, 4, 'M1', 'BV')
    gen_test_suites(7, 2, 'M2', 'BV')
    gen_test_suites(7, 3, 'M2', 'BV')
    gen_test_suites(7, 4, 'M2', 'BV')
    gen_test_suites(7, 2, 'M3', 'BV')
    gen_test_suites(7, 3, 'M3', 'BV')
    gen_test_suites(7, 4, 'M3', 'BV')

    gen_test_suites(11, 2, 'M1', 'CE')
    gen_test_suites(11, 3, 'M1', 'CE')
    gen_test_suites(11, 4, 'M1', 'CE')
    gen_test_suites(11, 2, 'M2', 'CE')
    gen_test_suites(11, 3, 'M2', 'CE')
    gen_test_suites(11, 4, 'M2', 'CE')
    gen_test_suites(11, 2, 'M3', 'CE')
    gen_test_suites(11, 3, 'M3', 'CE')
    gen_test_suites(11, 4, 'M3', 'CE')

    gen_test_suites(5, 2, 'M1', 'SM')
    gen_test_suites(5, 3, 'M1', 'SM')
    gen_test_suites(5, 4, 'M1', 'SM')
    gen_test_suites(5, 2, 'M2', 'SM')
    gen_test_suites(5, 3, 'M2', 'SM')
    gen_test_suites(5, 4, 'M2', 'SM')
    gen_test_suites(5, 2, 'M3', 'SM')
    gen_test_suites(5, 3, 'M3', 'SM')
    gen_test_suites(5, 4, 'M3', 'SM')

    gen_test_suites(10, 2, 'M1', 'IQFT')
    gen_test_suites(10, 3, 'M1', 'IQFT')
    gen_test_suites(10, 4, 'M1', 'IQFT')
    gen_test_suites(10, 2, 'M2', 'IQFT')
    gen_test_suites(10, 3, 'M2', 'IQFT')
    gen_test_suites(10, 4, 'M2', 'IQFT')
    gen_test_suites(10, 2, 'M3', 'IQFT')
    gen_test_suites(10, 3, 'M3', 'IQFT')
    gen_test_suites(10, 4, 'M3', 'IQFT')
    #
    gen_test_suites(9, 2, 'M1', 'QRAM')
    gen_test_suites(9, 3, 'M1', 'QRAM')
    gen_test_suites(9, 4, 'M1', 'QRAM')
    gen_test_suites(9, 2, 'M2', 'QRAM')
    gen_test_suites(9, 3, 'M2', 'QRAM')
    gen_test_suites(9, 4, 'M2', 'QRAM')
    gen_test_suites(9, 2, 'M3', 'QRAM')
    gen_test_suites(9, 3, 'M3', 'QRAM')
    gen_test_suites(9, 4, 'M3', 'QRAM')


    #executing test suites
    count_list = comb_testing('M1','AS',2)
    random_testing('M1','AS',count_list,6,2)
    count_list = comb_testing('M1','AS',3)
    random_testing('M1','AS',count_list,6,3)
    count_list = comb_testing('M1','AS',4)
    random_testing('M1','AS',count_list,6,4)
    count_list = comb_testing('M2','AS',2)
    random_testing('M2','AS',count_list,6,2)
    count_list = comb_testing('M2','AS',3)
    random_testing('M2','AS',count_list,6,3)
    count_list = comb_testing('M2','AS',4)
    random_testing('M2','AS',count_list,6,4)
    count_list = comb_testing('M3','AS',2)
    random_testing('M3','AS',count_list,6,2)
    count_list = comb_testing('M3','AS',3)
    random_testing('M3','AS',count_list,6,3)
    count_list = comb_testing('M3','AS',4)
    random_testing('M3','AS',count_list,6,4)

    count_list = comb_testing('M1','BV',2)
    random_testing('M1','BV',count_list,7,2)
    count_list = count_list('M1','BV',3)
    random_testing('M1','BV',count_list,7,3)
    count_list = count_list('M1','BV',4)
    random_testing('M1','BV',count_list,7,4)
    count_list = comb_testing('M2','BV',2)
    random_testing('M2','BV',count_list,7,2)
    count_list = comb_testing('M2','BV',3)
    random_testing('M2','BV',count_list,7,3)
    count_list = count_list('M2','BV',4)
    random_testing('M2','BV',count_list,7,4)
    count_list = comb_testing('M3','BV',2)
    random_testing('M3','BV',count_list,7,2)
    count_list = comb_testing('M3','BV',3)
    random_testing('M3','BV',count_list,7,3)
    count_list = comb_testing('M3','BV',4)
    random_testing('M3','BV',count_list,7,4)

    count_list = comb_testing('M1','CE',2)
    random_testing('M1','CE',count_list,11,2)
    count_list = comb_testing('M1','CE',3)
    random_testing('M1','CE',count_list,11,3)
    count_list = comb_testing('M1','CE',4)
    random_testing('M1','CE',count_list,11,4)
    count_list = comb_testing('M2','CE',2)
    random_testing('M2','CE',count_list,11,2)
    count_list = comb_testing('M2','CE',3)
    random_testing('M2','CE',count_list,11,3)
    count_list = comb_testing('M2','CE',4)
    random_testing('M2','CE',count_list,11,4)
    count_list = comb_testing('M3','CE',2)
    random_testing('M3','CE',count_list,11,2)
    count_list = comb_testing('M3','CE',3)
    random_testing('M3','CE',count_list,11,3)
    count_list = comb_testing('M3','CE',4)
    random_testing('M3','CE',count_list,11,4)

    count_list = comb_testing('M1','IQFT',2)
    random_testing('M1','IQFT',count_list,10,2)
    count_list = comb_testing('M1','IQFT',3)
    random_testing('M1','IQFT',count_list,10,3)
    count_list = comb_testing('M1','IQFT',4)
    random_testing('M1','IQFT',count_list,10,4)
    count_list = comb_testing('M2','IQFT',2)
    random_testing('M2','IQFT',count_list,10,2)
    count_list = comb_testing('M2','IQFT',3)
    random_testing('M2','IQFT',count_list,10,3)
    count_list = comb_testing('M2','IQFT',4)
    random_testing('M2','IQFT',count_list,10,4)
    count_list = comb_testing('M3','IQFT',2)
    random_testing('M3','IQFT',count_list,10,2)
    count_list = comb_testing('M3','IQFT',3)
    random_testing('M3','IQFT',count_list,10,3)
    count_list = comb_testing('M3','IQFT',4)
    random_testing('M3','IQFT',count_list,10,4)

    count_list = comb_testing('M1','QRAM',2)
    random_testing('M1','QRAM',count_list,9,2)
    count_list = count_list('M1','QRAM',3)
    random_testing('M1','QRAM',count_list,9,3)
    count_list = count_list('M1','QRAM',4)
    random_testing('M1','QRAM',count_list,9,4)
    count_list = comb_testing('M2','QRAM',2)
    random_testing('M2','QRAM',count_list,9,2)
    count_list = comb_testing('M2','QRAM',3)
    random_testing('M2','QRAM',count_list,9,3)
    count_list = count_list('M2','QRAM',4)
    random_testing('M2','QRAM',count_list,9,4)
    count_list = comb_testing('M3','QRAM',2)
    random_testing('M3','QRAM',count_list,9,2)
    count_list = comb_testing('M3','QRAM',3)
    random_testing('M3','QRAM',count_list,9,3)
    count_list = comb_testing('M3','QRAM',4)
    random_testing('M3','QRAM',count_list,9,4)

    count_list = comb_testing('M1','SM',2)
    random_testing('M1','SM',count_list,5,2)
    count_list = comb_testing('M1','SM',3)
    random_testing('M1','SM',count_list,5,3)
    count_list = comb_testing('M1','SM',4)
    random_testing('M1','SM',count_list,5,4)
    count_list = comb_testing('M2','SM',2)
    random_testing('M2','SM',count_list,5,2)
    count_list = comb_testing('M2','SM',3)
    random_testing('M2','SM',count_list,5,3)
    count_list = comb_testing('M2','SM',4)
    random_testing('M2','SM',count_list,5,4)
    count_list = comb_testing('M3','SM',2)
    random_testing('M3','SM',count_list,5,2)
    count_list = comb_testing('M3','SM',3)
    random_testing('M3','SM',count_list,5,3)
    count_list = comb_testing('M3','SM',4)
    random_testing('M3','SM',count_list,5,4)
