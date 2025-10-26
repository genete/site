import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


def diagnosticar_odb(odb_path):
    """Diagnostica la estructura de un archivo .odb para encontrar dónde están los controles."""
    odb_path = Path(odb_path)
    extract_dir = odb_path.parent / f"_diagnostico_{odb_path.stem}"

    print(f"[*] Extrayendo archivo a: {extract_dir}")
    
    with zipfile.ZipFile(odb_path, "r") as z:
        z.extractall(extract_dir)
        print(f"[*] Archivos en el .odb:")
        for name in sorted(z.namelist()):
            print(f"    {name}")

    print("\n" + "="*80)
    print("BUSCANDO ARCHIVOS XML CON CONTENIDO")
    print("="*80)

    # Buscar todos los XML
    xml_files = list(extract_dir.glob("**/*.xml"))
    
    for xml_path in xml_files:
        rel_path = xml_path.relative_to(extract_dir)
        print(f"\n[ARCHIVO] {rel_path}")
        print("-" * 80)
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Mostrar información básica
            print(f"Root tag: {root.tag}")
            print(f"Root attribs: {list(root.attrib.keys())[:5]}...")  # Primeros 5
            
            # Buscar elementos interesantes
            all_elements = list(root.iter())
            print(f"Total elementos en el árbol: {len(all_elements)}")
            
            # Contar elementos por namespace/tag
            tag_counts = {}
            for elem in all_elements:
                tag = elem.tag.split("}", 1)[-1] if "}" in elem.tag else elem.tag
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Mostrar los más relevantes
            relevant_tags = [t for t in tag_counts.keys() if 
                           any(keyword in t.lower() for keyword in 
                               ['form', 'control', 'text', 'button', 'list', 'combo', 'field'])]
            
            if relevant_tags:
                print(f"\n[TAGS RELEVANTES]:")
                for tag in sorted(relevant_tags):
                    print(f"    {tag}: {tag_counts[tag]} veces")
            
            # Buscar específicamente elementos form:*
            form_elements = [e for e in all_elements if 'form' in e.tag.lower()]
            if form_elements:
                print(f"\n[ELEMENTOS FORM] Total: {len(form_elements)}")
                for elem in form_elements[:10]:  # Mostrar primeros 10
                    tag = elem.tag.split("}", 1)[-1] if "}" in elem.tag else elem.tag
                    name = elem.get('{urn:oasis:names:tc:opendocument:xmlns:form:1.0}name', 
                                   elem.get('name', 'sin nombre'))
                    print(f"    - {tag} (name={name})")
                    if len(elem.attrib) > 0:
                        print(f"      Atributos: {list(elem.attrib.keys())[:3]}")
            
            # Mostrar un fragmento del XML para el primer form:form encontrado
            for elem in root.iter():
                if 'form:form' in elem.tag or elem.tag.endswith('}form'):
                    print(f"\n[MUESTRA XML] Primer form:form encontrado:")
                    print("-" * 80)
                    xml_str = ET.tostring(elem, encoding='unicode', method='xml')
                    # Mostrar primeras 2000 caracteres
                    print(xml_str[:2000])
                    if len(xml_str) > 2000:
                        print(f"\n... (truncado, total: {len(xml_str)} caracteres)")
                    break
                    
        except Exception as e:
            print(f"[ERROR] al parsear: {e}")

    print("\n" + "="*80)
    print("FIN DEL DIAGNÓSTICO")
    print("="*80)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    odb_file = filedialog.askopenfilename(
        title="Selecciona el archivo .odb para diagnosticar",
        filetypes=[("LibreOffice Base", "*.odb")],
    )

    if not odb_file:
        print("[X] No se seleccionó ningún archivo.")
    elif not odb_file.lower().endswith(".odb"):
        print("[X] El archivo seleccionado no es un .odb válido.")
    else:
        diagnosticar_odb(odb_file)
        print("\n💡 Revisa la salida para entender dónde están los controles.")