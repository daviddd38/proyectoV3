from .database import Database

class Computador:
    def __init__(self, id_computador, nombre, descripcion, estado):
        self.id_computador = id_computador
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def get_all():
        db = Database()
        try:
            db.connect()
            query = "SELECT * FROM Computadores"
            cursor = db.execute_query(query)
            computers = [Computador(*row) for row in cursor.fetchall()]
            return computers
        except Exception as e:
            print(f"Error al obtener todos los computadores: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def get_by_id(computer_id):
        db = Database()
        try:
            db.connect()
            query = "SELECT * FROM Computadores WHERE id_computador = %s"
            cursor = db.execute_query(query, (computer_id,))
            result = cursor.fetchone()
            if result:
                return Computador(*result)
            return None
        except Exception as e:
            print(f"Error al obtener el computador por ID: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def update_status(id_computador, new_status):
        db = Database()
        try:
            db.connect()
            query = "UPDATE Computadores SET estado = %s WHERE id_computador = %s"
            db.execute_query(query, (new_status, id_computador))
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el estado del computador: {e}")
            db.rollback()
            return False
        finally:
            db.disconnect()