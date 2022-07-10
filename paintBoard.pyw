
from tkinter import Menu, colorchooser
from tkinter.ttk import *
import tkinter as tk
from PIL import Image, ImageTk
from Modules.start import changeBackgroundColor, save, replace, openfile
from Modules.paint import weidth_appear, dele
from Modules.canvas import resize

window = tk.Tk()
window.title('paint')
window.geometry('1000x700')
window.iconphoto(True, tk.PhotoImage(file='icon\\paint_icon.png'))


class paint:
    def __init__(self):
        self.brushtype = 'pencil'
        self.color = 'black'
        self.backgroundColor = 'white'
        self.fillColor = ''
        self.entry = None
        self.text = None
        self.img = None
        self.img2 = None
        self.save_path = None
        self.name = None
        self.open_path = None
        self.openImg = None
        self.openfilename2 = None
        self.save = False
        self.width = 2
        self.x_ = 750
        self.y_ = 500
        self.dele_list = [[], []]

    def save_init_(self, save_type, save_back):
        self.save_type = save_type
        self.type_number = save_back
        self.save_file()

    def click(self, event):
        self.last_pos, self.linepos = [event.x, event.y], [event.x, event.y]
        if self.brushtype == 'text':
            cv.delete(self.text)
            if self.entry is None:
                self.entry = Entry(
                    window, foreground=self.color, width=3)
                self.text = cv.create_window(
                    event.x, event.y, window=self.entry)
                self.text_pos, self.nu = [event.x, event.y], 0
            else:
                if self.entry.get() != '':
                    text = cv.create_text(self.text_pos[0], self.text_pos[1], text=self.entry.get(
                    ), fill=self.color)
                    self.dele_list[0].append(text)
                    self.nu, self.entry = 1, None

        else:
            if self.brushtype == 'line':
                self.line_creat = cv.create_line(
                    self.linepos[0], self.linepos[1], event.x, event.y, fill=self.color, width=self.width)
            elif self.brushtype == 'rectangle':
                self.r_creat = cv.create_rectangle(
                    self.linepos[0], self.linepos[1], event.x, event.y, outline=self.color, width=self.width, fill=self.fillColor)
            elif self.brushtype == 'circle':
                self.circle = cv.create_oval(
                    self.linepos[0], self.linepos[1], event.x, event.y, outline=self.color, width=self.width, fill=self.fillColor)
            self.nu = 0
            cv.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        if self.brushtype == 'pencil':
            a = cv.create_line(self.last_pos[0], self.last_pos[1], event.x,
                               event.y, fill=self.color, width=self.width, capstyle='round', smooth=True)
            self.dele_list[0].append(a)
            self.nu += 1
            self.last_pos = [event.x, event.y]
        if self.brushtype == 'eraser':
            a = cv.create_line(self.last_pos[0], self.last_pos[1], event.x,
                               event.y, fill='white', width=self.width, capstyle='round', smooth=True)
            self.dele_list[0].append(a)
            self.nu += 1
            self.last_pos = [event.x, event.y]

        elif self.brushtype == 'line':
            cv.coords(self.line_creat, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.line_creat not in self.dele_list[0]:
                self.dele_list[0].append(self.line_creat)
            self.nu = 1
        elif self.brushtype == 'rectangle':
            cv.coords(self.r_creat, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.r_creat not in self.dele_list[0]:
                self.dele_list[0].append(self.r_creat)
            self.nu = 1
        elif self.brushtype == 'circle':
            cv.coords(self.circle, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.circle not in self.dele_list[0]:
                self.dele_list[0].append(self.circle)
            self.nu = 1

    def stop(self, event):
        if self.nu != 0:
            self.dele_list[1].append(self.nu)

    def pop(self, event):
        popmenu.post(event.x_root, event.y_root)

    def changeBrush(self, brush):
        self.brushtype = brush

    def Color(self):
        self.color = colorchooser.askcolor()[1]

    def Fill(self):
        self.fillColor = colorchooser.askcolor()[1]

    def ChangeWidth(self, width):
        if width == 'input':
            self.width = weidth_appear(self.width)
        else:
            self.width = width

    def dele(self):
        self.dele_list = dele(cv, self.dele_list)

    def save_file(self):
        returnvalue = save(self.save_path, window, self.name, self.open_path,
                           cv, self.save_type, self.type_number)
        self.save_path, self.name, self.open_path = returnvalue[
            0], returnvalue[1], returnvalue[2]

    def openfile(self):
        global background_r
        ret = openfile(cv, window, self.img, self.x_, self.y_, self.name, self.open_path,
                       background_r, self.backgroundColor, self.dele_list, self.img2, self.openImg, self.openfilename2)
        try:
            self.img, self.x_, self.y_, self.name, self.open_path, background_r, self.backgroundColor, self.dele_list, self.img2, self.openImg, self.openfilename2 = ret[
                0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9], ret[10]
        except:
            pass

    def save_replace(self):
        replace(self.name, self.open_path, cv, self)

    def resize(self):
        global background_r
        ret = resize(cv, self.x_, self.y_, background_r)
        self.x_, self.y_, background_r = ret[0], ret[1], ret[2]

    def bg_color(self):
        global background_r
        ret = changeBackgroundColor(cv, self.backgroundColor, background_r, self.name,
                                    self.img, self.img2, self.openImg, self.openfilename2)
        self.backgroundColor, background_r, self.img2, self.openImg = ret[
            0], ret[1], ret[2], ret[3]

    def clear_new(self, mode):
        if mode == 'clear':
            for id in self.dele_list[0]:
                cv.delete(id)
            self.dele_list = [[], []]
        else:
            cv.delete(tk.ALL)

    def savehotkey(self, event):
        self.save_replace()

    def undohotkey(self, event):
        self.dele()

    def openhotkey(self, event):
        self.openfile()


funcPaint = paint()

menu = Menu(window)
filemenu = Menu(menu)
paintmenu = Menu(menu)
canvasmenu = Menu(menu)
brushmenu = Menu(menu)
typemenu = Menu(menu)
widthmenu = Menu(menu)
popmenu = Menu(menu)
window.config(menu=menu)
menu.add_cascade(label='Start', menu=filemenu)
menu.add_cascade(label='Paint', menu=paintmenu)
menu.add_cascade(label='Canvas', menu=canvasmenu)
popmenu.add_command(label='undo', command=funcPaint.dele)
filemenu.add_command(label='save', command=funcPaint.save_replace)
filemenu.add_cascade(label='saveAs', menu=typemenu)
filemenu.add_command(label='open', command=funcPaint.openfile)
typemenu.add_command(
    label='PNG', command=lambda: funcPaint.save_init_('PNG', '.png'))
typemenu.add_command(
    label='JPG', command=lambda: funcPaint.save_init_('JPEG', '.jpeg'))
typemenu.add_command(
    label='GIF', command=lambda: funcPaint.save_init_('GIF', '.gif'))
canvasmenu.add_command(label='resize', command=funcPaint.resize)
canvasmenu.add_command(label='bgcolor', command=funcPaint.bg_color)
canvasmenu.add_command(label='clear canvas',
                       command=lambda: funcPaint.clear_new('clear'))
canvasmenu.add_command(
    label='new canvas', command=lambda: funcPaint.clear_new('new'))
paintmenu.add_cascade(label='Brush', menu=brushmenu)
brushmenu.add_command(
    label='pencil', command=lambda: funcPaint.changeBrush('pencil'))
brushmenu.add_command(
    label='eraser', command=lambda: funcPaint.changeBrush('eraser'))
brushmenu.add_command(
    label='line', command=lambda: funcPaint.changeBrush('line'))
brushmenu.add_command(
    label='rectangle', command=lambda: funcPaint.changeBrush('rectangle'))
brushmenu.add_command(
    label='text', command=lambda: funcPaint.changeBrush('text'))
brushmenu.add_command(
    label='circle', command=lambda: funcPaint.changeBrush('circle'))
paintmenu.add_cascade(label='Width', menu=widthmenu)
img1 = ImageTk.PhotoImage(Image.open('Icon\\1.png'))
widthmenu.add_command(command=lambda: funcPaint.ChangeWidth(2), image=img1)
img2 = ImageTk.PhotoImage(Image.open('Icon\\2.png'))
widthmenu.add_command(command=lambda: funcPaint.ChangeWidth(25), image=img2)
img3 = ImageTk.PhotoImage(Image.open('Icon\\3.png'))
widthmenu.add_command(command=lambda: funcPaint.ChangeWidth(50), image=img3)
img4 = ImageTk.PhotoImage(Image.open('Icon\\4.png'))
widthmenu.add_command(command=lambda: funcPaint.ChangeWidth(75), image=img4)
paintmenu.add_command(label='color', command=funcPaint.Color)
paintmenu.add_command(label='fill color', command=funcPaint.Fill)
widthmenu.add_command(
    label=' other', command=lambda: funcPaint.ChangeWidth('input'))
cv = tk.Canvas(window, width=funcPaint.x_, height=funcPaint.y_, bg='white')
background_r = cv.create_rectangle(
    0, 0, funcPaint.x_+10, funcPaint.y_+10, fill='white', outline='white')
cv.pack(side='left', anchor='nw')
cv.bind('<Button-1>', funcPaint.click)
cv.bind('<Button-3>', funcPaint.pop)
cv.bind('<ButtonRelease-1>', funcPaint.stop)
window.bind('<Control-s>', funcPaint.savehotkey)
window.bind('<Control-z>', funcPaint.undohotkey)
window.bind('<Control-o>', funcPaint.openhotkey)
window.mainloop()
