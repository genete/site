import os

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
    linea_mayus = linea.strip().upper()
    return any(linea_mayus.startswith(s) for s in sentencias_dml)

def main():
    """
    Función principal que procesa el archivo bdat.script.temp generado desde DBeaver,
    elimina las sentencias DML y genera bdat.script.txt limpio.
    
    PASO PREVIO: Ejecutar en DBeaver:
        SCRIPT 'W:/BDDATLIBRE/desarrollo/fuentesIA/bdat.script.temp';
    """
    # Rutas fijas según la estructura del proyecto
    base_path = "W:/BDDATLIBRE/desarrollo"
    fuentes_ia_path = os.path.join(base_path, "fuentesIA")
    
    # Archivos de entrada y salida
    script_temp_path = os.path.join(fuentes_ia_path, "bdat.script.temp")
    output_path = os.path.join(fuentes_ia_path, "bdat.script.txt")
    
    print("=" * 70)
    print("LIMPIADOR DE SCRIPT HSQLDB - Versión 4")
    print("=" * 70)
    print("\nPASO PREVIO: Ejecuta en DBeaver:")
    print("  SCRIPT 'W:/BDDATLIBRE/desarrollo/fuentesIA/bdat.script.temp';")
    print("\nLuego ejecuta este script Python.\n")
    print("=" * 70)
    
    # Verificar que existe el archivo de entrada
    if not os.path.exists(script_temp_path):
        print(f"\nERROR: No se encuentra el archivo:")
        print(f"   {script_temp_path}")
        print(f"\nSolucion:")
        print(f"   1. Abre DBeaver y conectate a la base de datos")
        print(f"   2. Ejecuta: SCRIPT 'W:/BDDATLIBRE/desarrollo/fuentesIA/bdat.script.temp';")
        print(f"   3. Vuelve a ejecutar este script Python")
        return
    
    print(f"\n[OK] Archivo de entrada encontrado: {script_temp_path}")
    
    # Leer el archivo temporal
    print(f"[...] Leyendo archivo...")
    with open(script_temp_path, "rb") as f:
        contenido = f.read()
    
    # Decodificar a texto UTF-8
    texto = contenido.decode("utf-8", errors="replace")
    
    # Dividir en líneas manteniendo los saltos de línea
    lineas = texto.splitlines(keepends=True)
    
    print(f"[OK] Archivo leido: {len(lineas)} lineas")
    
    # Filtrar las líneas que NO sean sentencias DML
    print(f"[...] Filtrando sentencias DML (INSERT, UPDATE, DELETE)...")
    lineas_filtradas = [linea for linea in lineas if not es_sentencia_dml(linea)]
    
    lineas_eliminadas = len(lineas) - len(lineas_filtradas)
    print(f"[OK] Filtrado completado: {lineas_eliminadas} lineas eliminadas")
    
    # Guardar en fuentesIA/bdat.script.txt
    print(f"[...] Guardando archivo limpio...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lineas_filtradas)
    
    print(f"[OK] Archivo guardado: {output_path}")
    
    # Eliminar el archivo temporal
    print(f"[...] Eliminando archivo temporal...")
    try:
        os.remove(script_temp_path)
        print(f"[OK] Archivo temporal eliminado")
    except Exception as e:
        print(f"[AVISO] No se pudo eliminar el archivo temporal: {e}")
    
    # Resumen final
    print(f"\n" + "=" * 70)
    print(f"PROCESO COMPLETADO EXITOSAMENTE")
    print(f"=" * 70)
    print(f"\nEstadisticas:")
    print(f"   Lineas originales:      {len(lineas):>6}")
    print(f"   Lineas en archivo final: {len(lineas_filtradas):>6}")
    print(f"   Lineas eliminadas (DML): {lineas_eliminadas:>6}")
    print(f"\nArchivo generado:")
    print(f"   {output_path}")
    print(f"\n" + "=" * 70)

if __name__ == "__main__":
    main()