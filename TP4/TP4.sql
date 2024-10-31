CREATE TABLE Pedidos (
    PedidoId INT PRIMARY KEY AUTO_INCREMENT,
    ClienteId INT NOT NULL,
    ProductoId INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    FechaPedido DATE NOT NULL
);

CREATE TABLE ConsolidadoVentas (
    ConsolidadoId INT PRIMARY KEY AUTO_INCREMENT,
    ClienteId INT NOT NULL,
    ProductoId INT NOT NULL,
    CantidadTotal INT NOT NULL,
    IngresoTotal DECIMAL(15,2) NOT NULL
);

INSERT INTO Pedidos (ClienteId, ProductoId, Cantidad, PrecioUnitario, FechaPedido)
VALUES 
    (1, 101, 2, 15.99, '2024-01-15'),
    (2, 102, 5, 9.49, '2024-01-20'),
    (3, 103, 1, 24.99, '2024-02-10'),
    (1, 101, 3, 18.75, '2024-02-15'),
    (4, 105, 10, 7.99, '2024-03-01'),
    (5, 106, 4, 12.49, '2024-03-05'),
    (2, 107, 6, 6.99, '2024-03-10'),
    (6, 108, 2, 21.49, '2024-03-15'),
    (3, 109, 7, 5.50, '2024-03-20'),
    (7, 110, 1, 29.99, '2024-03-25'),
    (8, 111, 3, 14.25, '2024-04-05'),
    (9, 112, 2, 19.99, '2024-04-10'),
    (1, 113, 5.7, 8.99, '2024-04-15'),
    (4, 105, 8, 11.25, '2024-04-20'),
    (10, 115, 6, 17.89, '2024-04-25');

DELIMITER //
CREATE PROCEDURE ConsolidadoVentas()
BEGIN
	
    DECLARE fin_cursor BOOLEAN DEFAULT FALSE;
    DECLARE ClienteId_actual INT;
    DECLARE ProductoId_actual INT;
    DECLARE Cantidad_actual INT;
    DECLARE PrecioUnitario_actual DECIMAL(10,2);
    DECLARE ConsolidadoId_elegida INT; 
    
    DECLARE MensajeSignalError TEXT; -- Esta variable va a guardar los distintos mensaje, dependiendo del tipo de erro que ocurra, para usar en el SIGNAL
    
    DECLARE cursor_pedidos CURSOR FOR
    SELECT ClienteId, ProductoId, Cantidad, PrecioUnitario FROM pedidos;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND
    SET fin_cursor = TRUE;
    
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION -- Cualquier error que ocurra durante la ejecucion del procedimiento va a hacer ejecutar el codigo entre el begin y end siguientes
    BEGIN
		DECLARE MensajeDeError_actual TEXT; -- A continuacion se nos ocurrio hacer una tabla para guardar mas informacion acerca del error. 
											-- Usar solo el SIGNAL parecia muy poco informativo y no ayudaria mucho, asi que incluimos informacion acerca...
                                            						-- ...del ultimo registro ingresado por el cursor asi es mas facil detectar la posicion de un posible error de input.
        SET MensajeDeError_actual = CONCAT('Error durante la ejecucion de ConsolidadoVentas. Ultimo registro ingresado:', CHAR(10),
										'Cliente ID: ', ClienteId_actual, CHAR(10),
                                        'Producto ID: ', ProductoId_actual, CHAR(10),
                                        'Cantidad: ', Cantidad_actual, CHAR(10),
                                        'Precio unitario: ', PrecioUnitario_actual);
        
		CREATE TABLE IF NOT EXISTS historialerrores(
			FechaError DATE,
            MensajeDeError TEXT
        );
        
        INSERT INTO historialerrores (FechaError, MensajeDeError) VALUES (CURRENT_DATE, MensajeDeError_actual);
        
        ROLLBACK; -- Si se detecta un error entonces el rollback revierte los datos hasta el "START TRANSACTION;"
		CLOSE cursor_pedidos; -- Cerramos el cursor asi podemos volver a abrirlo la proxima ves que iniciemos el codigo
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = MensajeSignalError;
		-- Singnal sqltate muestra en un mensaje de error personalizado.
    END;
    
	SET MensajeSignalError = 'Ocurrio un error durante la ejecucion de ConsolidadoVentas. Mas informacion en la tabla HistorialErrores.'; -- El mensaje de error del SIGNAL empieza siendo este predeterminadamente y cambia se se cumplen otras condiciones que implican distintos errores
    
	START TRANSACTION;
		OPEN cursor_pedidos;
		FETCH cursor_pedidos INTO ClienteId_actual, ProductoId_actual, Cantidad_actual, PrecioUnitario_actual;
			WHILE NOT fin_cursor DO
				SET ConsolidadoId_elegida = (SELECT ConsolidadoId -- Seleccionamos el ConsolidadoId, para usarlo mas adelante, basandonos en la existencia de la llave candidata que se forma cuando juntamos ClienteId y ProductoId
											FROM consolidadoventas 
											WHERE ClienteId = ClienteId_actual AND ProductoId = ProductoId_actual);
				IF Cantidad_actual <= 0 THEN
					SET MensajeSignalError = 'Error: La cantidad del pedido no puede ser menor o igual a 0'; -- Modificamos el mensaje del SIGNAL para detallar el origen del error
					SIGNAL SQLSTATE '45000';
				ELSEIF PrecioUnitario_actual <= 0 THEN
					SET MensajeSignalError = 'Error: El precio del producto no puede ser menor o igual a 0'; -- Modificamos el mensaje del SIGNAL para detallar el origen del error
					SIGNAL SQLSTATE '45000';
				ELSEIF ConsolidadoId_elegida IS NOT NULL THEN -- Si se selecciona un ConsolidadoId no nulo entonces el registro con esa clave candidata ya existe en la tabla por lo que podemos proceder a actualizar sus datos agregando las cantidades correspondientes
					UPDATE consolidadoventas SET CantidadTotal = CantidadTotal + Cantidad_actual, 
												IngresoTotal = IngresoTotal + Cantidad_actual * PrecioUnitario_actual
												WHERE ConsolidadoId = ConsolidadoId_elegida;
				ELSE -- Si se selecciona un valor nulo eso significa que la llave candidata no existe en la tabla por lo que tenemos que agregarle los valores del pedido a la tabla, creando un nuevo registro
					INSERT INTO consolidadoventas (ClienteId, ProductoId, CantidadTotal, IngresoTotal) VALUES (ClienteId_actual, ProductoId_actual, Cantidad_actual, Cantidad_actual * PrecioUnitario_actual);
				END IF;
				FETCH cursor_pedidos INTO ClienteId_actual, ProductoId_actual, Cantidad_actual, PrecioUnitario_actual;
			END WHILE;
		CLOSE cursor_pedidos;
	COMMIT;    
    
END//
DELIMITER ;