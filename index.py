# Importa la conexión a la BD
import conexion
# Importa la biblioteca tkinter para crear la interfaz gráfica
import tkinter as tk
# Importa la biblioteca para abrir el navegador web
import webbrowser

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

# Función para mostrar el contenido de la base de datos
def ver_contenido_bd():
    try:
        registros = conexion.obtener_contenido_bd()
        if registros:
            ventana = tk.Toplevel(root)
            ventana.title("Contenido de la Base de Datos")

            # Crear una barra de desplazamiento vertical para la ventana principal
            scrollbar = tk.Scrollbar(ventana)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            for archivo, contenido in registros:
                # Cuadro de texto para mostrar el contenido de cada archivo
                text_box_bd = tk.Text(ventana, width=50)

                # Contar el número de líneas en el contenido y ajustar la altura
                num_lineas = contenido.count('\n') + 3
                text_box_bd.config(height=num_lineas)

                text_box_bd.pack(pady=5, fill=tk.BOTH, expand=True)  # Rellenar la ventana y expandirse

                # Insertar contenido
                text_box_bd.insert(tk.END, f"Archivo: {archivo}\nContenido: {contenido}\n\n")

                # Verificar si el contenido contiene coordenadas
                if "Coordenadas:" in contenido or "coordenadas:" in contenido:
                    # Obtener las coordenadas
                    latitud, longitud = conexion.obtener_coordenadas(contenido)
                    # Mostrar el botón solo si se encuentran coordenadas
                    if latitud and longitud:
                        btn_abrir_mapa = tk.Button(ventana, text="Ver Coordenadas en Google Maps",
                                                   command=lambda lat=latitud, lon=longitud: conexion.abrir_google_maps(lat, lon))
                        btn_abrir_mapa.pack(pady=5)

                # Botón para ver/añadir nota
                btn_nota = tk.Button(ventana, text="Ver/Añadir Nota", command=lambda arch=archivo: abrir_ventana_nota(arch))
                btn_nota.pack(pady=5)

                # Configurar la barra de desplazamiento para que se desplace con el texto
                text_box_bd.config(yscrollcommand=scrollbar.set)

            # Configurar la barra de desplazamiento para que se mueva con el texto
            scrollbar.config(command=text_box_bd.yview)

            # Configurar el tamaño de la ventana para que se ajuste automáticamente al contenido
            ventana.update_idletasks()  # Actualizar la ventana para obtener el tamaño correcto
            ventana.geometry(f"{ventana.winfo_reqwidth()}x{ventana.winfo_reqheight()}")

            ventana.mainloop()
        else:
            messagebox.showinfo("Información", "No se encontraron registros en la base de datos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al obtener el contenido de la base de datos: {str(e)}")


def obtener_coordenadas(contenido):
    # Dividir el contenido en líneas
    lineas = contenido.split('\n')
    for linea in lineas:
        # Buscar la línea que contiene las coordenadas
        if "Coordenadas:" in linea or "coordenadas:" in linea:
            # Dividir la línea en partes usando ':'
            partes = linea.split(':')
            if len(partes) == 2:  # Verificar si hay dos partes separadas por ':'
                # Obtener las coordenadas de latitud y longitud
                coordenadas = partes[1].strip()
                if ',' in coordenadas:
                    latitud, longitud = coordenadas.split(',')
                    return latitud.strip(), longitud.strip()
    return None, None  # Devolver None si no se encuentran coordenadas


# Función para abrir la ventana de agregar nota
def abrir_ventana_nota(archivo):
    # Función para guardar la nota en la base de datos
    def guardar_nota():
        nota = text_nota.get("1.0", tk.END).strip()
        if nota:
            # Guardar la nota en la base de datos asociada al archivo
            conexion.guardar_nota_en_bd(archivo, nota)
            ventana_nota.destroy()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una nota.")

    # Verificar si ya existe una nota asociada al archivo en la base de datos
    nota_existente = conexion.obtener_nota_desde_bd(archivo)

    # Crear la ventana de agregar nota
    ventana_nota = tk.Toplevel(root)
    ventana_nota.title("Agregar Nota")

    # Etiqueta y cuadro de texto para ingresar la nota
    label_nota = tk.Label(ventana_nota, text="Nota:")
    label_nota.pack()

    text_nota = tk.Text(ventana_nota, height=5, width=50)
    text_nota.pack()

    if nota_existente:
        text_nota.insert(tk.END, nota_existente)

    # Botón para guardar la nota
    btn_guardar_nota = tk.Button(ventana_nota, text="Guardar Nota", command=guardar_nota)
    btn_guardar_nota.pack(pady=5)




# Crear la ventana principal
root = tk.Tk()
root.title("Seleccionar información de un Archivo")

# Botón para abrir archivo
btn_abrir_archivo = tk.Button(root, text="Abrir Archivo", command=leer_archivo)
btn_abrir_archivo.pack(pady=5)

# Cuadro de texto para mostrar el contenido del archivo seleccionado
text_box = tk.Text(root, height=20, width=50) 
text_box.pack(pady=5, fill=tk.BOTH, expand=True)


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
text_box_porcion.pack(pady=5, fill=tk.BOTH, expand=True)

# Botón para insertar datos en la base de datos desde el archivo JSON
btn_insertar_bd_desde_json = tk.Button(root, text="Insertar en Base de Datos desde JSON", command=insertar_en_bd_desde_json)
btn_insertar_bd_desde_json.pack(pady=5)

# Botón para ver el contenido de la base de datos
btn_ver_contenido_bd = tk.Button(root, text="Ver Contenido de la Base de Datos", command=ver_contenido_bd)
btn_ver_contenido_bd.pack(pady=5)

# Ejecutar la ventana principal
root.mainloop()