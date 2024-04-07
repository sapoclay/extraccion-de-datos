# Extracción de datos de archivos e inserción en base de datos MySQL

Este pequeño scritp lo he retomado para Walterio (para eso que tú querías hacer). Realmente recuerdo poco qué era lo que querías hacer, pero me suena que te interesaba extraer datos concretos de diferentes tipos de archivos.  Este pequeño script Python
hace justamente eso, funciona con archivos: txt, pdf, docx, xlsx, odt, csv y html (lo del OCR todavía no lo tengo implementado, por falta de tiempo). Permite que el usuario cargue un archivo de estos formatos comentados, y realice una búsqueda 
dentro del archivo en cuestión. Si encuentra lo que busca, se va a seleccionar todo, desde el término de búsqueda utilizado por el usuario (incluido) hasta el primer salto de línea que encuentre. Si el documento no cuenta con saltos de línea al final 
de cada línea, esto no funcionará. Además el script se va a quedar con la primera aparición del texto buscado, ya que esto se supone que debería funcionar con notas o albaranes donde la info no se repita.

![copiado](https://github.com/sapoclay/extraccion-de-datos/assets/6242827/9d304185-cba4-45e0-bbf7-1e352bea3029)

Una vez encontrado el texto buscado, aparecerá un aviso de que el texto se va a guardar dentro de un archivo .json llamado porcion. Este archivo se va a generar en la misma carpeta en la que ejecutes el archivo python. 

![extraccion-info](https://github.com/sapoclay/extraccion-de-datos/assets/6242827/e6a8c4a5-b7a5-4880-9d7e-0ddf38a38a32)

En el momento que quieras escribir los datos en la base de datos, solo es necesario pulsar sobre el botón "Insertar en Base de Datos desde JSON". Los datos de la conexión a la base de datos habrá que definirlos dentro del archivo conexion.py. En caso
de que la tabla (llamado datos) no exista, esta se creará automáticamente. Después se añadirán los datos del archivo json en un registro en la base de datos. Cada registro se va a diferenciar según el nombre del archivo cargado en el programa Python. 
En caso de que añadamos el texto de un archivo, después el de otro, y volvamos a abrir el primero de los archivos y añadamos más texto a la base de datos, se actualizará el registro de datos del primer archivo, por lo que no deberían generarse duplicados en la base de datos.

## 1 Actualización

- He añadido un botón que muestra los datos guardados en la base de datos. Cada registro es independendiente del resto, y dentro del registro (recordemos que están separados por el nombre del archivo desde el que se toman los datos) en caso de que alguno de los datos guardados sea Coordenadas: o coordenadas: se va a generar un botón para abrir las coordenadas en google maps. En caso de que no encuentre entre los datos ninguna de esas referencias a las coordenadas, no se mostrará el botón para ver en google maps.
- Además, a cada registro de la base de datos, he añadido un nuevo botón para poder dejar notas relacionadas con el registro en cuestión al que esté asociada la nota. En caso de que la nota ya esté creada, al pulsar sobre este botón permitirá leerla.
- He corregido también la capacidad de estirar o encoger los cuadros de texto en los que se muestra el archivo sobre el que va a trabajar el usuario, y eso también se aplica a los cuadros de texto que muestra el contenido de la base de datos.

## 2 Actualización

- Se ha corregido la respuesta de script cuando se pulsa alguno de los botones sin haber abierto un documento de los permitidos. Ahora muestra un error mediante ventana emergente.
- También se añadió un menú superior. Ahora para abrir un documento hay que ir a la opción Archivo. Se elimino el botón que había en la pantalla principal del script para abrir un archivo.
- Como opciones de la opción Archivo, se ha añadido la posibilidad de exportar la base de datos como archivo .CSV y .PDF. Se guardarán los tres campos que tiene la base de datos ("archivo","contenido" y "notas"). A la opción Archivo, también le añadí una opción para cerrar el programa.
- Las funciones para exportar la BD a CSV y PDF se han movido a un archivo independiente.
- La función para mostrar la ventana del about, también se ha movido a un archivo independiente.
- Las funciones para abrir las coordenadas en Google Maps y para separar los datos de las coordenadas de todos los datos recuperados de la BD se han movido a un archivo independiente.
- Además en el menú superior, ahora tiene una opción About (no sirve de nada, pero ahí la está).
- Se ha corregido el problema que aparecía cuando se guardaban unas coordenadas en la base de datos y se intentaban abrir en Google Maps, pues si había más registros guardados después de las coordenadas estos se cargaban como parte de la URL en el mapa, por lo que no realizaba su función.
- También se ha corregido el error que aparecía al eliminar una nota ya existente, pues el script no permitía eliminar una nota y dejar este campo vacío. Ahora ya se puede eliminar el contenido de la nota asociada a uno de los registros.
- Se ha solucionado el problema de que la ventana que muestra el contenido de la base de datos, se actualizaba automáticamente cuando se añadía o se eliminaba una nota.

## 3 Actutalización

- Movidas las opciones de exportación a CSV y PDF al menú de la ventana en la que se consultan los datos guardados en la base de datos.
- Ahora los cuadros en los que se muestran los datos guardados en la base de datos, son solo de lectura.
- Modificado el comportamiento de la ventana emergente para añadir notas.
- Se han modificado el cómo se entregan los resultados guardados en la base de datos.
## Dependencias
Las dependencias necesarias para que funcione este proyecto son:

- Conexión a la base de datos en el archivo conexion.py: 
    - mysql-connector-python: Este módulo te permite conectar tu aplicación Python a una base de datos MySQL. Puedes instalarlo usando pip:
    ```
    pip3 install mysql-connector-python 
    ```
    - json: Este módulo es parte de la biblioteca estándar de Python y generalmente no requiere instalación adicional.
    - tkinter.messagebox: Este módulo es parte de la biblioteca estándar de Python y generalmente no requiere instalación adicional.
    - webbrowser: Este módulo es parte de la biblioteca estándar de Python y generalmente no requiere instalación adicional.

- Interfaz gráfica (Tkinter):
    - En sistemas basados en Debian/Ubuntu: 
    ```
    sudo apt-get install python3-tk
    ```
    - En sistemas basados en Fedora: 
    ```
    sudo dnf install python3-tkinter
    ```
    - En sistemas basados en Windows y macOS, no se requiere ninguna instalación adicional, ya que Tkinter generalmente se instala junto con Python.

- Imágenes (Pillow):
    - Ejecuta: 
    ```
    pip3 install Pillow
    ``` 
    para instalar la biblioteca Pillow. Esto solo vale para mostrar la imagen del menú about. Pero quizás habría que pensar en permitir trabajar con imágenes al este script.

- Manipulación de archivos de diferentes formatos:
    - Para PyPDF2: 
    ```
    pip3 install PyPDF2
    ```
    - Para docx: 
    ```
    pip3 install python-docx
    ```
    - Para openpyxl: 
    ```
    pip3 install openpyxl
    ```
    - Para BeautifulSoup: 
    ```
    pip3 install beautifulsoup4
    ```

- Exportar a CSV y PDF:
    - Para CSV (creo que estaba incluido en la biblioteca estándar de Python, por lo que no debería requerir instalación adicional)
    - Para FPDF: 
    ```
    pip3 install fpdf
    ```

Asegúrate de tener Python 3 y pip3 instalados en tu sistema antes de ejecutar los comandos de instalación mencionados anteriormente. Puedes encontrar más información sobre cómo instalar Python3 y pip3 en la documentación oficial de Python: https://www.python.org/doc/.

Asegúrate de tener instaladas todas estas dependencias en tu entorno de Python para que el proyecto funcione correctamente. 

Este script lo he generado utilizando Python 3.10.12 en Ubuntu. Pero me imagino que si cumples las dependencias necesarias que mencioné antes, funcionará en cualquier sistema. En proximos días, intentaré subir un .EXE para un uso más sencillo en Windows (pero primero tendré que instalarme uno...)
