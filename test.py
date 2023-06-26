import os
import tkinter as tk
from tkinter import filedialog

def remove_extension(filepath):
    filename, extension = os.path.splitext(filepath)
    return filename

# ファイル選択ダイアログを表示
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# 拡張子を取り除いたファイルパスを表示
if file_path:
    file_without_extension = remove_extension(file_path)
    print("拡張子を取り除いたファイルパス:", file_without_extension)
