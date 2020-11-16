# -*- coding: utf-8 -*-
# RIP CURRENT PAPER SCRIPT
"""
Created on Thu Nov 22 15:29:00 2018

@author: Archie Withers and Sergio Maldonado

"This script computes the 'Brute Force' approach described in our supporting
paper 'On the swimming strategies to escape a rip current: a mathematical 
approach' Functions to calculate the work required for each strategy are 
defined, to which a range values for the variables defining our idealised rip,
are passed. The code outputs text files containing the data for the 
work and power required by each startegy for every possible combination of these 
parameters, and therefore every possible rip current. This data can be used to 
plot graphs to illustrate the results more clearly.


"NOTES: 
    
Not considering the term 0.5 rho C_D A in calculations, therefore 
work (power) is  NOT in J (W). 
Only relative quantities (e.g. W2/W1) are relevant."

"""
import math as ma
import numpy as np

#l - Swimmer starting distance offshore [m]
#lr- Starting distance offshore strategy 4 [m]
#lx - Distance swum parallel to shore in strategy 2 [m]
#Cd - Swimmer's drag coefficient
#Ve - Swimmer's escape velocity [m]
#Vr - Rip current channel velocity [m/s]
#Vf - Feeder channel velocity [m/s]
#wf - Feeder channel width [m]
#wr - Rip channel width [m]

#Firstly, functions are defined to calculate the work required for each strategy.                                         
     
#Strategy 1 - Swimming directly back to shore against the rip
def work_strategy1(l, lr, Ve, Vr, Vf, wf, wr):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via strategy 1
    """
    W1 = ((Ve+Vr)**3)*((l-wf)/Ve)                                              # Calculates work for section swimming in rip channel
    W2 = ((Ve+Vf)**3)*(wf/Ve)                                                  # Calculates work for section swimming in feeder channel
    if l - wf < 0 or l > wf + lr:                                              # Lower and upper limits of the starting distance
        return -1
    else:                                   
        return W1 + W2                                                         # Returns total value of work done for Strategy 1

#Strategy 2 - Swimming parallel to the rip for a distance lx to escape from rip
# channel beofre turning 90 degrees to swim directly back to shore
def work_strategy2(lx, l, lr, Ve, Vr, Vf, wf, wr):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via strategy 2
    """
    W1 = ((Ve**2 + Vr**2)**1.5)*(wr/(2*Ve))                                    # Calculates work for section swimming within rip channel
    W2 = ((Ve**2)*(lx-(wr/2)))                                                 # Calculates work for section outside rip current swimming parallel to shore
    W3 = ((Ve**2)*(l-wf))                                                      # Calculates work for section outside rip current but swimming directly back to shore
    W4 = ((Ve**2 + Vf**2)**1.5)*(wf/Ve)                                        # Calculates work done for section in feeder channel swimming directly back to shore
    if l - wf < 0 or l > wf + lr:                                              # Lower and upper limits of the starting distance
        return 10
    else:            
        return W1+W2+W3+W4                                                     # Returns total value of work done for Strategy 2


#Strategy 3 - Swimming at 45 degrees to the rip back to shore 
def work_strategy3(l, lr, Ve, Vr, Vf, wf, wr):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via strategy 3
    """
    a = Ve**2/2                                                                #First term in work done equation whilst swimming in the rip current channel
    b = (Ve*ma.sqrt(2))/2 + Vr                                                 # Second term in work done equation whilst swimming in the rip current channel
    c = (wr*ma.sqrt(2))/(2*Ve)                                                 # Third term in work done equation whilst swimming in the rip current channel
    W1= (((a + b**2)**1.5)*c)                                                  # Calculates work done for section swimming in rip current channel 
    d = Ve**2                                                                  # First term in work done equation whilst swimming outside rip channel
    e = (2*(l-wf-(wr/2)))/ma.sqrt(2)                                           # Second term in work done equation whilst swimming outside rip channel
    W2 = (d*e)                                                                 # Calculates work done for section swimming outside rip channel
    f = (Ve*ma.sqrt(2))/2 + Vf                                                 # First term in work done equation whilst swimming in feeder channel
    g = Ve**2/2                                                                # Second term in work done equation whilst swimming in feeder channel
    h = (2*wf)/(Ve*ma.sqrt(2))                                                 # Third term in work done equation whilst swimming in feeder channel
    W3 = ((((f**2)+g)**1.5)*h)                                                 # Calculates work done for section swimming in feeder channel
    if l < wf + 0.5*wr or l > wf + lr:                                         # Relation to ensure swimmer passes through all three sections in the model
        return 10
    else:
        return W1+W2+W3                                                        # Returns total value of work done for Strategy 3


def work_strategy4(lr, Ve, Vr, Vf, wf, wr, l):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via stratgey 4 
    (l is not used in formula but is needed for comparison with strategy 1)
    """
    W4 = ((2*Ve*Ve*lr) + (Ve*Ve + Vf*Vf)**1.5*(wf/Ve))                         # All terms in work done equation for strategy 4
    if l < wf or l > wf + lr:
        return 10
    else:
        return W4                                                              # Returns total value of work done for Strategy 3



