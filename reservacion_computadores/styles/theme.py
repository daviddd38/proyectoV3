from tkinter import ttk
import tkinter as tk


def set_dark_theme(root):
    style = ttk.Style(root)
    style.theme_use('clam')

    # Colores
    bg_color = '#2E3440'
    fg_color = '#ECEFF4'
    accent_color = '#5E81AC'
    button_color = '#4C566A'
    entry_bg = '#3B4252'

    # Configuración general
    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Helvetica', 12))
    style.configure('TButton', background=button_color, foreground=fg_color, font=('Helvetica', 12), borderwidth=1,
                    focusthickness=3, focuscolor=accent_color)
    style.map('TButton', background=[('active', accent_color)])
    style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color, font=('Helvetica', 12))
    style.map('TEntry', fieldbackground=[('focus', entry_bg)])
    style.configure('TNotebook', background=bg_color, borderwidth=0)
    style.configure('TNotebook.Tab', background=button_color, foreground=fg_color, padding=[10, 5],
                    font=('Helvetica', 12))
    style.map('TNotebook.Tab', background=[('selected', accent_color)], expand=[('selected', [1, 1, 1, 0])])

    # Configuración para Listbox y Text
    root.option_add('*Listbox*Font', ('Helvetica', 12))
    root.option_add('*Listbox*Background', entry_bg)
    root.option_add('*Listbox*Foreground', fg_color)
    root.option_add('*Text*Font', ('Helvetica', 12))
    root.option_add('*Text*Background', entry_bg)
    root.option_add('*Text*Foreground', fg_color)

    return style


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


def apply_rounded_corners(widget):
    try:
        bg_color = widget.cget('background')
    except tk.TclError:
        bg_color = '#2E3440'  # Color de fondo oscuro por defecto

    try:
        widget.configure(highlightthickness=0, borderwidth=0)
    except tk.TclError:
        pass

    canvas = tk.Canvas(widget, highlightthickness=0, bg=bg_color)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    def draw_rounded_rectangle(event=None):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        create_rounded_rectangle(canvas, 2, 2, width - 2, height - 2, radius=15, fill=bg_color, outline=bg_color)

    draw_rounded_rectangle()
    canvas.bind("<Configure>", draw_rounded_rectangle)

    # Intentamos mover el canvas al fondo, si es posible
    try:
        canvas.lower()
    except tk.TclError:
        # Si no podemos usar lower(), intentamos reorganizar los widgets manualmente
        for child in widget.winfo_children():
            if child != canvas:
                child.lift()

    return canvas