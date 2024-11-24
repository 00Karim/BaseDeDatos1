import tkinter as tk

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
    ventana.geometry("450x500")

    # Declarar grid de la ventana principal
    crearGridVentana(ventana)

    # Declarar header
    headerPrincipal = tk.Label(ventana, text="SISTEMA DE VENTAS EN LINEA", font=("Arial", 20, "bold"), bg="#d1d1e0")

    # Declarar botones
    GestionDeProductos = tk.Button(ventana, text="Gestion de productos", bg="#9494b8", font=("Arial", 14), command=ventanaGestionDeProductos)
    GestionDeClientes = tk.Button(ventana, text="Gestion de clientes", bg="#9494b8", font=("Arial", 14), command=ventanaGestionDeClientes)
    GestionDeOrdenes = tk.Button(ventana, text="Gestion de ordenes", bg="#9494b8", font=("Arial", 14), command=ventanaGestionDeOrdenes)

    # Posicionar header
    headerPrincipal.grid(row=2, column=2, sticky="nsew")

    # Posicionar botones
    GestionDeProductos.grid(row=4, column=2, sticky="nsew")
    GestionDeClientes.grid(row=6, column=2, sticky="nsew")
    GestionDeOrdenes.grid(row=8, column=2, sticky="nsew")

    ventana.mainloop()

def ventanaGestionDeProductos():
    global ventana_productos_abierta

    if ventana_productos_abierta:
        return

    # Declarar ventana de gestion de productos
    ventana_productos_abierta = True # Ponemos la variable en True para indicar que la ventana fue abierta y esta abierta 
    ventanaGestionDeProductos = tk.Toplevel()
    ventanaGestionDeProductos.config(bg="#d1d1e0")
    ventanaGestionDeProductos.title("Gestion de productos")
    ventanaGestionDeProductos.geometry("450x500")

    # Declarar grid de la ventana
    crearGridVentana(ventanaGestionDeProductos)

    def on_close():
        global ventana_productos_abierta
        ventana_productos_abierta = False
        ventanaGestionDeProductos.destroy()

    ventanaGestionDeProductos.protocol("WM_DELETE_WINDOW", on_close)

def ventanaGestionDeClientes():
    global ventana_clientes_abierta

    # Si la variable es True entonces significa que la ventana ya fue abierta entonces no queremos abrirla nuevamente por lo que vamos a hacer un return
    if ventana_clientes_abierta:
        return
    
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

    ventanaGestionDeClientes.protocol("WM_DELETE_WINDOW", on_close)

def ventanaGestionDeOrdenes():

    global ventana_ordenes_abierta

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

    ventanaGestionDeOrdenes.protocol("WM_DELETE_WINDOW", on_close)

ventanaPrincipal()