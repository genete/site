#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consolida todos los módulos BASIC de un archivo .odb en un único archivo XML
para facilitar su uso con IA.

Uso: python consolidar_modulos_basic.py ruta/al/archivo.odb
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Configurar stdout para UTF-8 en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def extraer_modulos_basic(ruta_odb, dir_salida=None):
    """
    Extrae todos los módulos BASIC de un archivo .odb y los consolida en un XML único.
    
    Args:
        ruta_odb: Ruta al archivo .odb
        dir_salida: Directorio donde guardar el resultado (opcional)
    
    Returns:
        Ruta al archivo XML consolidado generado
    """
    ruta_odb = Path(ruta_odb)
    
    if not ruta_odb.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta_odb}")
    
    # Determinar directorio de salida
    if dir_salida is None:
        dir_salida = ruta_odb.parent
    else:
        dir_salida = Path(dir_salida)
        dir_salida.mkdir(parents=True, exist_ok=True)
    
    # Crear archivo de salida
    nombre_salida = f"{ruta_odb.stem}_modulos_consolidados.xml"
    ruta_salida = dir_salida / nombre_salida
    
    # Estructura para almacenar todos los módulos
    modulos_por_biblioteca = {}
    
    # Abrir el archivo .odb como ZIP
    with zipfile.ZipFile(ruta_odb, 'r') as zip_ref:
        # Listar todos los archivos en Basic/
        archivos_basic = [f for f in zip_ref.namelist() if f.startswith('Basic/')]
        
        # Identificar bibliotecas (excluir archivos especiales)
        bibliotecas = set()
        for archivo in archivos_basic:
            partes = archivo.split('/')
            if len(partes) >= 2:
                nombre_bib = partes[1]
                # Excluir archivos de configuración
                if nombre_bib and not nombre_bib.endswith('.xml'):
                    bibliotecas.add(nombre_bib)
        
        print(f"Bibliotecas encontradas: {', '.join(sorted(bibliotecas))}")
        
        # Procesar cada biblioteca
        for biblioteca in sorted(bibliotecas):
            if biblioteca == '':
                continue
                
            modulos_por_biblioteca[biblioteca] = []
            
            # Buscar todos los módulos en esta biblioteca (excluir archivos de configuración)
            modulos_xml = [f for f in archivos_basic 
                          if f.startswith(f'Basic/{biblioteca}/') 
                          and f.endswith('.xml')
                          and 'script-lc.xml' not in f
                          and 'script-lb.xml' not in f
                          and 'dialog-lc.xml' not in f
                          and 'dialog-lb.xml' not in f]
            
            print(f"\nProcesando biblioteca '{biblioteca}':")
            print(f"  Módulos encontrados: {len(modulos_xml)}")
            
            for modulo_path in sorted(modulos_xml):
                nombre_modulo = Path(modulo_path).stem
                
                try:
                    with zip_ref.open(modulo_path) as f:
                        contenido = f.read().decode('utf-8')
                        
                        # Parsear el XML
                        root = ET.fromstring(contenido)
                        
                        # Extraer el código BASIC
                        # El código está en el texto del elemento script:module
                        codigo = root.text if root.text else ""
                        
                        modulos_por_biblioteca[biblioteca].append({
                            'nombre': nombre_modulo,
                            'path': modulo_path,
                            'codigo': codigo.strip(),
                            'atributos': root.attrib
                        })
                        
                        print(f"    [OK] {nombre_modulo}")
                        
                except Exception as e:
                    print(f"    [ERROR] {nombre_modulo}: {e}")
    
    # Generar XML consolidado
    generar_xml_consolidado(modulos_por_biblioteca, ruta_salida, ruta_odb.name)
    
    print(f"\n[OK] Archivo consolidado generado: {ruta_salida}")
    return ruta_salida


def generar_xml_consolidado(modulos_por_biblioteca, ruta_salida, nombre_odb):
    """
    Genera un archivo XML consolidado con todos los módulos.
    """
    # Crear el elemento raíz
    root = ET.Element('modulos-basic-consolidados')
    root.set('archivo-origen', nombre_odb)
    root.set('fecha-extraccion', datetime.now().isoformat())
    root.set('total-bibliotecas', str(len(modulos_por_biblioteca)))
    
    total_modulos = sum(len(mods) for mods in modulos_por_biblioteca.values())
    root.set('total-modulos', str(total_modulos))
    
    # Añadir cada biblioteca y sus módulos
    for nombre_biblioteca, modulos in modulos_por_biblioteca.items():
        biblioteca_elem = ET.SubElement(root, 'biblioteca')
        biblioteca_elem.set('nombre', nombre_biblioteca)
        biblioteca_elem.set('cantidad-modulos', str(len(modulos)))
        
        for modulo in modulos:
            modulo_elem = ET.SubElement(biblioteca_elem, 'modulo')
            modulo_elem.set('nombre', modulo['nombre'])
            modulo_elem.set('path-original', modulo['path'])
            
            # Añadir atributos del módulo original
            for attr, valor in modulo['atributos'].items():
                # Limpiar namespace del atributo
                if '}' in attr:
                    # Extraer solo el nombre después del namespace
                    attr_simple = attr.split('}')[1]
                elif ':' in attr:
                    # Quitar el namespace para simplificar
                    attr_simple = attr.split(':')[1]
                else:
                    attr_simple = attr
                modulo_elem.set(attr_simple, valor)
            
            # Añadir el código BASIC
            codigo_elem = ET.SubElement(modulo_elem, 'codigo')
            codigo_elem.text = '\n' + modulo['codigo'] + '\n'
    
    # Crear el árbol y escribir con formato bonito
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    
    # Escribir el archivo
    with open(ruta_salida, 'wb') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    # También generar versión .txt para la IA
    ruta_txt = ruta_salida.with_suffix('.xml.txt')
    with open(ruta_txt, 'wb') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
        tree.write(f, encoding='utf-8', xml_declaration=False)
    
    print(f"[OK] Tambien generado: {ruta_txt}")


def generar_markdown_indice(ruta_odb, dir_salida=None):
    """
    Genera un archivo Markdown con el índice de todos los módulos BASIC.
    """
    ruta_odb = Path(ruta_odb)
    
    if dir_salida is None:
        dir_salida = ruta_odb.parent
    else:
        dir_salida = Path(dir_salida)
    
    ruta_salida = dir_salida / f"{ruta_odb.stem}_indice_modulos.md"
    
    modulos_por_biblioteca = {}
    
    with zipfile.ZipFile(ruta_odb, 'r') as zip_ref:
        archivos_basic = [f for f in zip_ref.namelist() if f.startswith('Basic/')]
        bibliotecas = set()
        
        for archivo in archivos_basic:
            partes = archivo.split('/')
            if len(partes) >= 2:
                bibliotecas.add(partes[1])
        
        for biblioteca in sorted(bibliotecas):
            if biblioteca == '':
                continue
            
            modulos_xml = [f for f in archivos_basic 
                          if f.startswith(f'Basic/{biblioteca}/') 
                          and f.endswith('.xml')
                          and 'script-lc.xml' not in f
                          and 'script-lb.xml' not in f
                          and 'dialog-lc.xml' not in f
                          and 'dialog-lb.xml' not in f]
            
            modulos_por_biblioteca[biblioteca] = []
            
            for modulo_path in sorted(modulos_xml):
                nombre_modulo = Path(modulo_path).stem
                modulos_por_biblioteca[biblioteca].append(nombre_modulo)
    
    # Generar Markdown
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(f"# Índice de Módulos BASIC\n\n")
        f.write(f"**Archivo:** {ruta_odb.name}  \n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        
        total_modulos = sum(len(mods) for mods in modulos_por_biblioteca.values())
        f.write(f"**Total de bibliotecas:** {len(modulos_por_biblioteca)}  \n")
        f.write(f"**Total de módulos:** {total_modulos}  \n\n")
        
        f.write("---\n\n")
        
        for biblioteca, modulos in modulos_por_biblioteca.items():
            f.write(f"## Biblioteca: {biblioteca}\n\n")
            f.write(f"**Cantidad de módulos:** {len(modulos)}\n\n")
            
            for modulo in modulos:
                f.write(f"- `{modulo}`\n")
            
            f.write("\n")
    
    print(f"[OK] Indice generado: {ruta_salida}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python consolidar_modulos_basic.py <archivo.odb> [directorio_salida]")
        print("\nEjemplo:")
        print("  python consolidar_modulos_basic.py desarrollo/interfaz/mibase.odb")
        print("  python consolidar_modulos_basic.py mibase.odb desarrollo/fuentesIA")
        sys.exit(1)
    
    ruta_odb = sys.argv[1]
    dir_salida = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        print("=" * 60)
        print("CONSOLIDADOR DE MÓDULOS BASIC")
        print("=" * 60)
        
        # Generar archivo consolidado
        ruta_xml = extraer_modulos_basic(ruta_odb, dir_salida)
        
        # Generar índice Markdown
        print("\n" + "=" * 60)
        print("Generando índice...")
        generar_markdown_indice(ruta_odb, dir_salida)
        
        print("\n" + "=" * 60)
        print("[OK] Proceso completado exitosamente")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)