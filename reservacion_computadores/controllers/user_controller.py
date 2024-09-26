from reservacion_computadores.models.usuario import Usuario
from reservacion_computadores.models.computador import Computador
from reservacion_computadores.models.reservacion import Reservacion
from datetime import datetime, timedelta


class UserController:
    def get_user_reservations(self, user_id):
        return Reservacion.get_user_reservations(user_id)

    def get_all_computers(self):
        return Computador.get_all()

    def get_computer_status(self, computer_id):
        computer = Computador.get_by_id(computer_id)
        if not computer:
            return "No disponible", None, None

        if computer.estado == 'mantenimiento':
            return "En mantenimiento", None, None

        now = datetime.now()
        reservations = Reservacion.get_active_reservations_for_computer(computer_id)

        if reservations:
            current_reservation = next((r for r in reservations if r.fecha_inicio <= now <= r.fecha_fin), None)
            if current_reservation:
                user = Usuario.get_by_id(current_reservation.id_usuario)
                user_name = f"{user.nombre} {user.apellido}" if user else "Usuario desconocido"
                return "Reservado", current_reservation.fecha_fin, user_name

            next_reservation = min(reservations, key=lambda r: r.fecha_inicio)
            return "Disponible", next_reservation.fecha_inicio, None

        return "Disponible", None, None

    def create_reservation(self, user_id, computer_id, start_time, end_time):
        # Verificar si el computador está disponible en ese horario
        status, _, _ = self.get_computer_status(computer_id)
        if status != "Disponible":
            return False

        # Verificar si hay conflictos con otras reservaciones
        conflicts = Reservacion.check_conflicts(computer_id, start_time, end_time)
        if conflicts:
            return False

        # Crear la reservación
        success = Reservacion.create(user_id, computer_id, start_time, end_time)
        if success:
            # Actualizar el estado del computador a 'reservado'
            Computador.update_status(computer_id, 'reservado')
        return success

    def login(self, email, password):
        return Usuario.login(email, password)

    def register_user(self, nombre, apellido, email, contrasena):
        return Usuario.register(nombre, apellido, email, contrasena)

    def check_and_update_reservations(self):
        now = datetime.now()
        all_reservations = Reservacion.get_all_active()
        for reservation in all_reservations:
            if reservation.fecha_fin < now:
                Reservacion.update_status(reservation.id_reservacion, 'finalizada')
                Computador.update_status(reservation.id_computador, 'disponible')