import subprocess
import tkinter.messagebox
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk

window = Tk()
window.title("Notepad++")
menu = Menu(window)
window.config(menu=menu)
ico = Image.open('icon.ico')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)
editor = ScrolledText(window,font=("Consolas 12"), wrap=None)
editor.pack(fill=BOTH, expand=1)
editor.focus()
file_path = ""
def open_file(event=None):
    global code, file_path
    open_path = askopenfilename(filetypes=[("All files", "*.*")])
    file_path = open_path
    with open(open_path, "r") as file:
        code = file.read()
        editor.delete(1.0, END)
        editor.insert(1.0, code)
window.bind("<Control-o>", open_file)
def save_file(event=None):
    global code, file_path
    if file_path == '':
        save_path = asksaveasfilename(defaultextension = ".txt", filetypes=[("All Files", "*.*")])
        file_path =save_path
    else:
        save_path = file_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code) 
window.bind("<Control-s>", save_file)
def save_as(event=None):
    global code, file_path
    save_path = asksaveasfilename(defaultextension = ".py", filetypes=[("Python File", "*.py")])
    file_path = save_path
    with open(save_path, "w") as file:
        code = editor.get(1.0, END)
        file.write(code) 
window.bind("<Control-S>", save_as)
def run(event=None):
    global code, file_path
    '''
    code = editor.get(1.0, END)
    exec(code)
    '''    
    cmd = f"python {file_path}"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)
    output, error =  process.communicate()
    output_window.delete(1.0, END)
    output_window.insert(1.0, output)
    output_window.insert(1.0, error)
window.bind("<Control-r>", run)
def close(event=None):
    window.destroy()
window.bind("<Control-q>", close)
def cut_text(event=None):
        editor.event_generate(("<<Cut>>"))
def copy_text(event=None):
        editor.event_generate(("<<Copy>>"))
def paste_text(event=None):
        editor.event_generate(("<<Paste>>"))
def about():
    showinfo("Notepad", "Made by Rakshit Dogra")

def version():
    showinfo("Notepad", "Version: 1.0.0")

file_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
view_menu = Menu(menu, tearoff=0)
theme_menu = Menu(menu, tearoff=0)
about_menu = Menu(menu, tearoff=0)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_cascade(label ="View", menu=view_menu)
menu.add_cascade(label ="Theme", menu=theme_menu)
menu.add_cascade(label ="About", menu=about_menu)

file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=close)

edit_menu.add_command(label="Cut", command=cut_text) 
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
run_menu.add_command(label="Run", accelerator="Crtl+R", command=run)
about_menu.add_command(label="About", command=about) 
about_menu.add_command(label="Version", command=version) 

show_status_bar = BooleanVar()
show_status_bar.set(True)
def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar = False 
    else :
        status_bars.pack(side=BOTTOM)
        show_status_bar = True
        
view_menu.add_checkbutton(label = "Status Bar" , onvalue = True, offvalue = 0,variable = show_status_bar , command = hide_statusbar)
status_bars = ttk.Label(window,text = "characters: 0 words: 0")
status_bars.pack(side = BOTTOM)
text_change = False
def change_word(event = None):
    global text_change
    if editor.edit_modified():
        text_change = True
        word = len(editor.get(1.0, "end-1c").split())
        chararcter = len(editor.get(1.0, "end-1c").replace(" ",""))
        status_bars.config(text = f"characters: {chararcter} words: {word}")
    editor.edit_modified(False)
editor.bind("<<Modified>>",change_word)
def light():
    editor.config(fg="black", bg="#dbdbdb")
    output_window.config(fg="black", bg="#dbdbdb")
def dark():
    editor.config(fg="white", bg="#242222")
    output_window.config(fg="white", bg="#242222")
theme_menu.add_command(label="Light", command=light)
theme_menu.add_command(label="Dark", command=dark)
output_window = ScrolledText(window, height=10)
output_window.pack(fill=BOTH, expand=1)
window.mainloop()