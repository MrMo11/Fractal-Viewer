import PIL.ImageTk, PIL.Image, PIL.ImageFilter
import tkinter as tk
import fractals

from math import log, log2, sqrt
from tkinter import ttk

class Generic():
    img_width = 1024
    img_height = 768
    mouse_rect = 0
    mouse_pos = list((0, 0, 0, 0))
    julia_pos = [-1, -1]

def create_loading_text(event):
    t = event.widget.create_text(Generic.img_width, 0, anchor=tk.NE, font=("Helvetica", 40), text="Updating...", fill="white")
    r = event.widget.create_rectangle(event.widget.bbox(t), fill="black")
    event.widget.tag_lower(r, t)
    event.widget.update()
    return r, t

def delete_ids(event, *args):
    for id in args:
        event.widget.delete(id)

def fractal_image(fractal, img_width, img_height, mouse=(0, 0)):
    if fractal.func == fractals.julia:
        ret_val = fractal.func(Generic.julia_pos[0], Generic.julia_pos[1], img_width, img_height, fractal.max_iterations, mouse, fractal.xrange[0], fractal.xrange[1], fractal.yrange[0], fractal.yrange[1], fractal.power)
    else:
        ret_val = fractal.func(img_width, img_height, fractal.max_iterations, mouse, fractal.xrange[0], fractal.xrange[1], fractal.yrange[0], fractal.yrange[1], fractal.power)

    fractal.img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(ret_val[0], "HSV").convert("RGB"))#.resize((Generic.img_width, Generic.img_height), PIL.Image.ANTIALIAS))
    fractal.xrange = ret_val[1]
    fractal.yrange = ret_val[2]
    return fractal.img

def click(event):
    Generic.mouse_pos[0] = event.x
    Generic.mouse_pos[1] = event.y
    Generic.mousePressed = True

def right_click(event, fractal, id):
    Generic.julia_pos[0] = event.x
    Generic.julia_pos[1] = event.y
    r, t = create_loading_text(event)
    render = fractal_image(fractal, Generic.img_width, Generic.img_height)
    event.widget.itemconfig(id, image=render)
    delete_ids(event, r, t)

def released(event, fractal, id):
    event.widget.delete(Generic.mouse_rect)
    if Generic.mouse_pos[1] > Generic.mouse_pos[3]:
        # swap y values
        temp = Generic.mouse_pos[1]
        Generic.mouse_pos[1] = Generic.mouse_pos[3]
        Generic.mouse_pos[3] = temp

        # swap x values
        temp = Generic.mouse_pos[0]
        Generic.mouse_pos[0] = Generic.mouse_pos[2]
        Generic.mouse_pos[2] = temp

    r, t = create_loading_text(event)
    render = fractal_image(fractal, Generic.img_width, Generic.img_height, tuple(Generic.mouse_pos))
    event.widget.itemconfig(id, image=render)
    delete_ids(event, r, t)

def motion(event):
    Generic.mouse_pos[3] = event.y
    Generic.mouse_pos[2] = ((Generic.img_width * (Generic.mouse_pos[3] - Generic.mouse_pos[1])) / Generic.img_height) + Generic.mouse_pos[0]
    event.widget.delete(Generic.mouse_rect)
    Generic.mouse_rect = event.widget.create_rectangle(Generic.mouse_pos[0], Generic.mouse_pos[1], Generic.mouse_pos[2], Generic.mouse_pos[3], width=5, outline="white")

def updateInfo(event, fractal, img_id, iter_id, power_id):
    key = event.char.lower()
    if key == "w":
        fractal.max_iterations += 100
    elif key == "s":
        fractal.max_iterations -= 100
    elif key == "d":
        fractal.power += 1
    elif key == "a":
        fractal.power -= 1

    if fractal.max_iterations <= 0:
        fractal.max_iterations = 1

    if (fractal.power <= 0):
        fractal.power = 1

    event.widget.itemconfig(iter_id, text="Iterations: "+str(fractal.max_iterations))
    event.widget.itemconfig(power_id, text="Power: "+str(fractal.power))
    r, t = create_loading_text(event)
    render = fractal_image(fractal, Generic.img_width, Generic.img_height)
    event.widget.itemconfig(img_id, image=render)
    delete_ids(event, r, t)

