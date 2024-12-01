
import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Text
from tkcalendar import *
from conexion import BaseDeDatos
from producto import Producto
from orden import Orden
from cliente import Cliente
import re # Importamos re para chequear si un mail es valido en la funcion agregar() dentro de la ventana registraClientes en gestion de clientes

# Create DateEntry widget with no custom style (uses the default flatly theme) 

# Creamos la conexion a la base de datos
db = BaseDeDatos("127.0.0.1", "root", "ratadecueva", "kakidb")
db.conectar()

# Creamos instancias de las clases producto, orden y cliente para poder ejecutar las operaciones necesarias
producto_db = Producto(db)
orden_db = Orden(db)
cliente_db = Cliente(db)

# Con estas variables controlamos si una ventana esta abierta
ventana_productos_abierta = False
ventana_clientes_abierta = False
ventana_ordenes_abierta = False

def crearGridVentana(ventanaActual: tk.Tk):
    ventanaActual.columnconfigure((0, 1, 2, 3, 4), weight=1)
    ventanaActual.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)

def crearErrorPopUp(mensaje, color = "#D8000C", tamanio = "300x150"): # El color y el tamanio son siempre los mismos a menos que el error vaya a ser una advertencia o si tiene que cambiar el tamanio, entonces ahi vamos a ingresar los parametros cuando llamamos a la funcion
    popup_error = tk.Toplevel()
    popup_error.title("Error!")
    popup_error.geometry(tamanio)
    mensaje = tk.Label(popup_error, text=mensaje, font=("Arial", 14))
    mensaje.config(fg=color)
    mensaje.pack(pady=20)
    
    # extraemos el tamanio de la pantalla del sistema asi podemos encontrar el centro de ambos ejes (x, y) y asi encontrar el centro de la pantalla
    ancho_pantalla = popup_error.winfo_screenwidth()
    alto_pantalla = popup_error.winfo_screenheight()

    # definimos que tamanio va a tener el popup extrayendo los valores en la variable tamanio. Dividimos el string en 2 a partir de la x y asi sabemos el ancho y el largo por separado
    ancho_popup, alto_popup = map(int, tamanio.split("x"))

    # calculamos cuanto espacio necesita el popup para entrar en el medio 
    x_centrado = (ancho_pantalla // 2) - (ancho_popup // 2)
    y_centrado = (alto_pantalla // 2) - (alto_popup // 2)

    # configuramos la geometria del popup para adquirir el tamanio que le dio el usuario y las posiciones de x e y que calculamos antes
    popup_error.geometry(f"{tamanio}+{x_centrado}+{y_centrado}")

    boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
    boton_cerrar.pack()

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
    consultasAvanzadas = tk.Button(ventanaGestionDeProductos, text="Consultas avanzadas", bg="#9494b8", font=("Arial", 14), command=lambda: consultasAvanzadasProductos())

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
       
        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

        llenar_tabla()

        def agregar():
            db.conectar()
            nombre_ingresado = textareaNombre.get("1.0", "end").strip()
            cantidad_ingresada = textareaCantidadDisponible.get("1.0", "end").strip()
            categoria_ingresada = eleccion.get()
            if nombre_ingresado == '' or cantidad_ingresada == '' or categoria_ingresada == '': # Si algun parametro esta vacio, no vale la pena ejecutar el codigo y asi nos evitamos errores innecesarios
                crearErrorPopUp("Atencion, falta ingresar algun\nparametro", color="#FFC107")
            else:
                resultado = producto_db.agregarProducto(nombre_ingresado, cantidad_ingresada, categoria_ingresada)
                if resultado == 1:
                    crearErrorPopUp("Error, ya existe un producto\ncon ese nombre")
                elif resultado == 2:
                    crearErrorPopUp("Error, la cantidad no puede\nser negativa")
                elif resultado == 3:
                    tablaProductos.delete(*tablaProductos.get_children())
                    llenar_tabla()
                    crearErrorPopUp("Producto agregado correctamente!", color="#4CAF50") # Tambien podemos usar la funcion para crear popups de exito

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
            if id_AModificar == '':
                crearErrorPopUp("Atencion, no ingresaste un id", color="#FFC107")
            else:
                if cantidad_nueva == "":
                    cantidad_nueva = None # Tenemos que convertir cantidad nueva a none si el usuario no ingreso nada para que se traduzca a Null en sql y asi directamente no actualizamos la cantidad y la dejamos como esta
                resultado = producto_db.modificarProductoPorId(id_AModificar, nombre_nuevo, cantidad_nueva, categoria_nueva) # DATO: decidimos que las ventas totales no se pueden actualizar aca ya que se actualizan solas cuando se efectua una orden nueva
                if resultado == 1:
                    crearErrorPopUp("Error, la cantidad nueva no\npuede ser menor a 0!")
                elif resultado == 2:
                    crearErrorPopUp("Error, no existe un producto\ncon ese id")
                elif resultado == 3:  
                    tablaProductos.delete(*tablaProductos.get_children())
                    llenar_tabla()
                    crearErrorPopUp("Producto modificado correctamente", color="#4CAF50")    

        def on_close():
            nonlocal ventana_gestionProductos_abierta
            ventana_gestionProductos_abierta = False
            ventanaModificarProducto.destroy()
            ventanaGestionDeProductos.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeProductos.deiconify()
            
        ventanaModificarProducto.protocol("WM_DELETE_WINDOW", on_close)   

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
                crearErrorPopUp("Producto eliminado correctamente", color="#4CAF50")
            else:
                crearErrorPopUp("Error, no existe un producto\ncon ese id") 

    def consultasAvanzadasProductos():
        global crearGridVentana
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaAvanzadasProducto = tk.Toplevel()
        ventanaAvanzadasProducto.config(bg="#d1d1e0")
        ventanaAvanzadasProducto.title("Gestion de productos")
        ventanaAvanzadasProducto.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaAvanzadasProducto)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaAvanzadasProducto, text="Consultas avanzadas", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaAvanzadasProducto, text="Elige tu consulta avanzada", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaAvanzadasProducto, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())
        botonOrdenarPorMasVentas = tk.Button(ventanaAvanzadasProducto, text="Ordenar por mas ventas", font=("Arial", 14), command=lambda: ordenarPorMasVentas()) # Si el usuario hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado
        botonOrdenarPorMenorStock = tk.Button(ventanaAvanzadasProducto, text="Ordenar por menor stock", font=("Arial", 14), command=lambda: ordenarPorMenorStock())

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaAvanzadasProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings")
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
        botonOrdenarPorMasVentas.grid(row= 5, column=2, sticky="nse")
        botonOrdenarPorMenorStock.grid(row= 5, column=2, sticky="nsw")
        botonVolver.grid(row= 11, column=3, sticky="e")  
        
    
        # Posicionar tabla + Llenar tabla con sus valores default
        tablaProductos.grid(row=8, column=2, sticky="nsew")
        

        def llenar_tabla():
            lista_productos = producto_db.verProductos()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

        llenar_tabla() # Empezamos llenando la tabla con todos los valores

        def ordenarPorMenorStock():
            db.conectar()
            tablaProductos.delete(*tablaProductos.get_children()) # Borramos los datos de la tabla actual por si el usuario toca dos veces el boton entonces asi no se duplican valores
            tablaProductos.grid(row=8, column=2, sticky="nsew") # Insertamos la tabla elegida en el lugar correspondiente
            lista_productos = producto_db.verProductosPorStock()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

        def ordenarPorMasVentas():
            db.conectar()
            tablaProductos.delete(*tablaProductos.get_children())
            tablaProductos.grid(row=8, column=2, sticky="nsew")
            lista_productos = producto_db.verProductosPorVentas()
            for producto in lista_productos:
                tablaProductos.insert("", "end", values=producto)

