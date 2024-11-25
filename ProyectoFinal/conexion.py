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

db = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
if db.conectar():
    print("Database is ready to use.")
else:
    print("Failed to connect to the database.")

db.desconectar()
