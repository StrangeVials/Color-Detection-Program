import tkinter as tk
import cv2
from PIL import Image, ImageTk
from util import get_limits

current_color_filter = None

button_names = {"Blue":[255,0,0],
                "Green":[0,255,0],
                "Red":[0,0,255],
                "Yellow":[0,255,255],
                "Black":[0,0,0],
                "White":[255,255,255]
                }

def display_video():
    global current_color_filter
    if not camera.isOpened():
        print("Cannot open camera")
        exit()

    ret, frame = camera.read()

    if not ret:
        print("Failed to grab frame")
        window.after(10,display_video)
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if current_color_filter is not None:

        lower, upper = get_limits(current_color_filter)
        mask = cv2.inRange(hsv, lower, upper)

        boundary_box = Image.fromarray(mask).getbbox()

        if boundary_box is not None:
            x1, y1, x2, y2 = boundary_box
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    feed_display.imgtk = imgtk
    feed_display.config(image=imgtk)
    feed_display.after(10,display_video)

def quit_app(event=None):
    camera.release()
    cv2.destroyAllWindows()
    window.destroy()


window = tk.Tk()
window.title("Color Identifier")
window.bind('q',quit_app)

columns = 3

camera = cv2.VideoCapture(0)
feed_display = tk.Label(window)
feed_display.pack()


description = tk.Label(text="Select a color you want to identify",font=("Arial",15,'bold'))
description.pack()

frame = tk.Frame(window)
frame.pack(expand=True)

def select_color(name):
    global current_color_filter
    current_color_filter = button_names[name]

for i,name in enumerate(button_names):
    row = i//columns
    col = i % columns
    button = tk.Button(frame,text=name,width=15,height=3,font=("Arial",8),command= lambda n=name: select_color(n))
    button.grid(row=row,column=col,padx=5,pady=5)

display_video()

window.mainloop()
camera.release()
