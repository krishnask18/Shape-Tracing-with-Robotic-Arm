from sympy import *
import math as mt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np

cvt = 180/mt.pi

x = int(input('Enter x coordinate : '))
y = int(input('Enter y coordinate : '))
orientation = int(input('Enter angle of orientation in degrees:'))/cvt
l1 = int(input('Enter lengths of link 1 :'))
l2 = int(input('Enter lengths of link 2 :'))
l3 = int(input('Enter lengths of link 3 :'))

#init guess
x0 = Matrix([[mt.pi/3], [mt.pi/3], [mt.pi/3]])

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')

print('f1 = l1*cos(a) + l2*cos(a + b) + l3*cos(a+b+c) - x = 0\nf2 = l1*sin(a) + l2*sin(a + b) + l3*sin(a+b+c) - y = 0\nf3 = a + b + c - orientation = 0')

f = Matrix([[l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x], [l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y], [a + b + c - orientation]])
func_value = f.subs({a : x0[0], b : x0[1], c : x0[2]})

Jacobian = Matrix([ [diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, a), diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, b), diff(l1*cos(a) + l2*cos(a + b) + l3*cos(a + b + c) - x, c)], 
                    [diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, a), diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, b), diff(l1*sin(a) + l2*sin(a + b) + l3*sin(a + b + c) - y, c)],
                    [diff(a + b + c - orientation, a), diff(a + b + c - orientation, b), diff(a + b + c - orientation, c)]])

print('Function value : \n')
pretty_print(func_value)
print("Jacobian :\n")
pretty_print(Jacobian)

inv_jacobian = (Jacobian)**(-1)

for i in range(10):
    
    x1 = x0 - (inv_jacobian.subs({a:x0[0], b:x0[1], c:x0[2]}))*(f.subs({a:x0[0], b:x0[1], c:x0[2]}))
    x0 = x1
print('\nFinal values :\n')
pretty_print(x1*cvt)
print('\nerror :\n')
pretty_print(f.subs({a:x0[0], b:x0[1], c:x0[2]}))

fig = plt.figure()
axis = plt.axes(xlim =(-(l1+l2+l3), l1+l2+l3+2), 
                ylim =(-(l1+l2+l3), l1+l2+l3+2)) 
line, = axis.plot([], [], lw = 3) 
line1, = axis.plot([], [], lw = 3) 
line2, = axis.plot([], [], lw = 3) 
r = float(round(x1[0], 2))
r1 = float(round(x1[1], 2))
r2 = float(round(x1[2], 2))

rad=np.linspace(0,r,num =100)
rad1=np.linspace(0,r1,num =100)
rad2=np.linspace(0,r2,num =100)
   
def animate(i):
    t = l1*np.cos(rad[i-1])
    y = l1*np.sin(rad[i-1])
    t1 = l2*np.cos(rad1[i-1]+rad[i-1])
    y1 = l2*np.sin(rad1[i-1]+rad[i-1])
    t2 = l3*np.cos(rad2[i-1]+rad1[i-1]+rad[i-1])
    y2 = l3*np.sin(rad2[i-1]+rad1[i-1]+rad[i-1])

    line.set_data([0,t],[0,y])
    line1.set_data([t, t1+t], [y, y1+y])
    line2.set_data([t+t1, t2+t1+t], [y+y1, y2+y1+y])
      
    return line, line1, line2,
   
anim = FuncAnimation(fig, animate, frames = len(rad), interval = 10, blit = False)
plt.show()
writer = animation.PillowWriter(fps = 60)
anim.save('im.gif', writer=writer)