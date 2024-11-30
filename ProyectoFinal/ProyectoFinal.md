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
CREATE TABLE Clientes(
	dni_cliente INT PRIMARY KEY,
    nombre VARCHAR(150),
    apellido VARCHAR(150),
    mail VARCHAR(150),
    CONSTRAINT chequear_largo_dni CHECK (LENGTH(dni_cliente) = 8)
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
    dni_cliente INT DEFAULT NULL,
    id_producto INT DEFAULT NULL,
    cantidad INT,
    fecha DATE,
    estado VARCHAR(20),
    FOREIGN KEY (dni_cliente) REFERENCES Clientes(dni_cliente)
    ON UPDATE CASCADE ON DELETE SET NULL, -- De esta manera, cuando se elimine un cliente (lo cual no seria posible sin poner DEFAULT NULL despues de declara el atributo) el atibuto va a pasar a ser Null y asi no hay inconsistencias en la tabla: Si un cliente no existe, entonces no pudo haber hecho un pedido
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
    ON UPDATE CASCADE ON DELETE SET NULL, -- Lo mismo con el producto: Si un producto no existe, entonces no pudo haber sido encargado
    CHECK(estado IN ('En proceso', 'Entregado'))
)

```

# SQL GET GENERAL DE TABLA
Podriamos representar a cada tabla con un numero en vez de su nombre entero, pero de esta manera el codigo es mas intuitivo y legible por lo que preferimos dejarlo asi.
```sql
DELIMITER //
CREATE PROCEDURE ObtenerTablas
(
    IN Tabla VARCHAR(20)
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

# SQL AUMENTAR LAS VENTAS TOTALES DE PRODUCTO Y DISMINUIR CANTIDAD_DISPONIBLE
```sql
DELIMITER //

CREATE PROCEDURE ActualizarInventarioVentas(
    IN producto_id INT,
    IN cantidad_vendida INT
)
BEGIN
    UPDATE Productos
    SET ventas_totales = ventas_totales + cantidad_vendida
    WHERE id_producto = producto_id;

    UPDATE Productos
    SET cantidad_disponible = cantidad_disponible - cantidad_vendida
    WHERE id_producto = producto_id;
END //

DELIMITER ;
```

# SQL OBTENER LA CANTIDAD TOTAL DE ORDENES DEL CLIENTE (Con un procedimiento que COUNT * las ordenes con el id del cliente)
```sql
DELIMITER //
CREATE PROCEDURE ObtenerCantOrdCliente(
    IN cliente_id INT
)
BEGIN
    SELECT COUNT(*) FROM ordenesdecompra
    WHERE cliente_id = dni_cliente;
END //
DELIMITER ;
```

# SQL BOTON DE ORDENAR POR `atributo`
```sql
```

# SQL OBTENER POR MAXIMO O MINIMO DE UN `atributo`
```sql
```

# SQL Get cliente por dni, por nombre o por apellido
```sql
DELIMITER //
CREATE PROCEDURE ObtenerClientePorDni
(
    IN dni VARCHAR(20)
)
BEGIN
    IF dni = '' THEN
        SELECT * FROM clientes;
    ELSE
        SELECT * FROM productos WHERE id_producto = CAST(producto_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END//
DELIMITER ; 
```
# -------------------------------------------------------------------------
```sql
DELIMITER //
CREATE PROCEDURE ObtenerClientePorNombre
(
IN nombre_input VARCHAR(150),
)
    BEGIN
        SELECT * FROM clientes
        WHERE nombre LIKE CONCAT('%', nombre_input, '%');
    END //
DELIMITER ;
```
# ------------------------------------------------------------------------
```sql
DELIMITER //
CREATE PROCEDURE ObtenerClientePorApellido
(
IN apellido_input VARCHAR(150),
OUT resultado BOOLEAN
)
    BEGIN
        SELECT * FROM clientes
        WHERE apellido LIKE CONCAT('%', apellido_input, '%');
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

# SQL Modificar cliente por dni 
```sql
DELIMITER //
CREATE PROCEDURE ModificarClientePorDNI(
    IN dni INT,
    IN nombre_input VARCHAR(150),
    IN apellido_input VARCHAR(150),
    IN mail_input VARCHAR(150),
    OUT resultado BOOLEAN
)
BEGIN
    UPDATE clientes
    SET 
        nombre = CASE 
                    WHEN nombre_input != '' THEN nombre_input -- Si la columna no esta vacia entonces la reemplazamos
                    ELSE nombre -- Si la columna esta vacia entonces vamos a dejarla con el valor con el que estaba
                 END, -- De esta manera podemos modificar una variable por vez asi no es necesario ingresar todos los atributos si queremos modificar 1 solo
        apellido = CASE 
                    WHEN apellido_input != '' THEN apellido_input 
                    ELSE apellido 
                  END,
        mail = CASE 
                    WHEN mail_input != '' THEN mail_input 
                    ELSE mail 
               END
    WHERE clientes.dni_cliente = dni;

    IF (SELECT COUNT(*) FROM clientes WHERE dni_cliente = dni) > 0 THEN
		SET resultado = TRUE; -- Hay un cliente con ese dni
	ELSE
		SET resultado = FALSE; -- No hay un cliente con ese dni
	END IF;
END //
DELIMITER ; 
```

# SQL Get producto por id o por nombre
```sql
DELIMITER //
CREATE PROCEDURE ObtenerProductoPorId
(
    IN producto_id VARCHAR(5)
)
BEGIN
    IF producto_id = '' THEN
        SELECT * FROM productos;
    ELSE
        SELECT * FROM productos WHERE id_producto = CAST(producto_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END//

DELIMITER ;
```
# -------------------------------------------------------------------------
```sql
DELIMITER //

CREATE PROCEDURE ObtenerProductoPorNombre
(
    IN producto_nombre VARCHAR(255)
)

BEGIN
    SELECT * FROM productos
    WHERE nombre LIKE CONCAT('%', producto_nombre, '%')
END//

DELIMITER;
```
# SQL Get productos por categoria
```sql
DELIMITER //

CREATE PROCEDURE ObtenerProductoPorCategoria
(
    IN categoria_nombre VARCHAR(255)
)

BEGIN
    SELECT * FROM productos
    WHERE categoria LIKE CONCAT('%', categoria_nombre, '%');
END//

DELIMITER;
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
DELIMITER //
CREATE PROCEDURE BorrarCategorias(
    IN categoria_nombre VARCHAR(255)
)
BEGIN
    DELETE FROM productos
    WHERE categoria = categoria_nombre;
END //
DELIMITER ; 
```

# SQL Agregar producto
```sql
DELIMITER //
CREATE PROCEDURE AgregarProducto
(
IN nombre VARCHAR(150),
IN cantidad_disponible INT,
IN categoria VARCHAR(150),
OUT resultado INT
)
BEGIN
        DECLARE existe INT;
        
        SELECT COUNT(*) INTO existe 
        FROM productos WHERE productos.nombre = nombre;
        
        IF existe > 0 THEN
            SET resultado = 1; # Ya hay un producto con ese nombre
		ELSEIF cantidad_disponible < 0 THEN
			SET resultado = 2; # La cantidad disponible no puede ser negativa
        ELSE
            INSERT INTO productos (nombre, cantidad_disponible, categoria, ventas_totales) 
            VALUES(nombre, cantidad_disponible, categoria, 0);
            SET resultado = 3;
        END IF;
    END //
DELIMITER ; 
```

# SQL Modificar producto por id o por nombre
```sql
DELIMITER // 
CREATE PROCEDURE ModificarProductoPorId(
IN id INT,
IN nombre_nuevo VARCHAR(150),
IN cantidad_disponible_nueva INT,
IN categoria_nueva VARCHAR(150),
OUT resultado INT
)
BEGIN
	DECLARE cantidad_orden_vieja INT; -- Esta variable va a almacenar el valor de la cantidad de la orden que vamos a modificar y asi poder modificar los stocks de los productos
    DECLARE producto_orden_vieja INT; -- Con esta variable vamos a saber si el producto va a ser cambiado y asi vamos a saber que stocks de que productos van a tener que ser modificados, porque esto implica que la orden anterior estaba mal hecha por lo que vamos a tener que recuperar esa cantidad ordenada y luego sacarle la cantidad nueva al producto ingresado nuevo
    DECLARE cantidad_disponible_producto_nuevo INT; -- Con esta variable vamos a saber si el stock del producto elegido va a ser suficiente para abastecer la orden. Esta variable puede ser aplicada en ambos casos: Que el producto siga siendo el mismo o que el producto de la orden cambie
    SET cantidad_orden_vieja = (SELECT cantidad FROM ordenesdecompra WHERE id_orden = orden_id); -- Obtenemos la cantidad actual de la orden
    SET producto_orden_vieja = (SELECT id_producto FROM ordenesdecompra WHERE id_orden = orden_id); -- Obtenemos el producto actual de la orden
    SET cantidad_disponible_producto_nuevo = (SELECT cantidad_disponible FROM productos WHERE id_producto = producto_id_nuevo); -- Obtenemos el stock del nuevo producto
    SET resultado = 6; -- Inicializamos el valor en 6, luego si este valor sigue siendo 6 significa que los valores son todos correctos, entonces vamos a ejecutar el código que modifica el producto

    IF (SELECT COUNT(*) FROM ordenesdecompra WHERE id_orden = orden_id) = 0 THEN -- Chequear que el id_orden sea válido
		SET resultado = 1; -- No existe una orden con ese id
	ELSEIF (SELECT COUNT(*) FROM clientes WHERE dni_cliente = cliente_dni_nuevo) = 0 THEN -- Chequear que el dni sea válido
		SET resultado = 2; -- No existe un cliente con ese dni
	ELSEIF (SELECT COUNT(*) FROM productos WHERE id_producto = producto_id_nuevo) = 0 THEN -- Chequear que el producto id sea válido
		SET resultado = 3; -- No existe un producto con ese id
	ELSEIF cantidad_orden_nueva < 0 THEN
		SET resultado = 4; -- La cantidad nueva no puede ser negativa
	ELSEIF producto_id_nuevo = producto_orden_vieja THEN -- Si el producto sigue siendo el mismo
		IF cantidad_disponible_producto_nuevo + (cantidad_orden_vieja - cantidad_orden_nueva) < 0 THEN -- Chequear que haya suficiente stock para la cantidad nueva
			SET resultado = 5; -- El stock del producto no es suficiente para abastecer el cambio de tamaño de la orden
		ELSE -- Si hay stock suficiente para efectuar la orden:
			UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL AND cantidad_orden_nueva IS NOT NULL THEN cantidad_disponible + (cantidad_orden_vieja - cantidad_orden_nueva) 
                    ELSE cantidad_disponible
                END, -- Modificamos el stock del producto devolviendo la cantidad usada en la orden cambiada y efectuando la resta de stock usando la nueva cantidad ordenada: cantidad_disponible = cantidad_disponible + (cantidad_orden_vieja - cantidad_orden_nueva)
                ventas_totales = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN ventas_totales + (cantidad_orden_nueva - cantidad_orden_vieja) 
                    ELSE ventas_totales
                END -- También modificamos las ventas totales
            WHERE id_producto = producto_id_nuevo;
            SET resultado = 6; -- 6 = Hasta ahora todo salió bien y podemos proseguir con modificar la orden
        END IF;
	ELSEIF producto_id_nuevo != producto_orden_vieja THEN -- Si los productos cambiaron
		IF cantidad_disponible_producto_nuevo - cantidad_orden_nueva < 0 THEN -- Chequear que haya suficiente stock para ordenar del nuevo producto
			SET resultado = 7; -- No hay stock suficiente en el nuevo producto ingresado
		ELSE -- Si hay stock suficiente:
			UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN cantidad_disponible - cantidad_orden_nueva
                    ELSE cantidad_disponible
                END, -- Modificamos el stock del producto nuevo: cantidad_disponible = cantidad_disponible - cantidad_orden_nueva
                ventas_totales = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN ventas_totales + cantidad_orden_nueva
                    ELSE ventas_totales
                END -- Modificamos las ventas totales del producto nuevo
            WHERE id_producto = producto_id_nuevo; 
			UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL THEN cantidad_disponible + cantidad_orden_vieja
                    ELSE cantidad_disponible
                END, -- Recuperamos todo el stock del producto cambiado: cantidad_disponible = cantidad_disponible + cantidad_orden_vieja
                ventas_totales = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL THEN ventas_totales - cantidad_orden_vieja
                    ELSE ventas_totales
                END -- Recuperamos las ventas totales del producto cambiado
            WHERE id_producto = producto_orden_vieja; 
			SET resultado = 6; -- 6 = Hasta ahora todo salió bien y podemos proseguir con modificar la orden
        END IF;
    END IF;

    -- Finalmente, si no hubo ninguna excepción, modificamos la orden correspondiente con los valores ingresados
    IF resultado = 6 THEN
		UPDATE ordenesdecompra
        SET dni_cliente = cliente_dni_nuevo, id_producto = producto_id_nuevo, cantidad = cantidad_orden_nueva, fecha = fecha_nueva
        WHERE id_orden = orden_id;
        SET resultado = 6; -- Se modificó la orden correctamente
	END IF;
END //
DELIMITER ;
```

### Diseño pasado por https://dbdiagram.io/


# SQL Obtener orden por id_orden
```sql
DELIMITER //
CREATE PROCEDURE ObtenerOrdenPorId
(
    IN orden_id VARCHAR(10)
)
BEGIN
    IF orden_id = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE id_orden = CAST(orden_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END//
DELIMITER ;
```

# SQL Obtener orden por id_producto
```sql
DELIMITER //
CREATE PROCEDURE ObtenerOrdenPorIdProducto
(
    IN producto_id VARCHAR(10)
)
BEGIN
    IF producto_id = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE id_producto = CAST(producto_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END//
DELIMITER ;
```

# SQL Obtener orden por dni_cliente
```sql
DELIMITER //
CREATE PROCEDURE ObtenerOrdenPorDniCliente
(
    IN cliente_dni VARCHAR(10)
)
BEGIN
    IF cliente_dni = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE dni_cliente = CAST(cliente_dni AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END//
DELIMITER ;
```

# SQL Agregar Orden
```sql
DELIMITER //
CREATE PROCEDURE AgregarOrden
(
IN cliente_dni VARCHAR(150),
IN producto_id INT,
IN cantidad_pedido VARCHAR(150),
IN fecha DATE, 
OUT resultado INT
)
BEGIN
		IF cantidad_pedido < 0 THEN
			SET resultado = 1; # -- La cantidad del pedido no puede ser negativa
		ELSEIF (SELECT cantidad_disponible FROM productos WHERE id_producto = producto_id) - cantidad_pedido < 0 THEN
			SET resultado = 2; # -- No hay stock suficiente
		ELSEIF (SELECT COUNT(*) FROM productos WHERE id_producto = producto_id) = 0 THEN
			SET resultado = 3; -- No hay producto con ese id
		ELSEIF (SELECT COUNT(*) FROM clientes WHERE dni_cliente = cliente_dni) = 0 THEN
			SET resultado = 4; -- No hay cliente con ese dni
		ELSE
			INSERT INTO ordenesdecompra (dni_cliente, id_producto, cantidad, fecha) 
			VALUES(cliente_dni, producto_id, cantidad_pedido, fecha); -- Agregamos la orden
            UPDATE productos SET cantidad_disponible = cantidad_disponible - cantidad_pedido
            WHERE id_producto = producto_id; -- Disminuimos el stock del producto acorde al tamano del pedido
            SET resultado = 5; -- Exito
		END IF;
    END //
DELIMITER ; 
```

# MODIFICAR ORDEN POR ID
```sql
DELIMITER //
CREATE PROCEDURE ModificarOrdenPorId(
IN orden_id INT,
IN cliente_dni_nuevo INT,
IN producto_id_nuevo INT,
IN cantidad_orden_nueva INT,
IN fecha_nueva DATE,
OUT resultado INT
)
BEGIN
    DECLARE cantidad_orden_vieja INT; -- Esta variable va a almacenar el valor de la cantidad de la orden que vamos a modificar y asi poder modificar los stocks de los productos
    DECLARE producto_orden_vieja INT; -- Con esta variable vamos a saber si el producto va a ser cambiado y asi vamos a saber que stocks de que productos van a tener que ser modificados
    DECLARE dni_cliente_viejo VARCHAR(150); -- Agregado para almacenar el DNI del cliente viejo
    DECLARE cantidad_disponible_producto_nuevo INT; -- Con esta variable vamos a saber si el stock del producto elegido va a ser suficiente para abastecer la orden.
	DECLARE fecha_vieja DATE; -- Declaramos la fecha de la orden asi en caso de que no se ingrese una fecha podemos volver a ponerla como estaba usando esta variable
    
    -- Obtenemos los valores actuales de la orden asi en caso de que sean nulo los podemos guardar y volver a insertar en la fila asi solo se modifican los valores que fueron ingresados
    SET cantidad_orden_vieja = (SELECT cantidad FROM ordenesdecompra WHERE id_orden = orden_id);
    SET producto_orden_vieja = (SELECT id_producto FROM ordenesdecompra WHERE id_orden = orden_id);
    SET dni_cliente_viejo = (SELECT dni_cliente FROM ordenesdecompra WHERE id_orden = orden_id); 
    IF producto_id_nuevo IS NULL THEN
		SET cantidad_disponible_producto_nuevo = ( -- Agregamos esto porque si no lo agregabamos entonces mas adelante cuando se intentaba definir si habia suficiente stock, la cantidad disponible se inicializaba en un valor erroneo y por ende no se activaba el error de que el stock no es suficiente entonces se podia agregar cualquier cantidad
			SELECT p.cantidad_disponible 
			FROM productos p
			INNER JOIN ordenesdecompra o ON p.id_producto = o.id_producto
			WHERE o.id_orden = orden_id
			LIMIT 1
		);
    ELSE
		SET cantidad_disponible_producto_nuevo = (SELECT cantidad_disponible FROM productos WHERE id_producto = producto_id_nuevo);
    END IF;
    IF fecha_nueva IS NULL THEN
		SET fecha_vieja = ( -- Agregamos esto porque si no lo agregabamos entonces mas adelante la fecha se actualizaba como None
			SELECT o.fecha 
			FROM ordenesdecompra o
			WHERE o.id_orden = orden_id
			LIMIT 1
		);
	END IF;
    SET resultado = 6; -- Inicializamos el valor en 6, si no ocurre ningun error a lo largo del procedimiento entonces resultado = 6 va a cumplir cierta condicion mas adelante que permite continuar con la modificacion de la orden
    -- aca empieza la validacion de los parametros
    IF (SELECT COUNT(*) FROM ordenesdecompra WHERE id_orden = orden_id) = 0 THEN
        SET resultado = 1; -- No existe una orden con ese id
    ELSEIF cliente_dni_nuevo IS NOT NULL THEN -- Solo verificamos el DNI si fue proporcionado
        IF (SELECT COUNT(*) FROM clientes WHERE dni_cliente = cliente_dni_nuevo) = 0 THEN
            SET resultado = 2; -- No existe un cliente con ese dni
        END IF;
    ELSEIF producto_id_nuevo IS NOT NULL THEN -- Solo verificamos el producto si un producto fue ingresado
        IF (SELECT COUNT(*) FROM productos WHERE id_producto = producto_id_nuevo) = 0 THEN
            SET resultado = 3; -- No existe un producto con ese id
        END IF;
    ELSEIF cantidad_orden_nueva < 0 THEN
        SET resultado = 4; -- La cantidad nueva no puede ser negativa
    ELSEIF producto_id_nuevo = producto_orden_vieja OR producto_id_nuevo IS NULL THEN -- Si el producto sigue siendo el mismo
        IF cantidad_disponible_producto_nuevo + (cantidad_orden_vieja - cantidad_orden_nueva) < 0 THEN
            SET resultado = 5; -- El stock del producto no es suficiente para abastecer el cambio de tamaño de la orden
        ELSE
            UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL AND cantidad_orden_nueva IS NOT NULL THEN cantidad_disponible + (cantidad_orden_vieja - cantidad_orden_nueva) 
                    ELSE cantidad_disponible
                END,
                ventas_totales = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN ventas_totales + (cantidad_orden_nueva - cantidad_orden_vieja) 
                    ELSE ventas_totales
                END
            WHERE id_producto = producto_id_nuevo;
        END IF;
    END IF;
    IF producto_id_nuevo != producto_orden_vieja THEN -- Si los productos cambiaron, LO Ponemos en if porque por alguna razon cuando esta en elseif no es accesible
        IF cantidad_disponible_producto_nuevo < cantidad_orden_nueva THEN
            SET resultado = 7; -- No hay stock suficiente en el producto nuevo
        ELSE
            UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN cantidad_disponible - cantidad_orden_nueva
                    ELSE cantidad_disponible
                END,
                ventas_totales = CASE 
                    WHEN cantidad_orden_nueva IS NOT NULL THEN ventas_totales + cantidad_orden_nueva
                    ELSE ventas_totales
                END
            WHERE id_producto = producto_id_nuevo;

            UPDATE productos
            SET 
                cantidad_disponible = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL THEN cantidad_disponible + cantidad_orden_vieja
                    ELSE cantidad_disponible
                END,
                ventas_totales = CASE 
                    WHEN cantidad_orden_vieja IS NOT NULL THEN ventas_totales - cantidad_orden_vieja
                    ELSE ventas_totales
                END
            WHERE id_producto = producto_orden_vieja;
        END IF;
    END IF;

    -- Finalmente, si no hubo ninguna excepción, modificamos la orden correspondiente
    IF resultado = 6 THEN
        UPDATE ordenesdecompra
        SET 
            dni_cliente = CASE WHEN cliente_dni_nuevo IS NOT NULL THEN cliente_dni_nuevo ELSE dni_cliente_viejo END, -- Solo actualiza el dni si se proporcionó
            id_producto = CASE WHEN producto_id_nuevo IS NOT NULL THEN producto_id_nuevo ELSE producto_orden_vieja END, -- Solo actualiza el producto si se proporcionó
            cantidad = cantidad_orden_nueva, 
            fecha = CASE WHEN fecha_nueva IS NULL THEN fecha_vieja ELSE fecha_nueva END
        WHERE id_orden = orden_id;
    END IF;
END //
DELIMITER ;
```

    