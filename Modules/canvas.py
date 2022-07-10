
import tkinter.simpledialog


def resize(cv, x_, y_, background_r):
    x_y = tkinter.simpledialog.askstring(
        title=' ', prompt='resize', initialvalue=str(x_)+'x'+str(y_))
    if x_y != None:
        x_ = x_y.split('x')[0]
        y_ = x_y.split('x')[1]
    cv.configure(width=x_, height=y_)
    cv.coords(background_r, 0, 0, int(x_)+10, int(y_)+10)
    return (x_, y_, background_r)
