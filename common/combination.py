import math

def _nCr(n,r):
    f = math.factorial
    return f(n)/(f(r)*f(n-r))

combination = []
for i in range(0,20):
    combination.append([])
    for j in range(0,i+1):
        combination[i].append(_nCr(i,j))

#Don't use this function for n > 20
def nCr(n,r):
    return combination[n][r]

