import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt


def gauss_elimination(n, a):

    a = np.array(a, dtype='float32')

    # Applying Gauss Elimination
    # loop over each row
    for i in range(n):
        # make sure your first pivot is not equal to Zero
        if a[i][i] == 0:
            print('Divide by zero detected!')
            return

        # for each column under the pivot (starting from i+1 to move in a triangle shape)
        for j in range(i+1, n):
            ratio = a[j][i] / a[i][i]

            # apply the change to every element in the row
            for k in range(n+1):
                a[j][k] = a[j][k] - ratio * a[i][k]

    x = np.zeros(n)
    # Back Substitution for last element in X
    x[n-1] = a[n-1][n] / a[n-1][n-1]

    # get the other X elements in a reversing order
    for i in range(n-2, -1, -1):
        # get the last solved x
        x[i] = a[i][n]

        # apply the equation to get relation between found X's
        for j in range(i+1, n):
            x[i] = x[i] - (a[i][j]) * x[j]

        # Back Substitution for current X
        x[i] = x[i] / a[i][i]

    # for i in range(n):
    #     print(f'X{i}: {x[i]}', end='      ')
    # print()
    return x


def gauss_seidel(n, a, e=0.00001, itr = 50,x_0=False):
    # (assuming diagonally dominant)
    # Defining equations to be solved
    a = np.array(a, dtype='float32')

    # Creating a dict to hold each variable equation
    f = dict()
    x = [sp.Symbol(f"a{i}") for i in range(n)]

    # find the equation for each variable
    for i in range(n):
        fx = a[i][n]

        # check if the diagonals are zeros
        if a[i][i] == 0:
            print("error")
            return
        for j in range(n):
            # skip current variable since we are trying to find its equation
            if j == i:
                continue
            fx += -1 * (a[i][j]) * x[j]
        fx /= a[i][i]
        f[x[i]] = fx

    # for v in f.values():
    #     print(v)

    # Initial setup
    # if initial points were given
    if np.array(x_0).any():
        print("exist")
        x_0 = np.array(x_0).reshape(n)
    # otherwise initialize with zeros
    else:
        print("zeros")
        x_0 = np.zeros(n)

    x_1 = np.zeros(n)

    # to get number of iterations
    counter = 1

    # to hold the previous values for plotting
    x_i = [x_0]

    # Implementation of Gauss Seidel Iteration
    while True:
        # solving for each variable
        for k, v in enumerate(f.values()):
            current_x = v
            for i, xi in enumerate(x):
                current_x = current_x.subs(xi, x_1[i])
            x_1[k] = current_x

        # finding relative error
        e_t = np.absolute((x_0 - x_1)/x_1)
        # e_t = np.absolute((x_0 - x_1))

        # saving previous points
        x_0 = x_1.copy()
        x_i.append(x_0)

        # check convergence
        test = np.where(e_t > e, True, False)
        print(test)

        if not np.any(test):
            break

        if counter >= itr:
            print(f"max iterations reached {itr}")
            break
			
        counter += 1

    return counter, x_1, x_i

def plot_gs(counter, x_i, n):
    # PLOT
    # create the x-axis values (iterations)
    x_axis = np.array([i for i in range(counter+1)])
    plt.figure(figsize=(10, 5))
    # for each root 
    for i in range(n):
        # create the y-axis values for each root (values)
        y_axis = np.array([y[i] for y in x_i])
        # plot current root
        plt.plot(x_axis, y_axis, label=f"X{i+1}")
    plt.xlabel(f"Iterations ({counter})")
    plt.ylabel("Values")
    plt.legend()
    plt.show()

def save_gs(counter, x_i, n):
    print()
    print()
    print("Gauss Seidel Iteration Table")
    iterator = np.array([i for i in range(counter+1)])
    data_df = pd.DataFrame(iterator, columns=["i"])
    # add each root value to its own column
    for i in range(n):
        current_x = np.array([x[i] for x in x_i])
        data_df[f"x{i}"] = current_x
    print(data_df)
    # save the df to .txt file
    data_df.to_csv(r'gs_output.txt', index=None, sep=' ')

