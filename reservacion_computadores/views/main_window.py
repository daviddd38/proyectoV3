import tkinter as tk
from reservacion_computadores.views.login_view import LoginView
from reservacion_computadores.views.admin_view import AdminView
from reservacion_computadores.views.user_view import UserView

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Reservación de Computadores")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)
        self.current_view = None
        self.show_login()

    def show_login(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginView(self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_admin_view(self, user):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = AdminView(self, user)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_user_view(self, user):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = UserView(self, user)
        self.current_view.pack(fill=tk.BOTH, expand=True)