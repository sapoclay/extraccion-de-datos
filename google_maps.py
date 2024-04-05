import webbrowser
import tkinter.messagebox as messagebox

def abrir_google_maps(latitud, longitud):
    try:
        # Extraer solo las coordenadas del texto
        coordenadas = f"{latitud},{longitud}"
        # Construir la URL de Google Maps solo con las coordenadas
        url = f"https://www.google.com/maps/search/?api=1&query={coordenadas}"
        # Abrir la URL en el navegador web predeterminado
        webbrowser.open_new(url)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al abrir Google Maps: {str(e)}")
        
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