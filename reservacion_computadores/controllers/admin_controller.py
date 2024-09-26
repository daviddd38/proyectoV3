from reservacion_computadores.models.computador import Computador
from reservacion_computadores.models.reservacion import Reservacion
from reservacion_computadores.models.usuario import Usuario

class AdminController:
    def get_general_stats(self):
        total_computers = Computador.get_total_count()
        total_reservations = Reservacion.get_total_count()
        total_users = Usuario.get_total_count()
        return {
            "total_computers": total_computers,
            "total_reservations": total_reservations,
            "total_users": total_users
        }

    def get_all_computers(self):
        return Computador.get_all()

    def get_all_reservations(self):
        return Reservacion.get_all()

    def get_all_users(self):
        return Usuario.get_all()

    def add_computer(self, nombre, descripcion, estado):
        new_computer = Computador(None, nombre, descripcion, estado)
        new_computer.save()
        return new_computer

    def update_computer(self, id_computador, nombre, descripcion, estado):
        computer = Computador.get_by_id(id_computador)
        if computer:
            computer.nombre = nombre
            computer.descripcion = descripcion
            computer.estado = estado
            computer.save()
            return True
        return False

    def delete_computer(self, id_computador):
        Computador.delete(id_computador)

    def add_user(self, nombre, apellido, email, contrasena, rol):
        new_user = Usuario(None, nombre, apellido, email, contrasena, rol)
        new_user.save()
        return new_user

    def update_user(self, id_usuario, nombre, apellido, email, contrasena, rol):
        user = Usuario.get_by_id(id_usuario)
        if user:
            user.nombre = nombre
            user.apellido = apellido
            user.email = email
            user.contrasena = contrasena
            user.rol = rol
            user.save()
            return True
        return False

    def delete_user(self, id_usuario):
        Usuario.delete(id_usuario)