import math, os
import tkinter as tk
import tkinter.filedialog

from PIL import Image,ImageTk,ImageGrab

def create_view(file_path):
    #オリジナル画像の比率生成
    global origin_img, preview_img
    origin_img = Image.open(file_path)
    img_w = origin_img.width
    img_h = origin_img.height
    gcd = math.gcd(img_w,img_h)
    img_sr_w,img_sr_h = img_w//gcd,img_h//gcd

    #表示版のサイズ合わせ
    if desk_sr_w*img_sr_h >= desk_sr_h*img_sr_w:   #縦幅のほうが長い場合
        #モニターの横幅に画像を合わせる
        height = math.ceil(origin_img.height*desk_w//origin_img.width)
        preview_img = origin_img.resize((preview_canvas.winfo_width(),height))
    else:
        #モニターの縦幅に合わせる
        width = math.ceil(origin_img.width*desk_h//origin_img.height)
        preview_img = origin_img.resize((width,preview_canvas.winfo_height()))
        
    preview_img = ImageTk.PhotoImage(preview_img)
    preview_canvas.create_image(preview_canvas.winfo_width()//2, preview_canvas.winfo_height()//2, image=preview_img, tag='preview_img_tag', anchor=tk.CENTER)
    preview_canvas.bind("<Button-1>", click_in)
    preview_canvas.bind("<Button1-Motion>", click_hold)
    preview_canvas.bind("<ButtonRelease-1>", click_out)

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

def select_file():
    global file_path, folder_path
    dir = os.path.expanduser('~/Desktop')
    filetype = [("すべて", "*"), ("PNG", "*.png"), ("JPG", "*.jpg"), ("JPEG","*.jpeg")]
    file_path = tkinter.filedialog.askopenfilename(filetypes=filetype, initialdir=dir)
    folder_path = os.path.dirname(file_path)
    return file_path

def file_open():
    try:  
        file_path = select_file()
        create_view(file_path)
        preview_canvas.itemconfigure('select_btn', state=tk.HIDDEN)
    except:
        pass

def file_close():
    try:
        preview_canvas.delete("preview_img_tag")
        preview_canvas.itemconfigure('select_btn',state=tk.NORMAL)
        preview_canvas.unbind("<Button-1>", click_in)
        preview_canvas.unbind("<Button1-Motion>", click_hold)
        preview_canvas.unbind("<ButtonRelease-1>", click_out)
    except:
        pass

def preview_img_save():
    try:
        root.attributes("-alpha", 1.0)
        bbox = []
        for i in preview_canvas.bbox('preview_img_tag'):
            bbox.append(i)
        if bbox[0] <= 0:
            bbox[0] = abs(bbox[0])
        if bbox[1] <= 1:
            bbox[1] = abs(bbox[1])
        if bbox[2] >= desk_w:
            bbox[2] = bbox[0] + desk_w
        if bbox[3] >= desk_h:
            bbox[3] = bbox[1] + desk_h
        clip_img = preview_img.crop()
        print(folder_path + "/" + (len(folder_path) + 1) + ".png")
        # clip_img.save(folder_path + "/" + (len(folder_path) + 1) + ".png")
    except:
        pass

def close_root(event):
    root.destroy()

def press_keys(event):
    if event.keysym == "Escape":
        root.quit()     #quit()はmainloop終了後もリソースを保持する。
                        #destroy()はmainloop終了時にリソースを破棄する。
    elif event.keysym == "w" and event.state == 4:  # 4はCtrlキーのステート値
        file_close()
    elif event.keysym == "s" and event.state == 4:
        preview_img_save()

root = tk.Tk()                          #ウィンドウ生成
root.title("desktoping")                #ウィンドウ名
root.attributes('-fullscreen', True)    #ウィンドウの全画面化
root.attributes("-alpha", 0.8)          #ウィンドウの半透明化
root.bind('<Escape>', close_root)        #ウィンドウの終了条件
root.bind("<KeyPress>", press_keys)

#モニターの画面比率生成（システム設定でモニター番号1になっているモニター
desk_w = root.winfo_screenwidth()
desk_h = root.winfo_screenheight()
#比率出さなくてもピクセル数自体を比較に使ってもいいのでは？要検討
gcd = math.gcd(desk_w,desk_h)
desk_sr_w,desk_sr_h = desk_w//gcd,desk_h//gcd

preview_canvas = tk.Canvas(root, bg="white", highlightthickness = 0)
btn_file_open = tk.Button(preview_canvas, text='ファイルを選択する', command=file_open)
preview_canvas.create_window(desk_w//2, desk_h//2, anchor=tk.CENTER, tags='select_btn', window=btn_file_open)
preview_canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()     # ウィンドウの描画