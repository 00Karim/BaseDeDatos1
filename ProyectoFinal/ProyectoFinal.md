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

### DBML de las tablas
```
Table "Clientes" {
  "dni_cliente" INT [pk]
  "nombre" VARCHAR(150)
  "apellido" VARCHAR(150)
  "mail" VARCHAR(150)
}

Table "Productos" {
  "id_producto" INT [pk, increment]
  "nombre" VARCHAR(150)
  "cantidad_disponible" INT
  "categoria" VARCHAR(20)
  "ventas_totales" INT
}

Table "OrdenesDeCompra" {
  "id_orden" INT [pk, increment]
  "dni_cliente" INT [default: NULL]
  "id_producto" INT [default: NULL]
  "cantidad" INT
  "fecha" DATE
  "estado" VARCHAR(20)
}

Ref:"Clientes"."dni_cliente" < "OrdenesDeCompra"."dni_cliente" [update: cascade, delete: set null]

Ref:"Productos"."id_producto" < "OrdenesDeCompra"."id_producto" [update: cascade, delete: set null]
```