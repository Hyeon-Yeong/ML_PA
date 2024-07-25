import os
import math
import numpy as np

import pdb
import csv




def read_cti(filePath,write_path):
    print(filePath)
    read_c = open(filePath)
    data = read_c.read()
    read_c.close()
    data = data.split("BEGIN\n")

    #freq_str= data[1].split("END")

    s_str = data[2].split("END")
    s11_str = s_str[0].replace("\t", "")
    s11_str = s11_str.split("\n")

    s_str = data[3].split("END")
    s12_str = s_str[0].replace("\t", "")
    s12_str = s12_str.split("\n")

    s_str = data[4].split("END")
    s13_str = s_str[0].replace("\t", "")
    s13_str = s13_str.split("\n")

    s_str = data[5].split("END")
    s14_str = s_str[0].replace("\t", "")
    s14_str = s14_str.split("\n")

    s_str = data[6].split("END")
    s21_str = s_str[0].replace("\t", "")
    s21_str = s21_str.split("\n")

    s_str = data[7].split("END")
    s22_str = s_str[0].replace("\t", "")
    s22_str = s22_str.split("\n")

    s_str = data[8].split("END")
    s23_str = s_str[0].replace("\t", "")
    s23_str = s23_str.split("\n")

    s_str = data[9].split("END")
    s24_str = s_str[0].replace("\t", "")
    s24_str = s24_str.split("\n")

    s_str = data[10].split("END")
    s31_str = s_str[0].replace("\t", "")
    s31_str = s31_str.split("\n")

    s_str = data[11].split("END")
    s32_str = s_str[0].replace("\t", "")
    s32_str = s32_str.split("\n")

    s_str = data[12].split("END")
    s33_str = s_str[0].replace("\t", "")
    s33_str = s33_str.split("\n")

    s_str = data[13].split("END")
    s34_str = s_str[0].replace("\t", "")
    s34_str = s34_str.split("\n")

    s_str = data[14].split("END")
    s41_str = s_str[0].replace("\t", "")
    s41_str = s41_str.split("\n")

    s_str = data[15].split("END")
    s42_str = s_str[0].replace("\t", "")
    s42_str = s42_str.split("\n")

    s_str = data[16].split("END")
    s43_str = s_str[0].replace("\t", "")
    s43_str = s43_str.split("\n")

    s_str = data[17].split("END")
    s44_str = s_str[0].replace("\t", "")
    s44_str = s44_str.split("\n")



    freq=[]

    s11_r = []
    s11_i = []
    

    s12_r = []
    s12_i = []

    s13_r = []
    s13_i = []

    s14_r = []
    s14_i = []
    

    s21_r = []
    s21_i = []
    

    s22_r = []
    s22_i = []

    s23_r = []
    s23_i = []

    s24_r = []
    s24_i = []

    s31_r = []
    s31_i = []

    s32_r = []
    s32_i = []
    
    s33_r = []
    s33_i = []

    s34_r = []
    s34_i = []

    s41_r = []
    s41_i = []

    s42_r = []
    s42_i = []
    
    s43_r = []
    s43_i = []
    
    s44_r = []
    s44_i = []


    

    a=[]
    rows=[['freq','s11_real','s11_imag','s12_real','s12_imag','s13_real','s13_imag','s14_real','s14_imag','s21_real','s21_imag','s22_real','s22_imag','s23_real','s23_imag','s24_real','s24_imag','s31_real','s31_imag','s32_real','s32_imag','s33_real','s33_imag','s34_real','s34_imag','s41_real','s41_imag','s42_real','s42_imag','s43_real','s43_imag','s44_real','s44_imag']]


    for i in range(len(s11_str) - 1):
        s11_ri = s11_str[i].split(",")
        s12_ri = s12_str[i].split(",")
        s13_ri = s13_str[i].split(",")
        s14_ri = s14_str[i].split(",")
        s21_ri = s21_str[i].split(",")
        s22_ri = s22_str[i].split(",")
        s23_ri = s23_str[i].split(",")
        s24_ri = s24_str[i].split(",")
        s31_ri = s31_str[i].split(",")
        s32_ri = s32_str[i].split(",")
        s33_ri = s33_str[i].split(",")
        s34_ri = s34_str[i].split(",")
        s41_ri = s41_str[i].split(",")
        s42_ri = s42_str[i].split(",")
        s43_ri = s43_str[i].split(",")
        s44_ri = s44_str[i].split(",")

        s11_r.append(float(s11_ri[0]))
        s11_i.append(float(s11_ri[1]))
        s12_r.append(float(s12_ri[0]))
        s12_i.append(float(s12_ri[1]))
        s13_r.append(float(s13_ri[0]))
        s13_i.append(float(s13_ri[1]))
        s14_r.append(float(s14_ri[0]))
        s14_i.append(float(s14_ri[1]))
        s21_r.append(float(s21_ri[0]))
        s21_i.append(float(s21_ri[1]))
        s22_r.append(float(s22_ri[0]))
        s22_i.append(float(s22_ri[1]))
        s23_r.append(float(s23_ri[0]))
        s23_i.append(float(s23_ri[1]))
        s24_r.append(float(s24_ri[0]))
        s24_i.append(float(s24_ri[1]))
        s31_r.append(float(s31_ri[0]))
        s31_i.append(float(s31_ri[1]))
        s32_r.append(float(s32_ri[0]))
        s32_i.append(float(s32_ri[1]))
        s33_r.append(float(s33_ri[0]))
        s33_i.append(float(s33_ri[1]))
        s34_r.append(float(s34_ri[0]))
        s34_i.append(float(s34_ri[1]))
        s41_r.append(float(s41_ri[0]))
        s41_i.append(float(s41_ri[1]))
        s42_r.append(float(s42_ri[0]))
        s42_i.append(float(s42_ri[1]))
        s43_r.append(float(s43_ri[0]))
        s43_i.append(float(s43_ri[1]))
        s44_r.append(float(s44_ri[0]))
        s44_i.append(float(s44_ri[1]))
        

    

        freq.append(25+0.5*i)
        #pdb.set_trace()
        
        #a=[s11_db(i-1)]
        #a.append(s11_db(i),s11_phase(i),s12_db(i),s12_phase(i),s21_db(i),s21_phase(i),s22_db(i),s22_phase(i))
        a=[str(freq[i]),str(s11_r[i]),str(s11_i[i]),str(s12_r[i]),str(s12_i[i]),str(s13_r[i]),str(s13_i[i]),str(s14_r[i]),str(s14_i[i]),str(s21_r[i]),str(s21_i[i]),str(s22_r[i]),str(s22_i[i]),str(s23_r[i]),str(s23_i[i]),str(s24_r[i]),str(s24_i[i]),str(s31_r[i]),str(s31_i[i]),str(s32_r[i]),str(s32_i[i]),str(s33_r[i]),str(s33_i[i]),str(s34_r[i]),str(s34_i[i]),str(s41_r[i]),str(s41_i[i]),str(s42_r[i]),str(s42_i[i]),str(s43_r[i]),str(s43_i[i]),str(s44_r[i]),str(s44_i[i])]

        #a=[str(freq[i]),str(s11_r[i]),str(s11_i[i]),str(s12_r[i]),str(s12_i[i]),str(s21_r[i]),str(s21_i[i]),str(s22_r[i]),str(s22_i[i])]

        rows.append(a)
        #pdb.set_trace()
        

    #pdb.set_trace()

    # name of csv file 
    
    
    # writing to csv file 
    with open(write_path, 'w') as csvfile: 
    # creating a csv writer object
        writer = csv.writer(csvfile, delimiter=',') 
        for line in rows:

            writer.writerow(line)
        
   




    

    




    
