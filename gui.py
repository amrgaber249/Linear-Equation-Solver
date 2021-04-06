import tkinter as tk
from num_analysis import *
from Parsing_Equations import *
import time

root = tk.Tk()
root.geometry("400x500")
root.resizable(0,0)
root.title("Linear Equation Solver")

def file_opener():
    from tkinter import filedialog
    input = filedialog.askopenfile(initialdir="../")
    print(type(input))
    n = int(input.readline())
    num.delete(0,tk.END)
    num.insert(0,n)
    method = input.readline().strip()
    variable.set(method)
    A = ""
    for _ in range(n):
        A += input.readline()
    equations.delete('1.0','end')
    equations.insert('1.0',A)

    if method in ['Gauss Seidel', 'All']:
        gs_param.config(state=tk.NORMAL)
        precision.config(state=tk.NORMAL)
        max_iter.config(state=tk.NORMAL)
        points_list = input.readline()
        gs_param.delete(0,tk.END)
        gs_param.insert(0, points_list)      

equ_btn = tk.Button(root,text="Browse File",command = file_opener)
equ_btn.pack(pady=10)


num_label = tk.Label(root, text="Enter the # of equations")
num_label.pack(anchor = tk.CENTER)
num = tk.Entry(root, width=30, borderwidth=5)
num.pack(anchor = tk.CENTER)

equ_label = tk.Label(root, text="Enter the equations")
equ_label.pack(anchor = tk.CENTER)

equations = tk.Text(root,width=30, height=5, yscrollcommand = True)
equations.pack(anchor = tk.CENTER)

variable = tk.StringVar(root)
variable.set("Gauss Elimination") # default value


def optupdate(value):
    if value in ["Gauss Seidel","All"]:
        gs_param.config(state=tk.NORMAL)
        precision.config(state=tk.NORMAL)
        max_iter.config(state=tk.NORMAL)
    else:
        gs_param.config(state = tk.DISABLED)
        precision.config(state=tk.DISABLED)
        max_iter.config(state=tk.DISABLED)
    return


w = tk.OptionMenu(root, variable, " Gauss Elimination", "LU decomposition",\
     "Gauss Jordan","Gauss Seidel","All", command = optupdate)
w.pack(anchor = tk.CENTER,pady=10)

gs_lb = tk.Label(root, text="Enter Parameters | Space Separated")
gs_lb.pack(anchor = tk.CENTER)

gs_param = tk.Entry(root,width=15, borderwidth=5)
gs_param.pack(anchor = tk.CENTER)
gs_param.config(state = tk.DISABLED)

prec_label = tk.Label(root, text="Precision | Default is Ɛes = 0.00001")
prec_label.pack(anchor = tk.CENTER)
precision = tk.Entry(root, width=15, borderwidth=5)
precision.pack(anchor = tk.CENTER)
precision.config(state = tk.DISABLED)

maxiter_label = tk.Label(root, text="Max Iterations | Default is 50")
maxiter_label.pack(anchor = tk.CENTER)
max_iter = tk.Entry(root, width=15, borderwidth=5)
max_iter.pack(anchor = tk.CENTER,pady=5)
max_iter.config(state = tk.DISABLED)



def solve_sys():
    print()
    print()
    flag = 0
    try:
        n = int(num.get()) #Number of equations
        equs = equations.get('1.0','end')

        A = read_from_field(equs, n) #Augmented Matrix
        flag = 1

        method = variable.get() #Algorithm

        # check if a value is given, otherwise set default value
        if precision.get():
            gs_prec = float(precision.get())
        else:
            gs_prec = 0.00001

        # check if a value is given, otherwise set default value
        if max_iter.get():
            gs_maxIter = float(max_iter.get())
        else:
            gs_maxIter = 50
        
        # check if a value is given, otherwise set default value
        if gs_param.get():
            InitialPointList = list(map(float,gs_param.get().split()))
        else:
            InitialPointList = False

        start = time.time()
        end = []
        if method == "Gauss Elimination":
            x = gauss_elimination(n, A)
        elif method == "Gauss Jordan":
            x = gauss_jordan(A)
        elif method == "LU decomposition":
            x = lu_decomposition(A)
        elif method == "Gauss Seidel":
            counter, x, x_i = gauss_seidel(n, A, gs_prec, gs_maxIter, InitialPointList)
        else:
            # x = [gauss_elimination(n, A),gauss_jordan(A),lu_decomposition(A)]
            x1 = gauss_elimination(n, A)
            end.append((time.time()-start)*1000)

            x2 = gauss_jordan(A)
            end.append((time.time()-start)*1000)

            x3 = lu_decomposition(A)
            end.append((time.time()-start)*1000)

            counter, x_gs, x_i = gauss_seidel(n, A, gs_prec, gs_maxIter, InitialPointList)
            end.append((time.time()-start)*1000)

            x = [x1, x2, x3, x_gs]

        res_lb.config(text = f"Values : {x}")
        end.append((time.time()-start)*1000)
        exec_lb.config(text = f"Execution time: {end[0]} ms")
        print(method)
        print(x)
        # if you called all methods
        if len(end) > 1:
            end = end[:-1]
            print("Execution Times !!!")
            print(f"Gauss Elimination: {end[0]} ms")
            print(f"Gauss Jordan: {end[1]} ms")
            print(f"LU decomposition: {end[2]} ms")
            print(f"Gauss Seidel: {end[3]} ms")
            # all_times = ""
            # for i in range(4):
            #     all_times += str(end[i]) + ","
            # exec_lb.config(text = f"Execution time: {all_times} ms")
        # if you only called 1 method
        else:
            print(f"Execution time : {end[0]} ms")

        m = [method]
        if method == "All":
            m = ["Gauss Elimination", "Gauss Jordan", "LU decomposition", "Gauss Seidel"]

        save_method(x, end, n, m)

        if method in ["Gauss Seidel", "All"]:
            save_gs(counter, x_i, n)
            plot_gs(counter, x_i, n)
        
    
        
    except Exception as e:
        print(e)
        if flag == 0:
            print("There is a problem in your inputs (no solution)")
        else:
            print("make sure to enter all fields !!!")
    
  
solve_btn = tk.Button(root, text="Solve", width=10, bg='green', fg='white', command = solve_sys)
solve_btn.pack(pady=10)

res_lb = tk.Label(root,text="No Values yet")
res_lb.pack()

exec_lb = tk.Label(root,text="0 ms")
exec_lb.pack()

root.mainloop()