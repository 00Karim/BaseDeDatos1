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
    CHECK(categoria IN ('Carnes', 'Frutos Secos', 'Bebidas', 'Verduras', 'Condimentos')) 
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
);