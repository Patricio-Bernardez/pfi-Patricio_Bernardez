# Importa la librería de sqlite3 para usar la base de datos e importa un par de diseños de la librería de colorama para mayor claridad en los textos
import sqlite3
from colorama import init, Fore, Style, Back

# Inicializa colorama con autoreset para evitar el problema de resetear los colores manualmente
init(autoreset=True)


# Función para crea la base de datos sqlite si no existe y define la estructura de la tabla productos
def crear_base_datos(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
        """
    )


# Función para registrar un nuevo producto
def registrar_producto(cursor, nombre, descripcion, cantidad, precio, categoria):
    cursor.execute(
        """
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre, descripcion, cantidad, precio, categoria),
    )


# Función para consultar productos por nombre
def consultar_producto(cursor, nombre_producto):
    cursor.execute(
        """
        SELECT * FROM productos WHERE nombre LIKE ?
        """,
        ("%" + nombre_producto + "%",),
    )
    return cursor.fetchall()


# Función para consultar un producto por su ID
def consultar_producto_por_id(cursor, id_producto):
    cursor.execute(
        """
        SELECT * FROM productos WHERE id = ?
        """,
        (id_producto,),
    )
    return cursor.fetchone()


# Función para actualizar la cantidad de un producto
def actualizar_cantidad(cursor, id_producto, nueva_cantidad):
    cursor.execute(
        """
        UPDATE productos SET cantidad = ? WHERE id = ?
        """,
        (nueva_cantidad, id_producto),
    )


# Función para eliminar un producto por su ID
def eliminar_producto(cursor, id_producto):
    cursor.execute(
        """
        DELETE FROM productos WHERE id = ?
        """,
        (id_producto,),
    )


# Función para listar todos los productos
def listar_productos(cursor):
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()


# Función para generar un reporte de productos con bajo stock
def reporte_bajo_stock(cursor, umbral):
    cursor.execute(
        """
        SELECT * FROM productos WHERE cantidad < ?
        """,
        (umbral,),
    )
    return cursor.fetchall()


# Función para mostrar el menú principal
def mostrar_menu():
    print(Fore.CYAN + "\n--- Menú de Gestión de Inventario ---")
    print(Fore.YELLOW + "1. Registrar producto")
    print(Fore.YELLOW + "2. Consultar producto")
    print(Fore.YELLOW + "3. Actualizar cantidad de producto")
    print(Fore.YELLOW + "4. Eliminar producto")
    print(Fore.YELLOW + "5. Listar todos los productos")
    print(Fore.YELLOW + "6. Reporte de bajo stock")
    print(Fore.YELLOW + "7. Salir")


# Función para validar entradas numéricas
def pedir_entero(
    mensaje,
    mensaje_error="Entrada inválida. Por favor ingrese un número entero válido.",
):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print(Fore.RED + mensaje_error)


# Función para validar entradas flotantes
def pedir_flotante(
    mensaje,
    mensaje_error="Entrada inválida. Por favor ingrese un número decimal válido.",
):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print(Fore.RED + mensaje_error)


# Función que contiene el flujo del menú y las opciones
def menu():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    crear_base_datos(cursor)

    while True:
        mostrar_menu()
        opcion = input(Fore.GREEN + "Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            cantidad = pedir_entero("Ingrese la cantidad disponible: ")
            precio = pedir_flotante("Ingrese el precio del producto: ")
            categoria = input("Ingrese la categoría del producto: ")
            registrar_producto(cursor, nombre, descripcion, cantidad, precio, categoria)
            print(Fore.GREEN + "Producto registrado exitosamente.")

        elif opcion == "2":
            # Verificamos si hay productos registrados en la base de datos
            productos = listar_productos(cursor)
            if not productos:
                print(Fore.RED + "Todavía no se registró ningún producto.")
                continue

            # Opción para consultar productos por ID o por nombre
            print(Fore.YELLOW + "\n¿Desea consultar el producto por ID o por nombre?")
            print(Fore.GREEN + "1. Consultar por ID")
            print(Fore.GREEN + "2. Consultar por nombre")
            eleccion = input(Fore.GREEN + "Seleccione una opción: ")

            if eleccion == "1":
                id_producto = pedir_entero("Ingrese el ID del producto a consultar: ")
                producto = consultar_producto_por_id(cursor, id_producto)
                if producto:
                    print(Fore.CYAN + "\nProducto encontrado:")
                    print(
                        Fore.YELLOW
                        + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}"
                    )
                else:
                    print(Fore.RED + "No se encontró ningún producto con ese ID.")

            elif eleccion == "2":
                nombre_producto = input("Ingrese el nombre del producto a consultar: ")
                productos_encontrados = consultar_producto(cursor, nombre_producto)
                if productos_encontrados:
                    print(Fore.CYAN + "\nProductos encontrados:")
                    for producto in productos_encontrados:
                        print(
                            Fore.YELLOW
                            + f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}"
                        )
                else:
                    print(Fore.RED + "No se encontraron productos con ese nombre.")
            else:
                print(Fore.RED + "Opción inválida. Regresando al menú principal.")

        elif opcion == "3":
            id_producto = pedir_entero("Ingrese el ID del producto a actualizar: ")
            producto_existente = consultar_producto_por_id(cursor, id_producto)

            if not producto_existente:
                print(Fore.RED + "El producto con ese ID no existe en el inventario.")
                continue

            nueva_cantidad = pedir_entero("Ingrese la nueva cantidad disponible: ")
            actualizar_cantidad(cursor, id_producto, nueva_cantidad)
            print(Fore.GREEN + "Cantidad actualizada correctamente.")

        elif opcion == "4":
            id_producto = pedir_entero("Ingrese el ID del producto a eliminar: ")
            eliminar_producto(cursor, id_producto)
            print(Fore.GREEN + "Producto eliminado correctamente.")

        elif opcion == "5":
            productos = listar_productos(cursor)
            if productos:
                print(Fore.CYAN + "\nListado completo de productos:")
                for producto in productos:
                    print(
                        Fore.YELLOW
                        + f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: {producto[4]}"
                    )
            else:
                print(Fore.RED + "Todavía no se registraron productos.")

        elif opcion == "6":
            umbral = pedir_entero("Ingrese el umbral de bajo stock: ")
            productos_bajo_stock = reporte_bajo_stock(cursor, umbral)
            if productos_bajo_stock:
                print(Fore.CYAN + "\nReporte de productos con bajo stock:")
                for producto in productos_bajo_stock:
                    print(
                        Fore.RED
                        + f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}"
                    )
            else:
                print(
                    Fore.RED
                    + "No hay productos con bajo stock según el umbral proporcionado."
                )

        elif opcion == "7":
            print(Fore.GREEN + "Cerrando la aplicación...")
            break

        else:
            print(Fore.RED + "Opción inválida, por favor intente de nuevo.")

    conexion.commit()
    conexion.close()


# Punto de entrada principal
if __name__ == "__main__":
    menu()
