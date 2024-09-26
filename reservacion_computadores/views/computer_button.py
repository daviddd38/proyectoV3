import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class ComputerButton(ttk.Frame):
    def __init__(self, parent, computer, user_controller, on_select):
        super().__init__(parent)
        self.computer = computer
        self.user_controller = user_controller
        self.on_select = on_select
        self.tooltip = None
        self.is_selected = False
        self.draw()

    def draw(self):
        status, time_info, user_name = self.get_status_color()

        # Definir colores según el estado
        colors = {
            "Disponible": "#4CAF50",  # Verde
            "Reservado": "#FFC107",  # Amarillo
            "En mantenimiento": "#F44336",  # Rojo
            "No disponible": "#9E9E9E"  # Gris
        }

        button_color = colors.get(status, "#9E9E9E")
        if self.is_selected:
            button_color = "#2196F3"  # Azul para indicar selección

        self.button_frame = tk.Frame(self, bg=button_color, width=200, height=100)
        self.button_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.button_frame.pack_propagate(False)

        self.button_label = tk.Label(
            self.button_frame,
            text=f"{self.computer.nombre}\n{status}",
            bg=button_color,
            fg="white",
            font=("Helvetica", 10, "bold")
        )
        self.button_label.pack(expand=True)

        self.button_frame.bind("<Button-1>", self.on_click)
        self.button_label.bind("<Button-1>", self.on_click)

        self.button_frame.bind("<Enter>", self.show_tooltip)
        self.button_frame.bind("<Leave>", self.hide_tooltip)

        if status == "Disponible" and time_info:
            ttk.Label(self, text=f"Próxima reserva: {time_info.strftime('%I:%M %p')}").pack()
        elif status == "Reservado" and time_info:
            ttk.Label(self, text=f"Disponible a partir de: {time_info.strftime('%I:%M %p')}").pack()

    def get_status_color(self):
        return self.user_controller.get_computer_status(self.computer.id_computador)

    def on_click(self, event=None):
        status, _, _ = self.get_status_color()
        if status == "Disponible":
            self.is_selected = not self.is_selected
            self.on_select(self.computer, self.is_selected)
            self.update_status()
            print(
                f"Computador {self.computer.nombre} {'seleccionado' if self.is_selected else 'deseleccionado'} para reserva")
        else:
            print(f"El computador {self.computer.nombre} no está disponible")

    def update_status(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.draw()

    def show_tooltip(self, event):
        x = y = 0
        x, y, _, _ = self.button_frame.bbox("insert")
        x += self.button_frame.winfo_rootx() + 35
        y += self.button_frame.winfo_rooty() + 35

        # Crear un toplevel window
        self.tooltip = tk.Toplevel(self.button_frame)
        # Eliminar la decoración de la ventana
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.get_computer_info(), justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         font=("Helvetica", "8", "normal"), padx=5, pady=5)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def get_computer_info(self):
        status, time_info, user_name = self.get_status_color()
        info = f"ID: {self.computer.id_computador}\n"
        info += f"Nombre: {self.computer.nombre}\n"
        info += f"Descripción: {self.computer.descripcion}\n"
        info += f"Estado: {status}\n"
        if status == "Disponible" and time_info:
            info += f"Próxima reserva: {time_info.strftime('%I:%M %p')}\n"
        elif status == "Reservado":
            if time_info:
                info += f"Disponible a partir de: {time_info.strftime('%I:%M %p')}\n"
            if user_name:
                info += f"Reservado por: {user_name}"
        return info

    def set_selected(self, is_selected):
        if self.is_selected != is_selected:
            self.is_selected = is_selected
            self.update_status()