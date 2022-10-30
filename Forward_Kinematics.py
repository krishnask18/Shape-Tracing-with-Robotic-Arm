from sympy import *
from math import *
from pandas import *
print('Equation from DH parameters')
n = int(input('Enter number of joints : '))
a = [0]*n
alph = [0]*n
theta = [0]*n
d = [0]*n
for i in range(1, n+1):
    a[i-1] = float(input('Enter link {} length : '.format(i)))
    alph[i-1] = float(input('Enter link {} twist angle : '.format(i) ))
    theta[i-1] =  Symbol(input('Enter joint {} angle variable : '.format(i)))
    d[i-1] = float(input('Enter joint {} offset : '.format(i)))

mt = [0]*n
ctheta = [0]*n
stheta = [0]*n
calph = [0]*n
salph = [0]*n
finmat = eye(4)
for i in range(1, n+1):
    ctheta[i-1] = Symbol('cos({})'.format(theta[i-1]))
    stheta[i-1] = Symbol('sin({})'.format(theta[i-1]))
    calph[i-1] = cos(alph[i-1])
    salph[i-1] = sin(alph[i-1])
    mt[i-1] = Matrix([[ctheta[i-1], -stheta[i-1], 0, a[i-1]], 
    [stheta[i-1]*calph[i-1], calph[i-1]*ctheta[i-1], -salph[i-1], -d[i-1]*salph[i-1]],
    [salph[i-1]*stheta[i-1], salph[i-1]*ctheta[i-1], calph[i-1], d[i-1]*calph[i-1]],
    [0, 0, 0, 1]])
    finmat = finmat*mt[i-1]
pretty_print(finmat)
finmat = finmat.tolist()
print('\n\n Final Equations :')
print('x = ', finmat[0][3] - 10)
print('y = ', finmat[1][3])
print('z = ', finmat[2][3])