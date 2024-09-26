import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ReservationHistoryFrame(ttk.Frame):
    def __init__(self, parent, user_controller, user_id):
        super().__init__(parent)
        self.user_controller = user_controller
        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        # Título
        ttk.Label(self, text="Historial de Reservaciones", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Crear Treeview
        columns = ('ID', 'Computador', 'Fecha Inicio', 'Fecha Fin', 'Estado')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Botón para actualizar
        ttk.Button(self, text="Actualizar", command=self.load_reservations).pack(pady=10)

        # Cargar reservaciones
        self.load_reservations()

    def load_reservations(self):
        # Limpiar Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Obtener reservaciones
        reservations = self.user_controller.get_user_reservations(self.user_id)

        # Insertar reservaciones en Treeview
        for reservation in reservations:
            fecha_inicio = reservation.fecha_inicio
            fecha_fin = reservation.fecha_fin

            # Verificar si fecha_inicio y fecha_fin son strings o objetos datetime
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
            if isinstance(fecha_fin, str):
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")

            self.tree.insert('', 'end', values=(
                reservation.id_reservacion,
                reservation.nombre_computador,
                fecha_inicio.strftime("%Y-%m-%d %I:%M %p"),
                fecha_fin.strftime("%Y-%m-%d %I:%M %p"),
                reservation.estado
            ))