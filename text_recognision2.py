import tkinter as tk
from PIL import ImageGrab, Image, ImageEnhance, ImageFilter
import threading
import time
import pytesseract
import ctypes
import queue

def detect_mutation(result_queue):
    detected = ""
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    x1, y1 = width / 3.45, height / 2.35
    x2, y2 = width / 3.65 + width / 8, height / 2.7 + height / 8.2
    cordinates = (x1, y1, x2, y2)
    while True:
        screenshot = ImageGrab.grab(bbox=cordinates)
        screenshot.save("screenshot.jpg", "JPEG")
        img = Image.open("screenshot.jpg")
        img = img.convert('L')
        img = img.filter(ImageFilter.SMOOTH)
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        scale_factor = 3
        new_size = (img.width * scale_factor, img.height * scale_factor)
        img = img.resize(new_size, Image.LANCZOS)
        img = img.convert('L')
        img = img.point(lambda x: 0 if x < 140 else 255, '1')
        #img = img.filter(ImageFilter.EDGE_ENHANCE)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img.save('sc.jpg','JPEG')
        pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img,lang='eng')
        #print(time.thread_time())
        text = text.replace("\n", "", text.count("\n"))
        text = text.replace(" ","",text.count(" "))
        text = text.replace("_","",text.count("_"))
        text = text.replace("*", "+", text.count("*"))
        if text == detected and detected !="":
            result_queue.put(text)
            return text

        detected = text
        print(f"{detected=}")
        #print(text,detected)

def detect():
    threading.Thread(target=detect_mutation).start()


"""root = tk.Tk()
root.title("test")
root.geometry("100x100")
root.attributes("-topmost", True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x1, y1 = width / 3.45, height / 2.35
x2, y2 = width / 3.65 + width / 8, height / 2.7 + height / 8.2
cordinates = (x1,y1,x2,y2)
print(cordinates)
gomb = tk.Button(text="Detect",command=detect)
gomb.pack()
label = tk.Label(text="",font=12)
label.pack()
root.mainloop()"""

