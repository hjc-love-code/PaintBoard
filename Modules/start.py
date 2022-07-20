import os
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import tkinter as tk


def save(save_path, window, name, open_path, cv, save_type, type_number):
    list = os.listdir('C:\\Program Files')
    cv.update()
    if 'gs' in list:
        save = asksaveasfilename(
            filetypes=[(save_type, type_number)])
        if save != '':
            cv.postscript(file="%s%s" % (save, '.ps'), colormode='color')
            im = Image.open("%s%s" % (save, '.ps'))
            im.save("%s%s" % (save, type_number), type_number.replace('.', ''))
            im.close()
            os.remove("%s%s" % (save, '.ps'))
            name = os.path.split(save)
            open_path = [name[0], name[1]+type_number]
            name = name[1].replace('.', '').replace(
                'png', '').replace('jpeg', '').replace('gif', '')
            window.title(name)

    else:
        ret = messagebox.askquestion(title='warning', message="""Please install ghostscript, if not,
we can't save you image as PNG/JPEG/GIF
(Restart the program to enable).""")
        if ret == 'yes':
            webbrowser.open("https://www.ghostscript.com/releases/gsdnld.html")
    return (save_path, name, open_path)


def replace(name, open_path, cv, fuc_start):
    if name is not None:
        path = '%s%s%s%s' % (open_path[0], '\\', name, '.ps')
        cv.postscript(file=path, colormode='color')
        im = Image.open(path)
        end_type = open_path[1].replace(name, '')
        imgtypesave = '%s%s%s%s' % (open_path[0], '\\', name, end_type)
        os.remove(imgtypesave)
        im.save(imgtypesave,
                end_type.replace('.', ''))
        im.close()
        os.remove(path)
    else:
        fuc_start.save_as('PNG', '.png')


def openfile(cv, window, img, x_, y_, name, open_path, background_r, bg_c, dele_list, img2, openImg, openfilename2, isInsert):
    openfilename = askopenfilename(
        filetypes=[('PNG', '.png'), ('JPG', '.jpeg'), ('GIF', '.gif')])
    if openfilename != '' or openfilename is not None:
        openfilename = openfilename.replace('/', '\\')
        openfilename2 = openfilename
        img = Image.open(openfilename)
        if isInsert is False:
            name = os.path.split(openfilename)
            open_path = name
            name = name[1].replace('.', '').replace(
                'png', '').replace('jpeg', '').replace('gif', '')
            cv.delete(tk.ALL)
            x_ = img.width - 10
            y_ = img.height - 10
            cv.configure(width=x_, height=y_)
            background_r = cv.create_rectangle(
                0, 0, x_+10, y_+10, fill='white', outline='white')
            img2 = ImageTk.PhotoImage(img)
            openImg = cv.create_image(0, 0, anchor=tk.NW, image=img2)
            dele_list = [[], []]
            window.title(name)
        else:
            if img.width > x_ or img.height > y_:
                distance_x = img.width / x_
                distance_y = img.height / y_
                if distance_x > distance_y:
                    distance = distance_x
                elif distance_y > distance_x:
                    distance = distance_y
                else:
                    distance = img.height / distance_y
                img = img.resize((round(img.width/distance)-5,
                                 round(img.height/distance)-5))
            else:
                pass
            img2 = ImageTk.PhotoImage(img)
            openImg = cv.create_image(0, 0, anchor=tk.NW, image=img2)
            dele_list[0].append(openImg)
            dele_list[1].append(1)
        return (img, x_, y_, name, open_path, background_r, bg_c, dele_list, img2, openImg, openfilename2)

