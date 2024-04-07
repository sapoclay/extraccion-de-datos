import conexion
import exportarBD
import mostrar_about
import google_maps
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import docx
import openpyxl
import json
import os
from odf.opendocument import load
from odf import text, teletype
from bs4 import BeautifulSoup
import tkinter.ttk as ttk  # Importa ttk para usar el widget Separator

nombre_archivo = ""

def leer_archivo():
    global nombre_archivo
    nombre_archivo = filedialog.askopenfilename()
    try:
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

def leer_archivo_odt(nombre_archivo):
    doc = load(nombre_archivo)
    contenido = ''
    for para in doc.getElementsByType(text.P):
        contenido += teletype.extractText(para) + '\n'
    return contenido

def leer_archivo_csv(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_csv:
        contenido = archivo_csv.read()
    return contenido

def leer_archivo_html(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_html:
        contenido = archivo_html.read()
        soup = BeautifulSoup(contenido, 'html.parser')
        return soup.get_text()

def seleccionar_porcion():
    global nombre_archivo
    contenido = text_box.get("1.0", "end-1c")
    inicio = entry_inicio.get()

    if not inicio:
        messagebox.showerror("Error", "Es necesario establecer un campo de búsqueda.")
        return

    if nombre_archivo:
        if inicio in contenido:
            index_fin = contenido.find('\n', contenido.find(inicio))
            if index_fin != -1:
                porcion = contenido[contenido.find(inicio):index_fin]
            else:
                porcion = contenido[contenido.find(inicio):]

            nombre_archivo_sin_extension = os.path.splitext(os.path.basename(nombre_archivo))[0]

            contenido_json = {}
            if os.path.exists('porcion.json'):
                with open('porcion.json', 'r') as f:
                    contenido_json = json.load(f)

            if nombre_archivo_sin_extension not in contenido_json:
                contenido_json[nombre_archivo_sin_extension] = []

            contenido_json[nombre_archivo_sin_extension].append(porcion)

            with open('porcion.json', 'w', encoding='utf-8') as f:
                json.dump(contenido_json, f, ensure_ascii=False, indent=4)

            text_box_porcion.delete('1.0', tk.END)
            text_box_porcion.insert(tk.END, porcion)

            messagebox.showinfo("Búsqueda", "El texto se encontró en el archivo y se copió al archivo JSON.")
        else:
            messagebox.showinfo("Búsqueda", "El texto especificado no se encontró en el archivo.")
    else:
        print("Por favor, abre un archivo primero.")

def limpiar_busqueda():
    entry_inicio.delete(0, tk.END)
    text_box_porcion.delete('1.0', tk.END)
    text_box.delete('1.0', tk.END)

def insertar_en_bd_desde_json():
    global nombre_archivo
    contenido = text_box_porcion.get("1.0", "end-1c")

    if not contenido:
        messagebox.showerror("Error", "Primero se debe seleccionar un texto desde un archivo.")
        return

    conexion.insertar_en_bd_desde_json()

ventana_contenido_bd = None

def ver_contenido_bd():
    global ventana_contenido_bd

    try:
        registros = conexion.obtener_contenido_bd()
        if registros:
            if ventana_contenido_bd:
                ventana_contenido_bd.destroy()

            ventana_contenido_bd = tk.Toplevel(root)
            ventana_contenido_bd.title("Contenido de la Base de Datos")
            ventana_contenido_bd.geometry("500x500")

            menu_exportar = tk.Menu(ventana_contenido_bd)
            ventana_contenido_bd.config(menu=menu_exportar)

            submenu_exportar = tk.Menu(menu_exportar, tearoff=0)
            menu_exportar.add_cascade(label="Archivo", menu=submenu_exportar)
            submenu_exportar.add_command(label="Exportar a CSV", command=exportarBD.exportar_csv)
            submenu_exportar.add_command(label="Exportar a PDF", command=exportarBD.exportar_pdf)

            submenu_exportar.add_separator()
            submenu_exportar.add_command(label="Cerrar Ventana", command=ventana_contenido_bd.destroy)

            frame_widgets = tk.Frame(ventana_contenido_bd)
            frame_widgets.pack(fill=tk.BOTH, expand=True)

            scrollbar_y = tk.Scrollbar(frame_widgets, orient="vertical")
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

            inner_frame = tk.Frame(frame_widgets)
            inner_frame.pack(fill=tk.BOTH, expand=True)

            text_box_frame = tk.Text(inner_frame, wrap="word", yscrollcommand=scrollbar_y.set, state="normal")
            text_box_frame.pack(fill="both", expand=True)

            scrollbar_y.config(command=text_box_frame.yview)

            for registro in registros:
                archivo, contenido, notas = registro

                # Insertar el nombre del archivo en negrita
                text_box_frame.insert(tk.END, f"Archivo: {archivo}\n", "bold")
                text_box_frame.tag_configure("bold", font=("Arial", 10, "bold"))

                # Insertar el contenido y las notas
                text_box_frame.insert(tk.END, contenido + "\n")

                if notas is not None:
                    text_box_frame.insert(tk.END, f"Nota: {notas}\n\n")

                # Insertar botón para ver en Google Maps
                if "Coordenadas:" in contenido or "coordenadas:" in contenido:
                    latitud, longitud = google_maps.obtener_coordenadas(contenido)
                    if latitud and longitud:
                        btn_abrir_mapa = tk.Button(inner_frame, text="Ver en Google Maps",
                                                   command=lambda lat=latitud, lon=longitud: google_maps.abrir_google_maps(lat, lon))
                        text_box_frame.window_create(tk.END, window=btn_abrir_mapa)
                        text_box_frame.insert(tk.END, "\n")

                # Insertar botón para ver/añadir nota
                btn_nota = tk.Button(inner_frame, text="Ver/Añadir Nota", command=lambda arch=archivo: abrir_ventana_nota(arch))
                text_box_frame.window_create(tk.END, window=btn_nota)
                text_box_frame.insert(tk.END, "\n")

                # Insertar línea continua como separador
                text_box_frame.insert(tk.END, "-"*50 + "\n\n")

                # Cambiar el cursor a flecha al pasar por encima de los botones
                btn_abrir_mapa.bind("<Enter>", lambda event: btn_abrir_mapa.config(cursor="arrow"))
                btn_abrir_mapa.bind("<Leave>", lambda event: btn_abrir_mapa.config(cursor=""))

                btn_nota.bind("<Enter>", lambda event: btn_nota.config(cursor="arrow"))
                btn_nota.bind("<Leave>", lambda event: btn_nota.config(cursor=""))

            # Deshabilitar la edición del Text
            text_box_frame.config(state="disabled")

        else:
            messagebox.showinfo("Información", "No se encontraron registros en la base de datos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al obtener el contenido de la base de datos: {str(e)}")





def abrir_ventana_nota(archivo):
    def ajustar_tamano(event):
        text_nota.config(width=ventana_nota.winfo_width() // 10, height=ventana_nota.winfo_height() // 25)

    def guardar_nota():
        nota = text_nota.get("1.0", tk.END).strip()
        if nota != "":
            conexion.guardar_nota_en_bd(archivo, nota)
            ventana_nota.destroy()
            if hasattr(root, 'ventana_contenido_bd') and tk.Toplevel in root.ventana_contenido_bd.__class__.__mro__:
                root.ventana_contenido_bd.destroy()
            ver_contenido_bd()
        else:
            if messagebox.askokcancel("Advertencia", "¿Estás seguro de guardar una nota vacía?"):
                conexion.guardar_nota_en_bd(archivo, nota)
                ventana_nota.destroy()
                if hasattr(root, 'ventana_contenido_bd') and tk.Toplevel in root.ventana_contenido_bd.__class__.__mro__:
                    root.ventana_contenido_bd.destroy()
                ver_contenido_bd()

    nota_existente = conexion.obtener_nota_desde_bd(archivo)

    ventana_nota = tk.Toplevel(root)
    ventana_nota.title(f"Nota para {archivo}")
    ventana_nota.geometry("400x300")  # Establecer tamaño específico

    label_nota = tk.Label(ventana_nota, text="Nota:")
    label_nota.pack()

    text_nota = tk.Text(ventana_nota, wrap="word")
    text_nota.pack(fill="both", expand=True)

    ventana_nota.bind("<Configure>", ajustar_tamano)

    if nota_existente:
        text_nota.insert(tk.END, nota_existente)

    btn_guardar_nota = tk.Button(ventana_nota, text="Guardar Nota", command=guardar_nota)
    btn_guardar_nota.pack(pady=5)



def salir_del_programa():
    root.quit()

root = tk.Tk()
root.title("Seleccionar información de un Archivo")

menu_principal = tk.Menu(root)
root.config(menu=menu_principal,  borderwidth=0)

menu_archivo = tk.Menu(menu_principal, tearoff=False, border=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir Archivo", command=leer_archivo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)

menu_about = tk.Menu(menu_principal, tearoff=False)
menu_principal.add_cascade(label="About", menu=menu_about)
menu_about.add_command(label="Acerca de", command=mostrar_about.mostrar_about)

text_box = tk.Text(root, height=20, width=50) 
text_box.pack(pady=5, fill=tk.BOTH, expand=True)

lbl_inicio = tk.Label(root, text="Búsqueda:")
lbl_inicio.pack()
entry_inicio = tk.Entry(root, width=30)
entry_inicio.pack()

btn_limpiar_busqueda = tk.Button(root, text="Limpiar", command=limpiar_busqueda)
btn_limpiar_busqueda.pack(pady=5)

btn_seleccionar_porcion = tk.Button(root, text="Seleccionar Información", command=seleccionar_porcion)
btn_seleccionar_porcion.pack(pady=5)

text_box_porcion = tk.Text(root, height=5, width=50)
text_box_porcion.pack(pady=5, fill=tk.BOTH, expand=True)

btn_insertar_bd_desde_json = tk.Button(root, text="Insertar en Base de Datos", command=insertar_en_bd_desde_json)
btn_insertar_bd_desde_json.pack(pady=5)

btn_ver_contenido_bd = tk.Button(root, text="Ver Contenido de la Base de Datos", command=ver_contenido_bd)
btn_ver_contenido_bd.pack(pady=5)

root.mainloop()