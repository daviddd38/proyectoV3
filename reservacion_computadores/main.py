import tkinter as tk
from views.login_view import LoginView
from views.user_view import UserView
from views.admin_view import AdminView
from styles.theme import set_dark_theme, apply_rounded_corners


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservación de Computadores")
        self.geometry("1000x700")
        self.current_frame = None

        self.style = set_dark_theme(self)
        self.configure(bg='#2E3440')

        self.switch_frame(LoginView)

    def switch_frame(self, frame_class, *args, **kwargs):
        new_frame = frame_class(self, *args, **kwargs)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.after(10, lambda: self.safe_apply_rounded_corners(self.current_frame))

    def safe_apply_rounded_corners(self, widget):
        try:
            canvas = apply_rounded_corners(widget)
            for child in widget.winfo_children():
                if child != canvas:
                    child.lift()
        except Exception as e:
            print(f"No se pudieron aplicar bordes redondeados: {e}")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()