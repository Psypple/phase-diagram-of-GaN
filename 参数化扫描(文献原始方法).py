# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:15:58 2023

@author: psypple
"""

import numpy as np
import matplotlib.pyplot as plt
import xlwt

def equalibrim_conc_Ga(F,r,P0_Ga,α,K,P): #给定F和r计算平衡Ga浓度，单位为atm. 其中F是H2占载气（H2+N2）比例（注意即使没有通H2也可能不为0，因为产物有H2），r是Ⅴ/Ⅲ比
    Pr=P0_Ga*((1-F)+r*((1+α/2)-F*(1+α)))+F*P
    A=P0_Ga*(r-1)
    B=Pr-A
    
    # 定义四次方程的系数
    coeffs = [1, 2*A+8/K**2, -12*B/K**2+A**2, 6*B**2/K**2, -B**3/K**2]
    
    # 使用poly1d函数创建一元四次方程对象
    eq = np.poly1d(coeffs)
    
    # 使用roots函数求解方程
    roots = np.roots(eq)
    P_Ga=[]
    for i in roots:
        if i.imag==0:
            P_Ga.append(i)
    P_Ga_true=max(P_Ga) #取实数解中最小的
    return P_Ga_true

def scan_cons_Ga(T,P,α,P0_Ga): #扫描F，Ⅴ/Ⅲ比，固定Ga流量，单位°C，Torr
    K=10**(-12.2+1.78E4/(T+273.15)+1.79*np.log10(T+273.15)) #平衡常数，注意符号与文献不一样，因为原始文献是+号，单位atm^-1/2
    P=P/760 #换算为atm
    P0_Ga=P0_Ga/760 #换算为atm
    f = xlwt.Workbook() #创建工作薄
    sheet1 = f.add_sheet(u'过饱和度',cell_overwrite_ok=True) #创建sheet
    sheet2 = f.add_sheet(u'平衡Ga浓度',cell_overwrite_ok=True) #创建sheet
    plt.figure()
    for i in range(11): #扫描F从0-1
        F=0.1*i
        ratio=[] #记录自变量Ⅴ/Ⅲ比
        p_Ga_equ=[] #平衡Ga浓度
        supersateration=[]
        for j in range(2000):
            p_Ga=equalibrim_conc_Ga(F,10*j+80,P0_Ga,α,K,P)
            s=(P0_Ga-p_Ga)/p_Ga #过饱和度
            s=s.real
            p_Ga_equ.append(p_Ga.real*760) #单位Torr
            ratio.append(10*j+80)
            supersateration.append(s)
        
        sheet1.write(0,2*i,"F=%f"%F)
        sheet2.write(0,2*i,"F=%f"%F)
        sheet1.write(0,2*i+1,'')
        sheet2.write(0,2*i+1,'')
        sheet1.write(1,2*i,'Ⅴ/Ⅲ比')
        sheet2.write(1,2*i,'Ⅴ/Ⅲ比')
        sheet1.write(1,2*i+1,'过饱和度')
        sheet2.write(1,2*i+1,'平衡Ga浓度（Torr）')
        k = 0
        for l in ratio:
            sheet1.write(k+2,2*i,l) #循环写入 竖着写
            sheet2.write(k+2,2*i,l) #循环写入 竖着写
            k=k+1
        k = 0
        for l in supersateration:
            sheet1.write(k+2,2*i+1,l) #循环写入 竖着写
            k=k+1
        k = 0
        for l in p_Ga_equ:
            sheet2.write(k+2,2*i+1,l) #循环写入 竖着写
            k=k+1
        
        plt.plot(ratio,supersateration)
        plt.legend(labels='F=%f'%F)
    plt.xlabel('Ⅴ/Ⅲ')
    plt.ylabel('supersateration')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    P=P*760
    f.save('T=%d °C,Ga=%f Torr,P=%d, α=%f.xls'%(T,P0_Ga,P,α)) #保存文件
    

def scan_cons_r(T,P,α,r): #扫描F，通入Ga流量，固定Ⅴ/Ⅲ比，单位°C，Torr，sccm（mL/min）,这里假设H2+N2恒定为72L/min
    K=10**(-12.2+1.78E4/(T+273.15)+1.79*np.log10(T+273.15)) #平衡常数，注意符号与文献不一样，因为原始文献是+号，单位atm^-1/2
    P=P/760 #换算为atm
    f = xlwt.Workbook() #创建工作薄
    sheet1 = f.add_sheet(u'过饱和度',cell_overwrite_ok=True) #创建sheet
    sheet2 = f.add_sheet(u'平衡Ga浓度',cell_overwrite_ok=True) #创建sheet
    plt.figure()
    for i in range(11): #扫描F从0-1
        F=0.1*i
        I_Ga=[] #记录自变量Ga流量（sccm）
        p_Ga_equ=[] #平衡Ga浓度
        supersateration=[]
        for j in range(2000):
            I_Ga.append(5E-2+j*2E-3)
            P0_Ga=P*I_Ga[-1]*1E-3/(I_Ga[-1]*1E-3*(1+r)+72) #注意这里P已经是atm单位，不用换算Torr，直接计算就行
            p_Ga=equalibrim_conc_Ga(F,r,P0_Ga,α,K,P)
            s=(P0_Ga-p_Ga)/p_Ga #过饱和度
            s=s.real
            p_Ga_equ.append(p_Ga.real*760) #单位Torr
            supersateration.append(s)
        
        sheet1.write(0,2*i,"F=%f"%F)
        sheet2.write(0,2*i,"F=%f"%F)
        sheet1.write(0,2*i+1,'')
        sheet2.write(0,2*i+1,'')
        sheet1.write(1,2*i,'Ga通量（sccm）')
        sheet2.write(1,2*i,'Ga通量（sccm）')
        sheet1.write(1,2*i+1,'过饱和度')
        sheet2.write(1,2*i+1,'平衡Ga浓度（Torr）')
        k = 0
        for l in I_Ga:
            sheet1.write(k+2,2*i,l) #循环写入 竖着写
            sheet2.write(k+2,2*i,l) #循环写入 竖着写
            k=k+1
        k = 0
        for l in supersateration:
            sheet1.write(k+2,2*i+1,l) #循环写入 竖着写
            k=k+1
        k = 0
        for l in p_Ga_equ:
            sheet2.write(k+2,2*i+1,l) #循环写入 竖着写
            k=k+1
        
        plt.plot(I_Ga,supersateration)
        plt.legend('F=%f'%F)
    plt.xlabel('I_Ga (sccm)')
    plt.ylabel('supersateration')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    P=P*760
    f.save('T=%d °C,r=%d,P=%d Torr,α=%f.xls'%(T,r,P,α)) #保存文件

A=scan_cons_Ga(T=800,P=200,α=0.5,P0_Ga=2E-3)
A=scan_cons_Ga(T=850,P=200,α=0.5,P0_Ga=2E-3)
A=scan_cons_Ga(T=900,P=200,α=0.5,P0_Ga=2E-3)
A=scan_cons_Ga(T=850,P=76,α=0.5,P0_Ga=2E-3)
A=scan_cons_Ga(T=850,P=760,α=0.5,P0_Ga=2E-3)
A=scan_cons_Ga(T=850,P=200,α=0.2,P0_Ga=2E-3)
A=scan_cons_Ga(T=850,P=200,α=0.8,P0_Ga=2E-3)

A=scan_cons_r(T=850,P=200,α=0.5,r=20000)
A=scan_cons_r(T=800,P=200,α=0.5,r=20000)
A=scan_cons_r(T=900,P=200,α=0.5,r=20000)
A=scan_cons_r(T=850,P=76,α=0.5,r=20000)
A=scan_cons_r(T=850,P=760,α=0.5,r=20000)
A=scan_cons_r(T=850,P=200,α=0.2,r=20000)
A=scan_cons_r(T=850,P=200,α=0.8,r=20000)