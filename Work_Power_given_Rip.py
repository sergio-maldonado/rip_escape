# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18:46:24 2020

@author: Archie Withers & Sergio Maldonado
"""

"""
This script allows the user to calculate the work (& power) required to escape 
any given rip current via each of the four strategies considered: 1. Swim 
directly back to shore  2. Swim Parallel 3. Swim at 45 degrees 4. Float. The 
user must only input values for the variables defined below and run the code. 
The code will return the value for the ratio W1/Wi (&P1/Pi), which illustrates 
the performance of each strategy relative to a reference (worst) case strategy. 
"""
import math as ma
import numpy as np

#l  - Swimmer starting distance from shore [m]
#lr - Rip channel length [m]
#lx - Distance swum parallel to shore in strategy 2 [m]
#Ve - Swimmer's escape speed [m/s]
#Vr - Rip current channel velocity [m/s]
#Vf - Feeder channel velocity [m/s]
#wf - Feeder channel width [m]
#wr - Rip channel width [m]

# Input variables:
l = 115
lr = 55 
lx = 60 
Ve = 0.25 
Vr = 1.0 
Vf = 1.5 
wf = 60
wr = 50

#Firstly, functions are defined to calculate the work required for each strategy

#Strategy 1 - Swimming directly back to shore against the rip
def work_strategy1(l, Ve, Vr, Vf, wf, wr, lr):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via strategy 1
    """
    W1 = ((Ve+Vr)**3)*((l-wf)/Ve)                                              # Calculates work for section swimming in rip channel
    W2 = ((Ve+Vf)**3)*(wf/Ve)                                                  # Calculates work for section swimming in feeder channel
    if l < wf or l > lr + wf:                                                  #Limits Starting distance offshore to be further than the feeder width
        return -1
    else:                                   
        return W1 + W2                                                         # Returns total value of work done for Strategy 1

#Strategy 2 - Swimming parallel to the rip for a distance lx to escape from rip
# channel beofre turning 90 degrees to swim directly back to shore
def work_strategy2(lx, l, Ve, Vr, Vf, wf, wr, lr):
    """
    a function that returns the work done by a swimmer if they choose to escape
    from a rip current via strategy 2
    """
    W1 = ((Ve**2 + Vr**2)**1.5)*(wr/(2*Ve))                                    # Calculates work for section swimming within rip channel
    W2 = ((Ve**2)*(lx-(wr/2)))                                                 # Calculates work for section outside rip current swimming parallel to shore
    W3 = ((Ve**2)*(l-wf))                                                      # Calculates work for section outside rip current but swimming directly back to shore
    W4 = ((Ve**2 + Vf**2)**1.5)*(wf/Ve)                                        # Calculates work done for section in feeder channel swimming directly back to shore
    if l < wf or l > lr + wf:                                                  #Limits Starting distance offshore to be further than the feeder width
        return 10
    else:            
        return W1+W2+W3+W4                                                     # Returns total value of work done for Strategy 2


#Strategy 3 - Swimming at 45 degrees to the rip back to shore 
def work_strategy3(l, Ve, Vr, Vf, wf, wr, lr):
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
    if l < wf + 0.5*wr or l > lr + wf:                                         #Relation to ensure swimmer passes through all three sections in the model
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
    if l < wf:
        return 10
    else:
        return W4                                                              # Returns total value of work done for Strategy 4


# Etimate and display the work for each strategy
work1 = work_strategy1(l, Ve, Vr, Vf, wf, wr, lr)
work2 = work_strategy2(lx, l, Ve, Vr, Vf, wf, wr, lr)
work3 = work_strategy3(l, Ve, Vr, Vf, wf, wr, lr)
work4 = work_strategy4(lr, Ve, Vr, Vf, wf, wr, l)

np.disp('Ratio of W1 to W2 is:')
np.disp(work1/work2)
np.disp('Ratio of W1 to W3 is:')
np.disp(work1/work3)
np.disp('Ratio of W1 to W4 is:')
np.disp(work1/work4)
np.disp(' ')

# Estimate and display the power for each strategy
work1_time = l/Ve
work2_time = (lx + l)/Ve
work3_time = (ma.sqrt(2)*l)/Ve
work4_time = ((2*lr)+wf)/Ve 

power1 = work1/work1_time
power2 = work2/work2_time
power3 = work3/work3_time
power4 = work4/work4_time

np.disp('Ratio of P1 to P2 is:')
np.disp(power1/power2)
np.disp('Ratio of P1 to P3 is:')
np.disp(power1/power3)
np.disp('Ratio of P1 to P4 is:')
np.disp(power1/power4)
