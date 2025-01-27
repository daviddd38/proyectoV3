import tkinter as tk
from tkinter import ttk, messagebox
from reservacion_computadores.controllers.user_controller import UserController
from reservacion_computadores.views.user_view import UserView
from reservacion_computadores.views.admin_view import AdminView
from reservacion_computadores.views.register_view import RegisterView

class LoginView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_controller = UserController()
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ttk.Label(self, text="Iniciar Sesión", font=('Helvetica', 20, 'bold'))
        self.title_label.pack(pady=20)

        # Email
        self.email_label = ttk.Label(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.pack(pady=5)

        # Password
        self.password_label = ttk.Label(self, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = ttk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=20)

        # Register Button
        self.register_button = ttk.Button(self, text="Registrarse", command=self.open_register_view)
        self.register_button.pack(pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        user = self.user_controller.login(email, password)
        if user:
            if user.rol == 'administrador':
                self.master.switch_frame(AdminView, admin=user)
            else:
                self.master.switch_frame(UserView, user=user)
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    def open_register_view(self):
        self.master.switch_frame(RegisterView)