import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Text
from conexion import BaseDeDatos
from producto import Producto
from orden import Orden

# Creamos la conexion a la base de datos
db = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
db.conectar()

# Creamos instancias de las clases producto, orden y cliente para poder ejecutar las operaciones necesarias
producto_db = Producto(db)
orden_db = Orden(db)

# Con estas variables controlamos si una ventana esta abierta
ventana_productos_abierta = False
ventana_clientes_abierta = False
ventana_ordenes_abierta = False

def crearGridVentana(ventanaActual: tk.Tk):
    ventanaActual.columnconfigure((0, 1, 2, 3, 4), weight=1)
    ventanaActual.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)

def ventanaPrincipal():
    # Declarar ventana principal
    ventana = tk.Tk()
    ventana.config(bg="#d1d1e0")
    ventana.title("Sistema de ventas en linea")
    ventana.state("zoomed")

    # Declarar grid de la ventana principal
    crearGridVentana(ventana)

    # Declarar header
    headerPrincipal = tk.Label(ventana, text="SISTEMA DE VENTAS EN LINEA", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones
    GestionDeProductos = tk.Button(ventana, text="Gestion de productos", bg="#9494b8", font=("Arial", 14), command=lambda: ventanaGestionDeProductos(ventana))
    GestionDeClientes = tk.Button(ventana, text="Gestion de clientes", bg="#9494b8", font=("Arial", 14), command=lambda: ventanaGestionDeClientes(ventana))
    GestionDeOrdenes = tk.Button(ventana, text="Gestion de ordenes", bg="#9494b8", font=("Arial", 14), command=lambda: ventanaGestionDeOrdenes(ventana))

    botonSalir = tk.Button(ventana, text="Salir", bg="#9494b8", font=("Arial", 14), command=ventana.destroy)

    # Posicionar header
    headerPrincipal.grid(row=2, column=2, sticky="nsew")

    # Posicionar botones
    GestionDeProductos.grid(row=4, column=2, sticky="nsew")
    GestionDeClientes.grid(row=6, column=2, sticky="nsew")
    GestionDeOrdenes.grid(row=8, column=2, sticky="nsew")

    botonSalir.grid(row= 11, column=3, sticky="e")  

    ventana.mainloop()

def ventanaGestionDeProductos(ventanaAnterior):

    ventana_gestionProductos_abierta = False # Esta variable es para definir cuando las ventanas dentro de la ventana gestion de productos fueron abiertas y asi no podemos abrirlas mas de 1 vez

    global ventana_productos_abierta

    if ventana_productos_abierta:
        return
    
    # Cerramos la ventana principal
    ventanaAnterior.withdraw()

    # Declarar ventana de gestion de productos
    ventana_productos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
    ventanaGestionDeProductos = tk.Toplevel()
    ventanaGestionDeProductos.config(bg="#d1d1e0")
    ventanaGestionDeProductos.title("Gestion de productos")
    ventanaGestionDeProductos.state("zoomed")

    # Declarar grid de la ventana
    crearGridVentana(ventanaGestionDeProductos)

    # Declarar header
    headerPrincipal = tk.Label(ventanaGestionDeProductos, text="Gestion de productos", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones ESTOS SON LOS BOTONES QUE APARECEN EL MENU DE GESTION DE PRODUCTOS 
    verProducto = tk.Button(ventanaGestionDeProductos, text="Ver productos", bg="#9494b8", font=("Arial", 14), command=lambda: verProducto())
    agregarProducto = tk.Button(ventanaGestionDeProductos, text="Agregar producto", bg="#9494b8", font=("Arial", 14), command=lambda: agregarProducto())
    modificarProducto = tk.Button(ventanaGestionDeProductos, text="Modificar producto", bg="#9494b8", font=("Arial", 14), command=lambda: modificarProducto())
    eliminarProducto = tk.Button(ventanaGestionDeProductos, text="Eliminar producto", bg="#9494b8", font=("Arial", 14), command=lambda: eliminarProducto())
    consultasAvanzadas = tk.Button(ventanaGestionDeProductos, text="Consultas avanzadas", bg="#9494b8", font=("Arial", 14), command=lambda: consultasAvanzadas())

    botonVolver = tk.Button(ventanaGestionDeProductos, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

    # Posicionar header
    headerPrincipal.grid(row=1, column=2, sticky="nsew")

    # Posicionar botones
    verProducto.grid(row=3, column=2, sticky="nsew")
    agregarProducto.grid(row=5, column=2, sticky="nsew")
    modificarProducto.grid(row=7, column=2, sticky="nsew")
    eliminarProducto.grid(row=9, column=2, sticky="nswe")
    consultasAvanzadas.grid(row=11, column=2, sticky="nswe")  

    botonVolver.grid(row= 11, column=3, sticky="e")  
    
    def on_close():
        global ventana_productos_abierta
        ventana_productos_abierta = False
        ventanaGestionDeProductos.destroy()
        ventanaAnterior.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
        ventanaAnterior.deiconify()
        

    ventanaGestionDeProductos.protocol("WM_DELETE_WINDOW", on_close)

    def verProducto():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaVerProducto = tk.Toplevel()
        ventanaVerProducto.config(bg="#d1d1e0")
        ventanaVerProducto.title("Gestion de productos")
        ventanaVerProducto.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaVerProducto)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaVerProducto, text="Ver productos", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaVerProducto, text="Elige un atributo por el cual filtrar la busqueda de productos", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaVerProducto, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        eleccion.set("Id")
        dropdown = OptionMenu(ventanaVerProducto, eleccion, "Id", "Nombre", "Categoria")
        
        # Declarar input textarea + boton buscar
        dropdownTextarea = Text(ventanaVerProducto, height=max, width=25)
        botonBuscar = tk.Button(ventanaVerProducto, text="Buscar", command=lambda: buscar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para buscar el cliente por el atributo que haya elegido

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaVerProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings")
        tablaProductos.heading("id_producto", text="Id del producto", anchor="center")
        tablaProductos.heading("nombre", text="Nombre", anchor="center")
        tablaProductos.heading("cantidad_disponible", text="Cantidad disponible", anchor="center")
        tablaProductos.heading("categoria", text="Categoria", anchor="center")
        tablaProductos.heading("ventas_totales", text="Ventas totales", anchor="center")
        tablaProductos.column("id_producto", width=80, anchor="center")
        tablaProductos.column("nombre", width=130, anchor="center")
        tablaProductos.column("cantidad_disponible", width=100, anchor="center")
        tablaProductos.column("categoria", width=130, anchor="center")
        tablaProductos.column("ventas_totales", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar dropdown
        dropdown.grid(row=3, column=1, sticky="ew")

        # Posicionar input textarea + boton buscar
        dropdownTextarea.grid(row=3, column=2, sticky="we")
        botonBuscar.grid(row=3, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaProductos.grid(row=4, column=2, rowspan=7, sticky="nsew")
        
        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

        llenar_tabla() # Empezamos llenando la tabla con todos los valores

        # Una vez que el usuario eliga un atributo para filtrar la busqueda y toque aceptar, dependiendo de que atributo eligio y el valor que ingreso, vamos a hacer una busqueda y luego a insertar los valores devueltos en la tabla
        def buscar():
            db.conectar() # Nuevamente, por alguna razon se desconecta la bdd despues de ejecutar el codigo, por lo que vamos a conectarnos nuevamente cuando se llame a esta funcion
            tablaProductos.delete(*tablaProductos.get_children())
            if eleccion.get() == 'Id':
                id_elegida = dropdownTextarea.get("1.0", "end").strip()
                productos_seleccionados = producto_db.verProductoPorAtributo(id=(id_elegida,))
            elif eleccion.get() == 'Nombre':
                nombre_elegido = dropdownTextarea.get("1.0", "end").strip()
                productos_seleccionados = producto_db.verProductoPorAtributo(nombre=(nombre_elegido,))
            else:
                categoria_elegida = dropdownTextarea.get("1.0", "end").strip()
                productos_seleccionados = producto_db.verProductoPorAtributo(categoria=(categoria_elegida,))

            for producto in productos_seleccionados:
                    tablaProductos.insert("", "end", values=producto)

        def on_close():
            nonlocal ventana_gestionProductos_abierta
            ventana_gestionProductos_abierta = False
            ventanaVerProducto.destroy()
            ventanaGestionDeProductos.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeProductos.deiconify()
            
        ventanaVerProducto.protocol("WM_DELETE_WINDOW", on_close)

    def agregarProducto():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaAgregarProducto = tk.Toplevel()
        ventanaAgregarProducto.config(bg="#d1d1e0")
        ventanaAgregarProducto.title("Gestion de productos")
        ventanaAgregarProducto.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaAgregarProducto)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaAgregarProducto, text="Agregar productos", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaAgregarProducto, text="Ingresa los valores de tu nuevo producto", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaAgregarProducto, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para agregar
        labelNombre = tk.Label(ventanaAgregarProducto, text="Nombre: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCantidadDisponible = tk.Label(ventanaAgregarProducto, text="Cantidad disponible: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCategoria = tk.Label(ventanaAgregarProducto, text="Categoria: ", font=("Arial", 12, "bold"), bg="#d1d1e0")

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        dropdownCategoria = OptionMenu(ventanaAgregarProducto, eleccion, "Carnes", "Nueces", "Bebidas")
        
        # Declarar input textarea + boton buscar
        textareaNombre = Text(ventanaAgregarProducto, height=max, width=25)
        textareaCantidadDisponible = Text(ventanaAgregarProducto, height=max, width=25)
        botonAgregar = tk.Button(ventanaAgregarProducto, text="Agregar", command=lambda: agregar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaAgregarProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings", height=15)
        tablaProductos.heading("id_producto", text="Id del producto", anchor="center")
        tablaProductos.heading("nombre", text="Nombre", anchor="center")
        tablaProductos.heading("cantidad_disponible", text="Cantidad disponible", anchor="center")
        tablaProductos.heading("categoria", text="Categoria", anchor="center")
        tablaProductos.heading("ventas_totales", text="Ventas totales", anchor="center")
        tablaProductos.column("id_producto", width=80, anchor="center")
        tablaProductos.column("nombre", width=130, anchor="center")
        tablaProductos.column("cantidad_disponible", width=100, anchor="center")
        tablaProductos.column("categoria", width=130, anchor="center")
        tablaProductos.column("ventas_totales", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para agregar
        labelNombre.grid(row=3, column=1, sticky="e")
        labelCantidadDisponible.grid(row=4, column=1, sticky="e")
        labelCategoria.grid(row=5, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton agregar
        textareaNombre.grid(row=3, column=2, sticky="we")
        textareaCantidadDisponible.grid(row=4, column=2, sticky="we")
        dropdownCategoria.grid(row=5, column=2, sticky="we")
        botonAgregar.grid(row=6, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaProductos.grid(row=8, column=2, sticky="nsew")

        def popup_error():
            popup_error = tk.Toplevel()
            popup_error.title("Error!")
            popup_error.geometry("300x150")
            mensaje = tk.Label(popup_error, text="Error, ya existe un producto\ncon ese nombre!", font=("Arial", 14))
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

        llenar_tabla()

        def agregar():
            db.conectar()
            nombre_ingresado = textareaNombre.get("1.0", "end").strip()
            cantidad_ingresada = int(textareaCantidadDisponible.get("1.0", "end").strip())
            categoria_ingresada = eleccion.get()
            if producto_db.agregarProducto(nombre_ingresado, cantidad_ingresada, categoria_ingresada):
                tablaProductos.delete(*tablaProductos.get_children())
                llenar_tabla()
                print("Se agrego un producto correctamente")
            else:
                popup_error()

        def on_close():
            nonlocal ventana_gestionProductos_abierta
            ventana_gestionProductos_abierta = False
            ventanaAgregarProducto.destroy()
            ventanaGestionDeProductos.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeProductos.deiconify()
            
        ventanaAgregarProducto.protocol("WM_DELETE_WINDOW", on_close)

    def modificarProducto():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaModificarProducto = tk.Toplevel()
        ventanaModificarProducto.config(bg="#d1d1e0")
        ventanaModificarProducto.title("Gestion de productos")
        ventanaModificarProducto.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaModificarProducto)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaModificarProducto, text="Modificar productos", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaModificarProducto, text="Ingresa los valores para cambiarle al producto", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaModificarProducto, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para Modificar
        labelIdProductoAModificar = tk.Label(ventanaModificarProducto, text="Id del producto a modificar: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelNombre = tk.Label(ventanaModificarProducto, text="Nombre nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCantidadDisponible = tk.Label(ventanaModificarProducto, text="Cantidad disponible nueva: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCategoria = tk.Label(ventanaModificarProducto, text="Categoria nueva: ", font=("Arial", 12, "bold"), bg="#d1d1e0")

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        dropdownCategoria = OptionMenu(ventanaModificarProducto, eleccion, "Carnes", "Nueces", "Bebidas")
        
        # Declarar input textarea + boton buscar
        textareaId = Text(ventanaModificarProducto, height=max, width=25)
        textareaNombre = Text(ventanaModificarProducto, height=max, width=25)
        textAreaCantidadDisponible = Text(ventanaModificarProducto, height=max, width=25)
        botonModificar = tk.Button(ventanaModificarProducto, text="Modificar", command=lambda: Modificar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para Modificar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaModificarProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings", height=15)
        tablaProductos.heading("id_producto", text="Id del producto", anchor="center")
        tablaProductos.heading("nombre", text="Nombre", anchor="center")
        tablaProductos.heading("cantidad_disponible", text="Cantidad disponible", anchor="center")
        tablaProductos.heading("categoria", text="Categoria", anchor="center")
        tablaProductos.heading("ventas_totales", text="Ventas totales", anchor="center")
        tablaProductos.column("id_producto", width=80, anchor="center")
        tablaProductos.column("nombre", width=130, anchor="center")
        tablaProductos.column("cantidad_disponible", width=100, anchor="center")
        tablaProductos.column("categoria", width=130, anchor="center")
        tablaProductos.column("ventas_totales", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para Modificar
        labelIdProductoAModificar.grid(row=3, column=1, sticky="e")
        labelNombre.grid(row=4, column=1, sticky="e")
        labelCantidadDisponible.grid(row=5, column=1, sticky="e")
        labelCategoria.grid(row=6, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton Modificar
        textareaId.grid(row=3, column=2, sticky="we")
        textareaNombre.grid(row=4, column=2, sticky="we")
        textAreaCantidadDisponible.grid(row=5, column=2, sticky="we")
        dropdownCategoria.grid(row=6, column=2, sticky="we")
        botonModificar.grid(row=6, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaProductos.grid(row=8, column=2, sticky="nsew")

        def popup_error():
            popup_error = tk.Toplevel()
            popup_error.title("Error!")
            popup_error.geometry("450x100")
            mensaje = tk.Label(popup_error, text="1 - Error, no existe un producto con ese id!", font=("Arial", 14))
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)
        
        llenar_tabla()
        
        def Modificar(): 
            db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
            id_AModificar = textareaId.get("1.0", "end").strip()
            nombre_nuevo = textareaNombre.get("1.0", "end").strip()
            cantidad_nueva = textAreaCantidadDisponible.get("1.0", "end").strip()
            categoria_nueva = eleccion.get()
            if producto_db.modificarProductoPorId(id_AModificar, nombre_nuevo, cantidad_nueva, categoria_nueva):
                tablaProductos.delete(*tablaProductos.get_children())
                llenar_tabla()
                print("Se modifico al producto correctamente")
            else:
                popup_error()        

    def eliminarProducto():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaEliminarProducto = tk.Toplevel()
        ventanaEliminarProducto.config(bg="#d1d1e0")
        ventanaEliminarProducto.title("Gestion de productos")
        ventanaEliminarProducto.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaEliminarProducto)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaEliminarProducto, text="Eliminar productos", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaEliminarProducto, text="Ingresa el id del producto que queres eliminar", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaEliminarProducto, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para Eliminar
        labelIdProductoAEliminar = tk.Label(ventanaEliminarProducto, text="Id del producto a eliminar: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        
        # Declarar input textarea + boton buscar
        textareaId = Text(ventanaEliminarProducto, height=max, width=25)
        botonEliminar = tk.Button(ventanaEliminarProducto, text="Eliminar", command=lambda: Eliminar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para Eliminar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaEliminarProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings", height=15)
        tablaProductos.heading("id_producto", text="Id del producto", anchor="center")
        tablaProductos.heading("nombre", text="Nombre", anchor="center")
        tablaProductos.heading("cantidad_disponible", text="Cantidad disponible", anchor="center")
        tablaProductos.heading("categoria", text="Categoria", anchor="center")
        tablaProductos.heading("ventas_totales", text="Ventas totales", anchor="center")
        tablaProductos.column("id_producto", width=80, anchor="center")
        tablaProductos.column("nombre", width=130, anchor="center")
        tablaProductos.column("cantidad_disponible", width=100, anchor="center")
        tablaProductos.column("categoria", width=130, anchor="center")
        tablaProductos.column("ventas_totales", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para Eliminar
        labelIdProductoAEliminar.grid(row=3, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton eliminar
        textareaId.grid(row=3, column=2, sticky="we")
        botonEliminar.grid(row=3, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaProductos.grid(row=5, column=2, rowspan=7, sticky="nsew")

        def popup_error():
            popup_error = tk.Toplevel()
            popup_error.title("Error!")
            popup_error.geometry("500x150")
            mensaje = tk.Label(popup_error, text="1 - Error, no existe un producto con ese id!", font=("Arial", 14))
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)
        
        llenar_tabla()

        def Eliminar():
            db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
            id_AEliminar = textareaId.get("1.0", "end").strip()
            if producto_db.eliminarProductoPorId((id_AEliminar,)):
                tablaProductos.delete(*tablaProductos.get_children())
                llenar_tabla()
                print("Se elimino al producto correctamente")
            else:
                popup_error()  

    def consultasAvanzadas():
        pass

def ventanaGestionDeClientes(ventanaAnterior):
    global ventana_clientes_abierta

    # Si la variable es True entonces significa que la ventana ya fue abierta entonces no queremos abrirla nuevamente por lo que vamos a hacer un return
    if ventana_clientes_abierta:
        return
    
    # Cerramos la ventana principal
    ventanaAnterior.withdraw()
    
    # Declarar ventana de gestion de clientes
    ventana_clientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
    ventanaGestionDeClientes = tk.Toplevel()
    ventanaGestionDeClientes.config(bg="#d1d1e0")
    ventanaGestionDeClientes.title("Gestion de clientes")
    ventanaGestionDeClientes.geometry("450x500")

    # Declarar grid de la ventana 
    crearGridVentana(ventanaGestionDeClientes) 

    # Con el codigo a continuacion cambiamos la variable de ventana abierta a Falso asi podemos abrirlo nuevamente despues de cerrarlo
    def on_close():
        global ventana_clientes_abierta
        ventana_clientes_abierta = False
        ventanaGestionDeClientes.destroy()
        ventanaAnterior.deiconify()

    ventanaGestionDeClientes.protocol("WM_DELETE_WINDOW", on_close)

def ventanaGestionDeOrdenes(ventanaAnterior):

    ventana_gestionOrdenes_abierta = False # Esta variable es para definir cuando las ventanas dentro de la ventana gestion de ordenes fueron abiertas y asi no podemos abrirlas mas de 1 vez

    global ventana_ordenes_abierta
   
    # Si la variable es True entonces significa que la ventana ya fue abierta entonces no queremos abrirla nuevamente por lo que vamos a hacer un return
    if ventana_ordenes_abierta:
        return
    
    # Cerramos la ventana principal
    ventanaAnterior.withdraw()

    # Declarar ventana de gestion de ordenes
    ventana_ordenes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
    ventanaGestionDeOrdenes = tk.Toplevel()
    ventanaGestionDeOrdenes.config(bg="#d1d1e0")
    ventanaGestionDeOrdenes.title("Gestion de ordenes")
    ventanaGestionDeOrdenes.state("zoomed")

    # Declarar grid de la ventana 
    crearGridVentana(ventanaGestionDeOrdenes) 

    # Declarar header
    headerPrincipal = tk.Label(ventanaGestionDeOrdenes, text="Gestion de productos", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones ESTOS SON LOS BOTONES QUE APARECEN EL MENU DE GESTION DE PRODUCTOS 
    verOrdenes = tk.Button(ventanaGestionDeOrdenes, text="Ver ordenes", bg="#9494b8", font=("Arial", 14), command=lambda: verOrdenes())
    agregarOrden = tk.Button(ventanaGestionDeOrdenes, text="Agregar orden", bg="#9494b8", font=("Arial", 14), command=lambda: agregarOrden())
    modificarOrden = tk.Button(ventanaGestionDeOrdenes, text="Modificar orden", bg="#9494b8", font=("Arial", 14), command=lambda: modificarOrden())
    eliminarOrden = tk.Button(ventanaGestionDeOrdenes, text="Eliminar orden", bg="#9494b8", font=("Arial", 14), command=lambda: eliminarOrden())
    consultasAvanzadas = tk.Button(ventanaGestionDeOrdenes, text="Consultas avanzadas", bg="#9494b8", font=("Arial", 14), command=lambda: consultasAvanzadas())

    botonVolver = tk.Button(ventanaGestionDeOrdenes, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

    # Posicionar header
    headerPrincipal.grid(row=1, column=2, sticky="nsew")

    # Posicionar botones
    verOrdenes.grid(row=3, column=2, sticky="nsew")
    agregarOrden.grid(row=5, column=2, sticky="nsew")
    modificarOrden.grid(row=7, column=2, sticky="nsew")
    eliminarOrden.grid(row=9, column=2, sticky="nswe")
    consultasAvanzadas.grid(row=11, column=2, sticky="nswe")  

    botonVolver.grid(row= 11, column=3, sticky="e")  

    # Con el codigo a continuacion cambiamos la variable de ventana abierta a Falso asi podemos abrirlo nuevamente despues de cerrarlo
    def on_close():
        global ventana_ordenes_abierta
        ventana_ordenes_abierta = False
        ventanaGestionDeOrdenes.destroy()
        ventanaAnterior.state("zoomed")
        ventanaAnterior.deiconify()

    ventanaGestionDeOrdenes.protocol("WM_DELETE_WINDOW", on_close)

    def verOrdenes():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionOrdenes_abierta

        if ventana_gestionOrdenes_abierta:
            return 
        
        ventanaGestionDeOrdenes.withdraw()

        # Declarar ventana de gestion de Ordeness
        ventana_gestionOrdenes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaVerOrdenes = tk.Toplevel()
        ventanaVerOrdenes.config(bg="#d1d1e0")
        ventanaVerOrdenes.title("Gestion de ordenes")
        ventanaVerOrdenes.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaVerOrdenes)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaVerOrdenes, text="Ver Ordenes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaVerOrdenes, text="Elige un atributo por el cual filtrar la busqueda de ordenes", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        eleccion.set("id_orden")
        dropdown = OptionMenu(ventanaVerOrdenes, eleccion, "id_orden", "dni_cliente", "id_producto")
        
        # Declarar input textarea + boton buscar
        dropdownTextarea = Text(ventanaVerOrdenes, height=max, width=25)
        botonBuscar = tk.Button(ventanaVerOrdenes, text="Buscar", command=lambda: buscar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para buscar el cliente por el atributo que haya elegido

        # Declarar tabla
        tablaOrdenes = ttk.Treeview(ventanaVerOrdenes, columns= ("id_orden", "dni_cliente", "id_producto", "cantidad", "fecha"), show="headings")
        tablaOrdenes.heading("id_orden", text="Id de orden", anchor="center")
        tablaOrdenes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaOrdenes.heading("id_producto", text="Id del producto", anchor="center")
        tablaOrdenes.heading("cantidad", text="Cantidad", anchor="center")
        tablaOrdenes.heading("fecha", text="Fecha", anchor="center")
        tablaOrdenes.column("id_orden", width=80, anchor="center")
        tablaOrdenes.column("dni_cliente", width=80, anchor="center")
        tablaOrdenes.column("id_producto", width=80, anchor="center")
        tablaOrdenes.column("cantidad", width=80, anchor="center")
        tablaOrdenes.column("fecha", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew") 
        print("LLEGUE HASTA ACA 1")
        # Posicionar dropdown
        dropdown.grid(row=3, column=1, sticky="ew")

        # Posicionar input textarea + boton buscar
        dropdownTextarea.grid(row=3, column=2, sticky="we")
        botonBuscar.grid(row=3, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaOrdenes.grid(row=4, column=2, rowspan=7, sticky="nsew")
        
        def llenar_tabla():
            lista_ordenes = orden_db.verOrdenes()
            for orden in lista_ordenes:
                print(orden)
                tablaOrdenes.insert("", "end", values=orden)
        
        llenar_tabla() # Empezamos llenando la tabla con todos los valores
        
        # Una vez que el usuario eliga un atributo para filtrar la busqueda y toque aceptar, dependiendo de que atributo eligio y el valor que ingreso, vamos a hacer una busqueda y luego a insertar los valores devueltos en la tabla
        
        def buscar():
            db.conectar() # Nuevamente, por alguna razon se desconecta la bdd despues de ejecutar el codigo, por lo que vamos a conectarnos nuevamente cuando se llame a esta funcion
            tablaOrdenes.delete(*tablaOrdenes.get_children())
            if eleccion.get() == "id_orden":
                id_orden_elegida = dropdownTextarea.get("1.0", "end").strip()
                ordenes_seleccionados = orden_db.verOrdenPorAtributo(id_orden=(id_orden_elegida,))
            elif eleccion.get() == "dni_cliente":
                dni_cliente_elegido = dropdownTextarea.get("1.0", "end").strip()
                ordenes_seleccionados = orden_db.verOrdenPorAtributo(dni_cliente=(dni_cliente_elegido,))
            else:
                id_producto_elegido = dropdownTextarea.get("1.0", "end").strip()
                ordenes_seleccionados = orden_db.verOrdenPorAtributo(id_producto=(id_producto_elegido,))

            for orden in ordenes_seleccionados:
                    tablaOrdenes.insert("", "end", values=orden)
        
        # Declarar botones
        botonVolver = tk.Button(ventanaVerOrdenes, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())
        botonVolver.grid(row= 11, column=3, sticky="e")
        
        def on_close():
            nonlocal ventana_gestionOrdenes_abierta
            ventana_gestionOrdenes_abierta = False
            ventanaVerOrdenes.destroy()
            ventanaGestionDeOrdenes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeOrdenes.deiconify()
        
        ventanaVerOrdenes.protocol("WM_DELETE_WINDOW", on_close)
        

    def agregarOrden():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionOrdenes_abierta

        if ventana_gestionOrdenes_abierta:
            return 
        
        ventanaGestionDeOrdenes.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionOrdenes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaAgregarOrden = tk.Toplevel()
        ventanaAgregarOrden.config(bg="#d1d1e0")
        ventanaAgregarOrden.title("Gestion de Ordenes")
        ventanaAgregarOrden.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaAgregarOrden)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaAgregarOrden, text="Agregar ordenes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaAgregarOrden, text="Ingresa los valores la nueva orden", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaAgregarOrden, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para agregar
        labelIdProducto = tk.Label(ventanaAgregarOrden, text="Id producto: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelDniCliente = tk.Label(ventanaAgregarOrden, text="DNI cliente: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCantidad = tk.Label(ventanaAgregarOrden, text="Cantidad del producto: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelFecha = tk.Label(ventanaAgregarOrden, text="Fecha: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        
        # Declarar input textarea + boton buscar
        textareaIdProducto = Text(ventanaAgregarOrden, height=max, width=25)
        textAreaDniCliente = Text(ventanaAgregarOrden, height=max, width=25)
        textareaCantidad = Text(ventanaAgregarOrden, height=max, width=25)
        textAreaFecha = Text(ventanaAgregarOrden, height=max, width=25)
        botonAgregar = tk.Button(ventanaAgregarOrden, text="Agregar", command=lambda: agregar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaOrdenes = ttk.Treeview(ventanaAgregarOrden, columns= ("id_orden", "dni_cliente", "id_producto", "cantidad", "fecha"), show="headings")
        tablaOrdenes.heading("id_orden", text="Id de orden", anchor="center")
        tablaOrdenes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaOrdenes.heading("id_producto", text="Id del producto", anchor="center")
        tablaOrdenes.heading("cantidad", text="Cantidad", anchor="center")
        tablaOrdenes.heading("fecha", text="Fecha", anchor="center")
        tablaOrdenes.column("id_orden", width=80, anchor="center")
        tablaOrdenes.column("dni_cliente", width=80, anchor="center")
        tablaOrdenes.column("id_producto", width=80, anchor="center")
        tablaOrdenes.column("cantidad", width=80, anchor="center")
        tablaOrdenes.column("fecha", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para agregar
        labelIdProducto.grid(row=3, column=1, sticky="e")
        labelDniCliente.grid(row=4, column=1, sticky="e")
        labelCantidad.grid(row=5, column=1, sticky="e")
        labelFecha.grid(row=6, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton agregar
        textareaIdProducto.grid(row=3, column=2, sticky="we")
        textAreaDniCliente.grid(row=4, column=2, sticky="we")
        textareaCantidad.grid(row=5, column=2, sticky="we")
        textAreaFecha.grid(row=6, column=2, sticky="we")
        
        botonAgregar.grid(row=7, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaOrdenes.grid(row=8, column=2, sticky="nsew")

        def popup_error(): # hacer una lista de posibles errores en esta seccion del codigo
            popup_error = tk.Toplevel()
            popup_error.title("Error!")
            popup_error.geometry("300x150")
            mensaje = tk.Label(popup_error, text="Error, ya existe un orden\ncon ese id!", font=("Arial", 14))
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_ordenes = orden_db.verOrdenes()
            for orden in lista_ordenes:
                tablaOrdenes.insert("", "end", values=orden)

        llenar_tabla()

        # ESTO ESTA COPIADO DE AGREGARPRODUCTO, FALTA CAMBIARLE COSAS. ESTA 0 AVANZADO, PERO EL FORMATO SE QUEDA IGUAL ASI QUE LO DEJO ASI
        def agregar():
            db.conectar()
            nombre_ingresado = textareaNombre.get("1.0", "end").strip()
            cantidad_ingresada = int(textareaCantidadDisponible.get("1.0", "end").strip())
            categoria_ingresada = eleccion.get()
            if orden_db.agregarOrden(nombre_ingresado, cantidad_ingresada, categoria_ingresada):
                tablaOrdenes.delete(*tablaOrdenes.get_children())
                llenar_tabla()
                print("Se agrego una orden correctamente")
            else:
                popup_error()

        def on_close():
            nonlocal ventana_gestionOrdenes_abierta
            ventana_gestionOrdenes_abierta = False
            ventanaAgregarOrden.destroy()
            ventanaGestionDeOrdenes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeOrdenes.deiconify()
            
        ventanaAgregarOrden.protocol("WM_DELETE_WINDOW", on_close)

    def modificarOrden():
        pass

    def eliminarOrden():
        pass

    def consultasAvanzadas():
        pass

ventanaPrincipal()