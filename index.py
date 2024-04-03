# Importa la conexión a la BD
import conexion
# Importa la biblioteca tkinter para crear la interfaz gráfica
import tkinter as tk

# Importa módulos específicos de tkinter para diálogos de archivo y mensajes emergentes
from tkinter import filedialog, messagebox

# Importa módulos para manejar diferentes tipos de archivos
import PyPDF2  # Para archivos PDF
import docx  # Para archivos Word
import openpyxl  # Para archivos Excel
import json  # Para archivos JSON
import os  # Para interactuar con el sistema operativo

# Importa módulos para trabajar con otros tipos de archivos
from odf.opendocument import load  # Para archivos ODT
from odf import text, teletype
from bs4 import BeautifulSoup  # Para archivos HTML

# Inicializa una variable global para almacenar el nombre del archivo
nombre_archivo = ""

# Función para leer un archivo y mostrar su contenido en un cuadro de texto
def leer_archivo():
    global nombre_archivo
    # Abre un cuadro de diálogo para seleccionar un archivo y almacena su nombre en la variable 'nombre_archivo'
    nombre_archivo = filedialog.askopenfilename()
    try:
        # Determina el tipo de archivo basado en su extensión y procesa el contenido correspondiente
        if nombre_archivo.endswith('.txt'):
            with open(nombre_archivo, 'r') as archivo:
                contenido = archivo.read()
                text_box.delete('1.0', tk.END)
                text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.pdf'):
            with open(nombre_archivo, 'rb') as archivo:
                pdf_reader = PyPDF2.PdfReader(archivo)
                contenido = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    contenido += page.extract_text()
                text_box.delete('1.0', tk.END)
                text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.docx'):
            doc = docx.Document(nombre_archivo)
            contenido = ''
            for paragraph in doc.paragraphs:
                contenido += paragraph.text
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.xlsx'):
            wb = openpyxl.load_workbook(nombre_archivo)
            contenido = ''
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                for row in sheet.iter_rows(values_only=True):
                    contenido += ' '.join(str(cell) for cell in row) + '\n'
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.odt'):
            contenido = leer_archivo_odt(nombre_archivo)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.csv'):
            contenido = leer_archivo_csv(nombre_archivo)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, contenido)
        elif nombre_archivo.endswith('.html'):
            contenido = leer_archivo_html(nombre_archivo)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, contenido)
        else:
            print("Formato de archivo no compatible.")
    except FileNotFoundError:
        print("El archivo especificado no se encontró.")

# Función para leer archivos ODT y extraer su contenido
def leer_archivo_odt(nombre_archivo):
    doc = load(nombre_archivo)
    contenido = ''
    for para in doc.getElementsByType(text.P):
        contenido += teletype.extractText(para) + '\n'
    return contenido

# Función para leer archivos CSV y extraer su contenido
def leer_archivo_csv(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_csv:
        contenido = archivo_csv.read() # Lee el contenido del archivo CSV
    return contenido

# Función para leer archivos HTML y extraer su contenido
def leer_archivo_html(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_html:
        contenido = archivo_html.read() # Lee el contenido del archivo HTML
        soup = BeautifulSoup(contenido, 'html.parser')
        return soup.get_text() # Devuelve el texto extraído del archivo HTML

# Función para seleccionar una porción de texto y agregarla a un archivo JSON
def seleccionar_porcion():
    global nombre_archivo
    contenido = text_box.get("1.0", "end-1c") # Obtiene todo el contenido del cuadro de texto
    inicio = entry_inicio.get()  # Obtiene la cadena de búsqueda ingresada por el usuario

    if nombre_archivo:
        # Verificar si el texto buscado está presente en el contenido
        if inicio in contenido:
            # Encontrar el índice del siguiente salto de línea después del valor de inicio
            index_fin = contenido.find('\n', contenido.find(inicio))

            # Tomar la porción desde el valor de inicio hasta el siguiente salto de línea o hasta el final del texto
            if index_fin != -1:  # Si se encuentra un salto de línea después del valor de inicio
                porcion = contenido[contenido.find(inicio):index_fin]
            else:  # Si no se encuentra un salto de línea, tomar hasta el final del texto
                porcion = contenido[contenido.find(inicio):]

            # Obtener el nombre del archivo actual sin la extensión
            nombre_archivo_sin_extension = os.path.splitext(os.path.basename(nombre_archivo))[0]

            # Obtener el contenido actual del archivo JSON, si existe
            contenido_json = {}
            if os.path.exists('porcion.json'):
                with open('porcion.json', 'r') as f:
                    contenido_json = json.load(f)

            # Verificar si ya existe contenido para el archivo actual en el archivo JSON
            if nombre_archivo_sin_extension not in contenido_json:
                contenido_json[nombre_archivo_sin_extension] = []

            # Agregar la nueva porción al contenido existente para el archivo actual
            contenido_json[nombre_archivo_sin_extension].append(porcion)

            # Guardar el contenido actualizado en el archivo JSON sin codificar en ASCII
            with open('porcion.json', 'w', encoding='utf-8') as f:
                json.dump(contenido_json, f, ensure_ascii=False, indent=4)

            text_box_porcion.delete('1.0', tk.END)
            text_box_porcion.insert(tk.END, porcion)
            
            # Mostrar mensaje informativo al usuario
            messagebox.showinfo("Búsqueda", "El texto se encontró en el archivo y se copió al archivo JSON.")
        else:
            messagebox.showinfo("Búsqueda", "El texto especificado no se encontró en el archivo.")
    else:
        print("Por favor, abre un archivo primero.")

def limpiar_busqueda():
    entry_inicio.delete(0, tk.END) # Borra la entrada de búsqueda
    text_box_porcion.delete('1.0', tk.END)  # Borrar contenido de la caja de texto para la porción

def insertar_en_bd_desde_json():
    conexion.insertar_en_bd_desde_json()

# Crear la ventana principal
root = tk.Tk()
root.title("Seleccionar información de un Archivo")

# Botón para abrir archivo
btn_abrir_archivo = tk.Button(root, text="Abrir Archivo", command=leer_archivo)
btn_abrir_archivo.pack(pady=5)

# Cuadro de texto para mostrar el contenido del archivo seleccionado
text_box = tk.Text(root, height=15, width=50)
text_box.pack(pady=5)

# Etiqueta y entrada para la búsqueda de porciones de texto
lbl_inicio = tk.Label(root, text="Búsqueda:")
lbl_inicio.pack()
entry_inicio = tk.Entry(root)
entry_inicio.pack()

# Botón para limpiar la búsqueda
btn_limpiar_busqueda = tk.Button(root, text="Limpiar Búsqueda", command=limpiar_busqueda)
btn_limpiar_busqueda.pack(pady=5)

# Botón para seleccionar porción
btn_seleccionar_porcion = tk.Button(root, text="Seleccionar Información", command=seleccionar_porcion)
btn_seleccionar_porcion.pack(pady=5)

# Textbox para mostrar porción seleccionada
text_box_porcion = tk.Text(root, height=5, width=50)
text_box_porcion.pack(pady=5)

# Botón para insertar datos en la base de datos desde el archivo JSON
btn_insertar_bd_desde_json = tk.Button(root, text="Insertar en Base de Datos desde JSON", command=insertar_en_bd_desde_json)
btn_insertar_bd_desde_json.pack(pady=5)

# Ejecutar la ventana principal
root.mainloop()