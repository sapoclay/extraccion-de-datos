import mysql.connector
import json
import tkinter.messagebox as messagebox

def conectar_bd():
    # Conectar a la base de datos MySQL. Aquí hay que configurar los datos de tu conexión
    conn = mysql.connector.connect(
        host="localhost",
        user="XXX",
        password="XXXX",
        database="extraccion_datos"
    )
    return conn

def crear_tabla():
    # Crear una tabla en la base de datos si no existe
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS datos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        archivo VARCHAR(255),
                        contenido TEXT)''')
    conn.commit()
    conn.close()

def insertar_en_bd_desde_json():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Verificar si la tabla existe, si no existe, crearla
        cursor.execute('''CREATE TABLE IF NOT EXISTS datos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            archivo VARCHAR(255),
                            contenido TEXT)''')
        
        # Leer datos del archivo JSON
        with open('porcion.json', 'r') as f:
            data = json.load(f)
        
        # Obtener los datos existentes en la base de datos
        cursor.execute("SELECT archivo, contenido FROM datos")
        registros_exist = {archivo: contenido for archivo, contenido in cursor.fetchall()}
        
        # Insertar o actualizar datos en la base de datos
        for archivo, contenidos in data.items():
            for contenido in contenidos:
                # Verificar si el archivo ya existe en la base de datos
                if archivo in registros_exist:
                    # Si el contenido es diferente al de la base de datos, agregar el contenido nuevo
                    if contenido not in registros_exist[archivo]:
                        nuevo_contenido = registros_exist[archivo] + "\n" + contenido
                        cursor.execute("UPDATE datos SET contenido = %s WHERE archivo = %s", (nuevo_contenido, archivo))
                else:
                    # Si el archivo no existe en la base de datos, insertar
                    cursor.execute("INSERT INTO datos (archivo, contenido) VALUES (%s, %s)", (archivo, contenido))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Los datos fueron insertados/actualizados en la base de datos correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al insertar/actualizar los datos en la base de datos: {str(e)}")