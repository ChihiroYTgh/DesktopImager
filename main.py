import tkinter as tk, tkinter.filedialog
import math,os

#画像の表示
from PIL import Image,ImageTk
def create_view(file_path):
    global preview_img
    origin_img = Image.open(file_path)
    if origin_img.width//16 >= origin_img.height//9:
        width = math.ceil(origin_img.width*720//origin_img.height)
        hd_img = origin_img.resize((width,720))
    else:
        height = math.ceil(origin_img.height*1280//origin_img.width)
        hd_img = origin_img.resize((1280,height))
    preview_img = ImageTk.PhotoImage(hd_img)
    preview_canvas.create_image(642, 362, image=preview_img, tag='preview_img_tag', anchor=tk.CENTER)

def select_file():
    idir = os.path.expanduser('~/Desktop')
    filetype = [("PNG", "*.png"), ("JPG", "*.jpg"), ("すべて", "*")]
    file_path = tkinter.filedialog.askopenfilename(filetypes=filetype, initialdir=idir)
    folder_path = os.path.dirname(file_path)
    return file_path, folder_path

def folder_open(folder_path):
    global file_list
    file_list = os.listdir(folder_path)  # フォルダ内のファイル一覧を取得
    # for file_name in file_list:
    #     if file_name.lower().endswith((".png", ".jpg")):
    #         file_path = os.path.join(folder_path, file_name)
    #         # ここでファイルを開く処理を行う（例: create_view(file_path)など）
    #         # 開いたファイルの表示や処理方法はご自身のプログラムに合わせて実装してください

def file_open():
    file_path, folder_path = select_file()
    create_view(file_path)
    folder_open(folder_path)
    preview_canvas.itemconfigure('select_btn', state=tk.HIDDEN)

def file_close():
    try:
        preview_canvas.delete("preview_img_tag")
        preview_canvas.itemconfigure('select_btn',state=tk.NORMAL)
    except:
        pass

pvi_x = 0
pvi_y = 0

def click_in(event):
    global pvi_x, pvi_y
    pvi_x = event.x
    pvi_y = event.y

def click_hold(event):
    global pvi_x, pvi_y
    dx = event.x - pvi_x
    dy = event.y - pvi_y
    preview_canvas.move('preview_img_tag', dx, dy)
    pvi_x = event.x
    pvi_y = event.y

def click_out(event):
    xNW, yNW, xSE, ySE = preview_canvas.bbox('preview_img_tag')
    canvas_width = preview_canvas.winfo_width()
    canvas_height = preview_canvas.winfo_height()  

    if xNW < 0 and xSE < canvas_width:
       preview_canvas.move('preview_img_tag', canvas_width - xSE, 0)

    if yNW < 0 and ySE < canvas_height:
        preview_canvas.move('preview_img_tag', 0, canvas_height - ySE)

    if xSE > canvas_width and xNW > 0:
        preview_canvas.move('preview_img_tag', -xNW, 0)

    if ySE > canvas_height and yNW > 0:
        preview_canvas.move('preview_img_tag', 0, -yNW)



root = tk.Tk()
root.title("desktoping")  #title
root.geometry("1536x864")    #window size

# menubarの大元（コンテナ）の作成と設置
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
#メニューに親メニュー（ファイル）を作成する 
menu_file = tkinter.Menu(menu_bar,tearoff=False) 
menu_bar.add_cascade(label='ファイル', menu=menu_file) 
menu_file.add_command(label='ファイルを開く', command=file_open)
menu_file.add_command(label='閉じる', command=file_close)

preview_canvas = tk.Canvas(root, bg="white", height=720, width=1280)
btn_file_open = tk.Button(preview_canvas, text='ファイルを選択する', command=file_open)
preview_canvas.create_window(640, 360, anchor=tk.CENTER, tags='select_btn', window=btn_file_open)
preview_canvas.pack(anchor=tk.NW)

preview_canvas.bind("<Button-1>", click_in)
preview_canvas.bind("<Button1-Motion>", click_hold)
preview_canvas.bind("<ButtonRelease-1>", click_out)


# ウィンドウの描画
root.mainloop()