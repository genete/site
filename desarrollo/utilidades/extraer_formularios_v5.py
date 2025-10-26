import zipfile
import xml.etree.ElementTree as ET
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


# Namespaces comunes en formularios ODF / LibreOffice
COMMON_NS = {
    "form": "urn:oasis:names:tc:opendocument:xmlns:form:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "script": "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


def get_namespaces(elem):
    """Detecta los namespaces presentes en un XML."""
    nsmap = COMMON_NS.copy()
    # Buscar namespaces en el elemento raíz
    for k, v in elem.attrib.items():
        if k.startswith("{http://www.w3.org/2000/xmlns/}"):
            prefix = k.split("}", 1)[-1]
            if prefix:
                nsmap[prefix] = v
        elif k.startswith("xmlns:"):
            prefix = k.split(":")[1]
            nsmap[prefix] = v
    return nsmap


def parse_events(element, ns):
    """Extrae los eventos y macros asociados directamente a un elemento (no descendientes)."""
    events = {}
    
    # Buscar contenedores de eventos que sean HIJOS DIRECTOS
    event_containers = []
    for child in element:
        child_tag = child.tag.split("}", 1)[-1] if "}" in child.tag else child.tag
        if child_tag == "event-listeners":
            event_containers.append(child)
    
    # Ahora buscar listeners dentro de esos contenedores
    for container in event_containers:
        for listener in container:
            listener_tag = listener.tag.split("}", 1)[-1] if "}" in listener.tag else listener.tag
            if listener_tag == "event-listener":
                event_name = listener.get(f"{{{ns.get('script', '')}}}event-name")
                href = listener.get(f"{{{ns.get('xlink', '')}}}href")
                if href and event_name:
                    macro_name = href.split("vnd.sun.star.script:")[-1].split("?")[0]
                    events[event_name] = macro_name
    
    return events


def parse_control_model(model, ns):
    """Extrae la definición lógica de un control."""
    # Obtener el nombre del tag sin namespace
    tag = model.tag.split("}", 1)[-1] if "}" in model.tag else model.tag
    
    # Extraer propiedades básicas
    data = {
        "type": tag,
        "id": model.get(f"{{{ns.get('form', '')}}}id") or model.get("{http://www.w3.org/XML/1998/namespace}id"),
        "name": model.get(f"{{{ns.get('form', '')}}}name"),
        "label": model.get(f"{{{ns.get('form', '')}}}label"),
        "bound-field": model.get(f"{{{ns.get('form', '')}}}data-field"),
        "value-type": model.get(f"{{{ns.get('form', '')}}}value-type"),
        "datasource": model.get(f"{{{ns.get('form', '')}}}datasource"),
        "list-source": model.get(f"{{{ns.get('form', '')}}}list-source"),
        "control-source": model.get(f"{{{ns.get('form', '')}}}control-source"),
        "default-value": model.get(f"{{{ns.get('form', '')}}}default-value"),
        "min-value": model.get(f"{{{ns.get('form', '')}}}min-value"),
        "max-value": model.get(f"{{{ns.get('form', '')}}}max-value"),
        "readonly": model.get(f"{{{ns.get('form', '')}}}readonly"),
        "required": model.get(f"{{{ns.get('form', '')}}}input-required"),
        "validation": model.get(f"{{{ns.get('form', '')}}}validation"),
        "events": parse_events(model, ns),
        "properties": {},
        "columns": []  # Para grid controls
    }

    # Capturar todas las propiedades adicionales
    excluded_keys = {
        "name", "label", "data-field", "value-type", "datasource", 
        "list-source", "control-source", "default-value", "min-value", 
        "max-value", "id", "readonly", "input-required", "validation"
    }
    
    for key, val in model.attrib.items():
        keyname = key.split("}", 1)[-1] if "}" in key else key
        if keyname not in excluded_keys:
            data["properties"][keyname] = val
    
    # Si es un grid, buscar columnas
    if tag == "grid":
        for child in model:
            child_tag = child.tag.split("}", 1)[-1] if "}" in child.tag else child.tag
            if child_tag == "column":
                data["columns"].append(parse_control_model(child, ns))

    return data





def find_all_controls_recursive(element, ns, controls_list):
    """Busca recursivamente todos los controles en el árbol XML."""
    # Lista de tipos de controles conocidos en LibreOffice Base
    control_types = [
        "button", "text", "textarea", "formatted-text", "listbox", "combobox",
        "checkbox", "radio", "image", "file", "hidden", "grid", "value-range",
        "generic-control", "frame", "image-frame", "fixed-text", "column"
    ]
    
    for child in element:
        # Obtener el namespace URI del elemento
        if "}" in child.tag:
            namespace_uri = child.tag.split("}", 1)[0] + "}"
            tag_name = child.tag.split("}", 1)[1]
        else:
            namespace_uri = ""
            tag_name = child.tag
        
        # Verificar si es un control (debe tener namespace form: y ser un tipo conocido)
        is_form_namespace = namespace_uri == "{" + ns.get("form", "") + "}"
        is_control_type = tag_name in control_types
        
        if is_form_namespace and is_control_type:
            controls_list.append(parse_control_model(child, ns))
        
        # También capturar elementos "properties" que no sean controles pero tengan info relevante
        # Continuar búsqueda recursiva solo si no es un subformulario
        if not (is_form_namespace and tag_name == "form"):
            find_all_controls_recursive(child, ns, controls_list)


def parse_form(form_element, ns, root, source_file):
    """Extrae un formulario completo (modelo lógico + subformularios + controles visuales)."""
    form_data = {
        "name": form_element.get(f"{{{ns['form']}}}name"),
        "source_file": source_file,
        "datasource": form_element.get(f"{{{ns['form']}}}datasource"),
        "command": form_element.get(f"{{{ns['form']}}}command"),
        "command_type": form_element.get(f"{{{ns['form']}}}command-type"),
        "allow_updates": form_element.get(f"{{{ns['form']}}}allow-updates"),
        "allow_deletes": form_element.get(f"{{{ns['form']}}}allow-deletes"),
        "allow_inserts": form_element.get(f"{{{ns['form']}}}allow-inserts"),
        "events": parse_events(form_element, ns),
        "controls": [],
        "subforms": [],
    }

    # Buscar controles recursivamente dentro del formulario
    find_all_controls_recursive(form_element, ns, form_data["controls"])

    # Subformularios
    for subform in form_element.findall("form:form", ns):
        form_data["subforms"].append(parse_form(subform, ns, root, source_file))

    return form_data


def extract_database_info(extract_dir):
    """Extrae información de conexión del content.xml raíz."""
    content_xml = extract_dir / "content.xml"
    
    if not content_xml.exists():
        return None
    
    try:
        tree = ET.parse(content_xml)
        root = tree.getroot()
        
        # Namespaces para el content.xml raíz
        ns = {
            'db': 'urn:oasis:names:tc:opendocument:xmlns:database:1.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
        db_info = {}
        
        # Extraer URL de conexión
        conn_resource = root.find('.//db:connection-resource', ns)
        if conn_resource is not None:
            jdbc_url = conn_resource.get(f"{{{ns['xlink']}}}href")
            if jdbc_url:
                db_info['connection_url'] = jdbc_url
                
                # Parsear tipo de BD desde la URL
                if 'hsqldb' in jdbc_url.lower():
                    db_info['type'] = 'hsqldb'
                elif 'mysql' in jdbc_url.lower():
                    db_info['type'] = 'mysql'
                elif 'postgresql' in jdbc_url.lower():
                    db_info['type'] = 'postgresql'
                elif 'oracle' in jdbc_url.lower():
                    db_info['type'] = 'oracle'
                else:
                    db_info['type'] = 'unknown'
        
        # Extraer usuario
        login = root.find('.//db:login', ns)
        if login is not None:
            user = login.get(f"{{{ns['db']}}}user-name")
            if user:
                db_info['user'] = user
        
        # Extraer driver Java
        for setting in root.findall('.//db:data-source-setting', ns):
            setting_name = setting.get(f"{{{ns['db']}}}data-source-setting-name")
            if setting_name == 'JavaDriverClass':
                value_elem = setting.find('db:data-source-setting-value', ns)
                if value_elem is not None and value_elem.text:
                    db_info['driver'] = value_elem.text
                    break
        
        return db_info if db_info else None
        
    except Exception as e:
        print(f"[!] Error extrayendo info de BD del content.xml raíz: {e}")
        return None


def extract_forms_from_odb(odb_path):
    """Extrae la estructura de formularios de un archivo .odb."""
    odb_path = Path(odb_path)
    extract_dir = odb_path.parent / f"_extract_{odb_path.stem}"

    with zipfile.ZipFile(odb_path, "r") as z:
        z.extractall(extract_dir)

    # Extraer información de la base de datos
    database_info = extract_database_info(extract_dir)

    # Buscar formularios en múltiples ubicaciones
    form_files = (
        list(extract_dir.glob("forms/Obj*/content.xml")) +
        list(extract_dir.glob("database/forms/**/content.xml")) +
        list(extract_dir.glob("forms/**/content.xml"))
    )
    
    # También revisar content.xml en raíz si existe
    if (extract_dir / "content.xml").exists():
        form_files.append(extract_dir / "content.xml")

    # Eliminar duplicados manteniendo el orden
    seen = set()
    unique_form_files = []
    for f in form_files:
        if f not in seen:
            seen.add(f)
            unique_form_files.append(f)
    
    form_files = unique_form_files

    all_forms = []
    processed_files = []

    for xml_path in form_files:
        if not xml_path.exists():
            continue
            
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            ns = get_namespaces(root)

            # Buscar formularios
            forms_found = root.findall(".//form:form", ns)
            
            if forms_found:
                processed_files.append(str(xml_path.relative_to(extract_dir)))
                for form_element in forms_found:
                    all_forms.append(parse_form(form_element, ns, root, str(xml_path.relative_to(extract_dir))))

        except Exception as e:
            print(f"[!] Error procesando {xml_path}: {e}")

    return {
        "database_info": database_info,
        "forms": all_forms,
        "files_processed": processed_files,
        "total_forms": len(all_forms)
    }


if __name__ == "__main__":
    # Selecciona archivo .odb mediante cuadro de diálogo
    root = tk.Tk()
    root.withdraw()
    odb_file = filedialog.askopenfilename(
        title="Selecciona el archivo .odb de LibreOffice Base",
        filetypes=[("LibreOffice Base", "*.odb")],
    )

    if not odb_file:
        print("[X] No se seleccionó ningún archivo. Saliendo...")
    elif not odb_file.lower().endswith(".odb"):
        print("[X] El archivo seleccionado no es un .odb válido.")
    else:
        print(f"[*] Procesando: {odb_file}")
        data = extract_forms_from_odb(odb_file)
        
        out_path = Path(odb_file).with_name("formularios_completo.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Archivo generado: {out_path}")
        print(f"[INFO] Tipo de BD: {data.get('database_info', {}).get('type', 'desconocido')}")
        print(f"[INFO] Driver: {data.get('database_info', {}).get('driver', 'no especificado')}")
        print(f"[INFO] Formularios encontrados: {data['total_forms']}")
        print(f"[INFO] Archivos procesados: {len(data['files_processed'])}")
        
        # Mostrar resumen de controles por formulario
        for i, form in enumerate(data['forms'], 1):
            print(f"\n  Formulario {i}: {form['name']}")
            print(f"    - Archivo: {form['source_file']}")
            print(f"    - Controles: {len(form['controls'])}")
            print(f"    - Subformularios: {len(form['subforms'])}")