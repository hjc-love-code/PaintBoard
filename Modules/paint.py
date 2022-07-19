from PIL import Image, ImageTk
import webcolors
from tkinter import colorchooser

def changeBackgroundColor(cv, bg_c, background_r, name, img, img2, openImg, openfilename):
    bg_c = colorchooser.askcolor()
    if name is not None and img is None:
        cv.itemconfig(background_r, fill=bg_c[1], outline=bg_c[1])
    if name is None and img is None:
        cv.itemconfig(background_r, fill=bg_c[1], outline=bg_c[1])
    elif name is not None and img is not None:
        cv.itemconfig(background_r, fill=bg_c[1], outline=bg_c[1])
        color = webcolors.hex_to_rgb(bg_c[1])
        img = Image.open(openfilename)
        img2 = changeImg(img, color, img2)
        img2 = ImageTk.PhotoImage(img2)
        cv.itemconfig(openImg, image=img2)
    return(bg_c, background_r,  img2, openImg)


def changeImg(img, color, img2):
    i, j = 1, 1
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            data = (img.getpixel((i, j)))
            if (data[0] > 245 and data[1] > 245 and data[2] > 245):
                img.putpixel((i, j), color)
    img2 = img.convert("RGB")
    return img2

def dele(cv, dele_list):
    if dele_list != []:
        try:
            for i in range(dele_list[1][len(dele_list[1])-1]):
                number = len(dele_list[0])
                cv.delete(dele_list[0][number-1])
                dele_list[0] = dele_list[0][0:-1]
            dele_list[1] = dele_list[1][0:-1]
        except IndexError:
            pass
    return dele_list
