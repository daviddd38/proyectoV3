import tkinter as tk
from tkinter import ttk, messagebox
from reservacion_computadores.views.computer_button import ComputerButton
from datetime import datetime, timedelta


class NewReservationFrame(ttk.Frame):
    def __init__(self, parent, user_controller, user_id):
        super().__init__(parent)
        self.user_controller = user_controller
        self.user_id = user_id
        self.selected_computer = None
        self.computer_buttons = {}
        self.create_widgets()

    def create_widgets(self):
        # Título
        ttk.Label(self, text="Nueva Reservación", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Frame para la selección de fecha y hora
        self.datetime_frame = ttk.Frame(self)
        self.datetime_frame.pack(pady=10, fill=tk.X)

        # Selección de fecha
        ttk.Label(self.datetime_frame, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)

        # Opciones de fecha (hoy y mañana)
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        date_options = [
            ("Hoy", today),
            ("Mañana", tomorrow)
        ]
        self.selected_date = tk.StringVar()
        self.selected_date.set(date_options[0][1].strftime("%Y-%m-%d"))  # Establecer "Hoy" como valor predeterminado

        for i, (text, date) in enumerate(date_options):
            ttk.Radiobutton(self.datetime_frame, text=text, variable=self.selected_date,
                            value=date.strftime("%Y-%m-%d")).grid(row=0, column=i + 1, padx=5, pady=5)

        # Selección de hora de inicio
        ttk.Label(self.datetime_frame, text="Hora de inicio:").grid(row=0, column=3, padx=5, pady=5)
        self.start_hour = ttk.Combobox(self.datetime_frame, values=self.get_time_options(), width=8)
        self.start_hour.grid(row=0, column=4, padx=5, pady=5)
        self.start_hour.set("08:00 AM")

        # Selección de hora de fin
        ttk.Label(self.datetime_frame, text="Hora de fin:").grid(row=0, column=5, padx=5, pady=5)
        self.end_hour = ttk.Combobox(self.datetime_frame, values=self.get_time_options(), width=8)
        self.end_hour.grid(row=0, column=6, padx=5, pady=5)
        self.end_hour.set("09:00 AM")

        # Frame para los computadores
        self.computers_frame = ttk.Frame(self)
        self.computers_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Cargar computadores
        self.load_all_computers()

        # Botón de reservar
        self.reserve_button = ttk.Button(self, text="Reservar", command=self.make_reservation)
        self.reserve_button.pack(pady=10)

    def get_time_options(self):
        options = []
        for hour in range(8, 22):  # 8 AM to 9 PM
            if hour == 12:
                options.append(f"12:00 PM")
            elif hour > 12:
                options.append(f"{hour - 12:02d}:00 PM")
            else:
                options.append(f"{hour:02d}:00 AM")
        return options

    def load_all_computers(self):
        for widget in self.computers_frame.winfo_children():
            widget.destroy()

        self.computer_buttons = {}
        computers = self.user_controller.get_all_computers()
        row = 0
        col = 0
        for computer in computers:
            computer_button = ComputerButton(self.computers_frame, computer, self.user_controller,
                                             self.on_computer_select)
            computer_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.computer_buttons[computer.id_computador] = computer_button
            col += 1
            if col > 2:  # Ajusta este número para cambiar el número de columnas
                col = 0
                row += 1

        # Configurar el grid para que se expanda correctamente
        for i in range(3):  # Ajusta este número si cambias el número de columnas
            self.computers_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            self.computers_frame.rowconfigure(i, weight=1)

    def on_computer_select(self, computer, is_selected):
        if is_selected:
            if self.selected_computer and self.selected_computer != computer:
                self.computer_buttons[self.selected_computer.id_computador].set_selected(False)
            self.selected_computer = computer
        else:
            if self.selected_computer == computer:
                self.selected_computer = None

    def make_reservation(self):
        if not self.selected_computer:
            messagebox.showerror("Error", "Por favor, seleccione un computador.")
            return

        date = datetime.strptime(self.selected_date.get(), "%Y-%m-%d").date()
        start_time = datetime.strptime(self.start_hour.get(), "%I:%M %p").time()
        end_time = datetime.strptime(self.end_hour.get(), "%I:%M %p").time()

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        if start_datetime >= end_datetime:
            messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio.")
            return

        success = self.user_controller.create_reservation(
            self.user_id,
            self.selected_computer.id_computador,
            start_datetime,
            end_datetime
        )

        if success:
            messagebox.showinfo("Éxito", "Reservación creada con éxito.")
            self.update_computer_buttons()
            self.selected_computer = None
        else:
            messagebox.showerror("Error", "No se pudo crear la reservación. Por favor, intente de nuevo.")

    def update_computer_buttons(self):
        for computer_id, button in self.computer_buttons.items():
            button.update_status()