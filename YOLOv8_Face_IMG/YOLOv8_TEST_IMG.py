from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk

import os
import numpy
import torch
import torchvision
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from PIL import Image
import cv2

root = Tk()
root.geometry("640x800")
root.configure(background="#fccd12")
root.title("BCFPD YOLOv8 IMAGE Blur")

entry1_var=StringVar(root)
entry2_var=StringVar(root)
radiodel=StringVar(root, "0")

def pic_blur():
    torch.cuda.init
    print(torch.cuda.is_initialized())
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    model = YOLO(r"C:\US-R-PIIScrub\models\yolov8l-face.pt")

    global files
    files = []
    filesout = []
    desc_path = ""
    for (dirpath, dirnames, filenames) in os.walk(inputpath):
            for file in filenames:
                    if(file.lower().endswith(".jpg")):
                            files.append(os.path.join(dirpath, file))
                            filesout.append(os.path.join(outputpath, file))
                    if(file.lower().endswith(".json")):
                            desc_path = os.path.join(dirpath, file)
                            
    pb.step(2)
    root.update()

    piccount = len(file) + 2
    stepinc = 98/piccount

    for n, file in enumerate(files):
        image = Image.open(file)
        exif = image.getexif
        results = model.predict(file)
        image = (file)
        img_pil = cv2.imread(image)

        results = results[0]

        blur_ratio = 50

        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().tolist()
            clss = results.boxes.cls.cpu().tolist()
            for box in results.boxes:
                box_xy = box.xyxy[0].tolist()
                obj = img_pil[int(box_xy[1]):int(box_xy[3]), int(box_xy[0]):int(box_xy[2])]
                blur_obj = cv2.blur(obj, (blur_ratio, blur_ratio))
                img_pil[int(box_xy[1]):int(box_xy[3]), int(box_xy[0]):int(box_xy[2])] = blur_obj

        cv2.imwrite(filesout[n], img_pil)

def process_req():
    global inputpath
    inputpath = entry1_var.get()
    global outputpath
    outputpath = entry2_var.get()
    global delete
    delete = radiodel.get()
    pic_blur()
    entry1_var.set("")
    entry2_var.set("")
    if delete == "1":
        for file in files:
            os.remove(file)
    radiodel.set("0")

def open_req():
    top = Toplevel(root)
    top.geometry("320x200")
    top.title("Sanitizing Images")

    pbFont = tkFont.Font(family="System", size=12)
    text_var = "Sanitization in progress..."
    pblabel = Label(top, text=text_var, font=pbFont).pack(pady=25)
    global pb
    pb = ttk.Progressbar(top, length=100, mode="determinate")
    pb.pack()
    process_req()
    top.destroy()
    top.mainloop()

frame = Frame(root, bg="#1f3263")
frame.pack()

labelframein = Frame(frame, bg="#4c6dc2")
labelframein.pack(padx=35, pady=35)

titleFont = tkFont.Font(family="System", size=26)
label = Label(labelframein, text = "YOLOv8 Image Blur (MOTF1)\nDEV BUILD 0.1", bg="#4c6dc2", padx=125, pady=25, font=titleFont)
label.pack()

spacerframe1 = Frame(root, bg="#38508c")
spacerframe1.pack(pady=15)

baseframe = Frame(root, bg="#1f3263")
baseframe.pack()

buttonparent1 = Frame(baseframe, bg="#4c6dc2")
buttonparent1.pack(padx=20, pady=20)

buttonparent1_1 = Frame(buttonparent1, bg="#4c6dc2")
buttonparent1_1.pack(side=LEFT)

buttonparent1_2 = Frame(buttonparent1, bg="#4c6dc2")
buttonparent1_2.pack(side=RIGHT)

spacerframe1_1_1 = Frame(buttonparent1_1, bg="#4c6dc2")
spacerframe1_1_1.pack(pady=5)

buttonparent1_1tfont = tkFont.Font(family="System", size=16)
buttonparent1_1t = Label(buttonparent1_1, text = "Required Inputs", bg="#4c6dc2", pady=10, font=buttonparent1_1tfont)
buttonparent1_1t.pack()

entryframe1 = Frame(buttonparent1_1, bg="#4c6dc2", relief=RAISED)
entryframe1.pack(pady=10, padx=30)

entryframe2 = Frame(buttonparent1_1, bg="#4c6dc2", relief=RAISED)
entryframe2.pack(pady=10, padx=30)

radioframe3 = Frame(buttonparent1_1, bg="#4c6dc2", relief=RAISED)
radioframe3.pack(pady=10,padx=30)

entrytfont = tkFont.Font(family="System", size=8)
pathentry1t = Label(entryframe1, text = "Enter filepath to\nFOLDER CONTAINING\nphotos below:", bg="#4c6dc2", pady=5, padx=10, font=entrytfont)
pathentry1t.pack()

pathentry1 = Entry(entryframe1, textvariable=entry1_var, bg="#FFFFFF", justify=LEFT)
pathentry1.pack()

entrytfont = tkFont.Font(family="System", size=8)
pathentry2t = Label(entryframe2, text = "Enter filepath to\noutput folder\nbelow:", bg="#4c6dc2", pady=5, padx=10, font=entrytfont)
pathentry2t.pack()

pathentry2 = Entry(entryframe2, textvariable=entry2_var, bg="#FFFFFF", justify=LEFT)
pathentry2.pack()

radio3 = Radiobutton(radioframe3, text = "Delete Originals", font=entrytfont, variable=radiodel, value="1", bg="#4c6dc2", pady=5)
radio3.pack()

radio4 = Radiobutton(radioframe3, text = "Keep Originals", font=entrytfont, variable=radiodel, value="0", bg="#4c6dc2", pady=5, padx=5)
radio4.pack()

spacerframe1_1_2 = Frame(buttonparent1_1, bg="#4c6dc2")
spacerframe1_1_2.pack(pady=5)

spacerframe2 = Frame(baseframe, bg="#4c6dc2")
spacerframe2.pack(pady=5)

sub_btn = Button(baseframe,text = "Submit", command=open_req)
sub_btn.pack()

spacerframe3 = Frame(baseframe, bg="#4c6dc2")
spacerframe3.pack(pady=15)

spacerframe4 = Frame(root, bg="#4c6dc2")
spacerframe4.pack(pady=2)

#logo1 = Image.open(os.path.join(script_dir, "MOTF1_Logo.jpg"))
#logo_image = ImageTk.PhotoImage(logo1)
#logo_label = Label(root,image=logo_image, bg="#1f3263", bd=0)
#logo_label.image = logo_image
#logo_label.pack()

spacerframe5 = Frame(root, bg="#4c6dc2")
spacerframe5.pack(pady=20)

root.mainloop()
