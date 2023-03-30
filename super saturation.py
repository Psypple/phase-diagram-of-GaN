# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:18:59 2023

@author: psypple
"""

import numpy as np
import matplotlib.pyplot as plt
import xlwt

global P,T,α,P0_Ga,K
P=20 #总压强，单位torr
T=1050 #温度，单位°C
α=0.7 #NH3分解的比例
P0_Ga=8E-3 #输入TM(E)Ga分压，单位torr
K=10**(-12.2+1.78E4/(T+273.15)+1.79*np.log10(T+273.15)) #平衡常数，注意符号与文献不一样，因为原始文献是+号

def equalibrim_conc_Ga(F,r): #给定F和r计算平衡Ga浓度，单位为torr. 其中F是H2占载气（H2+N2）比例（注意即使没有通H2也可能不为0，因为产物有H2），r是Ⅴ/Ⅲ比
    Pr=(P0_Ga*((1-F)+r*((1+α/2)-F))+F*P)*P/(P+P0_Ga*r*α)
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

F=1
ratio=[]
supersateration=[]
for i in range(1900):
    p_Ga=equalibrim_conc_Ga(F,i+80)
    s=(P0_Ga-p_Ga)/p_Ga #过饱和度
    ratio.append(i+80)
    supersateration.append(s)
print (supersateration)
f = xlwt.Workbook() #创建工作bai薄du
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
j = 0
for i in ratio:
    sheet1.write(j,0,i) #循环写入zhi 竖着写
    j=j+1
j = 0
for i in supersateration:
    sheet1.write(j,1,i) #循环写入zhi 竖着写
    j=j+1
f.save('F=%f.xls'%F)#保存文件dao