import sys
from tkinter import Canvas, Label, Button, Tk, filedialog, Scrollbar, Entry, Menu, Listbox, Frame, END, Spinbox, ttk, \
    colorchooser, RIGHT, BOTH, S, N
from PIL import ImageTk, ImageDraw, Image, ImageOps, ImageFont

WIDTH = 1440
HEIGHT = 810
PATH = None
FACTOR = None
IMAGE_WIDTH, IMAGE_HEIGHT, POS_X, POS_Y = 0, 0, 0, 0
watermark_list = []
watermark_data_list = []
watermark_selection = 0
edited_file = None
layers = None
active_rectangle = None
ROOT_BG = "#19282F"
SIDEBAR_BG = "#5F7464"
COLOR_CODE_HEX = "#000000"
EDIT_COLOR_CODE_HEX = "#000000"
ACTIVE_LAYER_COLOR = "#FF9300"
TITLE = ("Sans-Serif", 12, "bold")
SUBTITLE = ("Arial", 10, "bold")
ENTRY_FONT = ("Arial", 10)
FONT_STYLES_TK = ["Arial", "Calibri", "Candara", "Courier", "Comic", "Elephant", "Gabriola", "Georgia", "Gigi","GOTHIC", "Jokerman", "Lato", "Quicksand", "Roboto", "Times New Roman", "Ubuntu Mono", "Verdana", "Webdings", "Yellowtail"]
FONT_STYLES_PIL = ["arial", "calibri", "Candara", "cour", "comic", "ELEPHNT", "Gabriola", "georgia", "GIGI", "GOTHIC", "JOKERMAN", "Lato-Regular", "Quicksand-Regular", "Roboto-Regular", "times", "UbuntuMono-Regular", "verdana", "webdings", "Yellowtail-Regular"]


