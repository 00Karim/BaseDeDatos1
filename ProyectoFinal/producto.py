from conexion import BaseDeDatos

class Producto:
    def __init__(self, db):
        self.db = db

    def verProductos(self):
        query = "CALL ObtenerTablas('productos')"
        return self.db.obtener_datos(query)
    
    def verProductosPorVentas(self):
        query = "CALL ObtenerProductosPorMasVentas();"
        return self.db.obtener_datos(query)
    
    def verProductosPorStock(self):
        query = "CALL ObtenerProductosPorMenosStock();"
        return self.db.obtener_datos(query)

    def verProductoPorAtributo(self, id = None, nombre = None, categoria = None): # Dependiendo de que atributo sea ingresado se va a elegir un query y un valor correspondientes
        if id is not None:
            query = "CALL ObtenerProductoPorId(%s)"
            valor = id
        if nombre is not None:
            query = "CALL ObtenerProductoPorNombre(%s)"
            valor = nombre
        if categoria is not None:
            query = "CALL ObtenerProductoPorCategoria(%s)"
            valor = categoria
        return self.db.obtener_datos(query, valor)
    
    def agregarProducto(self, nombre, cantidad_disponible, categoria):
        query = "CALL AgregarProducto(%s, %s, %s, @resultado)" # HACEMOS LOS CAMBIOS Y DESPUES OBTENEMOS EL OUTPUT PARA VER SI SALIO Todo BIEN.
        valores = (nombre, cantidad_disponible, categoria)
        self.db.ejecutar(query, valores)
        
        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0] # Extraemos el primer elemento del primer tuple

        return resultado # Es True si se agrega el producto y False si el nombre del producto ya existe. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS

    def modificarProductoPorId(self, id, nombre, cantidad, categoria):
        query = "CALL ModificarProductoPorId(%s, %s, %s, %s, @resultado)"
        valores = (id, nombre, cantidad, categoria)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado # Es True si se modifica el producto y False si no hay producto con ese id. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS
    
    def eliminarProductoPorId(self, id):
        query = "CALL EliminarProductoPorID(%s, @resultado)"
        valores = (id)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado

def Tester():
    bdd = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
    bdd.conectar()
    db = Producto(bdd)

    print(db.agregarProducto('Nuezpr23', 34, 'Nueces'))

if __name__ == '__main__':
    Tester()