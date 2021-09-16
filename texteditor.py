import webbrowser
from tkinter import *
from tkinter import messagebox
from threading import Thread
import texteditor_utils as t
from texteditor_utils import TextEditorUtils, window_geometry, startup_loader

startup_loader()
# main window loop
window = Tk()
window.iconphoto(True, PhotoImage(file="media_file/iconphoto.png"))
window_geometry(window)

# StringVars
statuL_text = StringVar()
statuL_text.set("")


# Text box and Scroll bar
bodyframe = Frame(window)
text = Text(bodyframe,font=(t.style,t.size))
scrollbary = Scrollbar(bodyframe, command=text.yview)
scrollbarx = Scrollbar(bodyframe, command=text.xview, orient=HORIZONTAL)
# bottom frame
bottomframe = Frame(window)
status_label = Label(bottomframe, textvariable=statuL_text)

# creating main menu bar and menus
menubar = Menu(window)
window.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
thememenu = Menu(menubar, tearoff=0)
helpmenu = Menu(menubar, tearoff=0)

# TextEditor Utils object
teu = TextEditorUtils(window, statuL_text, text,
                      bottomframe, status_label,menubar,filemenu,editmenu,thememenu,helpmenu)
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
status_label.grid(row=0, column=0)



# File Menu
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label="New", command=teu.new, accelerator="Ctrl+N")
filemenu.add_command(label='Open...', command=teu.fopen, accelerator="Ctrl+O")
filemenu.add_command(label='Save', command=teu.fsave, accelerator="Ctrl+S")
filemenu.add_command(label='Save As...', command=teu.fsave_as, accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Editor Settings",command=teu.font_window)
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
                     command=lambda: messagebox.showinfo(title="Version", message=f"App Version: 1.0.9"
                                                                                  f"\nTk Version: {TkVersion}"
                                                                                  f"\nTcl Version: {TclVersion}"
                                                                                  ))
helpmenu.add_separator()
helpmenu.add_command(label="Repository", command=lambda: webbrowser.open("https://github.com/SatzGOD/texteditor"))
helpmenu.add_separator()
helpmenu.add_command(label="Report a problem ⚠",
                     command=lambda: webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0"))

teu.window_keybinds()

# To update the state of text in text box(if it saved or not)
Thread(target=teu.textfileactivity, daemon=True).start()

# to set theme on startup
if t.state != None:
    teu.themeSwitcher()
else:
    teu.set_state(0)
window.update()  # to update idle tasks if any...

# custom quit protocol
window.protocol("WM_DELETE_WINDOW", teu.on_closing)
window.mainloop()







