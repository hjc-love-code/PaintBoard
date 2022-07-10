import tkinter.simpledialog
import numba

def weidth_appear(width_brushvalue):
    result = tkinter.simpledialog.askfloat(
        title=' ', prompt='width', initialvalue=width_brushvalue)
    if result is not None:
        if result == 1:
            return 2
        else:
            return result

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
