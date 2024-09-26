import tkinter as tk
from tkinter import ttk, messagebox
from reservacion_computadores.controllers.user_controller import UserController

class RegisterView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_controller = UserController()
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ttk.Label(self, text="Registro de Usuario", font=('Helvetica', 20, 'bold'))
        self.title_label.pack(pady=20)

        # Name
        self.name_label = ttk.Label(self, text="Nombre:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.pack(pady=5)

        # Surname
        self.surname_label = ttk.Label(self, text="Apellido:")
        self.surname_label.pack(pady=5)
        self.surname_entry = ttk.Entry(self, width=30)
        self.surname_entry.pack(pady=5)

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

        # Register Button
        self.register_button = ttk.Button(self, text="Registrarse", command=self.register)
        self.register_button.pack(pady=20)

        # Back to Login Button
        self.back_button = ttk.Button(self, text="Volver al Login", command=self.back_to_login)
        self.back_button.pack(pady=10)

    def register(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not all([name, surname, email, password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        success, message = self.user_controller.register_user(name, surname, email, password)
        if success:
            messagebox.showinfo("Éxito", message)
            self.back_to_login()
        else:
            messagebox.showerror("Error", message)

    def back_to_login(self):
        from reservacion_computadores.views.login_view import LoginView
        self.master.switch_frame(LoginView)