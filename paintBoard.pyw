
from tkinter import Menu, Toplevel, colorchooser
from tkinter.ttk import *
import tkinter as tk
from PIL import Image, ImageTk
from Modules.start import save, replace, openfile
from Modules.paint import changeBackgroundColor, dele
import matplotlib.pyplot as plt
import ttkbootstrap as tkb
import numpy as np

window = tkb.Window()
window.title('paint')
window.geometry('1200x800+%d+%d' % (
    (window.winfo_screenwidth()-1200) / 2, (window.winfo_screenheight()-800) / 2))
window.configure(bg='whitesmoke')


class FUNC:
    # init
    def __init__(self):
        self.brushtype = 'pencil'
        self.fgcolor = 'black'
        self.backgroundColor = 'white'
        self.bgColor = ''
        self.entry = self.text = self.img = self.img2 = self.savePath = self.name = self.openPath = self.openImg = self.holeName = self.save = None
        self.width = 2
        self.X = 1200
        self.Y = 800
        self.dele_list = [[], []]
    # paint

    def click(self, event):
        self.last_pos, self.linepos = [event.x, event.y], [event.x, event.y]
        if self.brushtype == 'text':
            cv.delete(self.text)
            if self.entry is None:
                self.entry = Entry(
                    window, foreground=self.fgcolor, width=3)
                self.text = cv.create_window(
                    event.x, event.y, window=self.entry)
                self.text_pos, self.number = [event.x, event.y], 0
            else:
                if self.entry.get() != '':
                    text = cv.create_text(self.text_pos[0], self.text_pos[1], text=self.entry.get(
                    ), fill=self.fgcolor)
                    self.dele_list[0].append(text)
                    self.number, self.entry = 1, None

        else:
            if self.brushtype == 'line':
                self.line_creat = cv.create_line(
                    self.linepos[0], self.linepos[1], event.x, event.y, fill=self.fgcolor, width=self.width)
            elif self.brushtype == 'rectangle':
                self.r_creat = cv.create_rectangle(
                    self.linepos[0], self.linepos[1], event.x, event.y, outline=self.fgcolor, width=self.width, fill=self.bgColor)
            elif self.brushtype == 'circle':
                self.circle = cv.create_oval(
                    self.linepos[0], self.linepos[1], event.x, event.y, outline=self.fgcolor, width=self.width, fill=self.bgColor)
            self.number = 0
            cv.bind("<B1-Motion>", self.move)

    def move(self, event):
        if self.brushtype == 'pencil':
            a = cv.create_line(self.last_pos[0], self.last_pos[1], event.x,
                               event.y, fill=self.fgcolor, width=self.width, capstyle='round', smooth=True)
            self.dele_list[0].append(a)
            self.number += 1
            self.last_pos = [event.x, event.y]
        if self.brushtype == 'eraser':
            a = cv.create_line(self.last_pos[0], self.last_pos[1], event.x,
                               event.y, fill='white', width=self.width, capstyle='round', smooth=True)
            self.dele_list[0].append(a)
            self.number += 1
            self.last_pos = [event.x, event.y]

        elif self.brushtype == 'line':
            cv.coords(self.line_creat, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.line_creat not in self.dele_list[0]:
                self.dele_list[0].append(self.line_creat)
            self.number = 1
        elif self.brushtype == 'rectangle':
            cv.coords(self.r_creat, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.r_creat not in self.dele_list[0]:
                self.dele_list[0].append(self.r_creat)
            self.number = 1
        elif self.brushtype == 'circle':
            cv.coords(self.circle, self.linepos[0],
                      self.linepos[1], event.x, event.y)
            if self.circle not in self.dele_list[0]:
                self.dele_list[0].append(self.circle)
            self.number = 1

    def stop(self, event):
        try:
            if self.number != 0:
                self.dele_list[1].append(self.number)
        except:
            pass

    def changeBrush(self, brush):
        self.brushtype = brush

    def Color(self):
        self.fgcolor = colorchooser.askcolor()[1]

    def Fill(self):
        self.bgColor = colorchooser.askcolor()[1]

    def ChangeWidth(self, width):
        self.width = width

    def dele(self):
        self.dele_list = dele(cv, self.dele_list)
    # file

    def save_file(self):
        returnvalue = save(self.savePath, window, self.name, self.openPath,
                           cv, self.save_type, self.type_number)
        self.savePath, self.name, self.openPath = returnvalue[
            0], returnvalue[1], returnvalue[2]

    def openfile(self, isInsert):
        global background_rectangle
        ret = openfile(cv, window, self.img, self.X, self.Y, self.name, self.openPath,
                       background_rectangle, self.backgroundColor, self.dele_list, self.img2, self.openImg, self.holeName, isInsert)
        try:
            self.img, self.X, self.Y, self.name, self.openPath, background_rectangle, self.backgroundColor, self.dele_list, self.img2, self.openImg, self.holeName = ret[
                0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9], ret[10]
            if isInsert is False:
                pass
            else:
                cv.tag_bind(self.openImg, '<B3-Motion>', self.insertMove)
        except:
            pass

    def insertMove(self, event):
        cv.coords(self.openImg, (event.x-50, event.y-50))
        pass

    def save_replace(self):
        replace(self.name, self.openPath, cv, self)

    def save_as(self, save_type, save_back):
        self.save_type = save_type
        self.type_number = save_back
        self.save_file()
    # canvas

    def resize(self):
        root = Toplevel()
        root.title('resize')
        root.resizable(0, 0)
        root.geometry('260x115+%d+%d' %
                      (window.winfo_x()+window.winfo_width() / 2-130, window.winfo_y()+window.winfo_height() / 2-57))
        XLabel = tkb.Label(root, text='width:')
        oldx = tk.StringVar(value=str(self.X))
        oldy = tk.StringVar(value=str(self.Y))
        XEntry = tkb.Entry(root, width=15, textvariable=oldx)
        YLabel = tkb.Label(root, text='height:')
        YEntry = tkb.Entry(root, width=15, textvariable=oldy)
        Button = tkb.Button(root, text='ok', command=lambda: self.ResizeGet(
            root, XEntry.get(), YEntry.get()), bootstyle='success-outline')
        Button.grid(column=2, row=2, padx=4, pady=3, ipadx=10)
        XLabel.grid(column=0, row=0, ipadx=5, pady=2)
        XEntry.grid(column=1, row=0, pady=2)
        YLabel.grid(column=0, row=1, ipadx=5, pady=2)
        YEntry.grid(column=1, row=1, pady=2)
        root.mainloop()

    def ResizeGet(self, root, input_x, input_y):
        root.destroy()
        if input_x != None and input_y != None:
            try:
                input_x, input_y = int(input_x), int(input_y)
                cv.configure(width=input_x, height=input_y)
                cv.coords(background_rectangle, 0, 0,
                          int(input_x)+10, int(input_y)+10)
                self.X = input_x
                self.Y = input_y
            except:
                pass

    def bg_color(self):
        global background_rectangle
        ret = changeBackgroundColor(cv, self.backgroundColor, background_rectangle, self.name,
                                    self.img, self.img2, self.openImg, self.holeName)
        self.backgroundColor, background_rectangle, self.img2, self.openImg = ret[
            0], ret[1], ret[2], ret[3]

    def clear_new(self, mode):
        if mode == 'clear':
            for id in self.dele_list[0]:
                cv.delete(id)
            self.dele_list = [[], []]
        else:
            cv.delete(tk.ALL)
    # hotkey

    def savehotkey(self, event):
        self.save_replace()

    def undohotkey(self, event):
        self.dele()

    def openhotkey(self, event):
        self.openfile()
    # chart

    def newChartWindow(self, get):
        root = Toplevel()
        root.title('new chart')
        root.resizable(False, False)
        window.update()
        frame = tkb.Frame(root)
        frame.pack(side='top')
        root.geometry('510x195+%d+%d' %
                      (window.winfo_x()+window.winfo_width() / 2-255, window.winfo_y()+window.winfo_height() / 2-97))
        button = tkb.Button(root, text='next',
                            command=lambda: self.getValueOfChart(root, get), bootstyle="success-outline")
        pointValue = tkb.Label(
            frame, text="""The value of a chart:""", font=('microsoft yahei', 10))
        graphUnit = tkb.Label(frame, text='Name of chart',
                              font=('microsoft yahei', 10))
        self.pointValueEntry = tkb.Entry(frame)
        self.pointUnitEntry = tkb.Entry(frame)
        self.formatImg = ImageTk.PhotoImage(Image.open("Icon\\format.png"))
        label = tkb.Label(
            root, image=self.formatImg, font=('microsoft yahei', 10), bootstyle='primary', justify='center')
        button.pack(side='right', anchor='se', padx=3, pady=3)
        pointValue.grid(column=0, row=0, padx=10, pady=5)
        graphUnit.grid(column=0, row=1, padx=10, pady=5)
        self.pointValueEntry.grid(column=2, row=0, pady=5)
        self.pointUnitEntry.grid(column=2, row=1, pady=5)
        label.pack(side='bottom', anchor='se', padx=15, pady=5)

        root.mainloop()

    def getValueOfChart(self, root, get):
        value = self.pointValueEntry.get()
        Name = self.pointUnitEntry.get()
        nameList = []
        if get == 1 or get == 2:
            objectsDict = {}
            value = value.split(")")
            for item in value:
                itemValue = item.replace('(', '')
                itemList = itemValue.split(',')
                if itemList != ['']:
                    nameList.append(itemList[0])
                    del itemList[0]
                    for i in range(len(itemList)):
                        item = itemList[i].split(':')
                        if item[0] not in objectsDict:
                            objectsDict[item[0]] = [int(item[1])]
                        else:
                            for key in sorted(objectsDict.keys()):
                                if key == item[0]:
                                    objectsDict[key].append(int(item[1]))
        else:
            valueList = []
            value = value.split(",")
            for item in value:
                itemList = item.split(':')
                nameList.append(itemList[0])
                valueList.append(int(itemList[1]))
        root.destroy()
        plt.figure(figsize=(10, 5), dpi=100)
        color = ['red', 'yellow', 'green', 'blue']
        kindLine = ['-', '--', '-.', ':']
        index = 0
        number = 0
        if get == 3:
            plt.pie(valueList, labels=nameList, autopct='%1.2f%%')
        else:
            for key, value in objectsDict.items():
                if index == 4:
                    index = 0
                if get == 1:
                    plt.plot(nameList, value, label=key,
                             c=color[index], linestyle=kindLine[index])
                    plt.scatter(nameList, value, c=color[index])
                    if Name == '':
                        plt.title("line chart")
                    else:
                        plt.title(Name)
                elif get == 2:
                    plt.xticks(np.arange(len(nameList))+0.17,
                               nameList, fontsize=12)
                    plt.bar(x=np.arange(len(nameList))+number, height=value, width=0.2, label=key,
                            edgecolor='white', color=color[index], tick_label=nameList)
                    if Name == '':
                        plt.title("bar chart")
                    else:
                        plt.title(Name)
            index += 1
            number += 0.2
        plt.legend()
        plt.show()


class ITEMS:
    def __init__(self):
        global funcPaint
        # items in menu Paint
        frame = tkb.Frame(window)
        frame.pack(side='top', anchor='nw', ipadx=3000)
        self.Insert = tkb.Button(
            frame, text='Insert', bootstyle='outline', command=lambda: funcPaint.openfile(True))
        self.Brushes = tkb.Menubutton(
            frame, text='Brushes', bootstyle="outline")
        self.Shapes = tkb.Menubutton(
            frame, text='Shapes', bootstyle="outline")
        self.Size = tkb.Scale(frame, from_=2, to=100,
                              bootstyle='info', command=funcPaint.ChangeWidth)
        self.Color = tkb.Menubutton(
            frame, text='Color', bootstyle="outline")
        self.SizeLabel = tkb.Label(frame, text='brush size',
                                   font=('', 11), bootstyle='primary')
        brushmenu = tkb.Menu(self.Brushes, relief='flat', activeborderwidth=5)
        shapemenu = tkb.Menu(self.Shapes, relief='flat', activeborderwidth=5)
        colormenu = tkb.Menu(self.Color, relief='flat', activeborderwidth=5)
        brushmenu.add_command(
            label='pencil', command=lambda: funcPaint.changeBrush('pencil'))
        brushmenu.add_command(
            label='eraser', command=lambda: funcPaint.changeBrush('eraser'))
        brushmenu.add_command(
            label='text', command=lambda: funcPaint.changeBrush('text'))
        shapemenu.add_command(
            label='line', command=lambda: funcPaint.changeBrush('line'))
        shapemenu.add_command(
            label='rectangle', command=lambda: funcPaint.changeBrush('rectangle'))
        shapemenu.add_command(
            label='circle', command=lambda: funcPaint.changeBrush('circle'))
        colormenu.add_command(label='foreground color',
                              command=funcPaint.Color)
        colormenu.add_command(label='background color', command=funcPaint.Fill)
        self.Brushes.config(menu=brushmenu)
        self.Shapes.config(menu=shapemenu)
        self.Color.config(menu=colormenu)
        # items in menu Canvas
        self.Resize = tkb.Button(frame, text='Resize',
                                 bootstyle='outline', command=funcPaint.resize)
        self.BackgroundColor = tkb.Button(
            frame, text='Canvas color', bootstyle='outline', command=funcPaint.bg_color)
        self.Clear = tkb.Button(
            frame, text='Clear canvas', bootstyle='outline', command=lambda: funcPaint.clear_new('clear'))
        # items in menu Chart
        self.Chart = tkb.Menubutton(
            frame, text='New chart', bootstyle="outline")
        chartmenu = tkb.Menu(self.Chart, relief='flat', activeborderwidth=5)
        chartmenu.add_command(label='line chart',
                              command=lambda: funcPaint.newChartWindow(1))
        chartmenu.add_command(
            label='bar chart', command=lambda: funcPaint.newChartWindow(2))
        chartmenu.add_command(
            label='pie chart', command=lambda: funcPaint.newChartWindow(3))
        self.Chart.config(menu=chartmenu)
        # default
        self.Insert.grid(column=0, row=0, padx=1, pady=1)
        self.Brushes.grid(column=1, row=0, padx=1, pady=1)
        self.Shapes.grid(column=2, row=0, padx=1, pady=1)
        self.Color.grid(column=3, row=0, padx=1, pady=1)
        self.SizeLabel.grid(column=4, row=0, padx=1, pady=4)
        self.Size.grid(column=5, row=0, padx=3, pady=9)

    def PaintButton(self):
        # clear items in frame
        self.Chart.grid_forget()
        self.Resize.grid_forget()
        self.BackgroundColor.grid_forget()
        self.Clear.grid_forget()
        # place new items in frame
        self.Insert.grid(column=0, row=0, padx=1, pady=1)
        self.Brushes.grid(column=1, row=0, padx=1, pady=1)
        self.Shapes.grid(column=2, row=0, padx=1, pady=1)
        self.Color.grid(column=3, row=0, padx=1, pady=1)
        self.SizeLabel.grid(column=4, row=0, padx=1, pady=4)
        self.Size.grid(column=5, row=0, padx=3, pady=9)

    def CanvasButton(self):
        # clear items in frame
        self.Chart.grid_forget()
        self.Brushes.grid_forget()
        self.Shapes.grid_forget()
        self.Color.grid_forget()
        self.SizeLabel.grid_forget()
        self.Size.grid_forget()
        self.Insert.grid_forget()
        # place new items in frame
        self.Resize.grid(column=0, row=0, padx=1, pady=1)
        self.BackgroundColor.grid(column=1, row=0, padx=1, pady=1)
        self.Clear.grid(column=2, row=0, padx=1, pady=1)

    def ChartButton(self):
        # clear items in frame
        self.Brushes.grid_forget()
        self.Shapes.grid_forget()
        self.Color.grid_forget()
        self.SizeLabel.grid_forget()
        self.Size.grid_forget()
        self.Resize.grid_forget()
        self.BackgroundColor.grid_forget()
        self.Clear.grid_forget()
        self.Insert.grid_forget()
        # place new items in frame
        self.Chart.grid(column=0, row=0, padx=1, pady=1)


funcPaint = FUNC()
ctrl = ITEMS()
menu = Menu(window)
filemenu = Menu(menu, activeborderwidth=10)
typemenu = Menu(menu)
window.config(menu=menu)
menu.add_cascade(label='File', menu=filemenu)
menu.add_command(label='Paint', command=ctrl.PaintButton)
menu.add_command(label='Canvas', command=ctrl.CanvasButton)
menu.add_command(label='Chart', command=ctrl.ChartButton)
filemenu.add_command(
    label='new', command=lambda: funcPaint.clear_new('new'))
filemenu.add_command(label='save', command=funcPaint.save_replace)
filemenu.add_cascade(label='saveAs', menu=typemenu)
filemenu.add_command(label='open', command=lambda: funcPaint.openfile(False))
typemenu.add_command(
    label='PNG', command=lambda: funcPaint.save_as('PNG', '.png'))
typemenu.add_command(
    label='JPG', command=lambda: funcPaint.save_as('JPEG', '.jpeg'))
typemenu.add_command(
    label='GIF', command=lambda: funcPaint.save_as('GIF', '.gif'))
img1 = ImageTk.PhotoImage(Image.open('Icon\\1.png'))
cv = tk.Canvas(window, width=funcPaint.X, height=funcPaint.Y, bg='white')
background_rectangle = cv.create_rectangle(
    0, 0, funcPaint.X+10, funcPaint.Y+10, fill='white', outline='white')
cv.pack(side='top', anchor='nw', pady=3)
cv.bind('<Button-1>', funcPaint.click)
cv.bind('<ButtonRelease-1>', funcPaint.stop)
window.bind('<Control-s>', funcPaint.savehotkey)
window.bind('<Control-z>', funcPaint.undohotkey)
window.bind('<Control-o>', funcPaint.openhotkey)
window.mainloop()
