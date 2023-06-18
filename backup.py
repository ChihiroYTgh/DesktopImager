#画像の移動
# def view_move(dir):
#     print(preview_canvas.bbox("preview_img_tag"))
#     if dir == 'up':
#         preview_canvas.move("preview_img_tag", 0, 8)
#     elif dir == 'down':
#         preview_canvas.move("preview_img_tag", 0, -8)
#     elif dir == 'left':
#         preview_canvas.move("preview_img_tag", 8, 0)
#     elif dir == 'right':
#         preview_canvas.move("preview_img_tag", -8, 0)
#     print(preview_canvas.bbox("preview_img_tag"))

# btn_img_up = tk.Button(root, text='↑', command=lambda:view_move('up'))
# preview_canvas.create_window(512,2, anchor=tk.NW,window=btn_img_up,width=256)
# btn_img_down = tk.Button(root, text='↓', command=lambda:view_move('down'))
# preview_canvas.create_window(512,722, anchor=tk.SW,window=btn_img_down,width=256)
# btn_img_left = tk.Button(root, text='←', command=lambda:view_move('left'))
# preview_canvas.create_window(2,290, anchor=tk.NW,window=btn_img_left,height=144)
# btn_img_right = tk.Button(root, text='→', command=lambda:view_move('right'))
# preview_canvas.create_window(1282,290, anchor=tk.NE,window=btn_img_right,height=144)