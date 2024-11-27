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
    
    def agregarOrden(self, dni_cliente, id_producto, cantidad, fecha):
        query = "CALL AgregarOrden(%s, %s, %s, %s, @resultado)" # HACEMOS LOS CAMBIOS Y DESPUES OBTENEMOS EL OUTPUT PARA VER SI SALIO Todo BIEN.
        valores = (dni_cliente, id_producto, cantidad, fecha) # internamente, el procedimiento sql usado aca, hace que el stock de un producto baje cuando se ejecuta el codigo
        self.db.ejecutar(query, valores)
        
        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0] # Extraemos el primer elemento del primer tuple

        return resultado # Es True si se agrega la orden y False si el no existe el id producto, dni o si el producto no tiene suficiente stock. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS