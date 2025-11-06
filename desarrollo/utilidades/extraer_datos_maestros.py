#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer los INSERT de tablas maestras desde bdat.script
Genera: datos_maestros.sql.txt en desarrollo/fuentesIA/

Uso:
    python extraer_datos_maestros.py
    
El script busca automáticamente:
    - desarrollo/bdat/bdat.script (entrada)
    - desarrollo/fuentesIA/tablas_maestras.txt (configuración)
    - desarrollo/fuentesIA/datos_maestros.sql.txt (salida)
"""

import os
import sys
from pathlib import Path

def leer_tablas_maestras(ruta_tablas):
    """Lee el archivo de tablas maestras y devuelve un set con los nombres."""
    try:
        with open(ruta_tablas, 'r', encoding='utf-8') as f:
            # Leer líneas, quitar espacios y comentarios
            tablas = {
                linea.strip().upper() 
                for linea in f 
                if linea.strip() and not linea.strip().startswith('#')
            }
        return tablas
    except FileNotFoundError:
        print(f"ERROR: No se encuentra el archivo {ruta_tablas}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR al leer tablas maestras: {e}")
        sys.exit(1)

def extraer_inserts_maestros(ruta_script, tablas_maestras):
    """
    Extrae las líneas INSERT INTO de las tablas maestras.
    Devuelve una tupla: (lista de líneas, dict con conteo por tabla)
    """
    inserts = []
    conteo_por_tabla = {tabla: 0 for tabla in tablas_maestras}
    
    try:
        with open(ruta_script, 'r', encoding='utf-8') as f:
            for linea in f:
                linea_strip = linea.strip()
                
                # Buscar líneas INSERT INTO
                if linea_strip.upper().startswith('INSERT INTO'):
                    # Extraer el nombre de la tabla
                    # Formato esperado: INSERT INTO T.NOMBRE_TABLA VALUES(...)
                    partes = linea_strip.split()
                    if len(partes) >= 3:
                        tabla_completa = partes[2].upper()  # "T.NOMBRE_TABLA" o "PUBLIC.T.NOMBRE_TABLA"
                        
                        # Extraer solo el nombre de la tabla (después del último punto)
                        nombre_tabla = tabla_completa.split('.')[-1]
                        
                        # Si la tabla está en la lista de maestras, guardar la línea
                        if nombre_tabla in tablas_maestras:
                            inserts.append(linea.rstrip())
                            conteo_por_tabla[nombre_tabla] += 1
        
        return inserts, conteo_por_tabla
    
    except FileNotFoundError:
        print(f"ERROR: No se encuentra el archivo {ruta_script}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR al leer bdat.script: {e}")
        sys.exit(1)

def guardar_datos_maestros(ruta_salida, inserts, tablas_maestras, conteo_por_tabla):
    """Guarda los INSERT en el archivo de salida con encabezado."""
    try:
        # Filtrar solo tablas con datos
        tablas_con_datos = [t for t in tablas_maestras if conteo_por_tabla[t] > 0]
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("-- =====================================================\n")
            f.write("-- DATOS MAESTROS - Definicion de logica de negocio\n")
            f.write("-- =====================================================\n")
            f.write("-- Generado automaticamente desde bdat.script\n")
            f.write(f"-- Tablas incluidas: {', '.join(sorted(tablas_con_datos))}\n")
            f.write("-- =====================================================\n\n")
            
            # Agrupar INSERTs por tabla
            inserts_por_tabla = {}
            for linea in inserts:
                # Extraer nombre de tabla de la línea
                partes = linea.split()
                tabla_completa = partes[2] if len(partes) >= 3 else "UNKNOWN"
                nombre_tabla = tabla_completa.split('.')[-1]
                
                if nombre_tabla not in inserts_por_tabla:
                    inserts_por_tabla[nombre_tabla] = []
                inserts_por_tabla[nombre_tabla].append(linea)
            
            # Escribir por secciones
            for tabla in sorted(inserts_por_tabla.keys()):
                f.write(f"-- Tabla: {tabla}\n")
                f.write(f"-- {'-' * 50}\n")
                for linea in inserts_por_tabla[tabla]:
                    f.write(linea + '\n')
                f.write('\n')
        
        print(f"[OK] Archivo generado: {ruta_salida}")
        print(f"[OK] Total de INSERT extraidos: {len(inserts)}")
        
        # Mostrar estadísticas detalladas
        print(f"\nEstadisticas por tabla:")
        tablas_encontradas = []
        tablas_vacias = []
        
        for tabla in sorted(tablas_maestras):
            count = conteo_por_tabla[tabla]
            if count > 0:
                print(f"  {tabla}: {count} registros")
                tablas_encontradas.append(tabla)
            else:
                tablas_vacias.append(tabla)
        
        # Advertencias
        if tablas_vacias:
            print(f"\n[ADVERTENCIA] Tablas sin datos encontrados:")
            for tabla in tablas_vacias:
                print(f"  - {tabla}")
            print(f"\nVerifica que los nombres en tablas_maestras.txt sean correctos")
            print(f"y coincidan exactamente con los nombres en bdat.script")
        
        return len(tablas_vacias) == 0
        
    except Exception as e:
        print(f"ERROR al guardar archivo: {e}")
        sys.exit(1)

def main():
    """Función principal."""
    print("=" * 60)
    print("Extractor de Datos Maestros - BDDATLIBRE")
    print("=" * 60)
    
    # Definir rutas (asumiendo que el script está en desarrollo/utilidades)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent  # desarrollo/
    
    ruta_script = base_dir / "bdat" / "bdat.script"
    ruta_tablas = base_dir / "fuentesIA" / "tablas_maestras.txt"
    ruta_salida = base_dir / "fuentesIA" / "datos_maestros.sql.txt"
    
    print(f"\nRutas configuradas:")
    print(f"  Script entrada: {ruta_script}")
    print(f"  Tablas maestras: {ruta_tablas}")
    print(f"  Salida: {ruta_salida}")
    print()
    
    # Verificar que existen los archivos de entrada
    if not ruta_script.exists():
        print(f"ERROR: No existe {ruta_script}")
        sys.exit(1)
    
    if not ruta_tablas.exists():
        print(f"ERROR: No existe {ruta_tablas}")
        sys.exit(1)
    
    # Leer tablas maestras
    print("Leyendo tablas maestras...")
    tablas_maestras = leer_tablas_maestras(ruta_tablas)
    print(f"  Tablas maestras configuradas: {', '.join(sorted(tablas_maestras))}")
    print()
    
    # Extraer INSERTs
    print("Extrayendo INSERT de bdat.script...")
    inserts, conteo_por_tabla = extraer_inserts_maestros(ruta_script, tablas_maestras)
    print(f"  INSERT encontrados: {len(inserts)}")
    print()
    
    # Guardar resultado
    print("Generando datos_maestros.sql.txt...")
    todo_ok = guardar_datos_maestros(ruta_salida, inserts, tablas_maestras, conteo_por_tabla)
    
    print("\n" + "=" * 60)
    if todo_ok:
        print("Proceso completado exitosamente")
    else:
        print("Proceso completado CON ADVERTENCIAS")
        print("Revisa las tablas que no tienen datos")
    print("=" * 60)

if __name__ == "__main__":
    main()