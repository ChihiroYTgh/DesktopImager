import math
import os, subprocess, webbrowser, datetime
import tkinter as tk
import tkinter.filedialog as filedialog, tkinter.messagebox as messagebox
from PIL import Image, ImageTk, ImageGrab

class App_setting_btn(tk.Button):
    def __init__(self, master, text, command):
        super().__init__(master)
        self.configure(
            text = text,
            command = command,
            relief=tk.GROOVE,
            bd=3,
            font = ("BIZ UDPゴシック", 18),
            bg = "#1f2447",
            activebackground = "#1f2447",
            fg = "#f3f4f8",
            activeforeground = "#f3f4f8"
        )


class App_setting_check(tk.Checkbutton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            text = text,
            relief = tk.GROOVE,
            bd = 3,
            selectcolor = "#1f2447",
            variable = tk.BooleanVar(),
            font = ("BIZ UDPゴシック", 18),
            bg = "#1f2447",
            activebackground = "#1f2447",
            fg = "#f3f4f8",
            activeforeground = "#f3f4f8"
        )

class Desktop_imagerApp:
    def __init__(self):
        self.simple_mode = tk.Tk()
        self.simple_mode.title("Desktoping")
        self.simple_mode.attributes('-fullscreen', True, "-alpha", 0.8)
        self.simple_mode.bind('<KeyPress>', self.press_keys)
        
        self.desk_w = self.simple_mode.winfo_screenwidth()
        self.desk_h = self.simple_mode.winfo_screenheight()
        gcd = math.gcd(self.desk_w, self.desk_h)
        self.desk_sr_w, self.desk_sr_h = self.desk_w // gcd, self.desk_h // gcd
        
        self.preview_canvas = tk.Canvas(self.simple_mode, bg="#1f2447", highlightthickness=0)
        self.conse_var = tk.BooleanVar()
        self.btn_file_open = tk.Button(self.preview_canvas, text='ファイルを選択する', command=self.file_open,
                                       font=("BIZ UDPゴシック",18),
                                       bg="#f3f4f8",
                                       fg="#1f2447")
        self.preview_canvas.create_window(self.desk_w // 2, self.desk_h // 2, anchor=tk.CENTER, tags='select_btn', window=self.btn_file_open)
        
        self.box_consecutive = App_setting_check(
            self.preview_canvas,
            text = "切り抜き後も作業を続ける"
        )

        self.preview_canvas.create_window(0, 50, anchor=tk.NW, tags='setting_op',window=self.box_consecutive)
        
        self.btn_sys_setting_open = App_setting_btn(self.preview_canvas,
                                                    text="設定からメインウィンドウを変更する",
                                                    command=self.open_sys_setting
                                                    )

        self.preview_canvas.create_window(0, 0, anchor=tk.NW, tags='setting_op',window=self.btn_sys_setting_open)
        
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)

        self.origin_img = None
        self.preview_img = None
        self.reset_x = None
        self.reset_y = None
        self.file_path = None
        self.folder_path = None
        self.pv_x = None
        self.pv_y = None
        
        self.simple_mode.mainloop()
    
    def create_view(self):
        try:
            self.origin_img = Image.open(self.file_path)
            
            img_w = self.origin_img.width
            img_h = self.origin_img.height
            gcd = math.gcd(img_w, img_h)
            img_sr_w, img_sr_h = img_w // gcd, img_h // gcd
            if self.desk_sr_w * img_sr_h >= self.desk_sr_h * img_sr_w:
                height = math.ceil(self.origin_img.height * self.desk_w // self.origin_img.width)
                self.preview_img = self.origin_img.resize((self.preview_canvas.winfo_width(), height))
            else:
                width = math.ceil(self.origin_img.width * self.desk_h // self.origin_img.height)
                self.preview_img = self.origin_img.resize((width, self.preview_canvas.winfo_height()))
            self.preview_img = ImageTk.PhotoImage(self.preview_img)
            self.preview_canvas.create_image(self.preview_canvas.winfo_width() // 2, self.preview_canvas.winfo_height() // 2, image=self.preview_img, tag='preview_img_tag', anchor=tk.CENTER)
            self.reset_x, self.reset_y, reset_w, reset_h = self.preview_canvas.bbox('preview_img_tag')
            self.preview_canvas.itemconfigure('select_btn', state=tk.HIDDEN)
            self.preview_canvas.itemconfigure('setting_op', state=tk.HIDDEN)
            self.id_click = self.preview_canvas.bind("<Button-1>", self.click_in)
            self.id_hold = self.preview_canvas.bind("<Button1-Motion>", self.click_hold)
            self.id_release = self.preview_canvas.bind("<ButtonRelease-1>", self.click_out)
        except:
            return
        
    def click_in(self, event):
        self.pv_x = event.x
        self.pv_y = event.y
    
    def click_hold(self, event):
        dx = event.x - self.pv_x
        dy = event.y - self.pv_y
        self.preview_canvas.move('preview_img_tag', dx, dy)
        self.pv_x = event.x
        self.pv_y = event.y
    
    def click_out(self, event):
        xNW, yNW, xSE, ySE = self.preview_canvas.bbox('preview_img_tag')
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        if xNW < 0 and xSE < canvas_width:
            self.preview_canvas.move('preview_img_tag', canvas_width - xSE, 0)
        if yNW < 0 and ySE < canvas_height:
            self.preview_canvas.move('preview_img_tag', 0, canvas_height - ySE)
        if xSE > canvas_width and xNW > 0:
            self.preview_canvas.move('preview_img_tag', -xNW, 0)
        if ySE > canvas_height and yNW > 0:
            self.preview_canvas.move('preview_img_tag', 0, -yNW)
    
    def select_file(self):
        if self.folder_path == None:
            dir = os.path.expanduser('~/Desktop')
        else:
            dir = self.folder_path
        filetype = [("画像ファイル", "*.png;*.jpg;*.jpeg;*.tif*.tiff;*.bmp")]
        self.file_path = filedialog.askopenfilename(filetypes=filetype, initialdir=dir)
        self.folder_path = os.path.dirname(self.file_path)
    
    def file_open(self):
        self.preview_canvas.delete("preview_img_tag")
        self.select_file()
        self.create_view()
        
    
    def file_close(self):
        self.preview_canvas.delete("preview_img_tag")
        self.preview_canvas.itemconfigure('select_btn', state=tk.NORMAL)
        self.preview_canvas.itemconfigure('setting_op', state=tk.NORMAL)
        self.preview_canvas.unbind("<Button-1>", self.id_click)
        self.preview_canvas.unbind("<Button1-Motion>", self.id_hold)
        self.preview_canvas.unbind("<ButtonRelease-1>", self.id_release)

    def preview_img_save(self):
        if self.preview_img is None:    
            pass
        else:
            self.simple_mode.attributes("-alpha", 1.0)
            file_name, file_ext = os.path.splitext(self.file_path)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            save_path = file_name + "_" + timestamp + ".png"
            ImageGrab.grab(bbox=(0, 0, self.desk_w, self.desk_h)).save(save_path)
            
        #事後処理(GUI)
        if self.conse_var.get() == True:
            self.simple_mode.attributes("-alpha", 0.8)
            self.file_close()
            self.file_open()
        else:
            try:
                subprocess.run(["start", save_path], shell=True)    #windowsの場合
            except:
                try:
                    subprocess.run(["open", save_path], shell=True) #MacOSの場合
                except:
                    pass
            self.simple_mode.destroy()

    def open_sys_setting(self):
        try:
            webbrowser.open('ms-settings:display')
            self.btn_sys_setting_open.configure(text="アプリを再読み込み", command=self.reload)
        except:
            pass

    def reload(self):
        self.simple_mode.destroy()
        Desktop_imagerApp()

    def batch_mode(self):
        self.batch_mode = tk.Tk()
        self.batch_mode.geometry("500x500")
        self.batch_mode.title("Desktopping")
        self.batch_mode.mainloop()

    def app_quit_check(self):
        quit_flg = messagebox.askyesno("確認","アプリを終了しますか？")
        if quit_flg == True:
            self.simple_mode.quit()

    def press_keys(self, event):    # 4はCtrlキー/8はNumLockキーのステート値
        if event.keysym == "Escape":
            self.app_quit_check()
        elif event.keysym == "o" and (event.state == 4 or 12):  #プレビューに表示する画像を選択
            self.file_open()
        elif event.keysym == "w" and (event.state == 4 or 12):  #プレビューから画像を削除
            self.file_close()
        elif event.keysym == "s" and (event.state == 4 or 12):  #プレビューの画像をキャンバスサイズで保存
            self.preview_img_save()
        elif event.keysym == "r" and (event.state == 4 or 12):  #画像の表示位置を初期化
            try:
                self.preview_canvas.moveto('preview_img_tag', self.reset_x, self.reset_y)
            except:
                pass

    

app = Desktop_imagerApp()
