from conexion import BaseDeDatos

class Orden:
    def __init__(self, db):
        self.db = db

    def verOrdenes(self):
        query = "CALL ObtenerTablas('ordenesdecompra')"
        return self.db.obtener_datos(query)

    def verOrdenPorAtributo(self, id_orden = None, dni_cliente = None, id_producto = None): # Dependiendo de que atributo sea ingresado se va a elegir un query y un valor correspondientes
        if id_orden is not None:
            query = "CALL ObtenerOrdenPorId(%s)"
            valor = id_orden
        if dni_cliente is not None:
            query = "CALL ObtenerOrdenPorDniCliente(%s)"
            valor = dni_cliente
        if id_producto is not None:
            query = "CALL ObtenerOrdenPorIdProducto(%s)"
            valor = id_producto
        return self.db.obtener_datos(query, valor)
    
    def agregarOrden(self, id_producto, dni_cliente, cantidad, fecha):
        query = "CALL AgregarOrden(%s, %s, %s, %s, @resultado)" # HACEMOS LOS CAMBIOS Y DESPUES OBTENEMOS EL OUTPUT PARA VER SI SALIO Todo BIEN.
        valores = (id_producto, dni_cliente, cantidad, fecha) # internamente, el procedimiento sql usado aca, hace que el stock de un producto baje cuando se ejecuta el codigo
        self.db.ejecutar(query, valores)
        
        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0] # Extraemos el primer elemento del primer tuple

        return resultado # Es True si se agrega la orden y False si el no existe el id producto, dni o si el producto no tiene suficiente stock. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS

    def modificarOrdenPorId(self, id_orden, dni_cliente, id_producto, cantidad, fecha):
        query = "CALL ModificarOrdenPorId(%s, %s, %s, %s, %s, @resultado)"
        valores = (id_orden, dni_cliente, id_producto, cantidad, fecha)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado # devuelv edistintos numeros y cada numero significa un error o advertencia distinta
    
    def eliminarOrdenPorId(self, id):
        query = "CALL EliminarOrdenPorID(%s, @resultado)"
        valores = (id)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado

def Tester():
    bdd = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
    bdd.conectar()
    db = Orden(bdd)

    print(db.agregarOrden(45378901, 9, 1, "2024-11-02"))

if __name__ == '__main__':
    Tester()