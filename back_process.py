import os, tkinter, tkinter.filedialog

def select_file():
    idir = os.path.expanduser('~/Desktop')
    filetype = [("PNG","*.png"), ("JPG","*.jpg"), ("すべて","*")]
    file_path = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
    return file_path
    