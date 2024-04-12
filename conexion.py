import mysql.connector
import json
import tkinter.messagebox as messagebox
import traceback
import datetime
import tkinter as tk
from tkinter import messagebox

def conectar_bd():
    # Conectar a la base de datos MySQL. Aquí hay que configurar los datos de tu conexión a la BD
    conn = mysql.connector.connect(
        host="localhost",
        user="xxxx",
        password="xxxx",
        database="extraccion_datos"
    )
    return conn

def insertar_en_bd_desde_json():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Verificar si la tabla existe, si no existe, crearla
        cursor.execute('''CREATE TABLE IF NOT EXISTS datos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            archivo VARCHAR(255),
                            contenido TEXT,
                            notas VARCHAR(255),
                            fecha_guardado DATETIME)''')
        
        # Leer datos del archivo JSON
        with open('porcion.json', 'r') as f:
            data = json.load(f)
        
        # Insertar o actualizar datos en la base de datos
        for archivo, contenidos in data.items():
            # Obtener el contenido existente para el archivo, si existe
            cursor.execute("SELECT contenido FROM datos WHERE archivo = %s", (archivo,))
            registro_existente = cursor.fetchone()
            contenido_existente = registro_existente[0] if registro_existente else None
            
            # Si el contenido existe, verificar y agregar solo contenido nuevo
            if contenido_existente:
                nuevo_contenido = contenido_existente
                for contenido_nuevo in contenidos:
                    if contenido_nuevo not in contenido_existente:
                        nuevo_contenido += "\n" + contenido_nuevo
                # Actualizar el registro existente en la base de datos
                cursor.execute("UPDATE datos SET contenido = %s WHERE archivo = %s", (nuevo_contenido, archivo))
            else:
                # Insertar un nuevo registro en la base de datos
                fecha_hora_actual = datetime.datetime.now()
                fecha_hora_actual_str = fecha_hora_actual.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO datos (archivo, contenido, fecha_guardado) VALUES (%s, %s, %s)", 
                               (archivo, "\n".join(contenidos), fecha_hora_actual_str))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Éxito", "Los datos fueron insertados/actualizados en la base de datos correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al insertar/actualizar los datos en la base de datos: {str(e)}")
        traceback.print_exc()
        
# Función para mostrar el contenido guardado en la base de datos
def obtener_contenido_bd():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT archivo, contenido, notas, fecha_guardado FROM datos")
        registros = cursor.fetchall()

        conn.close()

        return registros
    except Exception as e:
        print(f"Error al obtener el contenido de la base de datos: {str(e)}")
        return None

# Función para guardar la nota en la base de datos
def guardar_nota_en_bd(archivo, nota):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        # Actualizar la nota en la base de datos
        cursor.execute("UPDATE datos SET notas = %s WHERE archivo = %s", (nota, archivo))
        conn.commit()
        conn.close()
        messagebox.showinfo("Nota Guardada", "Nota guardada en la base de datos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar la nota en la base de datos: {str(e)}")

# Función para obtener la nota asociada al archivo desde la base de datos
def obtener_nota_desde_bd(archivo):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        # Obtener la nota desde la base de datos
        cursor.execute("SELECT notas FROM datos WHERE archivo = %s", (archivo,))
        nota = cursor.fetchone()
        conn.close()
        if nota:
            return nota[0]
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al obtener la nota desde la base de datos: {str(e)}")
        return None

def eliminar_registro_bd(archivo, callback):
    try:
        # Mostrar un mensaje de confirmación al usuario
        confirmacion = messagebox.askokcancel("Confirmar eliminación", f"¿Está seguro de eliminar el registro '{archivo}'?")
        
        if confirmacion:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM datos WHERE archivo = %s", (archivo,))
            conn.commit()
            conn.close()
           
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            # Llamar a la función para volver a mostrar los registros actualizados
            callback()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al eliminar el registro: {str(e)}")
        
