import math
import os, subprocess, datetime
import tkinter as tk
import tkinter.filedialog as filedialog, tkinter.messagebox as messagebox
from PIL import Image, ImageTk, ImageGrab

class Desk_topingApp:
    def __init__(self):
        self.single_mode = tk.Tk()
        self.single_mode.title("desk_toping")
        self.single_mode.attributes('-fullscreen', True, "-alpha", 0.8)
        self.single_mode.bind('<KeyPress>', self.press_keys)
        
        self.desk_w = self.single_mode.winfo_screenwidth()
        self.desk_h = self.single_mode.winfo_screenheight()
        gcd = math.gcd(self.desk_w, self.desk_h)
        self.desk_sr_w, self.desk_sr_h = self.desk_w // gcd, self.desk_h // gcd
        
        self.preview_canvas = tk.Canvas(self.single_mode, bg="white", highlightthickness=0)
        self.btn_file_open = tk.Button(self.preview_canvas, text='ファイルを選択する', command=self.file_open)
        self.preview_canvas.create_window(self.desk_w // 2, self.desk_h // 2, anchor=tk.CENTER, tags='select_btn', window=self.btn_file_open)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.origin_img = None
        self.preview_img = None
        self.reset_x = None
        self.reset_y = None
        self.file_path = None
        self.folder_path = None
        self.pvi_x = None
        self.pvi_y = None
        
        self.create_view()
        
        self.single_mode.mainloop()
    
    def create_view(self):
        if self.file_path is None:
            return
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
        self.preview_canvas.bind("<Button-1>", self.click_in)
        self.preview_canvas.bind("<Button1-Motion>", self.click_hold)
        self.preview_canvas.bind("<ButtonRelease-1>", self.click_out)
    
    def click_in(self, event):
        self.pvi_x = event.x
        self.pvi_y = event.y
    
    def click_hold(self, event):
        dx = event.x - self.pvi_x
        dy = event.y - self.pvi_y
        self.preview_canvas.move('preview_img_tag', dx, dy)
        self.pvi_x = event.x
        self.pvi_y = event.y
    
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
        dir = os.path.expanduser('~/Desktop')
        filetype = [("すべて", "*"), ("PNG", "*.png"), ("JPG", "*.jpg"), ("JPEG", "*.jpeg")]
        self.file_path = filedialog.askopenfilename(filetypes=filetype, initialdir=dir)
        self.folder_path = os.path.dirname(self.file_path)
    
    def file_open(self):
        try:
            self.select_file()
            self.create_view()
            self.preview_canvas.itemconfigure('select_btn', state=tk.HIDDEN)
        except:
            pass
    
    def file_close(self):
        try:
            self.preview_canvas.delete("preview_img_tag")
            self.preview_canvas.itemconfigure('select_btn', state=tk.NORMAL)
            self.preview_canvas.unbind("<Button-1>", self.click_in)
            self.preview_canvas.unbind("<Button1-Motion>", self.click_hold)
            self.preview_canvas.unbind("<ButtonRelease-1>", self.click_out)
        except:
            pass
    
    def preview_img_save(self):
        try:
            self.single_mode.attributes("-alpha", 1.0)
            file_name, file_ext = os.path.splitext(self.file_path)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            save_path = file_name + "_" + timestamp + ".png"
            ImageGrab.grab(bbox=(0, 0, self.desk_w, self.desk_h)).save(save_path)
            self.file_close()
            try:
                subprocess.run(["start", save_path], shell=True)
            except:
                try:
                    subprocess.run(["open", save_path], shell=True)
                except:
                    pass
            self.single_mode.destroy()
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの保存に失敗しました。\n\n{str(e)}")
    
    def close_single_mode(self, event):
        self.single_mode.destroy()
    
    def press_keys(self, event):
        if event.keysym == "Escape":
            self.single_mode.quit()
        elif event.keysym == "w" and (event.state == 4 or 12):  # 4はCtrlキーのステート値
            self.file_close()
        elif event.keysym == "s" and (event.state == 4 or 12):  # +8はNumLockキーのステート値
            self.preview_img_save()
        elif event.keysym == "r" and (event.state == 4 or 12):
            try:
                self.preview_canvas.moveto('preview_img_tag', self.reset_x, self.reset_y)
            except:
                pass

app = Desk_topingApp()
