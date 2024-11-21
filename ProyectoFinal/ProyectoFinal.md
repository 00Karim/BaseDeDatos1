# Proyecto final: Sistema de ventas en linea

**Entidades de la BD:**

Las entidades de la base de datos (Tienda) van a ser las siguientes:

1. Cliente
2. Producto
3. Orden de compra

Cada una va a tener su tabla correspondiente con todas sus instancias

Las tablas y atributos de la base de datos van a ser los siguientes:

1. Clientes
    - `dni_cliente`
    - `nombre`
    - `apellido`
    - `mail`
2. Productos
    - `id_producto`
    - `nombre`
    - `cantidad_disponible`
    - `categoria`
    - `ventas_totales`
3. Ordenes de compra
    - `id_orden`
    - `id_cliente`
    - `id_producto`
    - `cantidad`
    - `fecha`

### Diseño en Tercera Forma Normal (3NF)

El diseño en 3FN sería el siguiente

1. **Tabla `Clientes`**
    - `dni_cliente` (Clave primaria)
    - `nombre`
    - `apellido`
    - `mail`

    Creamos la tabla **`Clientes`** que va a almacenar instancias unicas de cada cliente que se registre. Nos vamos a asegurar de que sean unicos adquiriendo sus dnis. Haciendo una tabla para almacenar a cada cliente particular nos ahorramos el tener que repetir el nombre, apellido o mail de un cliente en caso de que haga muchos pedidos.

2. **Tabla `Productos`**
    - `id_producto` (Clave primaria)
    - `nombre`
    - `cantidad_disponible`
    - `categoria`

    Creamos la tabla **`Productos`** que va a almacenar instancias unicas de cada producto que exista dentro de la tienda. Cada producto va a tener un id propio asi nos aseguramos de que sean unicos y no se repitan a lo largo la tabla. Le agregamos el atributo `categoria` para poder manejar productos basandonos en esta caracteristica, por ejemplo si la empresa decide que ya no quiere vender juguetes entonces seria mas facil eliminar esos productos si los identificamos como tal.


3. **Table `Ordenes_de_compra`**
    - `id_orden` (Clave primaria)
    - `id_cliente` (Clave foranea referenciando a **`Clientes`**)
    - `id_producto` (Clave foranea referenciando a **`Productos`**)
    - `cantidad`
    - `fecha`

    Creamos la tabla **`Ordenes_de_compra`**. Esta tabla depende de las otras dos. Le tenemos que dar un id unico como a las otras tablas porque puede ocurrir que un cliente pida dos veces la misma cantidad del mismo producto en el mismo dia. Incluyendo el `id_cliente` podemos saber a quien corresponde el pedido y con `id_producto` podemos saber que producto pidio ese cliente y relacionar ambos datos con sus tablas asi no tenemos que repetir la informacion de ambas entidades por cada vez que sean incluidos en una orden de compra.


# SQL de las tablas

```sql
CREATE TABLE Clientes (
    dni_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150),
    apellido VARCHAR(150)
    );

CREATE TABLE Productos(
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150),
    cantidad_disponible INT,
    categoria VARCHAR(20),
    ventas_totales INT,
    CHECK(categoria IN ('Carnes', 'Nueces', 'Bebidas')) -- Vemos que otras categorias podriamos agregar
    );

CREATE TABLE OrdenesDeCompra(
    id_orden INT PRIMARY KEY AUTO_INCREMENT,
    dni_cliente INT,
    id_producto INT,
    cantidad INT,
    fecha DATE,
    FOREIGN KEY (dni_cliente) REFERENCES Clientes(dni_cliente) ON UPDATE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto) ON UPDATE CASCADE
    )
```

# SQL GET GENERAL DE TABLA
Podriamos representar a cada tabla con un numero en vez de su nombre entero, pero de esta manera el codigo es mas intuitivo y legible por lo que preferimos dejarlo asi.
```sql
DELIMITER //
CREATE PROCEDURE ObtenerTablas
(
    IN Tabla VARCHAR(10)
)
    BEGIN
        IF Tabla = 'clientes' THEN
            SELECT * FROM clientes;
        ELSEIF Tabla = 'productos' THEN
            SELECT * FROM productos;
        ELSE
            SELECT * FROM ordenesdecompra;
        END IF;
    END //
DELIMITER ; 

```

# SQL AUMENTAR LAS VENTAS TOTALES DE PRODUCTO
```sql

```

# SQL OBTENER LA CANTIDAD TOTAL DE ORDENES DEL CLIENTE (Con un procedimiento que COUNT * las ordenes con el id del cliente)
```sql
```

# SQL BOTON DE ORDENAR POR `atributo`
```sql
```

