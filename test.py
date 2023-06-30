import tkinter as tk

root = tk.Tk()

app1_window = None
app2_window = None

def launch_app1():
    global app1_window, app2_window

    if app1_window is None:
        app1_window = tk.Toplevel(root)
        app1_window.title("App1")
        app1_window.protocol("WM_DELETE_WINDOW", on_app1_close)  # ウィンドウの閉じるボタンに終了イベントを設定

        # App1のウィンドウに追加するコンテンツやロジックを記述
        # ...

        if app2_window is not None:
            app2_window.destroy()
            app2_window = None
    else:
        app1_window.lift()

def launch_app2():
    global app1_window, app2_window

    if app2_window is None:
        app2_window = tk.Toplevel(root)
        app2_window.title("App2")
        app2_window.protocol("WM_DELETE_WINDOW", on_app2_close)  # ウィンドウの閉じるボタンに終了イベントを設定

        # App2のウィンドウに追加するコンテンツやロジックを記述
        # ...

        if app1_window is not None:
            app1_window.destroy()
            app1_window = None
    else:
        app2_window.lift()

def on_app1_close():
    global app1_window
    app1_window.destroy()
    app1_window = None
    launch_app2()

def on_app2_close():
    global app2_window
    app2_window.destroy()
    app2_window = None
    launch_app1()

app1_button = tk.Button(root, text="App1を起動", command=launch_app1)
app1_button.pack()

app2_button = tk.Button(root, text="App2を起動", command=launch_app2)
app2_button.pack()

root.mainloop()
