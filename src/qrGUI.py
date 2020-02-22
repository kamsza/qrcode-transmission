from PIL import Image, ImageTk
import tkinter as tk
import shutil
import threading
import time
from os import listdir
from os.path import isfile, join

REFRESH_TIME = 75 #ms
IMAGE_PATH = "../img/tmp.jpg"
WINDOW_SIZE = 750


# Function shows qrcodes, that are placed in qrcode directory as .png files, one after another in infinite loop
def show():
    root = tk.Tk()
    root.title("QRcode sender")
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    canvas = tk.Canvas(root, height=WINDOW_SIZE, width=WINDOW_SIZE)
    img = None
    image_id = canvas.create_image(WINDOW_SIZE / 2, WINDOW_SIZE / 2, image=img)
    canvas.pack()

    th = threading.Thread(target=update_image_file, args=(IMAGE_PATH,))
    th.daemon = True
    th.start()

    refresh_image(canvas, img, IMAGE_PATH, image_id)
    root.mainloop()


# Function copies qrcodes from qrcode directory to IMAGE_PATH path, changing tmp image with REFRESH_TIME frequency
def update_image_file(dst):
    mypath = "../qrcodes"
    test_images = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    while True:
        for src in test_images:
            shutil.copy(src, dst)
            time.sleep(REFRESH_TIME/1000)


# Function refreshes shown image, taking new one from IMAGE_PATH
def refresh_image(canvas, img, IMAGE_PATH, image_id):
    try:
        pil_img = Image.open(IMAGE_PATH).resize((WINDOW_SIZE, WINDOW_SIZE), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)
    except IOError:
        img = None
    canvas.after(REFRESH_TIME, refresh_image, canvas, img, IMAGE_PATH, image_id)
