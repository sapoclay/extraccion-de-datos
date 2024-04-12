# Importa módulos necesarios para exportar la base de datos a pdf y csv
import csv
from fpdf import FPDF  # fpdf usando pip para utilizarlo
# Importa la conexión a la BD
import conexion

# Importa módulos específicos de tkinter para diálogos de archivo y mensajes emergentes
from tkinter import filedialog, messagebox


# Función para exportar la base de datos a un archivo CSV
def exportar_csv():
    try:
        # Obtener el contenido de la base de datos
        registros = conexion.obtener_contenido_bd()

        # Abrir un cuadro de diálogo para guardar el archivo CSV
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if nombre_archivo:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
                # Crear el escritor CSV
                csv_writer = csv.writer(archivo_csv)

                # Escribir los encabezados
                csv_writer.writerow(['Archivo', 'Contenido', 'Notas'])

                # Escribir los registros en el archivo CSV
                for registro in registros:
                    csv_writer.writerow(registro)

            messagebox.showinfo("Exportación exitosa", "La base de datos se exportó correctamente a un archivo CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar la base de datos a CSV: {str(e)}")

# Función para exportar la base de datos a un archivo PDF
def exportar_pdf():
    try:
        # Obtener el contenido de la base de datos
        registros = conexion.obtener_contenido_bd()

        # Abrir un cuadro de diálogo para guardar el archivo PDF
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if nombre_archivo:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Escribir los registros en el archivo PDF
            for i, registro in enumerate(registros):
                archivo = registro[0] if len(registro) > 0 else ''
                contenido = registro[1] if len(registro) > 1 else ''
                notas = registro[2] if len(registro) > 2 else ''

                # Escribir el archivo
                pdf.cell(0, 10, f"Archivo: {archivo}", ln=True)

                # Escribir el contenido
                pdf.multi_cell(0, 10, f"Contenido: {contenido}")

                # Escribir las notas
                pdf.multi_cell(0, 10, f"Notas: {notas}")

                # Agregar una línea horizontal para separar los registros, excepto en el último
                if i < len(registros) - 1:
                    pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())

            pdf.output(nombre_archivo)
            messagebox.showinfo("Exportación exitosa", "La base de datos se exportó correctamente a un archivo PDF.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar la base de datos a PDF: {str(e)}")

def exportar_contenido_html(registros, nombre_archivo):
    try:
        contenido_html = "<!DOCTYPE html><html><head><title>Contenido de la Base de Datos</title></head><body>"
        for registro in registros:
            archivo, contenido, notas = registro
            contenido_html += f"<h3>Archivo: {archivo}</h3>"
            contenido_html += f"<p>{contenido}</p>"
            if notas is not None:
                contenido_html += f"<p><h4>Nota:</h4> {notas}</p>"
            contenido_html += "<hr>"
        contenido_html += "</body></html>"

        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_html)

        messagebox.showinfo("Exportación exitosa", f"El contenido se exportó correctamente a '{nombre_archivo}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar el contenido a HTML: {str(e)}")