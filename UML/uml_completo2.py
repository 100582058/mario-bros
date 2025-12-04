import ast
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

class AnalizadorUML:
    def __init__(self, ruta_proyecto='.'):
        self.ruta = Path(ruta_proyecto)
        self.clases = {}
        self.dependencias = []
        self.herencias = []
        self.archivo_actual = Path(__file__).name
        
    def analizar_archivo(self, archivo):
        """Analiza un archivo Python y extrae clases, métodos, atributos"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                tree = ast.parse(contenido, filename=str(archivo))
            
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    info_clase = self.analizar_clase(node, archivo, imports)
                    nombre_completo = f"{archivo.stem}.{node.name}"
                    self.clases[nombre_completo] = info_clase
                    
        except Exception as e:
            print(f"⚠️  Error analizando {archivo}: {e}")
    
    def analizar_clase(self, node, archivo, imports):
        """Extrae información de una clase"""
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}")
        
        atributos = []
        metodos = []
        
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        tipo = self.inferir_tipo(item.value)
                        atributos.append((target.id, tipo))
            
            elif isinstance(item, ast.FunctionDef):
                if item.name == '__init__':
                    for stmt in ast.walk(item):
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Attribute):
                                    if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                        tipo = self.inferir_tipo(stmt.value)
                                        if (target.attr, tipo) not in atributos:
                                            atributos.append((target.attr, tipo))
                
                params = [arg.arg for arg in item.args.args if arg.arg != 'self']
                metodos.append((item.name, params))
        
        return {
            'archivo': archivo,
            'nombre': node.name,
            'bases': bases,
            'atributos': atributos,
            'metodos': metodos,
            'imports': imports
        }
    
    def inferir_tipo(self, node):
        """Intenta inferir el tipo de un valor"""
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.List):
            return 'list'
        elif isinstance(node, ast.Dict):
            return 'dict'
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
        return ''
    
    def analizar_proyecto(self):
        """Analiza todo el proyecto"""
        archivos_py = list(self.ruta.rglob('*.py'))
        
        archivos_py = [
            f for f in archivos_py 
            if '__pycache__' not in str(f) 
            and f.name != self.archivo_actual
            and 'venv' not in str(f)
            and 'env' not in str(f)
        ]
        
        print(f"📂 Analizando {len(archivos_py)} archivos...")
        
        for archivo in archivos_py:
            self.analizar_archivo(archivo)
        
        self.detectar_herencias()
        self.detectar_dependencias()
        
        print(f"✅ Encontradas {len(self.clases)} clases")
        print(f"✅ Encontradas {len(self.herencias)} herencias")
        print(f"✅ Encontradas {len(self.dependencias)} dependencias")
    
    def detectar_herencias(self):
        """Detecta relaciones de herencia"""
        for nombre_clase, info in self.clases.items():
            for base in info['bases']:
                for nombre_base, info_base in self.clases.items():
                    if info_base['nombre'] == base:
                        self.herencias.append((nombre_base, nombre_clase))
    
    def detectar_dependencias(self):
        """Detecta dependencias (imports y uso de clases)"""
        for nombre_clase, info in self.clases.items():
            for import_mod in info['imports']:
                for nombre_otra, info_otra in self.clases.items():
                    archivo_otra = str(info_otra['archivo']).replace('\\', '.').replace('/', '.').replace('.py', '')
                    if import_mod in archivo_otra:
                        dep = (nombre_clase, nombre_otra)
                        if dep not in self.dependencias and nombre_clase != nombre_otra:
                            self.dependencias.append(dep)

def generar_drawio_xml(analizador):
    """Genera archivo XML compatible con Draw.io"""
    
    # Crear estructura XML
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'modified': '2024-01-01T00:00:00.000Z',
        'agent': 'Python UML Generator',
        'version': '22.0.0',
        'type': 'device'
    })
    
    diagram = ET.SubElement(mxfile, 'diagram', {
        'id': 'uml-sprint4',
        'name': 'UML Sprint 4'
    })
    
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '1422',
        'dy': '794',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '827',
        'pageHeight': '1169',
        'math': '0',
        'shadow': '0'
    })
    
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Células base
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    cell_id = 2
    clase_ids = {}
    
    # Posicionamiento automático
    x_pos = 50
    y_pos = 50
    clases_por_fila = 3
    ancho_clase = 250
    alto_clase = 200
    espacio_x = 100
    espacio_y = 100
    
    # Crear clases
    idx = 0
    for nombre_clase, info in analizador.clases.items():
        clase_ids[nombre_clase] = cell_id
        
        # Calcular posición
        col = idx % clases_por_fila
        fila = idx // clases_por_fila
        x = x_pos + col * (ancho_clase + espacio_x)
        y = y_pos + fila * (alto_clase + espacio_y)
        
        # Construir contenido HTML de la clase
        contenido_html = f'<p style="margin:0px;margin-top:4px;text-align:center;"><b>{info["nombre"]}</b></p>'
        contenido_html += '<hr size="1"/>'
        
        # Atributos
        if info['atributos']:
            contenido_html += '<p style="margin:0px;margin-left:4px;">'
            for attr, tipo in info['atributos']:
                tipo_str = f': {tipo}' if tipo else ''
                contenido_html += f'+ {attr}{tipo_str}<br/>'
            contenido_html += '</p>'
            contenido_html += '<hr size="1"/>'
        
        # Métodos
        if info['metodos']:
            contenido_html += '<p style="margin:0px;margin-left:4px;">'
            for metodo, params in info['metodos']:
                params_str = ', '.join(params)
                contenido_html += f'+ {metodo}({params_str})<br/>'
            contenido_html += '</p>'
        
        # Calcular altura basada en contenido
        num_atributos = len(info['atributos'])
        num_metodos = len(info['metodos'])
        altura_calculada = 60 + (num_atributos * 20) + (num_metodos * 20)
        altura_final = max(alto_clase, altura_calculada)
        
        # Crear celda de clase
        clase_cell = ET.SubElement(root, 'mxCell', {
            'id': str(cell_id),
            'value': contenido_html,
            'style': 'swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;',
            'vertex': '1',
            'parent': '1'
        })
        
        ET.SubElement(clase_cell, 'mxGeometry', {
            'x': str(x),
            'y': str(y),
            'width': str(ancho_clase),
            'height': str(altura_final),
            'as': 'geometry'
        })
        
        cell_id += 1
        idx += 1
    
    # Crear herencias (flechas con triángulo blanco)
    for padre, hijo in analizador.herencias:
        if padre in clase_ids and hijo in clase_ids:
            edge_cell = ET.SubElement(root, 'mxCell', {
                'id': str(cell_id),
                'value': '',
                'style': 'endArrow=block;endSize=16;endFill=0;html=1;rounded=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;',
                'edge': '1',
                'parent': '1',
                'source': str(clase_ids[hijo]),
                'target': str(clase_ids[padre])
            })
            
            ET.SubElement(edge_cell, 'mxGeometry', {
                'relative': '1',
                'as': 'geometry'
            })
            
            cell_id += 1
    
    # Crear dependencias (flechas punteadas)
    for origen, destino in analizador.dependencias:
        if origen in clase_ids and destino in clase_ids:
            edge_cell = ET.SubElement(root, 'mxCell', {
                'id': str(cell_id),
                'value': 'usa',
                'style': 'endArrow=open;endSize=12;dashed=1;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;',
                'edge': '1',
                'parent': '1',
                'source': str(clase_ids[origen]),
                'target': str(clase_ids[destino])
            })
            
            ET.SubElement(edge_cell, 'mxGeometry', {
                'relative': '1',
                'as': 'geometry'
            })
            
            cell_id += 1
    
    # Convertir a string con formato bonito
    xml_str = ET.tostring(mxfile, encoding='unicode')
    
    # Formatear con minidom
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # Limpiar líneas vacías extras
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    return '\n'.join(lines)

# ============================================
# EJECUTAR
# ============================================

print("🔍 Iniciando análisis completo del proyecto...\n")

analizador = AnalizadorUML('.')
analizador.analizar_proyecto()

print("\n📝 Generando archivo Draw.io...")
xml_content = generar_drawio_xml(analizador)

# Guardar archivo .drawio
with open('UML_Sprint4.drawio', 'w', encoding='utf-8') as f:
    f.write(xml_content)

print("✅ Archivo Draw.io generado: UML_Sprint4.drawio")