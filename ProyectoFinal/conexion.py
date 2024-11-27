import mysql.connector

class BaseDeDatos:
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            # Try to connect to the database
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
            return True  # Connection successful
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Connection failed

    def desconectar(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexion cerrada")
        if self.cursor:
            self.cursor.close()

    def ejecutar(self, query, valores=None):
        self.cursor.execute(query, valores or ())
        self.conexion.commit()
        self.cursor.close()

    def obtener_datos(self, query, valores=None):
        cursor = self.conexion.cursor()
    
        try:
            cursor.execute(query, valores or ())
            datos = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            datos = []  # Si hay un error deurante la ejecucion, devolvemos una lista vacia
        finally:
            cursor.close()  # Nos aseguramos que se cierre el cursor para poder usar otro cursor la proxima vez
    
        return datos

# db = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
# if db.conectar():
#     print("Database is ready to use.")
# else:
#     print("Failed to connect to the database.")

# db.desconectar()
