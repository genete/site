import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def es_sentencia_dml(linea):
    """
    Función para identificar si una línea de texto es una sentencia SQL DML (Data Manipulation Language).
    Estas sentencias son las que modifican datos: INSERT INTO, UPDATE, DELETE FROM.
    
    Retorna True si la línea inicia con alguna de estas sentencias, ignorando espacios y mayúsculas/minúsculas.
    """
    sentencias_dml = (
        "INSERT INTO",
        "UPDATE",
        "DELETE FROM"
    )
    linea_mayus = linea.strip().upper()  # Normalizamos para comparar
    return any(linea_mayus.startswith(s) for s in sentencias_dml)

def main():
    """
    Función principal para la ejecución del script.
    Abre un diálogo para elegir el archivo 'bdat.script', luego procesa su contenido línea a línea
    y elimina las líneas que son sentencias DML para solo conservar la estructura, definiciones y configuraciones.
    Finalmente, abre otro diálogo para que el usuario elija el directorio donde quiere guardar
    el archivo resultante 'bdat.script.txt'.
    """
    # Ocultamos la ventana principal de Tkinter porque solo queremos los diálogos
    Tk().withdraw()
    
    # Diálogo para seleccionar archivo bdat.script
    archivo_path = askopenfilename(title="Selecciona el archivo bdat.script")
    
    # Si el usuario cancela o no elige archivo, terminamos la ejecución
    if not archivo_path:
        print("No se seleccionó ningún archivo.")
        return

    # Abrimos el archivo en modo lectura binaria para asegurar una buena lectura de bytes
    with open(archivo_path, "rb") as f:
        contenido = f.read()

    # Decodificamos el contenido a texto UTF-8
    # Usamos errors='replace' para sustituir caracteres inválidos y evitar errores de decodificación
    texto = contenido.decode("utf-8", errors="replace")
    
    # Dividimos el texto en líneas manteniendo los saltos de línea para que el archivo de salida tenga formato correcto
    lineas = texto.splitlines(keepends=True)

    # Filtramos las líneas, conservando solo las que NO sean sentencias DML
    lineas_filtradas = [linea for linea in lineas if not es_sentencia_dml(linea)]

    # Diálogo para seleccionar directorio donde guardar el archivo limpio
    carpeta_salida = askdirectory(title="Selecciona el directorio para guardar bdat.script.txt")
    
    # Si el usuario cancela el diálogo de selección de directorio, terminamos
    if not carpeta_salida:
        print("No se seleccionó ningún directorio de salida.")
        return
    
    # Construimos la ruta completa del nuevo archivo en el directorio elegido
    nuevo_archivo_path = os.path.join(carpeta_salida, "bdat.script.txt")

    # Guardamos las líneas filtradas en el archivo nuevo con codificación UTF-8
    with open(nuevo_archivo_path, "w", encoding="utf-8") as f:
        f.writelines(lineas_filtradas)

    # Mensaje de confirmación
    print(f"Archivo de estructura generado en: {nuevo_archivo_path}")

# Punto de entrada del script para ejecución directa
if __name__ == "__main__":
    main()
