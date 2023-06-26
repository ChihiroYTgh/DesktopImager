import math
import tkinter as tk

from PIL import Image,ImageTk

root = tk.Tk()

def create_view(file_path):
    #モニターの画面比率生成（windowsの場合、多分モニター番号1のやつを取ってくる
    desk_w = root.winfo_screenwidth()
    desk_h = root.winfo_screenheight()
    #比率出さなくてもピクセル数自体を比較に使ってもいいのでは？要検討
    gcd = math.gcd(desk_w,desk_h)
    desk_sr_w,desk_sr_h = desk_w//gcd,desk_h//gcd

    #オリジナル画像の比率生成
    global origin_img, preview_img
    origin_img = Image.open(file_path)
    img_w = origin_img.width
    img_h = origin_img.height
    gcd = math.gcd(img_w,img_h)
    img_sr_w,img_sr_h = img_w//gcd,img_h//gcd

    #表示板のサイズ合わせ
    if desk_sr_w*img_sr_h >= desk_h*img_sr_w:
        #モニターの横幅に画像を合わせる
        pass
    else:
        #モニターの縦幅に合わせる
        pass
