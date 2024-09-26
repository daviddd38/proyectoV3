from .database import Database

class Usuario:
    def __init__(self, id_usuario, nombre, apellido, email, contrasena, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def login(email, contrasena):
        db = Database()
        try:
            db.connect()
            query = """
            SELECT id_usuario, nombre, apellido, email, contrasena, rol
            FROM Usuarios
            WHERE email = %s AND contrasena = %s
            """
            cursor = db.execute_query(query, (email, contrasena))
            user_data = cursor.fetchone()
            if user_data:
                return Usuario(*user_data)
            return None
        except Exception as e:
            print(f"Error en el login: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def register(nombre, apellido, email, contrasena):
        db = Database()
        try:
            db.connect()
            check_query = "SELECT * FROM Usuarios WHERE email = %s"
            cursor = db.execute_query(check_query, (email,))
            if cursor.fetchone():
                return False, "El correo electrónico ya está registrado."

            query = "INSERT INTO Usuarios (nombre, apellido, email, contrasena, rol) VALUES (%s, %s, %s, %s, 'usuario')"
            db.execute_query(query, (nombre, apellido, email, contrasena))
            db.commit()
            return True, "Usuario registrado correctamente."
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            db.rollback()
            return False, f"Error al registrar usuario: {str(e)}"
        finally:
            db.disconnect()

    @staticmethod
    def get_by_id(user_id):
        db = Database()
        try:
            db.connect()
            query = "SELECT id_usuario, nombre, apellido, email, contrasena, rol FROM Usuarios WHERE id_usuario = %s"
            cursor = db.execute_query(query, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return Usuario(*user_data)
            return None
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def get_total_count():
        db = Database()
        try:
            db.connect()
            query = "SELECT COUNT(*) FROM Usuarios"
            cursor = db.execute_query(query)
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al obtener el total de usuarios: {e}")
            return 0
        finally:
            db.disconnect()

    @staticmethod
    def get_all():
        db = Database()
        try:
            db.connect()
            query = "SELECT id_usuario, nombre, apellido, email, contrasena, rol FROM Usuarios"
            cursor = db.execute_query(query)
            return [Usuario(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []
        finally:
            db.disconnect()