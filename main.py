# github.com/sjsdouglas/ping
# PING_TaskBar_1.0.0.0
# Python3.11.1


# - - - - - - - - - - IMPORTS - - - - - - - - - - #


from threading import Thread
from time import sleep
from tkinter import PhotoImage, Tk, ttk, Label, CENTER, Entry, Button
from PIL import Image, ImageDraw, ImageFont
from ping3 import ping
from pystray import Icon, Menu, MenuItem
from Resource_Path import resource_path


# - - - - - - - - - - LOG - - - - - - - - - - #


###########################################################################################
# from logging import basicConfig, DEBUG, exception, log, INFO                            #
# basicConfig(filename='log.txt',                                                         #
#             encoding='utf-8',                                                           #
#             format=' \n ---> %(asctime)s | %(name)s | %(levelname)s | %(message)s \n ', #
#             datefmt='%H:%M:%S',                                                         #
#             level=DEBUG)                                                                #
###########################################################################################


# - - - - - - - - - - VARIABLES - - - - - - - - - - #


z = False
loop = True


# - - - - - - - - - - TKINTER - - - - - - - - - - #


# TK Config
root = Tk()
frm = ttk.Frame(root, padding=10)
root.title('PING TaskBar - Address to be pinged')
root.wm_iconphoto(False, PhotoImage(file=r'img\main.png'))
root.attributes('-topmost', 1)
posx = (root.winfo_screenwidth() / 2) - (212 / 2)
posy = (root.winfo_screenheight() / 2) - (124 / 2)
root.geometry(f'{212}x{124}+{posx:.0f}+{posy:.0f}')
root.resizable(False, False)
# TK Widget
lab_1 = Label(frm,
              text='Enter the website or IP address',
              font='Arial 10')
ent_1 = Entry(frm,
              width=30,
              justify=CENTER)
lab_2 = Label(frm,
              text=f'-',
              font='Courier 9')
btn_1 = Button(frm,
               text='OK',
               width=11,
               command=lambda: get_data())
btn_2 = Button(frm,
               text='CANCEL',
               width=11,
               command=lambda: root.destroy())
ent_1.focus_force()
# TK Grid
frm.grid()
lab_1.grid(row=0, columnspan=2)
ent_1.grid(row=1, columnspan=2, padx=4, pady=4)
lab_2.grid(row=4, columnspan=2)
btn_1.grid(row=3, column=0, padx=4, pady=4)
btn_2.grid(row=3, column=1, padx=4, pady=4)
# TK Bind
root.bind('<Return>', lambda event: get_data())
root.bind('<Escape>', lambda event: root.destroy())


# - - - - - - - - - - DEF's - - - - - - - - - - #


def make_number_icon(number, color):
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    fnt = ImageFont.truetype(r'C:\Windows\Fonts\ARIAL.TTF', 58)
    d = ImageDraw.Draw(img)
    d.text((0, 0), f"{number:>02}", font=fnt, fill=f'{color}')
    return img


def get_data():
    global ent_get
    global z
    ent_get = ent_1.get().lower()
    x = False
    if ent_get == '':
        ent_get = 'google.com'
        x = True
    elif 'https://' in ent_get:
        lab_2.config(text='Delete "https://".')
    elif 'http://' in ent_get:
        lab_2.config(text='Delete "http://".')
    elif '/' in ent_get:
        lab_2.config(text='Delete "/".')
    else:
        x = True
    if x:
        root.destroy()
        z = True
        update_icon()


def update_icon():
    global loop
    bg = None
    while loop:
        try:
            ping_output = ping(ent_get, unit='ms')
            if ping_output == 0:
                bg = make_number_icon(
                    f'{ping_output:.0f}', 'white')
            elif 0 < ping_output <= 50:
                bg = make_number_icon(
                    f'{ping_output:.0f}', 'green')
            elif 50 < ping_output <= 60:
                bg = make_number_icon(
                    f'{ping_output:.0f}', 'yellow')
            elif 60 < ping_output < 100:
                bg = make_number_icon(
                    f'{ping_output:.0f}', 'orange')
            elif ping_output >= 100:
                bg = make_number_icon('99+', 'red')
            icon.icon = bg
        except TypeError:
            bg = make_number_icon('P.O.', 'white')
        sleep(1)


def on_clicked(icon, item):
    global loop
    if str(item) == 'Exit':
        loop = False
        icon.stop()


# - - - - - - - - - - RUN - - - - - - - - - - #


if __name__ == '__main__':
    root.mainloop()
    if z:
        icon = Icon(name='PING',
                    title=f'Pinging \'{ent_get}\'...',
                    icon=make_number_icon(0, 'black'),
                    menu=Menu(
                        MenuItem('Exit', on_clicked)))
        thread = Thread(target=update_icon)
        thread.start()
        icon.run()