def open_file(*args):
    global resized_file, PATH, watermark_list, IMAGE_WIDTH, IMAGE_HEIGHT, FACTOR, COLOR_CODE_HEX, layers, active_rectangle

    PATH = filedialog.askopenfile(filetypes=[("Image files", ".png .jpg .jpeg")]).name
    file = Image.open(PATH)
    resized_file = ImageTk.PhotoImage(ImageOps.contain(file, (WIDTH, HEIGHT)))
    IMAGE_WIDTH = resized_file.width()
    IMAGE_HEIGHT = resized_file.height()

    label_width.config(text=f"Width: {file.size[0]}px")
    label_height.config(text=f"Height: {file.size[1]}px")

    layers = 0
    delete_all()
    clear()
    canvas.itemconfig(viewport_text, text="")

    if abs(IMAGE_WIDTH - file.size[0]) > abs(IMAGE_HEIGHT - file.size[1]):
        FACTOR = IMAGE_WIDTH/file.size[0]
    else:
        FACTOR = IMAGE_HEIGHT / file.size[1]

    canvas.config(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
    canvas.create_image(IMAGE_WIDTH/2, IMAGE_HEIGHT/2, image=resized_file)
    active_rectangle = canvas.create_rectangle((0, 0, 0, 0), outline=ACTIVE_LAYER_COLOR)
    spinbox_pos_x.config(from_=0, to=IMAGE_WIDTH)
    spinbox_pos_y.config(from_=0, to=IMAGE_HEIGHT)
    spinbox_pos_x.insert(END, IMAGE_WIDTH//2)
    spinbox_pos_y.insert(END, IMAGE_HEIGHT // 2)
    spinbox_edit_pos_x.config(from_=0, to=IMAGE_WIDTH)
    spinbox_edit_pos_y.config(from_=0, to=IMAGE_HEIGHT)
    combo_font_style.set(value="Arial")
    spinbox_font_size.insert(END, 12)
    entry_watermark_text.delete(0, END)
    entry_watermark_text.insert(END, "Watermark")


def save_file(*args):
    global edited_file
    try:
        if edited_file is None:
            preview_file(preview=False)
        save_path = filedialog.asksaveasfile(initialfile="Untitled", defaultextension=".png", filetypes=[("All Files", "*"), ("Image Files", "*.png")]).name
        edited_file.save(save_path)

    except AttributeError:
        pass


def preview_file(*args, preview=True):
    global watermark_data_list, edited_file
    edited_file = Image.open(PATH)
    draw = ImageDraw.Draw(edited_file)
    for watermark in watermark_data_list:
        style = FONT_STYLES_PIL[FONT_STYLES_TK.index(watermark['font'])]
        font = ImageFont.truetype(f"{style}", int(float(watermark['font_size']) / FACTOR *1.335))
        draw.text(xy=(float(watermark["x"]) / FACTOR, float(watermark["y"]) / FACTOR), text=watermark["text"], font=font, fill=watermark["color"])#, anchor="mm")
    if preview:
        edited_file.show()


def watermark_image(*args):
    global watermark_list, watermark_selection, watermark_data_list, COLOR_CODE_HEX, EDIT_COLOR_CODE_HEX
    watermark = {}
    mark = entry_watermark_text.get()
    pos_x = int(spinbox_pos_x.get().split(".")[0])
    pos_y = int(spinbox_pos_y.get().split(".")[0])
    font = combo_font_style.get()
    size = int(spinbox_font_size.get())
    EDIT_COLOR_CODE_HEX = COLOR_CODE_HEX
    color = EDIT_COLOR_CODE_HEX

    watermark_text = canvas.create_text(pos_x, pos_y, text=mark, font=(font, size, "normal"), fill=color)
    watermark["id"] = watermark_text
    watermark["x"] = pos_x
    watermark["y"] = pos_y
    watermark["text"] = mark
    watermark["font"] = font
    watermark["font_size"] = size
    watermark["color"] = color
    watermark_data_list.append(watermark)
    watermark_list.append(watermark_text)
    watermark_selection = watermark_list.index(watermark_text)
    list_watermark.insert(watermark_list.index(watermark_text), f"{mark}")
    label_watermark_list.config(text=f"{mark}")
    listbox_select(list_select=False)


def choose_color(*args):
    global COLOR_CODE_HEX
    COLOR_CODE_HEX = colorchooser.askcolor()[1]
    button_choose_color.config(bg=COLOR_CODE_HEX)


def choose_update_color(*args):
    global EDIT_COLOR_CODE_HEX
    EDIT_COLOR_CODE_HEX = colorchooser.askcolor()[1]
    update_watermark()


def move(e):
    global watermark_list, watermark_selection, POS_X, POS_Y
    POS_X, POS_Y = int(e.x), int(e.y)
    spinbox_edit_pos_x.delete(0, END)
    spinbox_edit_pos_y.delete(0, END)
    entry_edit_watermark.delete(0, END)
    spinbox_change_font_size.delete(0, END)
    watermark_data_list[watermark_selection]["x"] = POS_X
    watermark_data_list[watermark_selection]["y"] = POS_Y
    if watermark_selection >= 0:
        entry_edit_watermark.insert(END, string=watermark_data_list[watermark_selection]["text"])
        spinbox_edit_pos_x.insert(END, s=POS_X)
        spinbox_edit_pos_y.insert(END, s=POS_Y)
        spinbox_change_font_size.insert(END, s=int(watermark_data_list[watermark_selection]["font_size"]))
        combo_change_font_style.set(value=watermark_data_list[watermark_selection]["font"])
        update_watermark()
    else:
        canvas.moveto(watermark_list[-1], POS_X, POS_Y)


def update_watermark(*args):
    global watermark_selection, EDIT_COLOR_CODE_HEX, canvas, active_rectangle
    button_update_color.config(bg=EDIT_COLOR_CODE_HEX)
    watermark_data_list[watermark_selection]["text"] = entry_edit_watermark.get()
    watermark_data_list[watermark_selection]["x"] = spinbox_edit_pos_x.get()
    watermark_data_list[watermark_selection]["y"] = spinbox_edit_pos_y.get()
    watermark_data_list[watermark_selection]["font"] = combo_change_font_style.get()
    watermark_data_list[watermark_selection]["font_size"] = spinbox_change_font_size.get()
    watermark_data_list[watermark_selection]["color"] = EDIT_COLOR_CODE_HEX
    font = (watermark_data_list[watermark_selection]["font"], watermark_data_list[watermark_selection]["font_size"], "normal")
    list_watermark.delete(watermark_selection)
    list_watermark.insert(watermark_selection, entry_edit_watermark.get().strip())
    for item in range(list_watermark.size()):
        list_watermark.itemconfig(list_watermark.index(item), bg="white", fg="black")
    list_watermark.itemconfig(watermark_selection, bg=ACTIVE_LAYER_COLOR, fg="white")
    label_watermark_list.config(text=f"Watermark Layers: {list_watermark.size()}")
    canvas.itemconfig(watermark_list[watermark_selection], text=entry_edit_watermark.get(), font=font, fill=watermark_data_list[watermark_selection]["color"])
    canvas.moveto(watermark_list[watermark_selection], spinbox_edit_pos_x.get(), spinbox_edit_pos_y.get())
    canvas.coords(active_rectangle, canvas.bbox(watermark_list[watermark_selection]))
    canvas.moveto(active_rectangle, int(spinbox_edit_pos_x.get()), int(spinbox_edit_pos_y.get()))


def increase_font_size(*args):
    spinbox_change_font_size.config(value=int(spinbox_change_font_size.get()) + 1)
    update_watermark()


def decrease_font_size(*args):
    spinbox_change_font_size.config(value=int(spinbox_change_font_size.get()) - 1)
    update_watermark()


def move_up(*args, control=False):
    if control:
        step = 5
    else:
        step=1
    spinbox_edit_pos_y.config(value=int(spinbox_edit_pos_y.get()) - step)
    update_watermark()


def move_down(*args, control=False):
    if control:
        step = 5
    else:
        step=1
    spinbox_edit_pos_y.config(value=int(spinbox_edit_pos_y.get()) + step)
    update_watermark()


def move_left(*args, control=False):
    if control:
        step = 5
    else:
        step = 1
    spinbox_edit_pos_x.config(value=int(spinbox_edit_pos_x.get()) - step)
    update_watermark()


def move_right(*args, control=False):
    if control:
        step = 5
    else:
        step=1
    spinbox_edit_pos_x.config(value=int(spinbox_edit_pos_x.get()) + step)
    update_watermark()


def delete(*args):
    global watermark_selection, watermark_list, watermark_data_list
    try:
        canvas.itemconfig(watermark_list[watermark_selection], text="")
    except IndexError:
        watermark_selection = watermark_list.index(watermark_list[-1])
        canvas.itemconfig(watermark_list[watermark_selection], text="")
    watermark_list.pop(watermark_selection)
    watermark_data_list.pop(watermark_selection)
    list_watermark.delete(watermark_selection)
    label_watermark_list.config(text=f"Watermark Layers: {list_watermark.size()}")


def delete_all(*args):
    global watermark_list, watermark_data_list
    for watermark in watermark_list:
        canvas.itemconfig(watermark, text="")
    watermark_list.clear()
    watermark_data_list.clear()
    list_watermark.delete(0, END)
    label_watermark_list.config(text=f"Watermark Layers: {list_watermark.size()}")


def listbox_select(*args, list_select=True):
    global watermark_selection, watermark_data_list, EDIT_COLOR_CODE_HEX
    entry_edit_watermark.delete(0, END)
    spinbox_edit_pos_x.delete(0, END)
    spinbox_edit_pos_y.delete(0, END)
    spinbox_change_font_size.delete(0, END)
    if list_select:
        watermark_selection = list_watermark.curselection()[0]
        EDIT_COLOR_CODE_HEX = watermark_data_list[watermark_selection]["color"]
    selected = watermark_data_list[watermark_selection]
    entry_edit_watermark.insert(END, string=selected["text"])
    spinbox_edit_pos_x.insert(END, s=selected["x"])
    spinbox_edit_pos_y.insert(END, s=selected["y"])
    combo_change_font_style.set(value=selected["font"])
    spinbox_change_font_size.insert(END, s=int(selected["font_size"]))
    update_watermark()


def clear():
    spinbox_pos_x.delete(0, END)
    spinbox_pos_y.delete(0, END)
    spinbox_font_size.delete(0, END)
    entry_watermark_text.delete(0, END)


def remove_focus(*args):
    root.focus_set()


root = Tk()
root.title("Watermarking App")
root.resizable(False, False)
topbar = Frame(root, bg=ROOT_BG)
sidebar = Frame(root, bg=SIDEBAR_BG)
viewport = Frame(root, width=WIDTH, height=HEIGHT, bg="#5F7464")
edit = Frame(sidebar, bg=SIDEBAR_BG)
app_frame = Frame(sidebar, bg=SIDEBAR_BG)

menubar = Menu(root)
filemenu = Menu(menubar, bg="#573391")
editmenu = Menu(menubar)

filemenu.add_command(label="Open Image", command=open_file)
filemenu.add_command(label="Save / Save As Image", command=save_file)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

editmenu.add_command(label="Delete", command=delete)
editmenu.add_command(label="Delete All", command=delete_all)
menubar.add_cascade(label="Edit", menu=editmenu)

button_mark = Button(topbar, text="Create Watermark", command=watermark_image, font=TITLE, bg="#187498", fg="white", width=16)
button_choose_color = Button(topbar, text="Color", command=choose_color, bg="#000000", font=SUBTITLE, fg="white")

button_open_file = Button(sidebar, text="Open Image", command=open_file, font=TITLE, bg="#224B0C", fg="white", width=27)
button_save_file = Button(sidebar, text="Save Image", command= save_file, font=SUBTITLE, width=16, bg="#219F94", fg="white")
button_delete = Button(sidebar, text="Remove", command=delete, font=SUBTITLE, width=16, bg="#FF7D7D", fg="white")
button_delete_all = Button(sidebar, text="Remove All", command=delete_all, font=SUBTITLE, width=16, bg="#FF6464", fg="white")
button_preview_image = Button(sidebar, text="Preview Image", command=preview_file, font=SUBTITLE, width=16, bg="#219F94", fg="white")

button_update_color = Button(edit, text="Color", command= choose_update_color, bg="#000000", font=SUBTITLE, fg="white")
button_update_watermark = Button(edit, text="Update Watermark", command=update_watermark, font=TITLE, width=19, bg="#187498", fg="white")

canvas = Canvas(viewport, width=WIDTH, height=HEIGHT, bg="#5F7464", highlightthickness=0)
canvas.bind("<B1-Motion>", move)
viewport_text = canvas.create_text(WIDTH/2, HEIGHT/2, text="Viewport", font=("Arial", 30, "bold"), fill="white")

combo_font_style = ttk.Combobox(topbar, state="readonly", values=FONT_STYLES_TK, width=24, font=ENTRY_FONT)

combo_change_font_style = ttk.Combobox(edit, state="readonly", values=FONT_STYLES_TK, width=24, font=ENTRY_FONT)
combo_change_font_style.bind("<<ComboboxSelected>>", update_watermark)

entry_watermark_text = Entry(topbar, width=46)
entry_edit_watermark = Entry(edit, width=46)

label_pos_x = Label(topbar, text="Coor X (px): ", font=SUBTITLE, bg=ROOT_BG, fg="white")
label_pos_y = Label(topbar, text="Coor Y (px): ", font=SUBTITLE, bg=ROOT_BG, fg="white")
label_watermark = Label(topbar, text="Watermark Text: ", font=SUBTITLE, bg=ROOT_BG, fg="white")
label_font = Label(topbar, text="Font Style: ", font=SUBTITLE, bg=ROOT_BG, fg="white")
label_font_size = Label(topbar, text="Font Size: ", font=SUBTITLE, bg=ROOT_BG, fg="white")

label_app_name = Label(root, text="Watermarking App", font=TITLE, bg="#7900FF", fg="white", width=29)

label_watermark_list = Label(sidebar, text=f"Watermark Layers: 0", font=TITLE, bg=SIDEBAR_BG, fg="white")
label_width = Label(sidebar, text=" ", font=SUBTITLE, bg=SIDEBAR_BG, fg="white")
label_height = Label(sidebar, text=" ", font=SUBTITLE, bg=SIDEBAR_BG, fg="white")

label_edit_watermark = Label(edit, text="EDIT WATERMARK", font=TITLE, bg=SIDEBAR_BG, fg="white")
label_edit_watermark_text = Label(edit, text="Watermark", font=SUBTITLE, bg=SIDEBAR_BG, fg="white")
label_edit_pos_x = Label(edit, text="Coor X (px): ", font=SUBTITLE, bg=SIDEBAR_BG, fg="white", width=10)
label_edit_pos_y = Label(edit, text="Coor Y (px): ", font=SUBTITLE, bg=SIDEBAR_BG, fg="white", width=10)
label_edit_font = Label(edit, text="Font Style: ", font=SUBTITLE, bg=SIDEBAR_BG, fg="white", width=10)
label_edit_font_size = Label(edit, text="Font Size:", font=SUBTITLE, bg=SIDEBAR_BG, fg="white", width=10)

list_watermark = Listbox(sidebar, width=44, height=20)
list_watermark.bind("<<ListboxSelect>>", listbox_select)

scrollbar = Scrollbar(sidebar, width=20)
list_watermark.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=list_watermark.yview)

spinbox_pos_x = Spinbox(topbar, font=ENTRY_FONT, width=10)
spinbox_pos_y = Spinbox(topbar, font=ENTRY_FONT, width=10)
spinbox_font_size = Spinbox(topbar, from_=0, to=150, font=ENTRY_FONT, width=10)

spinbox_edit_pos_x = Spinbox(edit, command=update_watermark, width=25, font=ENTRY_FONT)
spinbox_edit_pos_y = Spinbox(edit, command=update_watermark, width=25, font=ENTRY_FONT)
spinbox_change_font_size = Spinbox(edit, from_=0, to=150, command=update_watermark, width=25, font=ENTRY_FONT)

viewport.grid(row=1, column=0, columnspan=12, padx=(5, 0), pady=5, rowspan=2)
viewport.grid_propagate(0)
canvas.place(relx=0.5, rely=0.5, anchor="center")

topbar.grid(row=0, column=0, columnspan=12, pady=(10, 0))
label_pos_x.grid(row=0, column=0, padx=(5, 0))
spinbox_pos_x.grid(row=0, column=1, padx=(0, 10))
label_pos_y.grid(row=0, column=2)
spinbox_pos_y.grid(row=0, column=3, padx=(0, 10))
label_font.grid(row=0, column=4)
combo_font_style.grid(row=0, column=5, padx=(0, 10))
label_font_size.grid(row=0, column=6)
spinbox_font_size.grid(row=0, column=7, padx=(0, 10))
button_choose_color.grid(row=0, column=8, padx=(0, 10))
label_watermark.grid(row=0, column=9)
entry_watermark_text.grid(row=0, column=10, padx=(0, 10))
button_mark.grid(row=0, column=11)

sidebar.grid(row=0, column=12, sticky="n", padx=5, rowspan=2)
label_watermark_list.grid(row=0, column=0, columnspan=2)
list_watermark.grid(row=1, column=0, columnspan=2, sticky="e", padx=(5, 0))
scrollbar.grid(row=1, column=2, sticky=N+S, padx=(0, 5))
button_delete.grid(row=2, column=0, pady=(10, 5), padx=5)
button_delete_all.grid(row=2, column=1, columnspan=2, pady=(10, 5), padx=(0, 5))
button_open_file.grid(row=3, column=0, padx=5, columnspan=3)
button_preview_image.grid(row=4, column=0, pady=5, padx=5)
button_save_file.grid(row=4, column=1, columnspan=2, pady=5, padx=(0, 5))
label_width.grid(row=5, column=0)
label_height.grid(row=5, column=1)

edit.grid(row=6, column=0, columnspan=3, sticky="nw", pady=(48, 5))
label_edit_watermark.grid(row=0, column=0, columnspan=2)
entry_edit_watermark.grid(row=1, column=0, columnspan=2, pady=5)
label_edit_pos_x.grid(row=7, column=0, pady=5, sticky="e", padx=5)
spinbox_edit_pos_x.grid(row=7, column=1, pady=5, sticky="e", padx=(0, 5))
label_edit_pos_y.grid(row=8, column=0, pady=5, sticky="e", padx=5)
spinbox_edit_pos_y.grid(row=8, column=1, pady=5, sticky="e", padx=(0, 5))
label_edit_font.grid(row=9, column=0, pady=5, sticky="e", padx=5)
combo_change_font_style.grid(row=9, column=1, sticky="e", padx=(0, 5))
label_edit_font_size.grid(row=10, column=0, sticky="e", pady=5, padx=5)
spinbox_change_font_size.grid(row=10, column=1, pady=5, sticky="e", padx=(0, 5))
button_update_color.grid(row=12, column=0, columnspan=2, ipadx=100, pady=5, padx=5)
button_update_watermark.grid(row=13, column=0, columnspan=2, ipadx=20, pady=(5, 30))

app_frame.grid(row=0, column=0, columnspan=2)
label_app_name.grid(row=2, column=12)

root.config(menu=menubar, bg=ROOT_BG)

root.bind("<Escape>", remove_focus)
root.bind("<Control-n>", open_file)
root.bind("<Delete>", delete)
root.bind("<Control-Delete>", delete_all)
root.bind("<Alt-n>", watermark_image)
root.bind("<Control-s>", save_file)
root.bind("<Control-p>", preview_file)
root.bind("<Control-q>", sys.exit)
root.bind("<{>", decrease_font_size)
root.bind("<}>", increase_font_size)
root.bind("<Shift-Up>", move_up)
root.bind("<Shift-Down>", move_down)
root.bind("<Shift-Left>", move_left)
root.bind("<Shift-Right>", move_right)
root.bind("<Control-Up>", lambda event: move_up(control=True))
root.bind("<Control-Down>", lambda event: move_down(control=True))
root.bind("<Control-Left>", lambda event: move_left(control=True))
root.bind("<Control-Right>", lambda event: move_right(control=True))
root.bind("<Control-i>", choose_update_color)
root.bind("<Return>", update_watermark)

root.eval(f"tk::PlaceWindow . 10")

root.mainloop()
