import tkinter, tkinter.filedialog
import math,os

root = tkinter.Tk()
root.title("desktoping")  #title
root.geometry("1536x864")    #window size


#画像の表示
from PIL import Image,ImageTk
def create_view(file_path):
    global preview_img
    origin_img = Image.open(file_path)
    if origin_img.width/16 >= origin_img.height/9:
        width = math.ceil(origin_img.width*720/origin_img.height)
        hd_img = origin_img.resize((width,720))
    else:
        height = math.ceil(origin_img.height*1280/origin_img.width)
        hd_img = origin_img.resize((1280,height))
    preview_img = ImageTk.PhotoImage(hd_img)
    preview_canvas.create_image(642, 362, image=preview_img, tag='preview_img_tag', anchor=tkinter.CENTER)
    return preview_img

def select_file():
    idir = os.path.expanduser('~/Desktop')
    filetype = [("PNG","*.png"), ("JPG","*.jpg"), ("すべて","*")]
    file_path = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
    return file_path

#画像の移動
def view_move(dir):
    print(preview_canvas.bbox("preview_img_tag"))
    if dir == 'up':
        preview_canvas.move("preview_img_tag", 0, 8)
    elif dir == 'down':
        preview_canvas.move("preview_img_tag", 0, -8)
    elif dir == 'left':
        preview_canvas.move("preview_img_tag", 8, 0)
    elif dir == 'right':
        preview_canvas.move("preview_img_tag", -8, 0)
    print(preview_canvas.bbox("preview_img_tag"))

def file_open():
    create_view(select_file())
def file_close():
    try:
        preview_canvas.delete("preview_img_tag")
    except:
        preview_canvas.create_text(640,360,text="現在ファイルは指定されていません。",anchor='center')


# menubarの大元（コンテナ）の作成と設置
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
#メニューに親メニュー（ファイル）を作成する 
menu_file = tkinter.Menu(menu_bar,tearoff=False) 
menu_bar.add_cascade(label='ファイル', menu=menu_file) 
menu_file.add_command(label='ファイルを開く', command=file_open)
menu_file.add_command(label='閉じる', command=file_close)
    
# btn_file_open = tkinter.Button(root, text='ファイルを選択する', command=file_open)
# btn_file_open.place(x=1300, y=25)


preview_canvas = tkinter.Canvas(root, bg="white", height=720, width=1280)
preview_canvas.place(x=50, y=50)
preview_canvas.pack()


btn_img_up = tkinter.Button(root, text='↑', command=lambda:view_move('up'))
preview_canvas.create_window(512,2, anchor='nw',window=btn_img_up,width=256)
btn_img_down = tkinter.Button(root, text='↓', command=lambda:view_move('down'))
preview_canvas.create_window(512,720, anchor='sw',window=btn_img_down,width=256)
btn_img_left = tkinter.Button(root, text='←', command=lambda:view_move('left'))
preview_canvas.create_window(2,288, anchor='nw',window=btn_img_left,height=144)
btn_img_right = tkinter.Button(root, text='→', command=lambda:view_move('right'))
preview_canvas.create_window(1282,288, anchor='ne',window=btn_img_right,height=144)
# ウィンドウの描画
root.mainloop()