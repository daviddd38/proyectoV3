from reservacion_computadores.models.usuario import Usuario

class AuthController:
    def login(self, email, password):
        print(f"Intento de inicio de sesión para {email}")
        try:
            user = Usuario.get_by_email(email)
            if user and user.contrasena == password:  # En una aplicación real, verifica el hash de la contraseña
                print(f"Inicio de sesión exitoso para {email}")
                return user
            print(f"Inicio de sesión fallido para {email}")
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")
        return None