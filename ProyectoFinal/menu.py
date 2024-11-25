import tkinter as tk
from tkinter import ttk, OptionMenu, StringVar, Text

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
    ventana.attributes('-fullscreen', True)

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

    ventana_gestionProductos_abierta = False

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
    ventanaGestionDeProductos.attributes('-fullscreen', True)

    # Declarar grid de la ventana
    crearGridVentana(ventanaGestionDeProductos)

    # Declarar header
    headerPrincipal = tk.Label(ventanaGestionDeProductos, text="Gestion de productos", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones
    verProducto = tk.Button(ventanaGestionDeProductos, text="Ver productos", bg="#9494b8", font=("Arial", 14), command=lambda: verProducto())
    agregarProducto = tk.Button(ventanaGestionDeProductos, text="Agregar producto", bg="#9494b8", font=("Arial", 14), command=lambda: None)
    modificarProducto = tk.Button(ventanaGestionDeProductos, text="Modificar producto", bg="#9494b8", font=("Arial", 14), command=lambda: None)
    eliminarProducto = tk.Button(ventanaGestionDeProductos, text="Eliminar producto", bg="#9494b8", font=("Arial", 14), command=lambda: None)
    consultasAvanzadas = tk.Button(ventanaGestionDeProductos, text="Consultas avanzadas", bg="#9494b8", font=("Arial", 14), command=lambda: None)

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
        ventanaAnterior.deiconify()

    ventanaGestionDeProductos.protocol("WM_DELETE_WINDOW", on_close)

    def verProducto():
        nonlocal ventana_gestionProductos_abierta

        if ventana_gestionProductos_abierta:
            return 
        
        ventanaGestionDeProductos.withdraw()

        # Declarar ventana de gestion de productos
        ventana_gestionProductos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
        ventanaVerProducto = tk.Toplevel()
        ventanaVerProducto.config(bg="#d1d1e0")
        ventanaVerProducto.title("Gestion de productos")
        ventanaVerProducto.geometry("450x500")

        # Declarar grid de la ventana
        crearGridVentana(ventanaVerProducto)

        # Declarar header
        headerPrincipal = tk.Label(ventanaVerProducto, text="Ver productos", font=("Arial", 20, "bold"), bg="#d1d1e0")

        # Declarar botones

        # Declarar dropdown
        eleccion = StringVar() # Declaramos la variable como string var para poder acceder a ella para definir los metodos usados para mostrar la tabla
        eleccion.set("Id")
        dropdown = OptionMenu(ventanaVerProducto, eleccion, "Id", "Nombre", "Categoria")
        
        # Declarar input textarea + boton buscar
        dropdownTextarea = Text(ventanaVerProducto, height=max, width=25)
        botonBuscar = tk.Button(ventanaVerProducto, text="Aceptar", command=None)

        # Declarar tabla
        tablaProductos = ttk.Treeview(ventanaVerProducto, columns= ("id_producto", "nombre", "cantidad_disponible", "categoria", "ventas_totales"), show="headings")
        tablaProductos.heading("id_producto", text="Id del producto")
        tablaProductos.heading("nombre", text="Nombre")
        tablaProductos.heading("cantidad_disponible", text="Cantidad disponible")
        tablaProductos.heading("categoria", text="Categoria")
        tablaProductos.heading("ventas_totales", text="Ventas totales")
        tablaProductos.column("id_producto", width=80)
        tablaProductos.column("nombre", width=130)
        tablaProductos.column("cantidad_disponible", width=100)
        tablaProductos.column("categoria", width=130)
        tablaProductos.column("ventas_totales", width=100)

        # Posicionar header
        headerPrincipal.grid(row=1, column=2, sticky="nsew")
        

        # Posicionar botones

        # Posicionar dropdown
        dropdown.grid(row=3, column=1, sticky="ew")

        # Posicionar input textarea + boton buscar
        dropdownTextarea.grid(row=3, column=2, sticky="we")
        botonBuscar.grid(row=3, column=3, sticky="w")

        # Posicionar tabla
        tablaProductos.grid(row=4, column=2, rowspan=7, sticky="nsew")
    
        def on_close():
            nonlocal ventana_gestionProductos_abierta
            ventana_gestionProductos_abierta = False
            ventanaVerProducto.destroy()
            ventanaGestionDeProductos.deiconify()

        ventanaVerProducto.protocol("WM_DELETE_WINDOW", on_close)


    def agregarProducto():
        pass

    def modificarProducto():
        pass

    def eliminarProducto():
        pass

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

    global ventana_ordenes_abierta

    # Cerramos la ventana principal
    ventanaAnterior.withdraw()

    # Si la variable es True entonces significa que la ventana ya fue abierta entonces no queremos abrirla nuevamente por lo que vamos a hacer un return
    if ventana_ordenes_abierta:
        return

    # Declarar ventana de gestion de ordenes
    ventana_ordenes_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
    ventanaGestionDeOrdenes = tk.Toplevel()
    ventanaGestionDeOrdenes.config(bg="#d1d1e0")
    ventanaGestionDeOrdenes.title("Gestion de ordenes")
    ventanaGestionDeOrdenes.geometry("450x500")

    # Declarar grid de la ventana 
    crearGridVentana(ventanaGestionDeOrdenes) 

    # Con el codigo a continuacion cambiamos la variable de ventana abierta a Falso asi podemos abrirlo nuevamente despues de cerrarlo
    def on_close():
        global ventana_ordenes_abierta
        ventana_ordenes_abierta = False
        ventanaGestionDeOrdenes.destroy()
        ventanaAnterior.deiconify()

    ventanaGestionDeOrdenes.protocol("WM_DELETE_WINDOW", on_close)

ventanaPrincipal()