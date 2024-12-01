DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerTablas`(
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

-- PROCEDIMIENTOS GESTION DE CLIENTES --

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerTablaClientes2`()
BEGIN
    SELECT 
        clientes.dni_cliente,
        clientes.nombre,
        clientes.apellido,
        clientes.mail,
        COALESCE(COUNT(ordenesdecompra.id_orden), 0) AS cantidad_de_ordenes # Con COALESCE nos aseguramos que si un cliente no tiene ningun pedido entonces su columna cantidad_de_ordenes sera 0, sin el COALESCE seria NULL en vez de 0
    FROM 
        clientes 
    LEFT JOIN 
        ordenesdecompra ON clientes.dni_cliente = ordenesdecompra.dni_cliente
    GROUP BY clientes.dni_cliente
	ORDER BY cantidad_de_ordenes DESC;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `AgregarCliente`(
IN dni INT,
IN nombre VARCHAR(150),
IN apellido VARCHAR(150),
IN mail VARCHAR(150),
OUT resultado BOOL
)
BEGIN
		DECLARE existe INT;
        
        SELECT COUNT(*) INTO existe 
        FROM clientes WHERE dni_cliente = dni;
        
        IF existe > 0 THEN
			SET resultado = FALSE;
		ELSE
			INSERT INTO clientes VALUES(dni, nombre, apellido, mail);
			SET resultado = TRUE;
		END IF;
    END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerClientePorDni`(
    IN dni VARCHAR(20)
)
BEGIN
    IF dni = '' THEN
        SELECT * FROM clientes;
    ELSE
        SELECT * FROM clientes WHERE dni_cliente = CAST(dni AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerClientePorNombre`(
IN nombre_input VARCHAR(150)
)
BEGIN
        SELECT * FROM clientes
        WHERE nombre LIKE CONCAT('%', nombre_input, '%');
    END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerClientePorApellido`(
IN apellido_input VARCHAR(150)
)
BEGIN
        SELECT * FROM clientes
        WHERE apellido LIKE CONCAT('%', apellido_input, '%');
    END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ModificarClientePorDNI`(
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

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `EliminarClientePorDNI`(
IN dni INT,
OUT resultado BOOL
)
BEGIN
		DELETE FROM clientes
        WHERE clientes.dni_cliente = dni;
	
		IF ROW_COUNT() > 0 THEN
			SET resultado = TRUE;
		ELSE 
			SET resultado = FALSE;
		END IF;
    
    END //
DELIMITER ;

-- PROCEDIMIENTOS GESTION DE PRODUCTOS --

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `AgregarProducto`(
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
            SET resultado = 3; -- Exito
        END IF;
    END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerProductoPorCategoria`(
    IN categoria_nombre VARCHAR(255)
)
BEGIN
    SELECT * FROM productos
    WHERE categoria LIKE CONCAT('%', categoria_nombre, '%');
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerProductoPorId`(
    IN producto_id VARCHAR(5)
)
BEGIN
    IF producto_id = '' THEN
        SELECT * FROM productos;
    ELSE
        SELECT * FROM productos WHERE id_producto = CAST(producto_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerProductoPorNombre`(
    IN producto_nombre VARCHAR(255)
)
BEGIN
    SELECT * FROM productos
    WHERE nombre LIKE CONCAT('%', producto_nombre, '%');
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerProductosPorMenosStock`()
BEGIN
    SELECT * FROM productos ORDER BY cantidad_disponible ASC;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerProductosPorMasVentas`()
BEGIN
    SELECT * FROM productos ORDER BY ventas_totales DESC;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ModificarProductoPorId`(
    IN id INT,
    IN nombre_nuevo VARCHAR(150),
    IN cantidad_disponible_nueva INT,
    IN categoria_nueva VARCHAR(150),
    OUT resultado INT
)
BEGIN
    IF cantidad_disponible_nueva < 0 THEN
        SET resultado = 1; -- La cantidad nueva no puede ser menor a 0
	ELSEIF (SELECT COUNT(*) FROM productos WHERE id_producto = id)  = 0 THEN
		SET resultado = 2; -- El producto elegido no existe
    ELSE
        UPDATE productos
        SET 
            nombre = CASE 
                        WHEN nombre_nuevo != '' THEN nombre_nuevo 
                        ELSE nombre 
                     END,
            cantidad_disponible = CASE 
                                     WHEN cantidad_disponible_nueva IS NOT NULL THEN cantidad_disponible_nueva 
                                     ELSE cantidad_disponible 
                                  END,
            categoria = CASE 
                           WHEN categoria_nueva != '' THEN categoria_nueva 
                           ELSE categoria 
                        END
        WHERE productos.id_producto = id;
        SET resultado = 3; -- Exito, se modifico correctamente
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `EliminarProductoPorID`(
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

-- PROCEDIMIENTOS GESTION DE ORDENES DE COMPRA -- 

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `AgregarOrden`(
IN cliente_dni VARCHAR(150),
IN producto_id INT,
IN cantidad_pedido VARCHAR(150),
IN fecha VARCHAR(40), 
OUT resultado INT
)
BEGIN
		DECLARE estado VARCHAR(20);
        SET estado = "En proceso"; -- La orden siempre va a ser agregada como en proceso, una vez que se entregue es responsabilidad del usuario cambiarla a entregado
		IF cantidad_pedido < 0 THEN
			SET resultado = 1; # -- La cantidad del pedido no puede ser negativa
		ELSEIF (SELECT cantidad_disponible FROM productos WHERE id_producto = producto_id) - cantidad_pedido < 0 THEN
			SET resultado = 2; # -- No hay stock suficiente
		ELSEIF (SELECT COUNT(*) FROM productos WHERE id_producto = producto_id) = 0 THEN
			SET resultado = 3; -- No hay producto con ese id
		ELSEIF (SELECT COUNT(*) FROM clientes WHERE dni_cliente = cliente_dni) = 0 THEN
			SET resultado = 4; -- No hay cliente con ese dni
		ELSE
			INSERT INTO ordenesdecompra (dni_cliente, id_producto, cantidad, fecha, estado) 
			VALUES(cliente_dni, producto_id, cantidad_pedido, fecha, estado); -- Agregamos la orden
            UPDATE productos SET cantidad_disponible = cantidad_disponible - cantidad_pedido
            WHERE id_producto = producto_id; -- Disminuimos el stock del producto acorde al tamano del pedido
            SET resultado = 5; -- Exito
		END IF;
    END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerOrdenPorDniCliente`(
    IN cliente_dni VARCHAR(10)
)
BEGIN
    IF cliente_dni = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE dni_cliente = CAST(cliente_dni AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerOrdenPorId`(
    IN orden_id VARCHAR(10)
)
BEGIN
    IF orden_id = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE id_orden = CAST(orden_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerOrdenPorIdProducto`(
    IN producto_id VARCHAR(10)
)
BEGIN
    IF producto_id = '' THEN
        SELECT * FROM ordenesdecompra;
    ELSE
        SELECT * FROM ordenesdecompra WHERE id_producto = CAST(producto_id AS UNSIGNED); # Con CAST podemos extraer el valor ingresado por el cliente y convertirlo a un int de manera que evita muchos errores. Por ejemplo, si el usuario ingresa texto en vez de un numero, el cast va a convertir este input a un 0.
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `ModificarOrdenPorId`(
IN orden_id INT,
IN cliente_dni_nuevo INT,
IN producto_id_nuevo INT,
IN cantidad_orden_nueva INT,
IN fecha_nueva DATE,
IN estado_nuevo VARCHAR(20),
OUT resultado INT
)
BEGIN
    DECLARE cantidad_orden_vieja INT; -- Esta variable va a almacenar el valor de la cantidad de la orden que vamos a modificar y asi poder modificar los stocks de los productos
    DECLARE producto_orden_vieja INT; -- Con esta variable vamos a saber si el producto va a ser cambiado y asi vamos a saber que stocks de que productos van a tener que ser modificados
    DECLARE dni_cliente_viejo VARCHAR(150); -- Agregado para almacenar el DNI del cliente viejo
    DECLARE cantidad_disponible_producto_nuevo INT; -- Con esta variable vamos a saber si el stock del producto elegido va a ser suficiente para abastecer la orden.
	DECLARE fecha_vieja DATE; -- Declaramos la fecha de la orden asi en caso de que no se ingrese una fecha podemos volver a ponerla como estaba usando esta variable
    DECLARE id_del_producto_nuevo INT; -- Declaramos esta variable para poder modificar el producto en caso de que el usuario no haya ingresado ningun id entonces queda en NULL 
    DECLARE estado_de_orden VARCHAR(20);
    DECLARE cantidad_orden_actual INT;
    -- Obtenemos los valores actuales de la orden asi en caso de que sean nulo los podemos guardar y volver a insertar en la fila asi solo se modifican los valores que fueron ingresados
    SET cantidad_orden_vieja = (SELECT cantidad FROM ordenesdecompra WHERE id_orden = orden_id);
    SET producto_orden_vieja = (SELECT id_producto FROM ordenesdecompra WHERE id_orden = orden_id);
    SET dni_cliente_viejo = (SELECT dni_cliente FROM ordenesdecompra WHERE id_orden = orden_id); 
    SET estado_de_orden = (SELECT estado FROM ordenesdecompra WHERE id_orden = orden_id);
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
    END IF;
    IF estado_de_orden = "En proceso" THEN -- Si el estado esta en proceso entonces podemos hacerle los cambios de stock
		IF producto_id_nuevo IS NULL OR producto_id_nuevo = producto_orden_vieja THEN -- Si el producto sigue siendo el mismo
			IF cantidad_disponible_producto_nuevo + cantidad_orden_vieja < cantidad_orden_nueva THEN
				SET resultado = 5; -- El stock del producto no es suficiente para abastecer el cambio de tamaño de la orden
			ELSE
				SET id_del_producto_nuevo = (SELECT id_producto FROM ordenesdecompra WHERE id_orden = orden_id);
                SET cantidad_orden_actual = CASE
					WHEN cantidad_orden_nueva IS NULL THEN (SELECT cantidad FROM ordenesdecompra WHERE id_orden = orden_id)
                    ELSE cantidad_orden_nueva END;
                UPDATE productos
				SET 
					cantidad_disponible = CASE 
						WHEN cantidad_orden_nueva IS NOT NULL THEN cantidad_disponible + (cantidad_orden_vieja - cantidad_orden_nueva) 
						ELSE cantidad_disponible
					END,
					ventas_totales = CASE 
						WHEN cantidad_orden_nueva IS NOT NULL THEN ventas_totales + (cantidad_orden_nueva - cantidad_orden_vieja) 
						ELSE ventas_totales
					END
				WHERE id_producto = id_del_producto_nuevo;
			END IF;
		END IF;
		IF producto_id_nuevo != producto_orden_vieja THEN -- Si los productos cambiaron, LO Ponemos en if porque por alguna razon cuando esta en elseif no es accesible
			IF cantidad_disponible_producto_nuevo < cantidad_orden_nueva THEN
				SET resultado = 7; -- No hay stock suficiente en el producto nuevo
			ELSE
				SET cantidad_orden_actual = CASE
					WHEN cantidad_orden_nueva IS NULL THEN (SELECT cantidad FROM ordenesdecompra WHERE id_orden = orden_id)
                    ELSE cantidad_orden_nueva END;
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
	ELSEIF estado_de_orden = "Entregado" THEN
		SET resultado = 8; -- La orden ya fue entregada, no se puede modificar
	END IF;

    -- Finalmente, si no hubo ninguna excepción, modificamos la orden correspondiente
    IF resultado = 6 THEN
		IF estado_de_orden = "En proceso" THEN
			UPDATE ordenesdecompra
			SET 
			dni_cliente = CASE WHEN cliente_dni_nuevo IS NOT NULL THEN cliente_dni_nuevo ELSE dni_cliente_viejo END, -- Solo actualiza el dni si se proporcionó
			id_producto = CASE WHEN producto_id_nuevo IS NOT NULL THEN producto_id_nuevo ELSE producto_orden_vieja END, -- Solo actualiza el producto si se proporcionó
			cantidad = cantidad_orden_actual, 
			fecha = CASE WHEN fecha_nueva IS NULL THEN fecha_vieja ELSE fecha_nueva END,
            estado = CASE WHEN estado_nuevo = "En proceso" THEN "En proceso" ELSE "Entregado" END
			WHERE id_orden = orden_id;
		END IF;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `EliminarOrdenPorId`(
	IN id_elegida INT,
    OUT resultado BOOLEAN
)
BEGIN
    DELETE FROM ordenesdecompra
        WHERE ordenesdecompra.id_orden = id_elegida;
	
		IF ROW_COUNT() > 0 THEN
			SET resultado = TRUE;
		ELSE 
			SET resultado = FALSE;
		END IF;
END //
DELIMITER ;
