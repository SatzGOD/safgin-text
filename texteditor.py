import webbrowser
from tkinter import *
from tkinter import font, messagebox
from threading import Thread
from json import load
from texteditor_utils import TextEditorUtils

# On opening--------------------------------------------
window_cords = {'w': None, 'h': None, 'x': None, 'y': None}

try:
    with open('data.json', 'r') as f:
        loadeddata = load(f)
        path = loadeddata['path']
        state = loadeddata['state']
        style = loadeddata['fontstyle']
        size = loadeddata['fontsize']
        window_cords['w'] = loadeddata['w']
        window_cords['h'] = loadeddata['h']
        window_cords['x'] = loadeddata['x']
        window_cords['y'] = loadeddata['y']
except:
    # File Path
    path = ""
    # for themes
    state = None
    size = "15"
    style = "Consolas"
# --------------------------------------------
# main window loop
window = Tk()
window.iconphoto(True, PhotoImage(file="media_file/iconphoto.png"))
# Window Geometry
window_width = window_cords['w'] if window_cords['w'] != None else 500
window_height = window_cords['h'] if window_cords['h'] != None else 600
x = window_cords['x'] if window_cords['w'] != None else int((window.winfo_screenwidth() / 2) - (window_width / 2))
y = window_cords['y'] if window_cords['w'] != None else int((window.winfo_screenheight() / 2) - (window_height / 2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
# ------------------------------------------

# setting label text
font_style = StringVar()
font_style.set(style)
font_size = StringVar()
font_size.set(size)
statuL_text = StringVar()
statuL_text.set("")
# Text box and Scroll bar
bodyframe = Frame(window)
text = Text(bodyframe, font=(font_style.get(), font_size.get()))
scrollbary = Scrollbar(bodyframe, command=text.yview)
scrollbarx = Scrollbar(bodyframe, command=text.xview, orient=HORIZONTAL)
# bottom frame
bottomframe = Frame(window)
stylebox = OptionMenu(bottomframe, font_style, *font.families(),
                      command=lambda *_: text.config(font=(font_style.get(), font_size.get())))
sizebox = Spinbox(bottomframe, from_=1, to_=120, textvariable=font_size, width=4)
fcolorbutton = Button(bottomframe, text="Font color")
bcolorbutton = Button(bottomframe, text="Paper color")
status_label = Label(bottomframe, textvariable=statuL_text)

# creating main menubar and menus
menubar = Menu(window)
window.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
thememenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

# TextEditor Utils object
teu = TextEditorUtils(window, path, state, font_style, font_size, statuL_text, fcolorbutton, bcolorbutton, text,
                      bottomframe, stylebox, sizebox, status_label,menubar,filemenu,editmenu,thememenu,helpmenu)
# configs
teu.startupopen()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary.pack(side=RIGHT, fill=Y)
text.pack(expand=True, fill=BOTH)
text.config(yscrollcommand=scrollbary.set, undo=True, xscrollcommand=scrollbarx.set, wrap="none")
bodyframe.grid(sticky=N + E + W + S)
bottomframe.grid()
stylebox.grid(row=0, column=0)
sizebox.grid(row=0, column=1)
fcolorbutton.grid(row=0, column=2)
bcolorbutton.grid(row=0, column=3)
status_label.grid(row=0, column=4)
teu.bottomFrame_commandsetters()


# File Menu
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label="New", command=teu.new, accelerator="Ctrl+N")
filemenu.add_command(label='Open...', command=teu.fopen, accelerator="Ctrl+O")
filemenu.add_command(label='Save', command=teu.fsave, accelerator="Ctrl+S")
filemenu.add_command(label='Save As...', command=teu.fsave_as, accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label='Print 🖶', command=teu.print_file, accelerator="Ctrl+P")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=teu.on_closing)

# Edit Menu
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="↶ Undo", command=teu.undo, accelerator="Ctrl+Z")
editmenu.add_command(label="↷ Redo", command=teu.redo, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut", command=teu.cut, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", command=teu.copy, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", command=teu.paste, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=teu.selectall, accelerator="Ctrl+A")
editmenu.add_command(label="Delete All", command=teu.delete_all, accelerator="Shift+Del")

# Theme Menu
menubar.add_cascade(label="Themes", menu=thememenu)
thememenu.add_command(label="Dark", command=lambda: teu.set_state(1),activebackground="#242424",activeforeground="white")
thememenu.add_command(label="Light", command=lambda: teu.set_state(0),activebackground="white",activeforeground="black")

# Help Menu
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=lambda: teu.about())
helpmenu.add_separator()
helpmenu.add_command(label="Version",
                     command=lambda: messagebox.showinfo(title="Version", message=f"App Version: 1.0.7"
                                                                                  f"\nTk Version: {TkVersion}"
                                                                                  f"\nTcl Version: {TclVersion}"
                                                                                  ))
helpmenu.add_separator()
helpmenu.add_command(label="Repository", command=lambda: webbrowser.open("https://github.com/SatzGOD/texteditor"))
helpmenu.add_separator()
helpmenu.add_command(label="Report a problem ⚠",
                     command=lambda: webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0"))
# cursors = ["arrow", "circle", "clock", "cross", "dotbox", "exchange", "fleur", "heart", "man", "mouse", "pirate",
#            "plus", "shuttle", "sizing", "spider", "spraycan", "star", "target", "tcross", "trek", "watch"]

# key binds
# To Zoom in and Zoom out the text
window.bind("<Control-plus>", lambda _: teu.font_changer(font_size.set(str(int(font_size.get()) + 5))) if (
        int(font_size.get()) < 120) else font_size.set(120))  # ctr + plus
window.bind("<Control-minus>", lambda _: teu.font_changer(font_size.set(str(int(font_size.get()) - 5))) if (
        int(font_size.get()) > 5) else font_size.set(5))  # ctr + minus
# To Save
window.bind("<Control-S>", lambda _: teu.fsave())  # ctr + S
window.bind("<Control-s>", lambda _: teu.fsave())  # ctr + s
# To Save as
window.bind("<Control-Shift-S>", lambda _: teu.fsave_as())  # ctr + shift + S
window.bind("<Control-Shift-s>", lambda _: teu.fsave_as())  # ctr + shift + s
# To Open
window.bind("<Control-O>", lambda _: teu.fopen())  # ctr + O
window.bind("<Control-o>", lambda _: teu.fopen())  # ctr + o
# To New
window.bind("<Control-N>", lambda _: teu.new())  # ctr + N
window.bind("<Control-n>", lambda _: teu.new())  # ctr + n
# To Select All
window.bind("<Shift-Delete>", lambda _: teu.delete_all())  # ctr + A
# To Print
window.bind("<Control-P>", lambda _: teu.print_file())  # ctr + P
window.bind("<Control-p>", lambda _: teu.print_file())  # ctr + p

# To update the state of text in text box(if it saved or not)
Thread(target=teu.textfileactivity, daemon=True).start()

# to set theme on startup
if state != None:
    teu.themeSwitcher()
else:
    teu.set_state(0)
window.update()

# custom quit protocol
window.protocol("WM_DELETE_WINDOW", teu.on_closing)
window.mainloop()







