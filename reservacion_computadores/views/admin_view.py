import tkinter as tk
from tkinter import ttk
from reservacion_computadores.controllers.admin_controller import AdminController


class AdminView(ttk.Frame):
    def __init__(self, master, admin):
        super().__init__(master)
        self.master = master
        self.admin = admin
        self.admin_controller = AdminController()

        self.create_widgets()

    def create_widgets(self):
        # Título de bienvenida
        self.welcome_label = ttk.Label(self, text=f"Panel de Administración - Bienvenido, {self.admin.nombre}",
                                       font=('Helvetica', 20, 'bold'))
        self.welcome_label.pack(pady=20)

        # Notebook para pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both", padx=20, pady=10)

        # Pestaña de Resumen
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text='Resumen')
        self.create_summary_widgets()

        # Pestaña de Usuarios
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text='Usuarios')
        self.create_users_widgets()

        # Pestaña de Computadores
        self.computers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.computers_frame, text='Computadores')
        self.create_computers_widgets()

        # Pestaña de Reservaciones
        self.reservations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reservations_frame, text='Reservaciones')
        self.create_reservations_widgets()

    def create_summary_widgets(self):
        # Estadísticas generales
        stats = self.admin_controller.get_general_stats()

        ttk.Label(self.summary_frame, text="Estadísticas Generales", font=('Helvetica', 16, 'bold')).pack(pady=10)

        for key, value in stats.items():
            ttk.Label(self.summary_frame, text=f"{key}: {value}", font=('Helvetica', 12)).pack(pady=5)

    def create_users_widgets(self):
        ttk.Label(self.users_frame, text="Lista de Usuarios", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Tabla de usuarios
        columns = ('ID', 'Nombre', 'Apellido', 'Email')
        self.users_tree = ttk.Treeview(self.users_frame, columns=columns, show='headings')

        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)

        self.users_tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Botón para actualizar la lista de usuarios
        ttk.Button(self.users_frame, text="Actualizar Lista", command=self.update_users_list).pack(pady=10)

        self.update_users_list()

    def create_computers_widgets(self):
        ttk.Label(self.computers_frame, text="Lista de Computadores", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Tabla de computadores
        columns = ('ID', 'Nombre', 'Descripción', 'Estado')
        self.computers_tree = ttk.Treeview(self.computers_frame, columns=columns, show='headings')

        for col in columns:
            self.computers_tree.heading(col, text=col)
            self.computers_tree.column(col, width=100)

        self.computers_tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Botón para actualizar la lista de computadores
        ttk.Button(self.computers_frame, text="Actualizar Lista", command=self.update_computers_list).pack(pady=10)

        self.update_computers_list()

    def create_reservations_widgets(self):
        ttk.Label(self.reservations_frame, text="Lista de Reservaciones", font=('Helvetica', 16, 'bold')).pack(pady=10)

        # Tabla de reservaciones
        columns = ('ID', 'Usuario', 'Computador', 'Fecha Inicio', 'Fecha Fin', 'Estado')
        self.reservations_tree = ttk.Treeview(self.reservations_frame, columns=columns, show='headings')

        for col in columns:
            self.reservations_tree.heading(col, text=col)
            self.reservations_tree.column(col, width=100)

        self.reservations_tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Botón para actualizar la lista de reservaciones
        ttk.Button(self.reservations_frame, text="Actualizar Lista", command=self.update_reservations_list).pack(
            pady=10)

        self.update_reservations_list()

    def update_users_list(self):
        users = self.admin_controller.get_all_users()
        self.users_tree.delete(*self.users_tree.get_children())
        for user in users:
            self.users_tree.insert('', 'end', values=(user.id_usuario, user.nombre, user.apellido, user.email))

    def update_computers_list(self):
        computers = self.admin_controller.get_all_computers()
        self.computers_tree.delete(*self.computers_tree.get_children())
        for computer in computers:
            self.computers_tree.insert('', 'end', values=(
            computer.id_computador, computer.nombre, computer.descripcion, computer.estado))

    def update_reservations_list(self):
        reservations = self.admin_controller.get_all_reservations()
        self.reservations_tree.delete(*self.reservations_tree.get_children())
        for reservation in reservations:
            self.reservations_tree.insert('', 'end', values=(
            reservation.id_reservacion, reservation.id_usuario, reservation.id_computador, reservation.fecha_inicio,
            reservation.fecha_fin, reservation.estado))