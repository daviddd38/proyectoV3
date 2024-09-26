import tkinter as tk
from tkinter import ttk
from reservacion_computadores.controllers.user_controller import UserController
from datetime import datetime
from .reservation_history_frame import ReservationHistoryFrame
from .new_reservation_frame import NewReservationFrame

class UserView(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.user_controller = UserController()

        self.create_widgets()
        self.update_clock()
        self.check_reservations()

    def create_widgets(self):
        # Título de bienvenida
        self.welcome_label = ttk.Label(self, text=f"Bienvenido, {self.user.nombre}", font=('Helvetica', 20, 'bold'))
        self.welcome_label.pack(pady=20)

        # Reloj
        self.clock_label = ttk.Label(self, font=('Helvetica', 14))
        self.clock_label.pack(anchor='ne', padx=10, pady=10)

        # Notebook para pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both", padx=20, pady=10)

        # Pestaña de historial de reservaciones
        self.reservation_history_frame = ReservationHistoryFrame(self.notebook, self.user_controller, self.user.id_usuario)
        self.notebook.add(self.reservation_history_frame, text='Historial de Reservaciones')

        # Pestaña de nueva reservación
        self.new_reservation_frame = NewReservationFrame(self.notebook, self.user_controller, self.user.id_usuario)
        self.notebook.add(self.new_reservation_frame, text='Nueva Reservación')

    def update_clock(self):
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%I:%M:%S %p"))
        self.after(1000, self.update_clock)

    def check_reservations(self):
        self.user_controller.check_and_update_reservations()
        self.new_reservation_frame.load_all_computers()
        self.after(60000, self.check_reservations)  # Check every minute