import tkinter as tk
from Parsing_Equations import read_from_file
root = tk.Tk()
root.geometry("400x400")
root.resizable(0,0)
root.title("Linear Equation Solver")

def file_opener():
    from tkinter import filedialog
    input = filedialog.askopenfile(initialdir="../")
    print(type(input))
    n = int(input.readline())
    method = input.readline()
    A = ""
    for _ in range(n):
        A += input.readline()

    # n, method, A, params = read_from_file(input)
    
equ_btn = tk.Button(root,text="Browse File",command = file_opener)
equ_btn.pack(pady=10)


root.mainloop()