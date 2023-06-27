import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk, ImageGrab

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
class WorkFile:
    def __init__(self) -> None:
        self.path = ""
        self.width = 0
        self.height = 0
        self.expantion = ""
    def select_file():
        pass
    def select_folder():
        pass
    def open_file():
        pass