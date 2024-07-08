import tkinter as tk
import pyautogui
import threading
import time
from pynput import mouse
from PIL import Image
from PIL import ImageGrab
from pynput import keyboard

mutations = ["Attack", "Convert Amount", "Gather Amount", "Energy ", "Bee Ability Rate", "Critical Chance", "Movespeed",
             "Instant Conversion"]
mutations_color = [(235,59,55),(255,204,66),(208,255,127),(0,0,0),(185,165,240),(68,200,108),(81,191,241),(245,255,28)]
selected_colors = []
stop_event = None
stop_event_1 = None
stop_event_2 = None
cordinates_1 = None
cordinates_2 = None
cordinates_3 = None
search_thread = None

def search_for_mutation():
    global stop_event, search_thread
    while not stop_event.is_set():
        screenshot = ImageGrab.grab(bbox=cordinates_1 + cordinates_2)
        # Színvizsgálat a lefotózott képen
        width, height = screenshot.size
        for y in range(height):
            if stop_event.is_set():
                return
            for x in range(width):
                if stop_event.is_set():
                    return
                pixel_color = screenshot.getpixel((x, y))
                for target_color in selected_colors:
                    print(target_color)
                    if pixel_color[0] in range(target_color[1][0]-10,target_color[1][0]+10) and pixel_color[1] in range(target_color[1][1]-10,target_color[1][1]+10) and pixel_color[2] in range(target_color[1][2]-10,target_color[1][2]+10):
                        debug_label.configure(text="FOUND")
                        stop_event.set()
                        return

        debug_label.configure(text="NOT FOUND")
        #RAKD IDE AZ ÚJRA PRÓBÁLÁST
        pyautogui.leftClick(x=cordinates_3[0],y=cordinates_3[1])
def on_select():
    global selected_colors
    selected_colors = []
    for idx, var in enumerate(check_vars):
        if var.get() == 1:
            selected_colors.append([mutations[idx],mutations_color[idx]])

def get_mouse_1(x, y, button, pressed):
    global mouse_listener, cordinates_1
    if button == mouse.Button.left and pressed:
        x, y = pyautogui.position()
        cordinate_1_value_label.configure(text=f"X: {x} | Y: {y}")
        cordinates_1 = [x, y]
        mouse_listener.stop()

def select_1():
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=get_mouse_1)
    mouse_listener.start()

def get_mouse_2(x, y, button, pressed):
    global mouse_listener,cordinates_2
    if button == mouse.Button.left and pressed:
        x, y = pyautogui.position()
        cordinate_2_value_label.configure(text=f"X: {x} | Y: {y}")
        cordinates_2 = [x, y]
        mouse_listener.stop()

def select_2():
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=get_mouse_2)
    mouse_listener.start()

def get_mouse_3(x, y, button, pressed):
    global mouse_listener,cordinates_3
    if button == mouse.Button.left and pressed:
        x, y = pyautogui.position()
        cordinate_3_value_label.configure(text=f"X: {x} | Y: {y}")
        cordinates_3 = [x, y]
        mouse_listener.stop()

def select_3():
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=get_mouse_3)
    mouse_listener.start()

def show_cordinates():
    import tkinter as tk
    def draw_rectangle(x1, y1, x2, y2):
        # Létrehozzuk az ablakot
        show = tk.Tk()
        show.title('Ablak megjelenítése')
        show.attributes('-alpha', 0.5)
        show.attributes('-fullscreen', True)
        show.attributes("-topmost", True)
        # Számítjuk ki a téglalap koordinátáit
        x1, y1 = min(x1, x2), min(y1, y2)
        x2, y2 = max(x1, x2), max(y1, y2)

        # Kiszámítjuk a téglalap méreteit és elhelyezkedését
        width = x2 - x1
        height = y2 - y1

        # Létrehozzuk a rajzvásznat
        canvas = tk.Canvas(show, width=width, height=height)
        canvas.place(x=x1,y=y1)

        # Rajzoljuk meg a téglalapot
        canvas.create_rectangle(5,5, width, height, outline='black',)
        show.after(2000, show.destroy)
        # Indítjuk az eseménykezelést
        show.mainloop()

    if cordinates_1 and cordinates_2:
        # A megadott koordináták
        x1, y1 = cordinates_1
        x2, y2 = cordinates_2

        # Téglalap (ablak) rajzolása a megadott koordináták alapján
        draw_rectangle(x1, y1, x2, y2)
    else:
        print("ERROR")

def start():
    global selected_colors, search_thread, stop_event
    selected_colors = []
    for idx, var in enumerate(check_vars):
        if var.get() == 1:
            selected_colors.append([mutations[idx], mutations_color[idx]])
    if len(selected_colors) >0 and cordinates_1 and cordinates_2 and cordinates_3:
        pyautogui.leftClick(x=cordinates_3[0], y=cordinates_3[1])
        if stop_event is not None:
            stop_event.set()
            search_thread.join()
            stop_event = None
            search_thread = None
            debug_label.configure(text="")
        else:
            stop_event = threading.Event()
            search_thread = threading.Thread(target=search_for_mutation, daemon=True)
            search_thread.start()
    else:
        print("ERROR")

def on_press(key):
    try:
        if key.char == 'p':
            start()
    except AttributeError:
        pass

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

button_width = 7

root = tk.Tk()
root.title("Roblox auto mutator v1.0")
root.geometry("825x125")
root.attributes("-topmost", True)

cordinate_1_label = tk.Label(text="1 cordinate:",font=12)
cordinate_1_value_label = tk.Label(text="0000",font=12)
cordinate_1_button = tk.Button(text="SET",font=12,width=button_width,command=select_1)
cordinate_2_label = tk.Label(text="2 cordinate:",font=12)
cordinate_2_value_label = tk.Label(text="0000",font=12)
cordinate_2_button = tk.Button(text="SET",font=12,width=button_width,command=select_2)
cordinate_3_label = tk.Label(text="Use another:",font=12)
cordinate_3_value_label = tk.Label(text="0000",font=12)
cordinate_3_button = tk.Button(text="SET",font=12,width=button_width,command=select_3)
show_select_button = tk.Button(text="SHOW",font=12,width=button_width,command=show_cordinates)
start_button = tk.Button(text="START",font=12,width=button_width, command=start)

debug_label = tk.Label(text="",font=100,fg="red")

cordinate_1_label.grid(row=1,column=0)
cordinate_1_value_label.grid(row=1,column=1)
cordinate_1_button.grid(row=1,column=2)
cordinate_2_label.grid(row=2,column=0)
cordinate_2_value_label.grid(row=2,column=1)
cordinate_2_button.grid(row=2,column=2)
cordinate_3_label.grid(row=3,column=0)
cordinate_3_value_label.grid(row=3,column=1)
cordinate_3_button.grid(row=3,column=2)
show_select_button.grid(row=2,column=3)
start_button.grid(row=2,column=4)

debug_label.grid(row=2, column=5, sticky="e")

check_vars = [tk.IntVar() for _ in mutations]
for idx, option in enumerate(mutations):
    radio = tk.Checkbutton(root, text=option, variable=check_vars[idx], command=on_select)
    radio.grid(row=0,column=idx)

listener_thread = threading.Thread(target=start_keyboard_listener)
listener_thread.daemon = True
listener_thread.start()

root.mainloop()