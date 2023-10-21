from tkinter import *
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)
mycursor = mydb.cursor()

# Función para agregar un producto al inventario
def agregar_producto():
    
    
    if entry_nombre.get() != "":
        nombre = entry_nombre.get()
    else:
        messagebox.showerror("ERROR", "falta agregar NOMBRE")

    if entry_cantidad.get() != "":
        cantidad = entry_cantidad.get()
    else:
        messagebox.showerror("ERROR", "falta agregar CANTIDAD")
            
    if entry_precio.get() != "":
        precio = entry_precio.get()
    else:
     messagebox.showerror("ERROR", "falta agregar PRECIO")


    if nombre and cantidad and precio:
        sql= "INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)"
        val=(nombre, precio, cantidad)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("exito","producto agregado correctamente")
        obtener_productos()
    

# Función para buscar un producto en el inventario
def buscar_producto():
    nombre = entry_buscar.get()
    
    sql = "SELECT * FROM productos WHERE nombre LIKE %s"
    val = (f"%{nombre}%",)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    
    listbox.delete(0, END)
    for producto in result:
        listbox.insert(END, producto)

# Función para eliminar un producto del inventario
def eliminar_producto():
    seleccion = listbox.curselection() 
    if seleccion:
        producto_seleccionado = listbox.get(seleccion)
        try:
          depurar = producto_seleccionado.replace('ID: ', '')
          limpiar = depurar.split(',')
          dato = limpiar[0]
        except:
            limpiar = producto_seleccionado[0]
            dato = limpiar
        print(dato)
        mycursor.execute(f"DELETE FROM productos WHERE id_producto = {dato}")
        mydb.commit()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        obtener_productos() 
    else:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ningún producto")

# Función para obtener y mostrar todos los productos del inventario
def obtener_productos():
    mycursor.execute("SELECT * FROM productos")
    result = mycursor.fetchall()
    
    listbox.delete(0, END)
    for producto in result:
        producto_texto = f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Cantidad: {producto[3]}"
        listbox.insert(END, producto_texto)
    listbox.config(width=60)

def actualizar_productos():
    seleccion = listbox.curselection() 
   
    print(f"hola estoy actalizando {seleccion}")

# Creación de la ventana principal
root = Tk()
root.title("Sistema de Inventario")

# Campos de entrada de datos
label_nombre = Label(root, text="Nombre del producto:")
label_nombre.grid(row=0, column=0, padx=10, pady=10)
entry_nombre = Entry(root, width=40)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

label_cantidad = Label(root, text="cantidad:")
label_cantidad.grid(row=1, column=0, padx=10, pady=10)
entry_cantidad = Entry(root, width=40)
entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

label_precio = Label(root, text="precio:")
label_precio.grid(row=2, column=0, padx=10, pady=10)
entry_precio = Entry(root, width=40)
entry_precio.grid(row=2, column=1, padx=10, pady=10)

# Botón para agregar el producto
button_agregar = Button(root, text="Agregar", width=20, command=agregar_producto)
button_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Campo de búsqueda
label_buscar = Label(root, text="Buscar producto:")
label_buscar.grid(row=4, column=0, padx=10, pady=10)
entry_buscar = Entry(root, width=40)
entry_buscar.grid(row=4, column=1, padx=10, pady=10)

# Botón para buscar el producto
button_buscar = Button(root, text="Buscar", width=20, command=buscar_producto)
button_buscar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Botón para eliminar el producto
button_eliminar = Button(root, text="Eliminar", width=20, command=eliminar_producto)
button_eliminar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Botón para actualizar producto
button_actualizar = Button(root, text="Actualizar", width=20,command=actualizar_productos )
button_actualizar.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Lista de productos
listbox = Listbox(root, width=60)
listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Scrollbar para la lista de productos
scrollbar = Scrollbar(root)
scrollbar.grid(row=7, column=2, sticky=N+S)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Obtener y mostrar todos los productos al iniciar la aplicación
obtener_productos()

# color de fondos 
root.configure(background="dark blue")

# Ejecución de la ventana principal
root.mainloop()