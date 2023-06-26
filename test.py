import math
import tkinter as tk

root = tk.Tk()

y = root.winfo_screenheight()
x = root.winfo_screenwidth()

print(x,y)
i = math.gcd(x,y)

print(1920//i,1080//i)