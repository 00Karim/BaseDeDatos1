from conexion import BaseDeDatos

class Producto:
    def __init__(self, db):
        self.db = db

    def verProductos(self):
        query = "CALL ObtenerTablas('productos')"
        return self.db.obtener_datos(query)

    def verProductoPorAtributo(self):
        pass

# bdd = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
# bdd.conectar()
# db = Producto(bdd)

# print(db.verProductos())