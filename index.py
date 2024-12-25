from tkinter import *
from tkinter import TclError, filedialog, colorchooser, messagebox
import tkinter.font as tkFont  # Importing the font module
import os  # Importing os for print functionality

class MYNotepad:
    def _init_(self, master):
        self.master = master
        master.title("My Notepad")
        try:
            master.wm_iconbitmap("notepad.ico")
        except TclError:
            print("Icon file not found or invalid. Using default icon.")

        # Initialize current file and font
        self.current_file = None
        self.font_style = tkFont.Font(family="Arial", size=12)  # Default font style

        # Creating the text widget
        self.txt = Text(master, padx=5, pady=5, wrap=WORD, selectbackground="red", bd=2, insertwidth=3, undo=True, font=self.font_style)
        self.txt.pack(fill=BOTH, expand=1)

        # Creating the main menu
        self.main_menu = Menu(master)
        master.config(menu=self.main_menu)

        # Creating the file menu
        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="FILE", menu=self.file_menu)

        # Adding options to the file menu
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.saveas_file)
        self.file_menu.add_command(label="Print", accelerator="Ctrl+P", command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        # Creating the edit menu
        self.edit_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="EDIT", menu=self.edit_menu)

        # Adding options to the edit menu
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo_file)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_file)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_file)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", command=self.delete_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)

        # Creating the color menu
        self.color_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Color", menu=self.color_menu)

        # Adding options to the color menu
        self.color_menu.add_command(label="Background Color", command=self.change_back_color)
        self.color_menu.add_command(label="Foreground Color", command=self.change_fore_color)

        # Creating the format menu
        self.format_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Format", menu=self.format_menu)

        # Adding font size and style options to the format menu
        self.format_menu.add_command(label="Increase Font Size", accelerator="Ctrl+=", command=self.increase_font_size)
        self.format_menu.add_command(label="Decrease Font Size", accelerator="Ctrl+-", command=self.decrease_font_size)
        self.format_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", accelerator="Ctrl+U", command=self.toggle_underline)

        # Keyboard shortcuts
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-p>", lambda event: self.print_file())  # Shortcut for print
        self.master.bind("<Control-z>", lambda event: self.undo_file())
        self.master.bind("<Control-y>", lambda event: self.redo_file())
        self.master.bind("<Control-x>", lambda event: self.cut_file())
        self.master.bind("<Control-c>", lambda event: self.copy_file())
        self.master.bind("<Control-v>", lambda event: self.paste_file())
        self.master.bind("<Control-+>", lambda event: self.increase_font_size())  # Increase font size
        self.master.bind("<Control-minus>", lambda event: self.decrease_font_size())  # Decrease font size
        self.master.bind("<Control-b>", lambda event: self.toggle_bold())  # Bold
        self.master.bind("<Control-i>", lambda event: self.toggle_italic())  # Italic
        self.master.bind("<Control-u>", lambda event: self.toggle_underline())  # Underline
        self.master.bind("<Control-a>", lambda event: self.select_all())  # Select All

    def new_file(self):
        if self.txt.edit_modified():
            if not self.confirm_save():
                return
        self.txt.delete(1.0, END)
        self.current_file = None
        self.txt.edit_modified(False)

    def open_file(self):
        if self.txt.edit_modified():
            if not self.confirm_save():
                return
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", ".txt"), ("All Files", ".*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.txt.delete(1.0, END)
            self.txt.insert(END, content)
            self.current_file = file_path
            self.txt.edit_modified(False)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                content = self.txt.get(1.0, END)
                file.write(content.strip())
            self.txt.edit_modified(False)
        else:
            self.saveas_file()

    def saveas_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", ".txt"), ("All Files", ".*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.txt.get(1.0, END)
                file.write(content.strip())
            self.current_file = file_path
            self.txt.edit_modified(False)

    def print_file(self):
        if self.current_file:
            os.startfile(self.current_file, "print")  # Sends the file to the printer
        else:
            temp_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", ".txt")])
            if temp_file:
                with open(temp_file, "w") as file:
                    content = self.txt.get(1.0, END).strip()
                    file.write(content)
                os.startfile(temp_file, "print")

    def exit_app(self):
        if self.txt.edit_modified():
            answer = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before exiting?")
            if answer:  # Yes, save and exit
                self.save_file()
                self.master.quit()
            elif answer is None:  # Cancel, do nothing
                return
            else:  # No, exit without saving
                self.master.quit()
        else:
            self.master.quit()  # No changes, exit directly

    def confirm_save(self):
        answer = messagebox.askyesnocancel("Save Changes", "Do you want to save changes?")
        if answer:  # Yes, save
            self.save_file()
            return True
        elif answer is None:  # Cancel
            return False
        else:  # No
            return True

    def undo_file(self):
        try:
            self.txt.edit_undo()
        except TclError:
            pass

    def redo_file(self):
        try:
            self.txt.edit_redo()
        except TclError:
            pass

    def cut_file(self):
        self.copy_file()
        self.txt.delete(SEL_FIRST, SEL_LAST)

    def copy_file(self):
        try:
            self.master.clipboard_clear()
            text = self.txt.get(SEL_FIRST, SEL_LAST)
            self.master.clipboard_append(text)
        except TclError:
            pass

    def paste_file(self):
        try:
            text = self.master.clipboard_get()
            self.txt.insert(INSERT, text)
        except TclError:
            pass

    def delete_text(self):
        try:
            self.txt.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def change_back_color(self):
        color = colorchooser.askcolor()[1]  # Returns a tuple, we need the color code
        if color:
            self.txt.config(bg=color)

    def change_fore_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.txt.config(fg=color)

    def increase_font_size(self):
        current_size = self.font_style.cget("size")
        new_size = current_size + 2
        self.font_style.config(size=new_size)

    def decrease_font_size(self):
        current_size = self.font_style.cget("size")
        new_size = current_size - 2
        self.font_style.config(size=new_size)

    def toggle_bold(self):
        current_weight = self.font_style.cget("weight")
        new_weight = "bold" if current_weight != "bold" else "normal"
        self.font_style.config(weight=new_weight)

    def toggle_italic(self):
        current_slant = self.font_style.cget("slant")
        new_slant = "italic" if current_slant != "italic" else "roman"
        self.font_style.config(slant=new_slant)

    def toggle_underline(self):
        current_underline = self.font_style.cget("underline")
        new_underline = 1 if current_underline == 0 else 0
        self.font_style.config(underline=new_underline)

    def select_all(self):
        self.txt.tag_add("sel", "1.0", "end")
        self.txt.mark_set("insert", "1.0")
        self.txt.see("insert")


root = Tk()
app = MYNotepad(root)
root.mainloop()