# Next, matrices are generated for the data to be added to.
mat1 =  np.array([0,0])
mat2 = np.array([0,0])
mat3 = np.array([0,0])
mat4 = np.array([0,0])
mat_pars = np.array([0,0,0,0,0,0,0,0,0])

mat1_power = np.array([0,0])
mat2_power = np.array([0,0])
mat3_power = np.array([0,0])
mat4_power = np.array([0,0])

#The range of values given to each startegy to represent rips of all shapes and sizes
ls = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 150, 200, 250, 400]
Ve = [0.1, 1.0]
Vr = [0.2, 2.5] 
Vf = [0.25, 1.0]
wf = [25, 75]
wr = [10, 50]
lr = [25, 50, 75, 100, 200, 400]
lx = [1, 1.5, 2]      # this is lx in lx*wr                      

count = 0
# For loops to pass each value in the range to the work functions defined above
for i in ls:
    for m in wf:
        for k in Vr:
            for l in Vf:
                for j in Ve:
                    for n in wr:
                        for o in lr:
                            for p in lx:
                                work1 = work_strategy1(i, o, j, k, l, m, n)
                                work2 = work_strategy2(p*n, i, o, j, k, l, m, n) 
                                work3 = work_strategy3(i, o, j, k, l, m, n)
                                work4 = work_strategy4(o, j, k, l, m, n, i)     
                                
                                count = count + 1
                                
                                #Stacking results into matrices
                                newrow1 = np.array([i/m,work1]) 
                                mat1 = np.vstack((mat1,newrow1))
                                newrow2 = np.array([i/m, work2])
                                mat2 = np.vstack((mat2,newrow2))
                                newrow3 = np.array([i/m,work3])
                                mat3 = np.vstack((mat3,newrow3))
                                newrow4 = np.array([i/m, work4])
                                mat4= np.vstack((mat4,newrow4))
                                
                                newrow  = np.array([count,i,j,k,l,m,n,o,p])
                                mat_pars = np.vstack((mat_pars,newrow))
                         
                                #Calculating time to reach shore for each strategy
                                work1_time = i/j
                                work2_time = (p*n + i)/j
                                work3_time = (ma.sqrt(2)*i)/j
                                work4_time = ((2*o)+m)/j                         
                                    
                                #Stacking Power Resutls
                                newrow1 = np.array([i/m,work1/work1_time])
                                mat1_power = np.vstack((mat1_power,newrow1))
                                newrow2 = np.array([i/m,work2/work2_time])
                                mat2_power = np.vstack((mat2_power,newrow2))
                                newrow3 = np.array([i/m,work3/work3_time])
                                mat3_power = np.vstack((mat3_power,newrow3))
                                newrow4 = np.array([i/m,work4/work4_time])
                                mat4_power = np.vstack((mat4_power,newrow4))

#Finally, output work files are computed (work NOT in Joules - see notes).                               
outfile = open('work1.dat','w')
for row in mat1:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('work2.dat','w')
for row in mat2:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('work3.dat','w')
for row in mat3:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('work4.dat','w')
for row in mat4:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close() 

#output power files (power not in W - see notes)                               
outfile = open('power1.dat','w')
for row in mat1_power:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('power2.dat','w')
for row in mat2_power:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('power3.dat','w')
for row in mat3_power:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close()

outfile = open('power4.dat','w')
for row in mat4_power:
    for column in row:
        outfile.write('%14.3f' % column)
    outfile.write('\n')
outfile.close() 
