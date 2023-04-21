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

def scan_cons_Ga(T,P,α,I_Ga): #扫描F，Ⅴ/Ⅲ比，固定Ga流量I_Ga（sccm），单位°C，Torr
    K=10**(-12.2+1.78E4/(T+273.15)+1.79*np.log10(T+273.15)) #平衡常数，注意符号与文献不一样，因为原始文献是+号，单位atm^-1/2
    P=P/760 #换算为atm
    f = xlwt.Workbook() #创建工作薄
    sheet1 = f.add_sheet(u'过饱和度',cell_overwrite_ok=True) #创建sheet
    sheet2 = f.add_sheet(u'平衡Ga浓度',cell_overwrite_ok=True) #创建sheet
    g = xlwt.Workbook() #等高线图
    sheet3 = g.add_sheet(u'过饱和度',cell_overwrite_ok=True) #创建sheet
    sheet4 = g.add_sheet(u'平衡Ga浓度',cell_overwrite_ok=True) #创建sheet
    plt.figure()
    for i in range(11): #扫描F从0-1
        F=0.1*i
        I_NH3=[] #记录自变量NH3通量（L/min）
        p_Ga_equ=[] #平衡Ga浓度
        supersateration=[]
        for j in range(4000):
            P0_Ga=P*I_Ga*1E-3/(I_Ga*1E-3*(1+10*j+80)+72) #固定H2+N2通量为72L/min
            p_Ga=equalibrim_conc_Ga(F,10*j+80,P0_Ga,α,K,P)
            s=(P0_Ga-p_Ga)/p_Ga #过饱和度
            s=s.real
            p_Ga_equ.append(p_Ga.real*760) #单位Torr
            I_NH3.append(I_Ga*1E-3*(10*j+80))
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
        wusanbi=[] #NH3流量换算回Ⅴ/Ⅲ
        for m in range(len(I_NH3)):
            wusanbi.append(I_NH3[m]/(I_Ga*1E-3))
        for l in wusanbi:
            sheet1.write(k+2,2*i,l) #循环写入 竖着写
            sheet2.write(k+2,2*i,l) #循环写入 竖着写
            sheet3.write(k+2000*i,0,l) #循环写入 竖着写
            sheet3.write(k+2000*i,1,F) #循环写入 竖着写
            sheet4.write(k+2000*i,0,l) #循环写入 竖着写
            sheet4.write(k+2000*i,1,F) #循环写入 竖着写
            k=k+1
        k = 0
        for l in supersateration:
            sheet1.write(k+2,2*i+1,l) #循环写入 竖着写
            sheet3.write(k+2000*i,2,l) #循环写入 竖着写
            k=k+1
        k = 0
        for l in p_Ga_equ:
            sheet2.write(k+2,2*i+1,l) #循环写入 竖着写
            sheet4.write(k+2000*i,2,l) #循环写入 竖着写
            k=k+1
        
        plt.plot(I_NH3,supersateration)
        plt.legend(labels='F=%f'%F)
    plt.xlabel('I_NH3 (L/min)')
    plt.ylabel('supersateration')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    P=P*760
    f.save('T=%d °C,Ga=%f sccm,P=%d, α=%f.xls'%(T,I_Ga,P,α)) #保存文件
    g.save('等高线T=%d °C,Ga=%f sccm,P=%d, α=%f.xls'%(T,I_Ga,P,α)) #保存文件
    

A=scan_cons_Ga(T=880,P=76,α=0.5,I_Ga=5.45)