def ventanaGestionDeClientes(ventanaAnterior):
    ventana_gestionClientes_abierta = False
    
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
    ventanaGestionDeClientes.state("zoomed")

    # Declarar grid de la ventana 
    crearGridVentana(ventanaGestionDeClientes) 
    
    # Declarar header
    headerPrincipal = tk.Label(ventanaGestionDeClientes, text="Gestion de clientes", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones
    botonVerClientes = tk.Button(ventanaGestionDeClientes, text="Ver clientes", bg="#9494b8", font=("Arial", 14), command=lambda: verClientes())
    botonRegistraClientes = tk.Button(ventanaGestionDeClientes, text="Registrar cliente", bg="#9494b8", font=("Arial", 14), command=lambda: registraClientes())
    botonActualizarCliente = tk.Button(ventanaGestionDeClientes, text="Actualizar cliente", bg="#9494b8", font=("Arial", 14), command=lambda: modificarCliente())
    botonEliminarCliente = tk.Button(ventanaGestionDeClientes, text="Eliminar cliente", bg="#9494b8", font=("Arial", 14), command=lambda: eliminarCliente())
    botonConsultasAvanzadas = tk.Button(ventanaGestionDeClientes, text="Consultas avanzadas", bg="#9494b8", font=("Arial", 14), command=lambda: consultasAvanzadasClientes())

    botonVolver = tk.Button(ventanaGestionDeClientes, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

    # Posicionar header
    headerPrincipal.grid(row=1, column=2, sticky="nsew")

    # Posicionar botones
    botonVerClientes.grid(row=3, column=2, sticky="nsew")
    botonRegistraClientes.grid(row=5, column=2, sticky="nsew")
    botonActualizarCliente.grid(row=7, column=2, sticky="nsew")
    botonEliminarCliente.grid(row=9, column=2, sticky="nswe")
    botonConsultasAvanzadas.grid(row=11, column=2, sticky="nswe")    
    
    botonVolver.grid(row= 11, column=3, sticky="e") 

        # Con el codigo a continuacion cambiamos la variable de ventana abierta a Falso asi podemos abrirlo nuevamente despues de cerrarlo
    def on_close():
        global ventana_clientes_abierta
        ventana_clientes_abierta = False
        ventanaGestionDeClientes.destroy()
        ventanaAnterior.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
        ventanaAnterior.deiconify()

    ventanaGestionDeClientes.protocol("WM_DELETE_WINDOW", on_close) 
    
    def verClientes():
        nonlocal ventana_gestionClientes_abierta

        if ventana_gestionClientes_abierta:
            return 
        
        ventanaGestionDeClientes.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionClientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaVerClientes = tk.Toplevel()
        ventanaVerClientes.config(bg="#d1d1e0")
        ventanaVerClientes.title("Gestion de clientes")
        ventanaVerClientes.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaVerClientes)

        # Declarar header
        headerPrincipal = tk.Label(ventanaVerClientes, text="Ver clientes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaVerClientes, text="Elige un atributo por el cual filtrar la busqueda de clientes", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaVerClientes, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        eleccion.set("Nombre")
        dropdown = OptionMenu(ventanaVerClientes, eleccion, "Nombre", "Apellido", "DNI")

        # Declarar input textarea + boton buscar
        dropdownTextarea = Text(ventanaVerClientes, height=max, width=25)
        botonBuscar = tk.Button(ventanaVerClientes, text="Buscar", command= lambda: buscar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para buscar el cliente por el atributo que haya elegido

        # Declarar tabla
        tablaClientes = ttk.Treeview(ventanaVerClientes, columns= ("dni_cliente", "nombre", "apellido", "mail"), show="headings")
        tablaClientes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes.heading("nombre", text="Nombre", anchor="center")
        tablaClientes.heading("apellido", text="Apellido", anchor="center")
        tablaClientes.heading("mail", text="Mail", anchor="center")
        tablaClientes.column("dni_cliente", width=80, anchor="center")
        tablaClientes.column("nombre", width=130, anchor="center")
        tablaClientes.column("apellido", width=100, anchor="center")
        tablaClientes.column("mail", width=100, anchor="center")

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
        tablaClientes.grid(row=4, column=2, rowspan=7, sticky="nsew")

        #ACA FALTA AGREGAR LA FUNCION DE LLENAR TABLA Y BUSCAR CLIENTES
        def llenar_tabla():
            lista_clientes = cliente_db.verClientes()
            for producto in lista_clientes:
                tablaClientes.insert("", "end", values=producto)

        llenar_tabla() # Empezamos llenando la tabla con todos los valores

        # Una vez que el usuario eliga un atributo para filtrar la busqueda y toque aceptar, dependiendo de que atributo eligio y el valor que ingreso, vamos a hacer una busqueda y luego a insertar los valores devueltos en la tabla
        def buscar():
            db.conectar() # Nuevamente, por alguna razon se desconecta la bdd despues de ejecutar el codigo, por lo que vamos a conectarnos nuevamente cuando se llame a esta funcion
            tablaClientes.delete(*tablaClientes.get_children())
            if eleccion.get() == 'DNI':
                dni_elegido = dropdownTextarea.get("1.0", "end").strip()
                clientes_seleccionados = cliente_db.verClientePorAtributo(dni=(dni_elegido,))
            elif eleccion.get() == 'Nombre':
                nombre_elegido = dropdownTextarea.get("1.0", "end").strip()
                clientes_seleccionados = cliente_db.verClientePorAtributo(nombre=(nombre_elegido,))
            else:
                apellido_elegido = dropdownTextarea.get("1.0", "end").strip()
                clientes_seleccionados = cliente_db.verClientePorAtributo(apellido=(apellido_elegido,))

            for cliente in clientes_seleccionados:
                    tablaClientes.insert("", "end", values=cliente)
        
        def on_close():
            nonlocal ventana_gestionClientes_abierta
            ventana_gestionClientes_abierta = False
            ventanaVerClientes.destroy()
            ventanaGestionDeClientes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeClientes.deiconify()

        ventanaVerClientes.protocol("WM_DELETE_WINDOW", on_close)
    
    def registraClientes():
        global crearGridVentana
        nonlocal ventana_gestionClientes_abierta

        if ventana_gestionClientes_abierta:
            return 
        
        ventanaGestionDeClientes.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionClientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaRegistrarCliente = tk.Toplevel()
        ventanaRegistrarCliente.config(bg="#d1d1e0")
        ventanaRegistrarCliente.title("Gestion de clientes")
        ventanaRegistrarCliente.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaRegistrarCliente)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaRegistrarCliente, text="Registrar clientes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaRegistrarCliente, text="Ingresa los datos del cliente", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaRegistrarCliente, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para agregar
        labelNombre = tk.Label(ventanaRegistrarCliente, text="Nombre: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelApellido = tk.Label(ventanaRegistrarCliente, text="Apellido: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelDNI = tk.Label(ventanaRegistrarCliente, text="DNI: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelMail = tk.Label(ventanaRegistrarCliente, text="Mail: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        
        # Declarar input textarea + boton buscar
        textareaNombre = Text(ventanaRegistrarCliente, height=max, width=25)
        textareaApellido = Text(ventanaRegistrarCliente, height=max, width=25)
        textareaDNI = Text(ventanaRegistrarCliente, height=max, width=25)
        textareaMail = Text(ventanaRegistrarCliente, height=max, width=25)
        botonRegistrar = tk.Button(ventanaRegistrarCliente, text="Registrar", command=lambda: agregar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaClientes = ttk.Treeview(ventanaRegistrarCliente, columns= ("dni_cliente", "nombre", "apellido", "mail"), show="headings", height=15)
        tablaClientes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes.heading("nombre", text="Nombre", anchor="center")
        tablaClientes.heading("apellido", text="Apellido", anchor="center")
        tablaClientes.heading("mail", text="Mail", anchor="center")
        tablaClientes.column("dni_cliente", width=80, anchor="center")
        tablaClientes.column("nombre", width=130, anchor="center")
        tablaClientes.column("apellido", width=100, anchor="center")
        tablaClientes.column("mail", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para agregar
        labelDNI.grid(row=4, column=1, sticky="e")
        labelNombre.grid(row=5, column=1, sticky="e")
        labelApellido.grid(row=6, column=1, sticky="e")
        labelMail.grid(row=7, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton agregar
        textareaDNI.grid(row=4, column=2, sticky="we")
        textareaNombre.grid(row=5, column=2, sticky="we")
        textareaApellido.grid(row=6, column=2, sticky="we")
        textareaMail.grid(row=7, column=2, sticky="we")
        botonRegistrar.grid(row=7, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaClientes.grid(row=8, column=2, sticky="nsew")

        def llenar_tabla():
            lista_clientes = cliente_db.verClientes()
            for producto in lista_clientes:
                tablaClientes.insert("", "end", values=producto)

        llenar_tabla() # Empezamos llenando la tabla con todos los valores

        def agregar():
            db.conectar()
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Este es el patron que deberia seguir el mail ingresado
            dni_ingresado = textareaDNI.get("1.0", "end").strip()
            nombre_ingresado = textareaNombre.get("1.0", "end").strip()
            appellido_ingresado = textareaApellido.get("1.0", "end").strip()
            mail_ingresado = textareaMail.get("1.0", "end").strip()
            if dni_ingresado == '' or nombre_ingresado == '' or appellido_ingresado == '' or mail_ingresado == '': # Si algun parametro no se ingresa entonces vamos a evitar ejecutar el codigo para agregar un cliente asi evitamos errores innecesarios
                crearErrorPopUp("Atencion, falta ingresar\nalgun parametro", color="#FFC107")
            else:
                if len(dni_ingresado) != 8:
                    crearErrorPopUp("Error, dni no valido!")
                elif not re.match(email_regex, mail_ingresado): # Si el patron del mail ingresado no coincide con el estandar entonces el mail no es valido y le mostramos un error al usuario
                    crearErrorPopUp("Error, mail no valido!")
                elif cliente_db.agregarCliente(dni_ingresado, nombre_ingresado, appellido_ingresado, mail_ingresado):
                    tablaClientes.delete(*tablaClientes.get_children())
                    llenar_tabla()
                    crearErrorPopUp("Cliente agregado correctamente", color="#4CAF50")
                else:
                    crearErrorPopUp("Error, ya existe un cliente\ncon ese DNI!")

        #FALTA AGREGAR popup_error, llenar_tabla y agregar
        def on_close():
            nonlocal ventana_gestionClientes_abierta
            ventana_gestionClientes_abierta = False
            ventanaRegistrarCliente.destroy()
            ventanaGestionDeClientes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeClientes.deiconify()
            
        ventanaRegistrarCliente.protocol("WM_DELETE_WINDOW", on_close)

    def modificarCliente():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionClientes_abierta

        if ventana_gestionClientes_abierta:
            return 
        
        ventanaGestionDeClientes.withdraw()

        # Declarar ventana de gestion de Clientes
        ventana_gestionClientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaModificarCliente = tk.Toplevel()
        ventanaModificarCliente.config(bg="#d1d1e0")
        ventanaModificarCliente.title("Gestion de clientes")
        ventanaModificarCliente.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaModificarCliente)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaModificarCliente, text="Modificar clientes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaModificarCliente, text="Ingresa los valores para cambiarle al cliente", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaModificarCliente, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para Modificar
        labeDniClienteAModificar = tk.Label(ventanaModificarCliente, text="DNI del cliente a modificar: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelNombre = tk.Label(ventanaModificarCliente, text="Nombre nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelApellido = tk.Label(ventanaModificarCliente, text="Apellido nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelMail = tk.Label(ventanaModificarCliente, text="Mail nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        
        # Declarar input textarea + boton buscar
        textareaDniClienteAModificar = Text(ventanaModificarCliente, height=max, width=25)
        textareaNombre = Text(ventanaModificarCliente, height=max, width=25)
        textAreaApellido = Text(ventanaModificarCliente, height=max, width=25)
        textAreaMail = Text(ventanaModificarCliente, height=max, width=25)
        botonModificar = tk.Button(ventanaModificarCliente, text="Modificar", command=lambda: Modificar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para Modificar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaClientes = ttk.Treeview(ventanaModificarCliente, columns= ("dni_cliente", "nombre", "apellido", "mail"), show="headings", height=15)
        tablaClientes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes.heading("nombre", text="Nombre", anchor="center")
        tablaClientes.heading("apellido", text="Apellido", anchor="center")
        tablaClientes.heading("mail", text="Mail", anchor="center")
        tablaClientes.column("dni_cliente", width=80, anchor="center")
        tablaClientes.column("nombre", width=130, anchor="center")
        tablaClientes.column("apellido", width=100, anchor="center")
        tablaClientes.column("mail", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para Modificar
        labeDniClienteAModificar.grid(row=3, column=1, sticky="e")
        labelNombre.grid(row=4, column=1, sticky="e")
        labelApellido.grid(row=5, column=1, sticky="e")
        labelMail.grid(row=6, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton Modificar
        textareaDniClienteAModificar.grid(row=3, column=2, sticky="we")
        textareaNombre.grid(row=4, column=2, sticky="we")
        textAreaApellido.grid(row=5, column=2, sticky="we")
        textAreaMail.grid(row=6, column=2, sticky="we")
        botonModificar.grid(row=6, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaClientes.grid(row=8, column=2, sticky="nsew")
       
        def llenar_tabla():
            lista_clientes = cliente_db.verClientes()
            for cliente in lista_clientes:
                tablaClientes.insert("", "end", values=cliente)
        
        llenar_tabla()
        
        def Modificar(): 
            db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Este es el patron que deberia seguir el mail ingresado
            dni_aModificar = textareaDniClienteAModificar.get("1.0", "end").strip()
            nombre_nuevo = textareaNombre.get("1.0", "end").strip()
            apellido_nuevo = textAreaApellido.get("1.0", "end").strip()
            mail_nuevo = textAreaMail.get("1.0", "end").strip()
            if dni_aModificar == '': # Si el dni esta vacio entonces vamos a ignorar esta parte del codigo ya que seria innecesario ejecutuarla si el cliente nisiquiere ingreso un dni. Asi evitamos que haya un error de sql por faltar valor en el procedimiento o por tener valores incorrectos en el dni
                 crearErrorPopUp("Atencion, no ingresaste\nun DNI", color="#FFC107")
            else:
                if mail_nuevo == '': # Si el cliente no ingresa nada en la casilla de mail entonces podemos saltear el chequeo de patron. Y no nos tenemos que preocupar con que el mail quede vaicio porque el procedimiento sql esta diseniado para que no se cambien los atributos si ningun valor es ingresado
                    if cliente_db.modificarClientePorDni(dni_aModificar, nombre_nuevo, apellido_nuevo, mail_nuevo):
                        tablaClientes.delete(*tablaClientes.get_children())
                        llenar_tabla()
                        crearErrorPopUp("Cliente modificado correctamente!", color="#4CAF50")
                    else:
                        crearErrorPopUp("Error, no existe un cliente\ncon ese DNI") 
                else:
                    if not re.match(email_regex, mail_nuevo): # Si el patron del mail ingresado no coincide con el estandar entonces el mail no es valido y le mostramos un error al usuario
                        crearErrorPopUp("Error, mail no valido!")
                        mail_nuevo = '' # Hacemos que el mail quede vacio porque existe la posibilidad que el usuario ingrese un mail invalido y si eso sucede el codigo siguiente seria ejecutado y el mail seria cambiado a un mail invalido. Si hacemos que el mail input quede vacio entonces no se van a efectuar cambios gracias a la manera en la que esta diseniado el procedimiento sql que se activa cuando ejecutamos este codigo    
                    elif cliente_db.modificarClientePorDni(dni_aModificar, nombre_nuevo, apellido_nuevo, mail_nuevo):
                        tablaClientes.delete(*tablaClientes.get_children())
                        llenar_tabla()
                        crearErrorPopUp("Cliente modificado correctamente!", color="#4CAF50")
                    else:
                        crearErrorPopUp("Error, no existe un cliente\ncon ese DNI") 

        def on_close():
            nonlocal ventana_gestionClientes_abierta
            ventana_gestionClientes_abierta = False
            ventanaModificarCliente.destroy()
            ventanaGestionDeClientes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeClientes.deiconify()
            
        ventanaModificarCliente.protocol("WM_DELETE_WINDOW", on_close)
                
    def eliminarCliente():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionClientes_abierta

        if ventana_gestionClientes_abierta:
            return 
        
        ventanaGestionDeClientes.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionClientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaEliminarCliente = tk.Toplevel()
        ventanaEliminarCliente.config(bg="#d1d1e0")
        ventanaEliminarCliente.title("Gestion de clientes")
        ventanaEliminarCliente.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaEliminarCliente)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaEliminarCliente, text="Eliminar clientes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaEliminarCliente, text="Ingresa el DNI del cliente que queres eliminar", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaEliminarCliente, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para Eliminar
        labelDniClienteAEliminar = tk.Label(ventanaEliminarCliente, text="DNI del cliente a eliminar: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        
        # Declarar input textarea + boton buscar
        textareaDni = Text(ventanaEliminarCliente, height=max, width=25)
        botonEliminar = tk.Button(ventanaEliminarCliente, text="Eliminar", command=lambda: Eliminar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para Eliminar el cliente con los parametros que haya ingresado

        # Declarar tabla
        # Declarar tabla
        tablaClientes = ttk.Treeview(ventanaEliminarCliente, columns= ("dni_cliente", "nombre", "apellido", "mail"), show="headings", height=15)
        tablaClientes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes.heading("nombre", text="Nombre", anchor="center")
        tablaClientes.heading("apellido", text="Apellido", anchor="center")
        tablaClientes.heading("mail", text="Mail", anchor="center")
        tablaClientes.column("dni_cliente", width=80, anchor="center")
        tablaClientes.column("nombre", width=130, anchor="center")
        tablaClientes.column("apellido", width=100, anchor="center")
        tablaClientes.column("mail", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para Eliminar
        labelDniClienteAEliminar.grid(row=3, column=1, sticky="e")

        # Posicionar input textarea + dropdownCategoria + boton eliminar
        textareaDni.grid(row=3, column=2, sticky="we")
        botonEliminar.grid(row=3, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaClientes.grid(row=5, column=2, rowspan=7, sticky="nsew")

        def popup_error():
            popup_error = tk.Toplevel()
            popup_error.title("Error!")
            popup_error.geometry("500x150")
            mensaje = tk.Label(popup_error, text="1 - Error, no existe un cliente con ese DNI!", font=("Arial", 14))
            mensaje.config(fg="#D8000C")
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_clientes = cliente_db.verClientes()
            for cliente in lista_clientes:
                tablaClientes.insert("", "end", values=cliente)
        
        llenar_tabla()

        def Eliminar():
            db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
            dni_AEliminar = textareaDni.get("1.0", "end").strip()
            if dni_AEliminar == '': # Si el cliente no ingresa ningun dni entonces nos ahoramos la busqueda
                pass
            else:
                if cliente_db.eliminarClientePorDni((dni_AEliminar,)):
                    tablaClientes.delete(*tablaClientes.get_children())
                    llenar_tabla()
                    crearErrorPopUp("Cliente eliminado correctamente!", color="#4CAF50")
                else:
                    crearErrorPopUp("Error, no existe un cliente\ncon ese DNI!")

        def on_close():
            nonlocal ventana_gestionClientes_abierta
            ventana_gestionClientes_abierta = False
            ventanaEliminarCliente.destroy()
            ventanaGestionDeClientes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeClientes.deiconify()
            
        ventanaEliminarCliente.protocol("WM_DELETE_WINDOW", on_close)    

    def consultasAvanzadasClientes():
        global crearGridVentana
        nonlocal ventana_gestionClientes_abierta

        if ventana_gestionClientes_abierta:
            return 
        
        ventanaGestionDeClientes.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionClientes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaAvanzadasCliente = tk.Toplevel()
        ventanaAvanzadasCliente.config(bg="#d1d1e0")
        ventanaAvanzadasCliente.title("Gestion de clientes")
        ventanaAvanzadasCliente.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaAvanzadasCliente)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaAvanzadasCliente, text="Consultas avanzadas", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaAvanzadasCliente, text="Elige tu consulta avanzada", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaAvanzadasCliente, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())
        botonOrdenarAlfabeticamente = tk.Button(ventanaAvanzadasCliente, text="Ordenar clientes alfabeticamente", font=("Arial", 14), command=lambda: ordenarAlfabeticamente()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado
        botonOrdenarPorPedidos = tk.Button(ventanaAvanzadasCliente, text="Ordenar por cantidad de pedidos", font=("Arial", 14), command=lambda: ordenarPorPedidos())

        # Declarar tabla
        tablaClientes = ttk.Treeview(ventanaAvanzadasCliente, columns= ("dni_cliente", "nombre", "apellido", "mail"), show="headings", height=15)
        tablaClientes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes.heading("nombre", text="Nombre", anchor="center")
        tablaClientes.heading("apellido", text="Apellido", anchor="center")
        tablaClientes.heading("mail", text="Mail", anchor="center")
        tablaClientes.column("dni_cliente", width=80, anchor="center")
        tablaClientes.column("nombre", width=130, anchor="center")
        tablaClientes.column("apellido", width=100, anchor="center")
        tablaClientes.column("mail", width=100, anchor="center")

        tablaClientes2 = ttk.Treeview(ventanaAvanzadasCliente, columns= ("dni_cliente", "nombre", "apellido", "mail", "cantidad_ordenes"), show="headings", height=15)
        tablaClientes2.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaClientes2.heading("nombre", text="Nombre", anchor="center")
        tablaClientes2.heading("apellido", text="Apellido", anchor="center")
        tablaClientes2.heading("mail", text="Mail", anchor="center")
        tablaClientes2.heading("cantidad_ordenes", text="Cantidad de ordenes", anchor="center")
        tablaClientes2.column("dni_cliente", width=80, anchor="center")
        tablaClientes2.column("nombre", width=130, anchor="center")
        tablaClientes2.column("apellido", width=100, anchor="center")
        tablaClientes2.column("mail", width=100, anchor="center")
        tablaClientes2.column("cantidad_ordenes", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonOrdenarAlfabeticamente.grid(row= 5, column=2, sticky="nse")
        botonOrdenarPorPedidos.grid(row= 5, column=2, sticky="nsw")
        botonVolver.grid(row= 11, column=3, sticky="e")  
        
    
        # Posicionar tabla + Llenar tabla con sus valores default
        tablaClientes.grid(row=8, column=2, sticky="nsew")
        

        def llenar_tabla():
            tablaClientes2.grid_remove()
            tablaClientes.delete(*tablaClientes.get_children())
            lista_clientes = cliente_db.verClientes()
            for producto in lista_clientes:
                tablaClientes.insert("", "end", values=producto)

        llenar_tabla() # Empezamos llenando la tabla con todos los valores

        def ordenarAlfabeticamente():
            db.conectar()
            tablaClientes2.grid_remove() # Eliminamos la tabla anterior
            tablaClientes.delete(*tablaClientes.get_children()) # Borramos los datos de la tabla actual por si el usuario toca dos veces el boton entonces asi no se duplican valores
            tablaClientes.grid(row=8, column=2, sticky="nsew") # Insertamos la tabla elegida en el lugar correspondiente
            lista_clientes = cliente_db.verClientesAlfabeticamente()
            for producto in lista_clientes:
                tablaClientes.insert("", "end", values=producto)

        def ordenarPorPedidos():
            db.conectar()
            tablaClientes.grid_remove()
            tablaClientes2.delete(*tablaClientes2.get_children())
            tablaClientes2.grid(row=8, column=2, sticky="nsew")
            lista_clientes = cliente_db.verClientesTabla2()
            for producto in lista_clientes:
                tablaClientes2.insert("", "end", values=producto)

        def on_close():
            nonlocal ventana_gestionClientes_abierta
            ventana_gestionClientes_abierta = False
            ventanaAvanzadasCliente.destroy()
            ventanaGestionDeClientes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeClientes.deiconify()
            
        ventanaAvanzadasCliente.protocol("WM_DELETE_WINDOW", on_close)

        

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
    headerPrincipal = tk.Label(ventanaGestionDeOrdenes, text="Gestion de ordenes", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones ESTOS SON LOS BOTONES QUE APARECEN EL MENU DE GESTION DE ORDENES 
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
        tablaOrdenes = ttk.Treeview(ventanaVerOrdenes, columns= ("id_orden", "dni_cliente", "id_producto", "cantidad", "fecha", "estado"), show="headings")
        tablaOrdenes.heading("id_orden", text="Id de orden", anchor="center")
        tablaOrdenes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaOrdenes.heading("id_producto", text="Id del producto", anchor="center")
        tablaOrdenes.heading("cantidad", text="Cantidad", anchor="center")
        tablaOrdenes.heading("fecha", text="Fecha", anchor="center")
        tablaOrdenes.heading("estado", text="Estado", anchor="center")
        tablaOrdenes.column("id_orden", width=80, anchor="center")
        tablaOrdenes.column("dni_cliente", width=80, anchor="center")
        tablaOrdenes.column("id_producto", width=80, anchor="center")
        tablaOrdenes.column("cantidad", width=80, anchor="center")
        tablaOrdenes.column("fecha", width=100, anchor="center")
        tablaOrdenes.column("estado", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew") 
    
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

        # Declarar ventana de gestion de ordenes
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
        calendarioFecha = Calendar(ventanaAgregarOrden, setmode="day", date_pattern="yy/m/d")
        botonAgregar = tk.Button(ventanaAgregarOrden, text="Agregar", command=lambda: agregar()) # Si el cliente hace click en este boton, vamos a ejecutar el codigo para agregar el cliente con los parametros que haya ingresado

        # Declarar tabla
        tablaOrdenes = ttk.Treeview(ventanaAgregarOrden, columns= ("id_orden", "dni_cliente", "id_producto", "cantidad", "fecha", "estado"), show="headings")
        tablaOrdenes.heading("id_orden", text="Id de orden", anchor="center")
        tablaOrdenes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaOrdenes.heading("id_producto", text="Id del producto", anchor="center")
        tablaOrdenes.heading("cantidad", text="Cantidad", anchor="center")
        tablaOrdenes.heading("fecha", text="Fecha", anchor="center")
        tablaOrdenes.heading("estado", text="Estado", anchor="center")
        tablaOrdenes.column("id_orden", width=80, anchor="center")
        tablaOrdenes.column("dni_cliente", width=80, anchor="center")
        tablaOrdenes.column("id_producto", width=80, anchor="center")
        tablaOrdenes.column("cantidad", width=80, anchor="center")
        tablaOrdenes.column("fecha", width=100, anchor="center")
        tablaOrdenes.column("estado", width=100, anchor="center")

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

        # Posicionar input textarea + boton agregar
        textareaIdProducto.grid(row=3, column=2, sticky="we")
        textAreaDniCliente.grid(row=4, column=2, sticky="we")
        textareaCantidad.grid(row=5, column=2, sticky="we")
        calendarioFecha.grid(row=6, column=2, sticky="we")
        
        botonAgregar.grid(row=7, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaOrdenes.grid(row=8, column=2, sticky="nsew")

        def popup_exito():
            popup_error = tk.Toplevel()
            popup_error.title("Exito!")
            popup_error.geometry("300x150")
            mensaje = tk.Label(popup_error, text="Se agrego la orden correctamente!", font=("Arial", 14))
            mensaje.config(fg="#4CAF50")
            mensaje.pack(pady=20)
    
            # Crear botón para cerrar el popup
            boton_cerrar = tk.Button(popup_error, text="Cerrar", command=popup_error.destroy)
            boton_cerrar.pack()
       
        def llenar_tabla():
            lista_ordenes = orden_db.verOrdenes()
            for orden in lista_ordenes:
                tablaOrdenes.insert("", "end", values=orden)

        llenar_tabla()

        def agregar():
            db.conectar()
            dni_cliente_ingresado = textAreaDniCliente.get("1.0", "end").strip()
            id_producto_ingresado = textareaIdProducto.get("1.0", "end").strip()
            cantidad_ingresada = textareaCantidad.get("1.0", "end").strip()
            fecha_ingresada = calendarioFecha.get_date()
            if dni_cliente_ingresado == '' or id_producto_ingresado == '' or cantidad_ingresada == '' or fecha_ingresada == '':
                crearErrorPopUp("Atencion, falta ingresar algun\nparametro!", color="#FFC107") # Si alguno de los valores no es ingresado entonces no vale la pena ejecutar el codigo, asi evitamos generar errores innecesarios
            elif not cantidad_ingresada.isdigit():
                crearErrorPopUp("Error, la cantidad ingresada tiene\nque ser un numero entero\npositivo!")
            else:
                resultado = orden_db.agregarOrden(dni_cliente_ingresado, id_producto_ingresado, cantidad_ingresada, fecha_ingresada)
                if resultado == 5: # Exito
                    tablaOrdenes.delete(*tablaOrdenes.get_children())
                    llenar_tabla()
                    crearErrorPopUp("Se agrego la orden correctamente!", color="#4CAF50")
                elif resultado == 1: 
                    crearErrorPopUp("Error, la cantidad del pedido\nno puede ser menor a 0") # La cantidad del pedido no puede ser menor a 0
                elif resultado == 2:
                    crearErrorPopUp("Error, el producto elegido no\ntiene stock suficiente") # El producto elegido no tiene stock suficiente
                elif resultado == 3:
                    crearErrorPopUp("Error, no existe un producto\ncon ese id") # No existe un producto con ese id
                elif resultado == 4:
                    crearErrorPopUp("Error, no existe un cliente\ncon ese DNI") # No existe un cliente con ese dni

        def on_close():
            nonlocal ventana_gestionOrdenes_abierta
            ventana_gestionOrdenes_abierta = False
            ventanaAgregarOrden.destroy()
            ventanaGestionDeOrdenes.state("zoomed") # Hacemos el zoom antes de traer la ventana nuevamente porque sino se nota mucho cuando se hace el zoom y queda feo
            ventanaGestionDeOrdenes.deiconify()
            
        ventanaAgregarOrden.protocol("WM_DELETE_WINDOW", on_close)

    def modificarOrden():
        db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
        nonlocal ventana_gestionOrdenes_abierta

        if ventana_gestionOrdenes_abierta:
            return 
        
        ventanaGestionDeOrdenes.withdraw()

        # Declarar ventana de gestion de Ordens
        ventana_gestionOrdenes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaModificarOrden = tk.Toplevel()
        ventanaModificarOrden.config(bg="#d1d1e0")
        ventanaModificarOrden.title("Gestion de ordenes")
        ventanaModificarOrden.state("zoomed")

        # Declarar grid de la ventana
        crearGridVentana(ventanaModificarOrden)

        # Declarar header y texto
        headerPrincipal = tk.Label(ventanaModificarOrden, text="Modificar ordenes", font=("Arial", 20, "bold"), bg="#d1d1e0")
        subtitulo = tk.Label(ventanaModificarOrden, text="Ingresa los valores para cambiarle al orden", font=("Arial", 17, "bold"), bg="#d1d1e0")

        # Declarar botones
        botonVolver = tk.Button(ventanaModificarOrden, text="Volver", bg="#9494b8", font=("Arial", 14), command=lambda: on_close())

        # Declarar label de atributos para Modificar
        labeIdOrden = tk.Label(ventanaModificarOrden, text="ID de la orden a modificar: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelIdProducto = tk.Label(ventanaModificarOrden, text="ID producto nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelDniCliente = tk.Label(ventanaModificarOrden, text="DNI cliente nuevo: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelCantidad = tk.Label(ventanaModificarOrden, text="Cantidad nueva: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelFecha = tk.Label(ventanaModificarOrden, text="Nueva fecha: ", font=("Arial", 12, "bold"), bg="#d1d1e0")
        labelEstado = tk.Label(ventanaModificarOrden, text="Estado de orden:", font=("Arial", 12, "bold"), bg="#d1d1e0")

        # Declarar input textarea + boton buscar + dropdown
        textareaIdOrdenAModificar = Text(ventanaModificarOrden, height=max, width=25)
        textareaIdProductoAModificar= Text(ventanaModificarOrden, height=max, width=25)
        textAreaDniClienteAModificar = Text(ventanaModificarOrden, height=max, width=25)
        textAreaCantidadAModificar = Text(ventanaModificarOrden, height=max, width=25)
        textAreaFechaAModificar = Text(ventanaModificarOrden, height=max, width=25)

        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        eleccion.set("En proceso")
        dropdownEstado = OptionMenu(ventanaModificarOrden, eleccion, "En proceso", "Entregado")

        botonModificar = tk.Button(ventanaModificarOrden, text="Modificar", command=lambda: Modificar()) # Si el usuaario hace click en este boton, vamos a ejecutar el codigo para Modificar la orden con los parametros que haya ingresado

        # Declarar tabla
        tablaOrdenes = ttk.Treeview(ventanaModificarOrden, columns= ("id_orden", "dni_cliente", "id_producto", "cantidad", "fecha", "estado"), show="headings")
        tablaOrdenes.heading("id_orden", text="Id de orden", anchor="center")
        tablaOrdenes.heading("dni_cliente", text="DNI del cliente", anchor="center")
        tablaOrdenes.heading("id_producto", text="Id del producto", anchor="center")
        tablaOrdenes.heading("cantidad", text="Cantidad", anchor="center")
        tablaOrdenes.heading("fecha", text="Fecha", anchor="center")
        tablaOrdenes.heading("estado", text="Estado", anchor="center")
        tablaOrdenes.column("id_orden", width=80, anchor="center")
        tablaOrdenes.column("dni_cliente", width=80, anchor="center")
        tablaOrdenes.column("id_producto", width=80, anchor="center")
        tablaOrdenes.column("cantidad", width=80, anchor="center")
        tablaOrdenes.column("fecha", width=100, anchor="center")
        tablaOrdenes.column("estado", width=100, anchor="center")

        # Posicionar header + subtitulo
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        subtitulo.grid(row=2, column=2, sticky="sew")

        # Posicionar botones
        botonVolver.grid(row= 11, column=3, sticky="e")  

        # Posicionar label de atributos para Modificar
        labeIdOrden.grid(row=3, column=1, sticky="e")
        labelIdProducto.grid(row=4, column=1, sticky="e")
        labelDniCliente.grid(row=5, column=1, sticky="e")
        labelCantidad.grid(row=6, column=1, sticky="e")
        labelFecha.grid(row=7, column=1, sticky="e")
        labelEstado.grid(row=8, column=1, sticky="e")

        # Posicionar input textarea + Modificar
        textareaIdOrdenAModificar.grid(row=3, column=2, sticky="we")
        textareaIdProductoAModificar.grid(row=4, column=2, sticky="we")
        textAreaDniClienteAModificar.grid(row=5, column=2, sticky="we")
        textAreaCantidadAModificar.grid(row=6, column=2, sticky="we")
        textAreaFechaAModificar.grid(row=7, column=2, sticky="we")
        dropdownEstado.grid(row=8, column=3, sticky="w")
        botonModificar.grid(row=8, column=3, sticky="w")

        # Posicionar tabla + Llenar tabla con sus valores default
        tablaOrdenes.grid(row=8, column=2, sticky="nsew")
       
        def llenar_tabla():
            lista_ordenes = orden_db.verOrdenes()
            for orden in lista_ordenes:
                tablaOrdenes.insert("", "end", values=orden)
        
        llenar_tabla()
        def Modificar(): 
            db.conectar() # Por alguna razon se desconecta la base de datos una vez que cerramos esta ventana, por lo que vamos a poner este parche para solucionarlo
            estado_orden_nuevo = eleccion.get()
            id_orden_a_modificar = textareaIdOrdenAModificar.get("1.0", "end").strip()
            id_producto_nuevo = textareaIdProductoAModificar.get("1.0", "end").strip()
            dni_cliente_nuevo = textAreaDniClienteAModificar.get("1.0", "end").strip()
            cantidad_nueva = textAreaCantidadAModificar.get("1.0", "end").strip()
            fecha_nueva = textAreaFechaAModificar.get("1.0", "end").strip()
            if id_orden_a_modificar == '': # Si el id esta vacio entonces vamos a ignorar esta parte del codigo ya que seria innecesario ejecutuarla si el usuario nisiquiere ingreso un dni. Asi evitamos que haya un error de sql por faltar valor en el procedimiento o por tener valores incorrectos en otros parametros
                 crearErrorPopUp("Atencion, no ingresaste\nun ID de orden", color="#FFC107")
            else:
                if id_producto_nuevo == '' and dni_cliente_nuevo == '' and cantidad_nueva == '' and fecha_nueva == '':
                    pass # Si el usuario no ingreso ningun valor entonces nos vamos a ahorrar la ejecucion del procedimiento
                else:
                    if estado_orden_nuevo == '':
                        estado_orden_nuevo == None
                    if cantidad_nueva == '':
                        cantidad_nueva = None # Convertimos la cantidad a None si no se le ingresa ningun valor: de esta manera, la conversion a sql lo convierte en un valor NULL y, al cumplir con una condicion, el codigo sql evita atualizar el stock del producto nuevo ingresado o el antiguo ya presente en la orden siendo modificada
                    if id_producto_nuevo == '':
                        id_producto_nuevo = None
                    if dni_cliente_nuevo == '':
                        dni_cliente_nuevo = None
                    if fecha_nueva == '':
                        fecha_nueva = None # Hacemos lo mismo con todas las variables para que, al cumplirse cierta condicion en el codigo sql, los valores no van a ser modificado sino que se van a quedar como estaban antes.
                    resultado = orden_db.modificarOrdenPorId(id_orden_a_modificar, dni_cliente_nuevo, id_producto_nuevo, cantidad_nueva, fecha_nueva, estado_orden_nuevo)
                    if resultado == 1:
                        crearErrorPopUp("Error, no existe una orden\ncon ese ID")
                    elif resultado == 2:
                        crearErrorPopUp("Error, no existe un cliente\ncon ese DNI")
                    elif resultado == 3:
                        crearErrorPopUp("Error, no existe un producto\ncon ese ID")
                    elif resultado == 4:
                        crearErrorPopUp("Error, la cantidad nueva no\npuede ser negativa")
                    elif resultado == 5:
                        crearErrorPopUp("Error, el stock del produto\nno es suficiente para abastecer\nel nuevo cambio de cantidad")
                    elif resultado == 7:
                        crearErrorPopUp("Error, no hay stock suficiente\ndel nuevo producto ingresado")
                    elif resultado == 8:
                        crearErrorPopUp("Error, la orden ya fue entregada,\nya no puede ser modificada")
                    else:
                        tablaOrdenes.delete(*tablaOrdenes.get_children())
                        llenar_tabla()
                        crearErrorPopUp("Orden modificada correctamente!", color="#4CAF50")
                     

    def eliminarOrden():
        pass

    def consultasAvanzadas():
        pass

ventanaPrincipal()