
# Importamos PIL para la imagen
from PIL import Image, ImageTk
import requests
from io import BytesIO
# Importa la biblioteca tkinter para crear la interfaz gráfica
import tkinter as tk

def mostrar_about():
    # Crear la ventana About
    ventana_about = tk.Toplevel()
    ventana_about.title("Acerca de")

   # Descargar la imagen desde la URL
    url_imagen = "https://entreunosyceros.net/wp-content/uploads/2023/07/entreunosyceros.net-logo-150x150-2.png"
    response = requests.get(url_imagen)
    imagen_data = response.content

    # Convertir la imagen descargada a formato compatible con tkinter
    imagen = Image.open(BytesIO(imagen_data))
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Mostrar la imagen en un widget Label
    label_imagen = tk.Label(ventana_about, image=imagen_tk)
    label_imagen.image = imagen_tk  # Guardar una referencia para evitar que la imagen sea eliminada por el recolector de basura
    label_imagen.pack(pady=10, padx=(0, 30), side="right")
    
    # Agregar texto informativo
    texto = """
    Extractor de datos\n
    Autor: entreunosyceros
    Fecha de creación: Abril 2024
    Versión: 0.9
    Lenguaje: Python 3 y MySQL
    Contacto: admin@entreunosyceros.net
    Licencia: GPL (General Public License)
    Más información y actualizaciones en:\n
    https://github.com/sapoclay/extraccion-de-datos
    """

    label_info = tk.Label(ventana_about, text=texto, justify="left")
    label_info.pack(padx=20, pady=10)

 