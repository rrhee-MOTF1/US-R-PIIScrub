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
root.title("BCFPD YOLOv11 VIDEO Blur")

entry1_var=StringVar(root)
radiodel=StringVar(root, "0")

def vid_blur():
    torch.cuda.init
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    model = YOLO(r"C:\US-R-PIIScrub\models\yolov11m-face.pt")
    names = model.names

    cap = cv2.VideoCapture(inputvid)
    assert cap.isOpened(), "Error reading video file"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    blur_ratio = 50

    video_writer = cv2.VideoWriter(outputvid, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        results = model.predict(im0, show=False)
        boxes = results[0].boxes.xyxy.cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()

        if boxes is not None:
            for box, cls in zip(boxes, clss):
                
                obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                blur_obj = cv2.blur(obj, (blur_ratio, blur_ratio))

                im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj

        video_writer.write(im0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

def process_req():
    global inputvid
    inputvid = entry1_var.get().strip('"')
    temp_list = inputvid.split('.')
    temp_string = ''
    for i, item in enumerate(temp_list):
        if i == 0:
            temp_string += item + '_output'
        elif i == 1:
            temp_string += '.mp4'
    print(temp_string)
    global outputvid
    outputvid = temp_string
    global delete
    delete = radiodel.get()
    vid_blur()
    entry1_var.set("")
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
label = Label(labelframein, text = "YOLOv11 Video Blur (MOTF1)\nDEV BUILD 0.1", bg="#4c6dc2", padx=125, pady=25, font=titleFont)
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
pathentry1t = Label(entryframe1, text = "Enter filepath to\nvideo below:", bg="#4c6dc2", pady=5, padx=10, font=entrytfont)
pathentry1t.pack()

pathentry1 = Entry(entryframe1, textvariable=entry1_var, bg="#FFFFFF", justify=LEFT)
pathentry1.pack()

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

buttonparent3_1tfont = tkFont.Font(family="System", size=16)
buttonparent3_1t = Label(buttonparent1_1, text = "Scrubbing complete when text\nentry box is cleared", bg="#4c6dc2", pady=10, font=buttonparent1_1tfont)
buttonparent3_1t.pack()

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

