from tkinter import colorchooser, filedialog, messagebox, font
from tkinter import *
from os.path import exists
from win32print import GetDefaultPrinter
from win32api import ShellExecute
from json import dump, load
from time import sleep

# diclaring variables
app_name = "TextEditor"
path = None
state = None
style = None
size = None
window_cords = {'w': None, 'h': None, 'x': None, 'y': None}

# startup json loader
def startup_loader():
    global path,state, style, size, window_cords
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

# window geometry setter
def window_geometry(window):
    window_width = window_cords['w'] if window_cords['w'] != None else 500
    window_height = window_cords['h'] if window_cords['h'] != None else 600
    x = window_cords['x'] if window_cords['w'] != None else int((window.winfo_screenwidth() / 2) - (window_width / 2))
    y = window_cords['y'] if window_cords['w'] != None else int((window.winfo_screenheight() / 2) - (window_height / 2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

# Utilities Class
class TextEditorUtils:

    def __init__(self, window, statusL_text, text,
                 bottomframe, status_label, menubar, filemenu, editmenu, thememenu, helpmenu):
        self.window = window
        self.statusL_text = statusL_text
        self.text = text
        self.bottomframe = bottomframe
        self.status_label = status_label
        self.menubar = menubar
        self.filemenu = filemenu
        self.editmenu = editmenu
        self.thememenu = thememenu
        self.helpmenu = helpmenu

        # module attributes
        self.path = path
        self.state = state
        self.font_style = StringVar()
        self.font_style.set(style)
        self.font_size = StringVar()
        self.font_size.set(size)
        self.tripemp = StringVar() # triple emphasis
        self.tripemp.set("None")

    # new untitled file opener
    def new(self):
        self.text.config(undo=False)
        self.window.title(f"Untitled - {app_name}")
        self.delete_all()
        self.path = ""
        self.text.config(undo=True)
        self.statusL_text.set("")

    # to open an existing file

    def fopen(self):
        self.text.config(undo=False)
        opath = filedialog.askopenfilename(title='Open File', filetypes=(
            ("text file", "*.txt"), ("all files", "*.*"), ("Python File", "*.py"), ("HTML File", "*.html")))

        if exists(opath):
            with open(opath, 'r') as f:
                self.delete_all()
                self.text.insert(1.0, f.read()[:-1])
            self.window.title(f"{opath} - {app_name}")
            self.path = opath
            self.text.config(undo=False)
        else:
            pass

    def startupopen(self):
        if exists(self.path):
            with open(self.path, 'rt') as f:
                self.window.title(f"{self.path} - {app_name}")
                self.text.insert(1.0, f.read()[:-1])
        else:
            self.window.title("Untitled - TextEditor")

    # to save as a new file or save within an existing file
    def fsave_as(self):
        spath = filedialog.asksaveasfile(title="Where you want you to save your file?", defaultextension=".txt",
                                         filetypes=(
                                             ("text File", "*.txt"), ("HTML File", "*.html"), ("Python File", "*.py"),
                                             ("all File", "*.*")))

        if spath != None and exists(spath.name):
            filetext = self.text.get(1.0, "end")
            spath.write(filetext)
            spath.close()
            self.window.title(f"{spath.name} - {app_name}")
            self.path = spath.name
            self.statusL_text.set("Saved!")
        else:
            pass

    def fsave(self):
        if exists(self.path):
            with open(self.path, 'w') as f:
                filetext = self.text.get(1.0, "end")
                f.write(filetext)
                self.window.title(f"{self.path} - {app_name}")
                self.statusL_text.set("Saved!")
        else:
            self.fsave_as()

    def print_file(self):
        printer = GetDefaultPrinter()
        if printer:
            self.statusL_text.set(printer)
            ask = messagebox.askokcancel(title="Print", message=f"Click ok to print this file \n{self.path} ")
            if ask and exists(self.path):
                ShellExecute(0, "print", self.path, None, ".", 0)
            # elif ask == False:
            #     popath = filedialog.askopenfilename(title='Open File', filetypes=(
            #         ("text file", "*.txt"), ("all files", "*.*"), ("Python File", "*.py"), ("HTML File", "*.html")))
            #     if exists(popath):
            #         ShellExecute(0, "print", popath, None, ".", 0)
            else:
                pass
        else:
            self.statusL_text.set("No Printer Available")
            messagebox.showwarning(title=f"{app_name}", message="Cannot Detect a printer:"
                                                                "\nBe sure that your printer is connected properly and use "
                                                                "Control Panel to verify that the printer is configured properly.")
        self.statusL_text.set("")

    # text file activity detector
    def textfileactivity(self):
        while True:
            if exists(self.path):
                with open(self.path, 'rt') as f:
                    if f.read() == self.text.get(1.0, "end"):
                        self.window.title(f"{self.path} - {app_name}")
                    else:
                        self.window.title(f"{self.path}* - {app_name}")
                        self.statusL_text.set("")
            else:
                if self.text.get(1.0, "end") > "   ":
                    self.window.title(f"Untitled* - {app_name}")
                else:
                    self.window.title(f"Untitled - {app_name}")
            sleep(0.01)  # for smooth experience

    def on_closing(self):
        if exists(self.path):
            with open(self.path, 'r') as f:
                if f.read() != self.text.get(1.0, "end"):
                    ask = messagebox.askyesnocancel(title="Quit",
                                                    message=f"Do you want to save changes to this \n{self.path} File?")
                    if ask == True:
                        self.fsave()
                        self.__dumpjson_and_destroy()
                    elif ask == False:
                        self.__dumpjson_and_destroy()
                    else:
                        pass
                else:
                    self.__dumpjson_and_destroy()
        elif self.text.get(1.0, "end") > " ":
            ask = messagebox.askyesnocancel(title="Quit", message=f"Do you want to save changes to this Untitled File?")
            if ask == True:
                self.fsave()
                try:
                    with open(self.path, 'r') as f:
                        if f.read() == self.text.get(1.0, "end")[:-1]:
                            self.__dumpjson_and_destroy()
                except:
                    pass
            elif ask == False:
                self.__dumpjson_and_destroy()
            else:
                pass
        else:
            self.__dumpjson_and_destroy()


    def font_window(self):

        self.tripemp_list = ["Bold", "Italics", "Underline"]
        self.filemenu.entryconfig(5,state="disabled")
        self.fw = Toplevel()
        self.fw.attributes('-topmost',True)
        self.fw.resizable(False,False)
        self.fw.title("Editor Settings")
        width , height = 300, 130
        x = int((self.window.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.window.winfo_screenheight() / 2) - (height / 2))
        self.fw.geometry(f"{width}x{height}-{x}+{y}")
        self.frame = Frame(self.fw)
        self.l1 = Label(self.frame,text="Font Family:")
        self.l1.grid(row=0,column=0,sticky=W,pady=3)
        self.stylebox = OptionMenu(self.frame, self.font_style, *font.families(), command=self.__font_changer)
        self.stylebox.grid(row=0,column=1,sticky=E,pady=3)
        self.l2 = Label(self.frame, text="Font Style:")
        self.l2.grid(row=1,column=0,sticky=W,pady=3)
        self.tripempbox = OptionMenu(self.frame, self.tripemp, *self.tripemp_list, command=self.__tripemp_func)
        self.tripempbox.grid(row=1,column=1,sticky=W,pady=3)
        self.l3 = Label(self.frame, text="Font Size:")
        self.l3.grid(row=2,column=0,sticky=W,pady=3)
        self.sizebox = Spinbox(self.frame, from_=1, to_=120, textvariable=self.font_size, width=4,command=self.__font_changer)
        self.sizebox.grid(row=2,column=1,sticky=W,pady=3)
        self.fcolorbutton = Button(self.frame, text="Font color", command=self.__color_fchanger)
        self.fcolorbutton.grid(row=3,column=0,sticky=W,pady=3,padx=2)
        self.bcolorbutton = Button(self.frame, text="Paper color",command=self.__color_bchanger)
        self.bcolorbutton.grid(row=3,column=1,sticky=W,pady=3)
        self.frame.grid(row=0,column=0,sticky=W)

        self.ts_fw()
        self.fw.protocol("WM_DELETE_WINDOW", self.__fwonclosing)
        self.fw.mainloop()


    def window_keybinds(self):
        # key binds
        # To Zoom in and Zoom out the text
        self.window.bind("<Control-plus>", lambda _: self.__font_changer(self.font_size.set(str(int(self.font_size.get()) + 5))) if (
                int(self.font_size.get()) < 120) else self.font_size.set(120))  # ctr + plus
        self.window.bind("<Control-minus>", lambda _: self.__font_changer(self.font_size.set(str(int(self.font_size.get()) - 5))) if (
                int(self.font_size.get()) > 5) else self.font_size.set(5))  # ctr + minus
        #To Save
        self.window.bind("<Control-S>", lambda _: self.fsave())  # ctr + S
        self.window.bind("<Control-s>", lambda _: self.fsave())  # ctr + s
        # To Save as
        self.window.bind("<Control-Shift-S>", lambda _: self.fsave_as())  # ctr + shift + S
        self.window.bind("<Control-Shift-s>", lambda _: self.fsave_as())  # ctr + shift + s
        # To Open
        self.window.bind("<Control-O>", lambda _: self.fopen())  # ctr + O
        self.window.bind("<Control-o>", lambda _: self.fopen())  # ctr + o
        # To New
        self.window.bind("<Control-N>", lambda _: self.new())  # ctr + N
        self.window.bind("<Control-n>", lambda _: self.new())  # ctr + n
        # To Delete All
        self.window.bind("<Shift-Delete>", lambda _: self.delete_all())  # shift + del
        # To Print
        self.window.bind("<Control-P>", lambda _: self.print_file())  # ctr + P
        self.window.bind("<Control-p>", lambda _: self.print_file())  # ctr + p

    # general methods..........................................................
    # cut
    def cut(self):
        self.text.event_generate("<<Cut>>")

    # copy the selected text
    def copy(self):
        self.text.event_generate("<<Copy>>")

    # paste the text from the clipboard
    def paste(self):
        self.text.event_generate("<<Paste>>")

    # select all the text from the text box
    def selectall(self):
        self.text.tag_add('sel', 1.0, "end")

    def undo(self):
        try:
            self.text.edit_undo()
        except:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except:
            pass

    # delete all text from the text box
    def delete_all(self):
        self.text.delete(1.0, "end")

    # popup about message box
    def about(self):
        messagebox.showinfo("About TextEditor",
                            "A Simple Text editor python application by Satz!\nSource Code at SatzGOD github or Click `Repository` in the Help Menu."
                            "\ninstagram: @satz_._")

    # helper methods.........................................................
    def __font_changer(self,*args):
        self.text.config(font=(self.font_style.get(), self.font_size.get()))

    def __fwonclosing(self):
        self.filemenu.entryconfig(5, state="normal")
        self.fw.destroy()

    def __color_fchanger(self):
        fcolor = colorchooser.askcolor(title="Choose a color for font")[1]
        self.fcolorbutton.config(bg=fcolor)
        self.text.config(fg=fcolor)

    def __color_bchanger(self):
        bcolor = colorchooser.askcolor(title="Choose a color for paper")[1]
        self.bcolorbutton.config(bg=bcolor)
        self.text.config(bg=bcolor)

    def __tripemp_func(self,*args):

        def __helper(style):
            if style in current_tag:
                self.text.tag_remove(style, "sel.first", "sel.last")
                self.tripemp.set("None")
            else:
                self.text.tag_add(style, "sel.first", "sel.last")

        try:
            if self.tripemp.get() == self.tripemp_list[0]:
                self.selectall()
                bold_font = font.Font(self.text, self.text.cget("font"))
                bold_font.configure(weight="bold")
                self.text.tag_configure("bold", font=bold_font)
                current_tag = self.text.tag_names("sel.first")
                __helper("bold")
            elif self.tripemp.get() == self.tripemp_list[1]:
                self.selectall()
                italic_font = font.Font(self.text, self.text.cget("font"))
                italic_font.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_font)
                current_tag = self.text.tag_names("sel.first")
                __helper("italic")
            elif self.tripemp.get() == self.tripemp_list[2]:
                self.selectall()
                underline_font = font.Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=True)
                self.text.tag_configure("underline", font=underline_font)
                current_tag = self.text.tag_names("sel.first")
                __helper("underline")
            else:
                self.tripemp.set("None")
        except:
            self.tripemp.set("None")

    def __dumpjson_and_destroy(self):
        data = {'x': self.window.winfo_x(), 'y': self.window.winfo_y(), 'w': self.window.winfo_width(),
                'h': self.window.winfo_height(),
                'path': self.path, 'state': self.state, 'fontstyle': self.font_style.get(),
                'fontsize': self.font_size.get()}
        with open('data.json', 'w') as f:
            dump(data, f, indent=4)
        self.window.destroy()

    # Theme methods ..............................................................
    def set_state(self, newstate):
        self.state = newstate
        self.themeSwitcher()

    def themeSwitcher(self):
        if self.state == 0:
            white = "#FFFFFF"
            defsyswhite = "#F0F0F0"
            black = "#000001"
            relief = "flat"
            highlightgrey = "#b0b0b0"
            font, size = "Consolas", "10"
            self.window.config(bg=defsyswhite)
            self.bottomframe.config(bg=defsyswhite)
            self.text.config(fg=black, bg=white)

            self.status_label.config(fg=black, bg=defsyswhite)
            self.menubar.config(bg=white, fg=black, relief=relief, activebackground=highlightgrey,
                                selectcolor=highlightgrey, font=(font, size))
            self.filemenu.config(bg=white, fg=black, relief=relief, activebackground=highlightgrey,
                                 selectcolor=highlightgrey, font=(font, size))
            self.editmenu.config(bg=white, fg=black, relief=relief, activebackground=highlightgrey,
                                 selectcolor=highlightgrey, font=(font, size))
            self.thememenu.config(bg=white, fg=black, relief=relief, activebackground=highlightgrey,
                                  selectcolor=highlightgrey, font=(font, size))
            self.helpmenu.config(bg=white, fg=black, relief=relief, activebackground=highlightgrey,
                                 selectcolor=highlightgrey, font=(font, size))

        elif self.state == 1:
            white = "white"
            textwhite = '#ebebeb'
            darkgrey = "#242424"
            lightgrey = "#414245"
            relief = "flat"
            font, size = "Consolas", "10"
            self.window.config(bg=darkgrey)
            self.bottomframe.config(bg=darkgrey)
            self.text.config(fg=textwhite, bg=lightgrey)
            self.status_label.config(bg=darkgrey, fg=white)
            self.menubar.config(bg=darkgrey, fg=white, relief=relief, activebackground=lightgrey,
                                selectcolor=lightgrey, font=(font, size))
            self.filemenu.config(bg=darkgrey, fg=white, relief=relief, activebackground=lightgrey,
                                 selectcolor=lightgrey, font=(font, size))
            self.editmenu.config(bg=darkgrey, fg=white, relief=relief, activebackground=lightgrey,
                                 selectcolor=lightgrey, font=(font, size))
            self.thememenu.config(bg=darkgrey, fg=white, relief=relief, activebackground=lightgrey,
                                  selectcolor=lightgrey, font=(font, size))
            self.helpmenu.config(bg=darkgrey, fg=white, relief=relief, activebackground=lightgrey,
                                 selectcolor=lightgrey, font=(font, size))

    def ts_fw(self):
        if self.state == 0:
            defsyswhite = "#F0F0F0"
            black = "#000001"
            relief = "groove"
            highlightgrey = "#b0b0b0"
            self.stylebox.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                 relief=relief, highlightthickness=False)
            self.sizebox.config(fg=black, bg=defsyswhite, relief=relief, highlightthickness=3,
                                highlightbackground=defsyswhite)
            self.fcolorbutton.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                     relief=relief)
            self.bcolorbutton.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                     relief=relief)
            self.tripempbox.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                   relief=relief)
            self.fw.config(bg=defsyswhite)
            self.frame.config(bg=defsyswhite)
            self.l1.config(bg=defsyswhite, fg=black)
            self.l2.config(bg=defsyswhite, fg=black)
            self.l3.config(bg=defsyswhite, fg=black)
        elif state == 1:
            white = "white"
            darkgrey = "#242424"
            lightdarkgrey = "#353535"
            lightgrey = "#414245"
            relief = "groove"
            self.stylebox.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                 relief=relief, highlightthickness=False)
            self.sizebox.config(bg=lightdarkgrey, fg=white, relief=relief, highlightthickness=3,
                                highlightbackground=lightdarkgrey)
            self.fcolorbutton.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                     relief=relief)
            self.bcolorbutton.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                     relief=relief)
            self.tripempbox.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                   relief=relief, highlightthickness=False)
            self.fw.config(bg=darkgrey)
            self.frame.config(bg=darkgrey)
            self.l1.config(bg=darkgrey, fg=white)
            self.l2.config(bg=darkgrey, fg=white)
            self.l3.config(bg=darkgrey, fg=white)