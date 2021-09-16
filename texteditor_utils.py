from tkinter import colorchooser, filedialog, messagebox
from os.path import exists
from win32print import GetDefaultPrinter
from win32api import ShellExecute
from json import dump
from time import sleep

app_name = "TextEditor"


class TextEditorUtils:

    def __init__(self, window, path, state, font_style, font_size, statusL_text, fcolorbutton, bcolorbutton, text,
                 bottomframe, stylebox, sizebox, status_label, menubar, filemenu, editmenu, thememenu, helpmenu):
        self.path = path
        self.window = window
        self.state = state
        self.font_style = font_style
        self.font_size = font_size
        self.statusL_text = statusL_text
        self.fcolorbutton = fcolorbutton
        self.bcolorbutton = bcolorbutton
        self.text = text
        self.bottomframe = bottomframe
        self.stylebox = stylebox
        self.sizebox = sizebox
        self.status_label = status_label
        self.menubar = menubar
        self.filemenu = filemenu
        self.editmenu = editmenu
        self.thememenu = thememenu
        self.helpmenu = helpmenu

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

    # delete the entier text from the text box
    def delete_all(self):
        self.text.delete(1.0, "end")

    # popup about message box
    def about(self):
        messagebox.showinfo("About TextEditor",
                            "A Simple Text editor python application by Satz!\nSource Code at SatzGOD github or Click `Repository` in the Help Menu."
                            "\ninstagram: @satz_._")

    # foreground color changer
    def color_fchanger(self):
        fcolor = colorchooser.askcolor(title="Choose a color for font")[1]
        self.fcolorbutton.config(bg=fcolor)
        self.text.config(fg=fcolor)

    # background color changer
    def color_bchanger(self):
        bcolor = colorchooser.askcolor(title="Choose a color for paper")[1]
        self.bcolorbutton.config(bg=bcolor)
        self.text.config(bg=bcolor)

    # font changer
    def font_changer(self, *args):
        self.text.config(font=(self.font_style.get(), self.font_size.get()))

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
            sleep(0.1)

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

            # Helper function

    def __dumpjson_and_destroy(self):
        data = {'x': self.window.winfo_x(), 'y': self.window.winfo_y(), 'w': self.window.winfo_width(),
                'h': self.window.winfo_height(),
                'path': self.path, 'state': self.state, 'fontstyle': self.font_style.get(),
                'fontsize': self.font_size.get()}
        with open('data.json', 'w') as f:
            dump(data, f, indent=4)
        self.window.destroy()

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
            self.stylebox.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                 relief=relief, highlightthickness=False)
            self.sizebox.config(fg=black, bg=defsyswhite, relief=relief, highlightthickness=3,
                                highlightbackground=defsyswhite)
            self.fcolorbutton.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                     relief=relief)
            self.bcolorbutton.config(fg=black, bg=defsyswhite, activebackground=highlightgrey, activeforeground=black,
                                     relief=relief)
            self.status_label.config(fg=black, bg=defsyswhite)
            self.menubar.config(bg=white,fg=black,relief=relief,activebackground=highlightgrey,selectcolor=highlightgrey,font=(font, size))
            self.filemenu.config(bg=white,fg=black,relief=relief,activebackground=highlightgrey,selectcolor=highlightgrey,font=(font, size))
            self.editmenu.config(bg=white,fg=black,relief=relief,activebackground=highlightgrey,selectcolor=highlightgrey,font=(font, size))
            self.thememenu.config(bg=white,fg=black,relief=relief,activebackground=highlightgrey,selectcolor=highlightgrey,font=(font, size))
            self.helpmenu.config(bg=white,fg=black,relief=relief,activebackground=highlightgrey,selectcolor=highlightgrey,font=(font, size))
            # filemenu.config(bg="#1B1B1B", fg="white", activeborderwidth=2, relief=FLAT, activebackground="#646464",
            #                 selectcolor="#2B2B2B", font=("Consolas", "10"))
        elif self.state == 1:
            white = "white"
            textwhite = '#ebebeb'
            darkgrey = "#242424"
            lightdarkgrey = "#353535"
            lightgrey = "#414245"
            relief = "flat"
            font, size = "Consolas", "10"
            self.window.config(bg=darkgrey)
            self.bottomframe.config(bg=darkgrey)
            self.text.config(fg=textwhite, bg=lightgrey)
            self.stylebox.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                 relief=relief, highlightthickness=False)
            self.sizebox.config(bg=lightdarkgrey, fg=white, relief=relief, highlightthickness=3,
                                highlightbackground=lightdarkgrey)
            self.fcolorbutton.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                     relief=relief)
            self.bcolorbutton.config(bg=lightdarkgrey, fg=white, activebackground=lightgrey, activeforeground=white,
                                     relief=relief)
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

    def bottomFrame_commandsetters(self):
        self.sizebox.config(command=self.font_changer)
        self.fcolorbutton.config(command=self.color_fchanger)
        self.bcolorbutton.config(command=self.color_bchanger)