# SQL OBTENER POR MAXIMO O MINIMO DE UN `atributo`
```sql
```

# SQL Get cliente por dni o por nombre
```sql
DELIMITER //
CREATE PROCEDURE ObtenerClientePorDNI
(
IN dni INT
)
    BEGIN
        SELECT * FROM clientes
        WHERE clientes.dni_cliente = dni;
    END //
DELIMITER ; 
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE ObtenerClientePorNombre
(
IN nombre_input VARCHAR(150)
)
    BEGIN
        SELECT * FROM clientes
        WHERE clientes.nombre = nombre_input;
    END //
DELIMITER ;
```

# SQL Borrar cliente por dni o por nombre
Podriamos hacer, en todos los casos, que el nombre simplemente nos lleve a adquirir el dni. Por ende solo vamos a precisar la funcion de sql siguiente para eliminar un elemento y asi no tener que hacer otro procedure, ademas que borrar por nombre es peligroso ya que pueden haber 2 clientes con nombres parecidos.
Entonces la idea seria que el usuario busque clientes por cierto nombre y luego eliga entre la lista a cual o cuales quiere borrar.
```sql
DELIMITER //
CREATE PROCEDURE EliminarClientePorDNI
(
IN dni INT,
OUT resultado BOOL
)
    BEGIN
        DELETE FROM clientes
        WHERE clientes.dni_cliente = dni;
	
        IF ROW_COUNT() > 0 THEN
            SET resultado = TRUE;
        ELSE 
            SET resultado = FALSE; # El cliente no existe o ya fue eliminado
        END IF;
    
    END //
DELIMITER ; 
```

# SQL Agregar cliente
```sql
DELIMITER //
CREATE PROCEDURE AgregarCliente
(
IN dni INT,
IN nombre VARCHAR(150),
IN apellido VARCHAR(150),
OUT resultado BOOL
)
	BEGIN
        DECLARE existe INT;
        
        SELECT COUNT(*) INTO existe 
        FROM clientes WHERE dni_cliente = dni;
        
        IF existe > 0 THEN
            SET resultado = FALSE; # El cliente ya existe
        ELSE
            INSERT INTO clientes VALUES(dni, nombre, apellido);
            SET resultado = TRUE;
        END IF;
    END //
DELIMITER ; 
```

# SQL Modificar cliente por dni o por nombre
```sql
DELIMITER //
CREATE PROCEDURE ModificarClientePorDNI
(
IN dni INT,
IN nombre_input VARCHAR(150),
IN apellido_input VARCHAR(150),
OUT resultado BOOLEAN
)
    BEGIN
        UPDATE clientes
        SET nombre = nombre_input, apellido = apellido_input 
        WHERE clientes.dni_cliente = dni;
    
        IF ROW_COUNT() > 0 THEN
            SET resultado = TRUE;
        ELSE 
            SET resultado = FALSE; # El cliente no existe o hubo un error durante la ejecucion yqc
        END IF;
    END //
DELIMITER ; 
```

# SQL Get producto por id o por nombre
```sql
```

# SQL Get productos por categoria
```sql
```

# SQL Borrar producto por id o por nombre
```sql
DELIMITER //
CREATE PROCEDURE EliminarProductoPorID
(
IN id INT,
OUT resultado BOOL
)
    BEGIN
        DELETE FROM productos
        WHERE productos.id_producto = id;
	
        IF ROW_COUNT() > 0 THEN
            SET resultado = TRUE;
        ELSE 
            SET resultado = FALSE; # El producto no existe o ya fue eliminado
        END IF;
    
    END //
DELIMITER ; 
```

# SQL Borrar categorias
```sql
```

# SQL Agregar producto
```sql
DELIMITER //
CREATE PROCEDURE AgregarProducto
(
IN nombre VARCHAR(150),
IN cantidad_disponible INT,
IN categoria VARCHAR(150),
OUT resultado BOOL
)
    BEGIN
        DECLARE existe INT;
        
        SELECT COUNT(*) INTO existe 
        FROM productos WHERE # Que condicion, cuando se cumple, indicaria que 
        esta instancia del objeto ya existe? Porque el id se asigna solo, entonces 
        quizas podriamos chequear el nombre y darle la oportunidad al usuario de si 
        quiere agregar el producto igualmente? Algo corte: "Ya existe un producto 
        con ese nombre, deseas agregarlo igualmente?"
        
        IF existe > 0 THEN
            SET resultado = FALSE; # El producto ya existe
        ELSE
            INSERT INTO productos VALUES(nombre, cantidad_disponible, categoria);
            SET resultado = TRUE;
        END IF;
    END //
DELIMITER ; 
```

# SQL Modificar producto por id o por nombre
```sql
```

### Diseño pasado por https://dbdiagram.io/

    