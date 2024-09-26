from .database import Database
from datetime import datetime

class Reservacion:
    def __init__(self, id_reservacion, id_usuario, id_computador, fecha_inicio, fecha_fin, estado):
        self.id_reservacion = id_reservacion
        self.id_usuario = id_usuario
        self.id_computador = id_computador
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.nombre_computador = None

    @staticmethod
    def get_all():
        db = Database()
        try:
            db.connect()
            query = "SELECT * FROM Reservaciones"
            cursor = db.execute_query(query)
            return [Reservacion(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener todas las reservaciones: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def get_all_active():
        db = Database()
        try:
            db.connect()
            query = "SELECT * FROM Reservaciones WHERE estado = 'activa'"
            cursor = db.execute_query(query)
            return [Reservacion(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener las reservaciones activas: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def update_status(id_reservacion, new_status):
        db = Database()
        try:
            db.connect()
            query = "UPDATE Reservaciones SET estado = %s WHERE id_reservacion = %s"
            db.execute_query(query, (new_status, id_reservacion))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el estado de la reservación: {e}")
            db.rollback()
            return False
        finally:
            db.disconnect()

    @staticmethod
    def get_total_count():
        db = Database()
        try:
            db.connect()
            query = "SELECT COUNT(*) FROM Reservaciones"
            cursor = db.execute_query(query)
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al obtener el total de reservaciones: {e}")
            return 0
        finally:
            db.disconnect()

    @staticmethod
    def get_active_count():
        db = Database()
        try:
            db.connect()
            query = "SELECT COUNT(*) FROM Reservaciones WHERE estado = 'activa'"
            cursor = db.execute_query(query)
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al obtener el total de reservaciones activas: {e}")
            return 0
        finally:
            db.disconnect()

    @staticmethod
    def create(id_usuario, id_computador, fecha_inicio, fecha_fin):
        db = Database()
        try:
            db.connect()
            query = """
                INSERT INTO Reservaciones (id_usuario, id_computador, fecha_inicio, fecha_fin, estado)
                VALUES (%s, %s, %s, %s, 'activa')
                """
            db.execute_query(query, (id_usuario, id_computador, fecha_inicio, fecha_fin))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al crear la reservación: {e}")
            db.rollback()
            return False
        finally:
            db.disconnect()

    @staticmethod
    def get_user_reservations(user_id):
        db = Database()
        try:
            db.connect()
            query = """
            SELECT r.id_reservacion, r.id_usuario, r.id_computador, r.fecha_inicio, r.fecha_fin, r.estado, c.nombre
            FROM Reservaciones r
            JOIN Computadores c ON r.id_computador = c.id_computador
            WHERE r.id_usuario = %s
            ORDER BY r.fecha_inicio DESC
            """
            cursor = db.execute_query(query, (user_id,))
            reservations = []
            for row in cursor.fetchall():
                reservation = Reservacion(*row[:6])
                reservation.nombre_computador = row[6]
                if isinstance(reservation.fecha_inicio, str):
                    reservation.fecha_inicio = datetime.strptime(reservation.fecha_inicio, "%Y-%m-%d %H:%M:%S")
                if isinstance(reservation.fecha_fin, str):
                    reservation.fecha_fin = datetime.strptime(reservation.fecha_fin, "%Y-%m-%d %H:%M:%S")
                reservations.append(reservation)
            return reservations
        except Exception as e:
            print(f"Error al obtener las reservaciones del usuario: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def get_active_reservations_for_computer(computer_id):
        db = Database()
        try:
            db.connect()
            query = """
                SELECT * FROM Reservaciones
                WHERE id_computador = %s AND estado = 'activa' AND fecha_fin > NOW()
                ORDER BY fecha_inicio
                """
            cursor = db.execute_query(query, (computer_id,))
            reservations = []
            for row in cursor.fetchall():
                reservation = Reservacion(*row)
                if isinstance(reservation.fecha_inicio, str):
                    reservation.fecha_inicio = datetime.strptime(reservation.fecha_inicio, "%Y-%m-%d %H:%M:%S")
                if isinstance(reservation.fecha_fin, str):
                    reservation.fecha_fin = datetime.strptime(reservation.fecha_fin, "%Y-%m-%d %H:%M:%S")
                reservations.append(reservation)
            return reservations
        except Exception as e:
            print(f"Error al obtener las reservaciones activas del computador: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def check_conflicts(computer_id, start_time, end_time):
        db = Database()
        try:
            db.connect()
            query = """
                SELECT * FROM Reservaciones
                WHERE id_computador = %s AND estado = 'activa'
                AND ((fecha_inicio <= %s AND fecha_fin > %s)
                OR (fecha_inicio < %s AND fecha_fin >= %s)
                OR (fecha_inicio >= %s AND fecha_fin <= %s))
                """
            cursor = db.execute_query(query,
                                      (computer_id, start_time, start_time, end_time, end_time, start_time, end_time))
            conflicts = cursor.fetchall()
            return len(conflicts) > 0
        except Exception as e:
            print(f"Error al verificar conflictos de reservación: {e}")
            return True
        finally:
            db.disconnect()