def save_method(x, t, n, m):
    print()
    print()
    if len(m) == 1:
        x = [x]

    # create a dataframe with the roots
    data_df = pd.DataFrame(x)

    # rename the columns to better represent its values
    data_df.columns = ["x" + str(i) for i in range(n)]

    # adding the method name
    data_df["method"] = m
    # adding the method execution time in millisec
    data_df["time(ms)"] = t
    
    # rearrange cols
    cols = data_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    data_df = data_df[cols]
    print(data_df)
    # save the df to .txt file
    data_df.to_csv(r'output.txt', index=None, sep=' ')

# #implementing Gauss Jordan
def gauss_jordan(a):
    '''
    A: The Transformation Matrix
    b: The Constant Vector
    '''
    a = np.array(a, dtype='float32')
    n = a.shape[0]
    b = a[:,n]

    #Main loop
    for k in range(n):
        
        if a[k][k] == 0:
            print('Divide by zero detected!')
            return "DivByZero"

        #Partial Pivoting
        if np.fabs(a[k,k]) < 1.0e-12: #Exchange Pivot
            for i in range(k+1, n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]) :
                    for j in range(k,n):
                        a[i, j], a[k, j] = a[k, j], a[i, j]
                    b[i], b[k] = b[k], b[i]
                    break
        
        #Pivot Row Div
        pivot = a[k,k]
        for j in range(k,n):
            a[k,j] /= pivot
        b[k]  /= pivot

        #Elimination
        for i in range(n):
            if i==k or a[i, k] == 0:
                continue
            multiplier = a[i,k]
            for j in range(k,n):
                a[i,j] -= multiplier * a[k,j]
            b[i] -= multiplier * b[k]
    
    #b will be x in the final case
    return b

#Doolittle
def lu_decomposition(A):
    n = len(A)

    A = np.array(A)
    b = A[:,n]
    A = A[:,:n]

    L = [[0 for x in range(n)] for y in range(n)] #Lower triangular matrix
    U = [[0 for x in range(n)] for y in range(n)] #Upper triangular matrix

    for i in range(n): #loop on rows
        if A[i][i] == 0:
            print('Divide by zero detected!')
            return "DivbyZero"

        #Construct Upper matrix
        for k in range(i, n): #loop on cols
            sum = 0
            for j in range(i):
                sum += (L[i][j] * U[j][k])

            U[i][k] = round(A[i][k] - sum, 3)

        #Construct Lower matrix
        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                sum = 0
                for j in range(i):
                    sum += (L[k][j] * U[j][i])
 
                L[k][i] = round((A[k][i] - sum) / U[i][i], 3)
        
        
    '''Solving the system'''
    L = np.array(L,dtype='float32')
    U = np.array(U,dtype='float32')
    b = np.array(b,dtype='float32')

    #Forward sub
    y = np.zeros(n)
    for i in range(n):
        tmp = b[i]
        for j in range(i):
            tmp -= L[i,j] * y[j]
        y[i] = tmp / L[i,i]
        
    #Backsub
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        tmp = y[i]
        for j in range(i+1, n):
            tmp -= U[i,j] * x[j]
        x[i] = tmp / U[i,i]    

    return x


if __name__ == "__main__":

    n = 3

    a1 = [
        [1, 1, 1, 9],
        [2, -3, 4, 13],
        [3, 4, 5, 40]
    ]

    a2 = [
        [20, 1, -2, -17],
        [3, 20, -1, 18],
        [2, -3, 20, -25]
    ]

    a3 = [
        [10, 2, -1, 27],
        [-3, 6, 2, -61.5],
        [1, 1, 5, -21.5]
    ]

    print(gauss_seidel(n, a3, e=0.055))
    # print(gauss_elimination(n, a3))

    # a4 = [
    #     [2, 1, -1, 2, 5],
    #     [4, 5, -3, 6, 9],
    #     [-2, 5, -2, 6, 4],
    #     [4, 11, -4, 8, 2]
    # ]

    # print("Guass Elim",gauss_elimination(4,a4))
    # print("Gauss Seidel",gauss_seidel(4, a4, e=0.0001))
    # print("Gauss Jordan",gauss_jordan(a4))
    # print("LU",lu_decomposition(a4))


    # a5 = np.array([[4, 2, 1, 11],[-1, 2, 0, 3],[2, 1, 4, 16]])
    # print("Guass Elim",gauss_elimination(3,a5))
    # print("Gauss Seidel",gauss_seidel(3, a5, e=0.0001))
    # print("Gauss Jordan",gauss_jordan(a5))
    # print("LU",lu_decomposition(a5))