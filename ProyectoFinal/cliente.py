from conexion import BaseDeDatos

class Cliente:
    def __init__(self, db):
        self.db = db

    def verClientes(self):
        query = "CALL ObtenerTablas('clientes')"
        return self.db.obtener_datos(query)
    
    def verClientePorAtributo(self, dni = None, nombre = None, apellido = None): # Dependiendo de que atributo sea ingresado se va a elegir un query y un valor correspondientes
        if dni is not None:
            query = "CALL ObtenerClientePorDNI(%s)"
            valor = dni
        if nombre is not None:
            query = "CALL ObtenerClientePorNombre(%s)"
            valor = nombre
        if apellido is not None:
            query = "CALL ObtenerClientePorApellido(%s)"
            valor = apellido
        return self.db.obtener_datos(query, valor)
    
    def agregarCliente(self, dni, nombre, apellido, mail):
        query = "CALL AgregarCliente(%s, %s, %s, %s, @resultado)" # HACEMOS LOS CAMBIOS  
        valores = (dni, nombre, apellido, mail)
        self.db.ejecutar(query, valores)
        
        queryResultado = "SELECT @resultado" # OBTENEMOS EL OUTPUT PARA VER SI SALIO Todo BIEN.
        resultado = self.db.obtener_datos(queryResultado)[0][0] # Extraemos el primer elemento del primer tuple

        return resultado # Es True si se agrega el producto y False si el dni del cliente ya existe. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS
    
    def modificarClientePorDni(self, dni, nombre, apellido, mail):
        query = "CALL ModificarClientePorDNI(%s, %s, %s, %s, @resultado)"
        valores = (dni, nombre, apellido, mail)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado # Es True si se modifica el cliente y False si no hay cliente con ese cni. DESPUES, EN MENU.PY ESTE OUTPUT CAUSA DISTINTOS EFECTOS
    
    def eliminarClientePorDni(self, dni):
        query = "CALL EliminarClientePorDni(%s, @resultado)"
        valores = (dni)
        self.db.ejecutar(query, valores)

        queryResultado = "SELECT @resultado"
        resultado = self.db.obtener_datos(queryResultado)[0][0]

        return resultado