# Extracción de datos de archivos e inserción en base de datos MySQL

Este pequeño scritp lo he retomado para Walterio (para eso que tú querías hacer). Realmente recuerdo poco qué era lo que querías hacer, pero me suena que te interesaba extraer datos concretos de diferentes tipos de archivos.  Este pequeño script Python
hace justamente eso, funciona con archivos: txt, pdf, docx, xlsx, odt, csv y html (lo del OCR todavía no lo tengo implementado, por falta de tiempo). Permite que el usuario cargue un archivo de estos formatos comentados, y realice una búsqueda 
dentro del archivo en cuestión. Si encuentra lo que busca, se va a seleccionar todo, desde el término de búsqueda utilizado por el usuario (incluido) hasta el primer salto de línea que encuentre. Si el documento no cuenta con saltos de línea al final 
de cada línea, esto no funcionará. Además el script se va a quedar con la primera aparición del texto buscado, ya que esto se supone que debería funcionar con notas o albaranes donde la info no se repita.

![copiado](https://github.com/sapoclay/extraccion-de-datos/assets/6242827/9d304185-cba4-45e0-bbf7-1e352bea3029)

Una vez encontrado el texto buscado, aparecerá un aviso de que el texto se va a guardar dentro de un archivo .json llamado porcion. Este archivo se va a generar en la misma carpeta en la que ejecutes el archivo python. 

![extraccion-info](https://github.com/sapoclay/extraccion-de-datos/assets/6242827/e6a8c4a5-b7a5-4880-9d7e-0ddf38a38a32)

En el momento que quieras escribir los datos en la base de datos, solo es necesario pulsar sobre el botón "Insertar en Base de Datos desde JSON". Los datos de la conexión a la base de datos habrá que definirlos dentro del archivo conexion.py. En caso
de que la tabla no exista, esta se creará automáticamente. Después se añadirán los datos del archivo json en un registro en la base de datos. Cada regustro se va a diferenciar según el nombre del archivo cargado en el programa Python. 
En caso de que añadamos el texto de un archivo, después el de otro, y volvamos a abrir el primero de los archivos y añadamos más texto a la base de datos, se actualizará el registro de datos del primer archivo, por lo que no deberían generarse duplicados en la base de datos.

También he añadido un botón que muestra los datos guardados en la base de datos. Cada registro es independendiente del resto, y dentro del registro (recordemos que están separados por el nombre del archivo desde el que se toman los datos) en caso de que alguno de los datos guardados sea Coordenadas: o coordenadas: se va a generar un botón para abrir las coordenadas en google maps. En caso de que no encuentre entre los datos ninguna de esas referencias a las coordenadas, no se mostrará el botón para ver en google maps.

Además, a cada registro de la base de datos, he añadido un nuevo botón para poder dejar notas relacionadas con el registro en cuestión al que esté asociada la nota. En caso de que la nota ya esté creada, al pulsar sobre este botón permitirá leerla.

He corregido también la capacidad de estirar o encoger los cuadros de texto en los que se muestra el archivo sobre el que va a trabajar el usuario, y eso también se aplica a los cuadros de texto que muestra el contenido de la base de datos.

## Dependencias
Las dependencias necesarias para que funcione este proyecto son:

- MySQL Connector: Para conectar y comunicarse con la base de datos MySQL.
- tkinter: Para crear la interfaz gráfica de usuario (GUI).
- PyPDF2: Para manejar archivos PDF.
- python-docx: Para trabajar con archivos de Microsoft Word.
- openpyxl: Para interactuar con archivos de Microsoft Excel.
- Beautiful Soup (bs4): Para extraer datos de archivos HTML.
- odfpy: Para trabajar con archivos ODT (Open Document Text).
- json: Para manejar archivos JSON.
- os: Para interactuar con el sistema operativo y manejar rutas de archivo.

Asegúrate de tener instaladas todas estas dependencias en tu entorno de Python para que el proyecto funcione correctamente. Puedes instalarlas usando pip, el gestor de paquetes de Python, ejecutando "pip install nombre_del_paquete".
Este script lo he generado utilizando Python 3.10.12 en Ubuntu. Pero me imagino que si cumples las dependencias necesarias que mencioné antes, funcionará en cualquier sistema.
