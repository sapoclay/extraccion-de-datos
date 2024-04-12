import json
import os
import tkinter as tk
from tkinter import messagebox

# Clase para manejar la selección de una porción de texto en el archivo
class SeleccionAparicion:
    def __init__(self, indices, contenido, inicio, text_box_porcion, text_box, nombre_archivo):
        self.indices = indices
        self.contenido = contenido
        self.inicio = inicio
        self.text_box_porcion = text_box_porcion
        self.seleccion = None
        self.text_box_principal = text_box
        self.nombre_archivo = nombre_archivo
        self.mensaje_abierto = False  # Agregar esta línea para definir el atributo mensaje_abierto
        self.root = tk.Tk()
        self.root.title("Seleccionar Aparición")
        self.root.geometry("400x300")

        lbl_mensaje = tk.Label(self.root, text="Búsquedas encontradas. Selecciona una", fg="blue", font=("Arial", 10, "bold"))
        lbl_mensaje.pack(pady=(10, 5))

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box_principal = tk.Text(self.frame, wrap="word", yscrollcommand=self.scrollbar.set)
        self.text_box_principal.pack(fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.text_box_principal.yview)

        self.actualizar_texto()

        self.text_box_principal.bind("<Button-1>", self.seleccionar_con_raton)
        self.text_box_principal.bind("<Double-1>", self.seleccionar_doble_clic)
        self.text_box_principal.config(cursor="arrow")

        self.text_box_principal.bind("<Enter>", lambda event: self.text_box_principal.config(cursor="arrow"))
        self.text_box_principal.bind("<Leave>", lambda event: self.text_box_principal.config(cursor=""))


        
    def seleccionar(self, event):
        if self.seleccion is not None:
            index_inicio = self.indices[self.seleccion]
            index_fin = self.contenido.find('\n', index_inicio)
            if index_fin != -1:
                index_fin = index_fin + 1
                porcion = self.contenido[index_inicio:index_fin]

                nombre_archivo_sin_extension = os.path.splitext(os.path.basename(self.nombre_archivo))[0]

                contenido_json = {}
                if os.path.exists('porcion.json'):
                    with open('porcion.json', 'r') as f:
                        contenido_json = json.load(f)

                if nombre_archivo_sin_extension not in contenido_json:
                    contenido_json[nombre_archivo_sin_extension] = []

                contenido_json[nombre_archivo_sin_extension].append(porcion)

                with open('porcion.json', 'w', encoding='utf-8') as f:
                    json.dump(contenido_json, f, ensure_ascii=False, indent=4)

                self.text_box_porcion.delete('1.0', tk.END)
                self.text_box_porcion.insert(tk.END, porcion)

                if self.root:
                    self.root.destroy()

                messagebox.showinfo("Selección", "La porción de texto se guardó en el archivo JSON.")
            else:
                messagebox.showinfo("Selección", "No se pudo obtener la porción de texto.")



    # Función para mostrar un mensaje de confirmación
    def mostrar_mensaje(self):
        self.mensaje_abierto = True
        messagebox.showinfo("Selección", "La porción de texto se guardó en el archivo JSON.")
        self.mensaje_abierto = False

    def mover_arriba(self, event):
        if self.seleccion is None:
            self.seleccion = 0
        elif self.seleccion > 0:
            self.seleccion -= 1
        self.actualizar_texto()

    def mover_abajo(self, event):
        if self.seleccion is None:
            self.seleccion = 0
        elif self.seleccion < len(self.indices) - 1:
            self.seleccion += 1
        self.actualizar_texto()


    def actualizar_texto(self):
        self.text_box_principal.config(state=tk.NORMAL)
        self.text_box_principal.delete('1.0', tk.END)
        for i, indice in enumerate(self.indices):
            fin_linea = self.contenido.find('\n', indice)
            if fin_linea == -1:
                fin_linea = len(self.contenido)
            porcion = self.contenido[indice:fin_linea]
            marcado = "<-- opción seleccionada" if self.seleccion == i else ""
            if self.seleccion == i:
                self.text_box_principal.tag_config("selected", background="yellow", font=("Arial", 10, "bold"))
                self.text_box_principal.insert(tk.END, f"Opción {i + 1}: {porcion} {marcado}\n", "selected")
            else:
                self.text_box_principal.insert(tk.END, f"Opción {i + 1}: {porcion} {marcado}\n")
        self.text_box_principal.config(state=tk.DISABLED)

    def seleccionar_con_raton(self, event):
        index = self.text_box_principal.index(f"@{event.x},{event.y}")
        line_number = int(index.split('.')[0])
        self.seleccion = line_number - 1
        self.actualizar_texto()

    def seleccionar_doble_clic(self, event):
        if not self.mensaje_abierto:
            try:
                self.calcular_altura_linea()
                if self.line_height != 0:
                    y_index = int(event.y / self.line_height)
                    self.text_box_principal.tag_remove("selected", "1.0", tk.END)
                    self.text_box_principal.tag_add("selected", f"{y_index + 1}.0", f"{y_index + 2}.0")
                    self.text_box_principal.mark_set("insert", f"{y_index + 1}.0")
                    self.text_box_principal.see(f"{y_index + 1}.0")
                    self.seleccion = y_index
                    self.actualizar_texto()
                    self.seleccionar(event)
            except tk.TclError:
                pass
            
    def calcular_altura_linea(self, event=None):
        line_info = self.text_box_principal.dlineinfo('1.0')
        if line_info is not None:
            self.line_height = line_info[3]
        else:
            self.line_height = 20