# Ejercicio: Programas de radio

**Esquema de BD:**

`PROGRAMA<radio, año, programa, conductor, gerente, frecuencia_radio>`

**Restricciones:**

a. Una radio se transmite por una única frecuencia (frecuencia_radio) en un año determinado, y puede cambiarla en años diferentes.

b. Cada radio tiene un único gerente por año, pero el mismo gerente puede repetirse en la misma radio en diferentes años. Y la misma persona puede ser gerente de diferentes radios durante el mismo año.

c. Un mismo programa puede transmitirse por varias radios y en diferentes años.

d. Un programa transmitido en una radio en un año determinado tiene un solo conductor
### Paso 1: Determinar las Dependencias Funcionales (DFs)

A partir del esquema y las restricciones dadas, podemos determinar las siguientes dependencias funcionales:

1. **radio, anio -> frecuencia_radio:** Cada frecuencia es usada por una unica radio durante un año especifico, por lo que el atributo `frecuencia_radio` depende funcionalmente de la combinacion de `radio` y `anio`.

2. **frecuencia_radio, anio -> radio:** Cada radio usa una unica frecuencia en un año especifico, por lo que la combinacion de `frecuencia_radio` y `anio` es suficiente para identificar la radio (Nunca se aclara si muchas radios pueden o no pueden usar la misma frecuencia durante el mismo año, pero, al ser la unica manera que esta dependencia pueda tener sentido, vamos a suponer que no pueden).

3. **radio, anio -> gerente:** Solo puede haber 1 gerente trabajando en una radio especifica durante un año especifico, por lo que gerente depende de la combinacion de `radio` y `anio`. 

4. **radio, anio, conductor -> programa:** Cada programa en una radio especifica durante un año especifico solo puede tener un conductor que es unico, por ende el atributo `programa` depende de la combinacion de los atributos `radio`, `anio` y `conductor`.

5. **anio, programa -> conductor:** Un conductor puede conducir un solo programa durante un anio especifico por lo que conductor depende de la combinacion de `anio` y `programa`.

### Paso 2: Determinar las Claves Candidatas

Ahora vamos a buscar distintas combinaciones de atributos que sirvan para identificar de forma unica cada fila de la tabla principal en nuestra base de datos. Cada una de las combinaciones a continuacion es una **clave candidata** para el atributo especifico que estamos intentando identificar, por eso tenemos que encontrar una combinacion que pueda identificar a todos los atributos.

En este caso, podemos ver que:

- La combinación de **`radio`, `anio`, y `programa`** es suficiente para identificar de forma única cada registro en la tabla, ya que:
  - `radio` identifica la radio.
  - `anio` identifica el año.
  - `radio` y `anio` identifican la frecuencia de radio siendo utilizada ese año por esa radio
  - `radio` y `anio` identifican a un gerente trabajando en la radio en el año especificado
  - `anio` y `programa` identifican al conductor que dirije al programa siendo transmitido, en ese año especifico
  - `programa` identifica el programa

Por lo tanto, la **clave candidata** es:

- (`radio`, `anio`, `programa`)

Esta combinación asegura que cada registro en la tabla sea único y no haya duplicados.

### Paso 3: Diseño en Tercera Forma Normal (3FN)

Para llevar el esquema a la **Tercera Forma Normal (3FN)**, necesitamos eliminar dependencias transitivas y asegurarnos de que cada atributo no clave dependa únicamente de la clave primaria completa. Esto implica dividir la tabla en varias tablas relacionadas para reducir la redundancia y asegurar la integridad de los datos.

Se dividió la tabla original en cuatro tablas (`Programas`, `Radios`, `Frecuencia_y_gerente` y `Transmisiones_de_radio`) para eliminar dependencias transitivas y garantizar que cada atributo no clave dependa únicamente de la clave primaria completa.

Este proceso de normalización permite reducir la redundancia y mantener la consistencia de los datos en la base de datos.

El nuevo diseño en 3FN sería el siguiente


1. **Tabla `Programas`**
   - `programa` (Clave primaria)

    En un principio intentamos hacer una tabla principal que sea **`Programas_de_radio`** con la clave candidata (`radio`, `anio` y `programa`), pero a la hora de querer identificar las distintas frecuencias y gerentes de cada radio habia redundancia (en el atributo `programa`) cuando usabamos esa clave primaria, en forma de clave foranea en otra tabla, para identificar estos datos. Por lo que preferimos dividir los datos en porciones (distintas tablas) mas pequeñas para poder tratarlos mas facilmente.

2. **Tabla `Radios`**
   - `radio` (Clave primaria)

    Creamos una tabla **`Radios`** con el atributo `radios` porque lo mas probable,  al igual que la tabla **`Programas`** con el atributo `programa`, es que haya una cantidad pequeña de estaciones de radio, por lo que nos parecio adecuado hacer una tabla a parte que guarde todas las radios para evitar redundancia.
    
3. **Tabla `Frecuencia_y_Gerente`**
   - `radio` (Clave primaria) (Clave foranea que referencia a **`Radios`**)
   - `anio` (Clave primaria)
   - `frecuencia_radio`
   - `gerente` 
   - Clave primaria compuesta: (`radio`, `anio`)

    Los atributos `frecuencia_de_radio` y `gerente` dependen de la combinacion de `radio` y `anio` por lo que seria adecuado ponerlos en una tabla a parte y que dependan de esos dos atributos como una clave combinada. Ademas, aca se puede ver claramente como la creacion de la tabla **`Radios`** y su referenciacion en esta tabla garantiza integridad y no redundancia de los datos.

4. **Tabla `Transmisiones_de_radio`**
    - `programa` (Clave foranea que referencia a **`Programas`**)
    - `radio` 
    - `anio`
    - `conductor`
    - Clave primaria compuesta (`radio`, `anio`) (Clave foranea que referencia a **`Frecuencia_y_gerente`**)
    - Clave primaria compuesta (`programa`, `radio`, `anio`)

    La tabla **`Transmisiones_de_radio`** es la que le da coherencia al resto de las tablas centralizando todos sus datos junto a la clave candidata. Esta tabla nos muestra cual radio esta transmitiendo cual programa dirigido por cual conductor y en que año. Y al tener el año especifico y la radio en la que se esta transmitiendo podemos saber con que `gerente` y `frecuencia_de_radio` esta tratando una transmision especifica.

### Diseño pasado por https://dbdiagram.io/

    1. Table "Programas" {
        "programa" VARCHAR(50) [pk]        
    }


    2. Table "Radios" {
        "radio" VARCHAR(50) [pk]
    }


    3. Table "Frecuencia_y_gerente" {
        "radio" VARCHAR(50)
        "anio" INT
        "frecuencia_radio" INT
        "gerente" VARCHAR(50)

    Indexes{
            (radio, anio) [pk]
        }
    }


    4. Table "Transmisiones_de_radio" {
        "programa" VARCHAR(50)
        "radio" VARCHAR(50)
        "anio" INT
        "conductor" VARCHAR(50)

    Indexes {
        (programa, radio, anio) [pk]
        }
    }

    Ref:"Radios"."radio" < "Frecuencia_y_gerente"."radio"

    Ref:"Programas"."programa" < "Transmisiones_de_radio"."programa"

    Ref:"Frecuencia_y_gerente".("radio", "anio") < "Transmisiones_de_radio".("radio", "anio")




