from sympy import *
import math as mt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np

cvt = 180/mt.pi

print('from (x1, y1) to (x2, y2)')
x1 = float(input('Enter x1 : '))
y1 = float(input('Enter y1 : '))
x2 = float(input('Enter x2 : '))
y2 = float(input('Enter y2 : '))
orientation = int(input('Enter angle of orientation in degrees:'))/cvt
l1 = int(input('Enter lengths of link 1 :'))
l2 = int(input('Enter lengths of link 2 :'))
l3 = int(input('Enter lengths of link 3 :'))

#init guess
x0 = Matrix([[mt.pi/3], [mt.pi/3], [mt.pi/3]])

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')

x = x1
y = y1

theta_list = []

for i in range(100):
    f = Matrix([[l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x], [l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y], [a + b + c - orientation]])
    func_value = f.subs({a : x0[0], b : x0[1], c : x0[2]})

    Jacobian = Matrix([ [diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, a), diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, b), diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, c)], 
                        [diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, a), diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, b), diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, c)],
                        [diff(a + b + c - orientation, a), diff(a + b + c - orientation, b), diff(a + b + c - orientation, c)]])

    inv_jacobian = (Jacobian)**(-1)

    for i in range(10):
        
        sol = x0 - (inv_jacobian.subs({a:x0[0], b:x0[1], c:x0[2]}))*(f.subs({a:x0[0], b:x0[1], c:x0[2]}))
        x0 = sol
    theta_list.append(sol)
    x = x + (x2 - x1)/100
    y = y + (y2 - y1)/100
print(theta_list)



fig = plt.figure()
axis = plt.axes(xlim =(-3, l1+l2+l3+2), 
                ylim =(-3, l1+l2+l3+2)) 
sctx, scty = [], []
links,  = axis.plot([], [], lw = 3) 

def animate(i):
    cx1, cy1 = 0, 0
    cx2, cy2 = l1*cos(theta_list[i][0]), l1*sin(theta_list[i][0])
    cx3, cy3 = cx2 + l2*cos(theta_list[i][1] + theta_list[i][0]), cy2 + l2*sin(theta_list[i][1] + theta_list[i][0])
    cx4, cy4 = cx3 + l3*cos(theta_list[i][2] + theta_list[i][1] + theta_list[i][0]), cy3 + l3*sin(theta_list[i][2] + theta_list[i][1] + theta_list[i][0])

    links.set_data([cx1, cx2, cx3, cx4], [cy1, cy2, cy3, cy4])
    sctx.append(cx4)
    scty.append(cy4)
    plt.scatter(sctx, scty, lw = 0.1, color = '#F90038')
    return links

anim = animation.FuncAnimation(fig, animate,frames = len(theta_list), interval = 3)
plt.show()