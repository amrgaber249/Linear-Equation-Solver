import numpy as np
import sympy as sp
from sympy import Eq, Matrix, poly
from sympy.abc import a, b, c
import sys


def read_from_file(filename):

    coefficientList=[]
    EquationLines=[]
    InitialPointList=[]


    f=open(filename,"r")
    MatrixSize=f.readline()
    Method=f.readline()

    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    for x in range(int(MatrixSize)):
        
        flags=[]
        for i in range(26):
            flags.append(0)

        EquationLines.append(f.readline())
        #print(EquationLines[x])

        for k in range(26):
            if (alphabet[k] in EquationLines[x])==0:
                flags[k]=1

        i=poly(EquationLines[x])
        Temp=i.coeffs()
            
        for j in range(26):
            if flags[j]:
                Temp.insert(j,0)
        if (len(Temp)<(26)):
            Temp.append(0)
        coefficientList.append(Temp)
    InitialPointList=f.readline()
    f.close()

    indicestopop=[]
    for u in range(27):
        zeroflags=[]
        for x in range(int(MatrixSize)):
            zeroflags.append(0)
        for y in range(int(MatrixSize)):
            if coefficientList[y][u]==0:
                zeroflags[y]=1
            else: break
        zeroflags.insert(0,1)
        if all(elem == zeroflags[0] for elem in zeroflags):
            indicestopop.append(u)


    newCoefficentList=[[] for i in range(int(MatrixSize))]

    for i in range(int(MatrixSize)):
        for x in range(27):
            if (x in indicestopop)==0:
                newCoefficentList[i].append(coefficientList[i][x])

    MatrixSize = int(MatrixSize)
    print(MatrixSize)
    print(Method)

    square_mat = []
    for j in newCoefficentList:    
        square_mat.append(j)
    print(square_mat)

    InitialPointList = list(map(float,InitialPointList.split()))
    print(InitialPointList)

    if len(InitialPointList) != MatrixSize:
        print(f'{MatrixSize - len(InitialPointList)} points mismatching size')
        sys.exit("Error")


    return MatrixSize, Method, square_mat, InitialPointList



def read_from_field(s, n):
    coefficientList=[]
    s = s.split("\n")


    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    for x in range(n):
        
        flags=[]
        for i in range(26):
            flags.append(0)

        #print(EquationLines[x])

        for k in range(26):
            if (alphabet[k] in s[x])==0:
                flags[k]=1

        i=poly(s[x])
        Temp=i.coeffs()
            
        for j in range(26):
            if flags[j]:
                Temp.insert(j,0)
        if (len(Temp)<(26)):
            Temp.append(0)
        coefficientList.append(Temp)

    indicestopop=[]
    for u in range(27):
        zeroflags=[]
        for x in range(n):
            zeroflags.append(0)
        for y in range(n):
            if coefficientList[y][u]==0:
                zeroflags[y]=1
            else: break
        zeroflags.insert(0,1)
        if all(elem == zeroflags[0] for elem in zeroflags):
            indicestopop.append(u)


    newCoefficentList=[[] for i in range(n)]

    for i in range(n):
        for x in range(27):
            if (x in indicestopop)==0:
                newCoefficentList[i].append(coefficientList[i][x])


    square_mat = []
    for j in newCoefficentList:    
        square_mat.append(j)


    return square_mat

