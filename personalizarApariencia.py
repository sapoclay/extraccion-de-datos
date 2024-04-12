import tkinter as tk
from tkinter import font, colorchooser

class PersonalizarApariencia:
    def __init__(self, ventana_principal, caja_texto_archivo, caja_texto_copiado, lbl_inicio, frame_botones_1, frame_botones_2, btn_limpiar_busqueda, btn_seleccionar_porcion, btn_insertar_bd_desde_json, btn_ver_contenido_bd, entry_inicio):
        self.ventana_principal = ventana_principal
        self.caja_texto_archivo = caja_texto_archivo
        self.caja_texto_copiado = caja_texto_copiado
        self.frame_botones_1 = frame_botones_1
        self.frame_botones_2 = frame_botones_2
        self.btn_limpiar_busqueda = btn_limpiar_busqueda
        self.btn_seleccionar_porcion = btn_seleccionar_porcion
        self.btn_insertar_bd_desde_json = btn_insertar_bd_desde_json
        self.btn_ver_contenido_bd = btn_ver_contenido_bd
        self.entry_inicio = entry_inicio
        self.lbl_inicio = lbl_inicio
        self.opciones_abiertas = False
        
        self.ventana_personalizacion = tk.Toplevel(self.ventana_principal)
        self.ventana_personalizacion.withdraw()  # Ocultar la ventana de personalización al inicio
        self.ventana_personalizacion.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_personalizacion)  # Configurar el cierre de la ventana

        self.ventana_personalizacion.title("Personalización de la Apariencia")

        self.tamano_fuente_var = tk.IntVar()
        self.tamano_fuente_var.set(12)

        self.tipo_fuente_var = tk.StringVar()
        self.tipo_fuente_var.set("Arial")

        # Controles de personalización
        frame_personalizacion = tk.Frame(self.ventana_personalizacion)

        lbl_tamano_fuente = tk.Label(frame_personalizacion, text="Tamaño de Fuente:")
        lbl_tamano_fuente.grid(row=0, column=0, padx=5, pady=5)

        scale_tamano_fuente = tk.Scale(frame_personalizacion, from_=8, to=24, orient="horizontal", variable=self.tamano_fuente_var, command=self.cambiar_tamano_fuente)
        scale_tamano_fuente.grid(row=0, column=1, padx=5, pady=5)

        btn_color_fondo = tk.Button(frame_personalizacion, text="Color de Fondo", command=self.cambiar_color_fondo)
        btn_color_fondo.grid(row=1, column=0, columnspan=2, pady=5)

        lbl_tipo_fuente = tk.Label(frame_personalizacion, text="Tipo de Fuente:")
        lbl_tipo_fuente.grid(row=2, column=0, padx=5, pady=5)

        option_menu_tipo_fuente = tk.OptionMenu(frame_personalizacion, self.tipo_fuente_var, "Arial", "Times New Roman", "Courier New", command=self.cambiar_tipo_fuente)
        option_menu_tipo_fuente.grid(row=2, column=1, padx=5, pady=5)

        frame_personalizacion.pack(padx=10, pady=10)

        # Ajustar tamaño mínimo de la ventana de personalización
        self.ventana_personalizacion.minsize(300, 150)

    def cambiar_tamano_fuente(self, tamano):
        familia_actual, tamano_actual = self.obtener_fuente_actual()
        nueva_fuente = (familia_actual, tamano)
        self.ventana_principal.option_add("*Font", nueva_fuente)
        self.actualizar_fuente_texto()

    def cambiar_color_fondo(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.ventana_principal.config(bg=color)
            self.lbl_inicio.config(bg=color)
            self.frame_botones_1.config(bg=color)
            self.frame_botones_2.config(bg=color)

    def cambiar_tipo_fuente(self, *args):
        familia_nueva = self.tipo_fuente_var.get()
        familia_actual, tamano_actual = self.obtener_fuente_actual()
        nueva_fuente = (familia_nueva, tamano_actual)
        self.ventana_principal.option_add("*Font", nueva_fuente)
        self.actualizar_fuente_texto()

    def obtener_fuente_actual(self):
        fuente = self.ventana_principal.option_get("font", "Text")
        if fuente:
            return fuente.split()
        else:
            return ("Arial", 12)

    def actualizar_fuente_texto(self):
        nueva_fuente = self.obtener_fuente_personalizada()
        if nueva_fuente:
            self.caja_texto_archivo.config(font=nueva_fuente)
            self.caja_texto_copiado.config(font=nueva_fuente)
            self.lbl_inicio.config(font=nueva_fuente)
            self.btn_limpiar_busqueda.config(font=nueva_fuente)
            self.btn_seleccionar_porcion.config(font=nueva_fuente)
            self.btn_insertar_bd_desde_json.config(font=nueva_fuente)
            self.btn_ver_contenido_bd.config(font=nueva_fuente)
            self.entry_inicio.config(font=nueva_fuente)

    def obtener_fuente_personalizada(self):
        familia = self.tipo_fuente_var.get()
        tamano = self.tamano_fuente_var.get()
        return (familia, tamano)

    def abrir_ventana_personalizacion(self):
        if not self.opciones_abiertas:
            self.opciones_abiertas = True
            self.ventana_personalizacion.deiconify()  # Mostrar la ventana de personalización

    def cerrar_ventana_personalizacion(self):
        if self.opciones_abiertas:
            self.opciones_abiertas = False
            self.ventana_personalizacion.withdraw()  # Ocultar la ventana de personalización

if __name__ == "__main__":
    ventana_principal = tk.Tk()

    # Crear cajas de texto con barras de desplazamiento
    scrollbar_vertical = tk.Scrollbar(ventana_principal, orient="vertical")
    scrollbar_horizontal = tk.Scrollbar(ventana_principal, orient="horizontal")
    scrollbar_vertical.pack(side="right", fill="y")
    scrollbar_horizontal.pack(side="bottom", fill="x")

    caja_texto_archivo = tk.Text(ventana_principal, font=("Arial", 12), wrap="word", yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
    caja_texto_archivo.pack(fill="both", expand=True)
    scrollbar_vertical.config(command=caja_texto_archivo.yview)
    scrollbar_horizontal.config(command=caja_texto_archivo.xview)

    caja_texto_copiado = tk.Text(ventana_principal, font=("Arial", 12), wrap="word")
    caja_texto_copiado.pack(fill="both", expand=True)

    # Crear una instancia de PersonalizarApariencia
    personalizar_apariencia = PersonalizarApariencia(ventana_principal, caja_texto_archivo, caja_texto_copiado)

    # Configurar el menú de la ventana principal
    menu_principal = tk.Menu(ventana_principal)
    ventana_principal.config(menu=menu_principal)
    menu_personalizar = tk.Menu(menu_principal)
    menu_principal.add_cascade(label="Personalizar Apariencia", menu=menu_personalizar)
    menu_personalizar.add_command(label="Abrir/Ocultar", command=personalizar_apariencia.abrir_ventana_personalizacion)

    ventana_principal.mainloop()