def setFocus(event, canvases):
    selected_tab = event.widget.select()
    text = event.widget.tab(selected_tab, "text")
    canvases[text].focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(str(Generic.img_width)+"x"+str(Generic.img_height))

    tab_parent = ttk.Notebook(root)

    mandelbrot_tab = ttk.Frame(tab_parent)
    julia_tab = ttk.Frame(tab_parent)
    bship_tab = ttk.Frame(tab_parent)

    # set up mandelbrot set
    mandelbrot = fractals.Fractal(func=fractals.multibrot, xrange=(-2.0, 1.0), yrange=(-1.3, 1.1))
    mandelbrot_canvas = tk.Canvas(mandelbrot_tab, width=Generic.img_width, height=Generic.img_height)
    mandelbrot_img = fractal_image(mandelbrot, Generic.img_width, Generic.img_height)
    mandelbrot_img_id = mandelbrot_canvas.create_image(0, 0, anchor=tk.NW, image=mandelbrot_img)
    mandelbrot_iter_id = mandelbrot_canvas.create_text(0, 0, anchor=tk.NW, font=("Helvetica", 15), text="Iterations: "+str(mandelbrot.max_iterations), fill="white")
    mandelbrot_power_id = mandelbrot_canvas.create_text(0, mandelbrot_canvas.bbox(mandelbrot_iter_id)[3], anchor=tk.NW, font=("Helvetica", 15), text="Power: "+str(mandelbrot.power), fill="white")
    mandelbrot_canvas.pack()
    mandelbrot_canvas.bind("<Button-1>", lambda event: click(event))
    mandelbrot_canvas.bind("<ButtonRelease-1>", lambda event, fractal=mandelbrot, id=mandelbrot_img_id: released(event, fractal, id))
    mandelbrot_canvas.bind("<B1-Motion>", lambda event: motion(event))
    mandelbrot_canvas.focus_set()
    mandelbrot_canvas.bind("<Key>", lambda event, fractal=mandelbrot, img_id=mandelbrot_img_id, iter_id=mandelbrot_iter_id, power_id=mandelbrot_power_id: updateInfo(event, fractal, img_id, iter_id, power_id))

    # set up julia set
    julia = fractals.Fractal(func=fractals.julia, xrange=(-1.5, 1.5), yrange=(-1.5, 1.5))
    julia_canvas = tk.Canvas(julia_tab, width=Generic.img_width, height=Generic.img_height)
    julia_img = fractal_image(julia, Generic.img_width, Generic.img_height)
    julia_img_id = julia_canvas.create_image(0, 0, anchor=tk.NW, image=julia_img)
    julia_iter_id = julia_canvas.create_text(0, 0, anchor=tk.NW, font=("Helvetica", 15), text="Iterations: "+str(julia.max_iterations), fill="white")
    julia_power_id = julia_canvas.create_text(0, julia_canvas.bbox(julia_iter_id)[3], anchor=tk.NW, font=("Helvetica", 15), text="Power: "+str(julia.power), fill="white")
    julia_canvas.pack()
    julia_canvas.bind("<Button-1>", lambda event: click(event))
    julia_canvas.bind("<Button-3>", lambda event, fractal=julia, img_id=julia_img_id: right_click(event, fractal, img_id))
    julia_canvas.bind("<ButtonRelease-1>", lambda event, fractal=julia, id=julia_img_id: released(event, fractal, id))
    julia_canvas.bind("<B1-Motion>", lambda event: motion(event))
    julia_canvas.bind("<Key>", lambda event, fractal=julia, img_id=julia_img_id, iter_id=julia_iter_id, power_id=julia_power_id: updateInfo(event, fractal, img_id, iter_id, power_id))

    # set up burning ship
    bship = fractals.Fractal(func=fractals.burning_ship)
    bship_canvas = tk.Canvas(bship_tab, width=Generic.img_width, height=Generic.img_height)
    bship_img = fractal_image(bship, Generic.img_width, Generic.img_height)
    bship_img_id = bship_canvas.create_image(0, 0, anchor=tk.NW, image=bship_img)
    bship_iter_id = bship_canvas.create_text(0, 0, anchor=tk.NW, font=("Helvetica", 15), text="Iterations: "+str(bship.max_iterations), fill="white")
    bship_power_id = bship_canvas.create_text(0, bship_canvas.bbox(bship_iter_id)[3], anchor=tk.NW, font=("Helvetica", 15), text="Power: "+str(bship.power), fill="white")
    bship_canvas.pack()
    bship_canvas.bind("<Button-1>", lambda event: click(event))
    bship_canvas.bind("<ButtonRelease-1>", lambda event, fractal=bship, id=bship_img_id: released(event, fractal, id))
    bship_canvas.bind("<B1-Motion>", lambda event: motion(event))
    bship_canvas.bind("<Key>", lambda event, fractal=bship, img_id=bship_img_id, iter_id=bship_iter_id, power_id=bship_power_id: updateInfo(event, fractal, img_id, iter_id, power_id))

    root.bind("<<NotebookTabChanged>>", lambda event, canvases={"Mandelbrot":mandelbrot_canvas, "Julia":julia_canvas, "Burning Ship":bship_canvas}: setFocus(event, canvases))

    tab_parent.add(mandelbrot_tab, text="Mandelbrot")
    tab_parent.add(julia_tab, text="Julia")
    tab_parent.add(bship_tab, text="Burning Ship")
    tab_parent.pack(expand=True, fill="both")

    root.mainloop()
