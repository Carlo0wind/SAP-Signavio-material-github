"""
Generador de Informe Word — INDUPRO S.A.
SAP Signavio Regional Challenge 2026
Formato de entrega para el concurso
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ═══════════════════════════════════════════════════════
# RUTAS
# ═══════════════════════════════════════════════════════
BASE = r"c:\Users\drago\projects\ProyectoSAPSignavio"
CARATULA_IMG = BASE + r"\material-concurso\imagen-caratula.png"
OUTPUT_PATH  = BASE + r"\Analisis Final\INDUPRO_Informe_Concurso.docx"

# ═══════════════════════════════════════════════════════
# COLORES
# ═══════════════════════════════════════════════════════
SAP_BLUE  = RGBColor(0x00, 0x70, 0xF2)
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x49)
GOLD      = RGBColor(0xF0, 0xAB, 0x00)
GREEN     = RGBColor(0x2E, 0x8B, 0x57)
RED       = RGBColor(0xC0, 0x39, 0x2B)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MED_GRAY  = RGBColor(0x66, 0x66, 0x66)
LIGHT_BG  = RGBColor(0xF2, 0xF8, 0xFF)


# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════

def set_cell_bg(cell, hex_color):
    """Pone color de fondo a una celda de tabla."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_col_width(table, col_idx, width_cm):
    for row in table.rows:
        row.cells[col_idx].width = Cm(width_cm)

def heading(doc, text, level=1, color=DARK_BLUE, space_before=12):
    h = doc.add_heading(text, level=level)
    run = h.runs[0] if h.runs else h.add_run(text)
    run.font.color.rgb = color
    run.font.bold = True
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after  = Pt(6)
    return h

def body(doc, text, space_after=6, indent=0, italic=False, color=None, bold=False):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    for run in p.runs:
        if italic: run.font.italic = True
        if bold:   run.font.bold   = True
        if color:  run.font.color.rgb = color
    return p

def note_box(doc, text, prefix="📌 Nota:"):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(8)
    r1 = p.add_run(prefix + " ")
    r1.font.bold = True
    r1.font.color.rgb = SAP_BLUE
    r2 = p.add_run(text)
    r2.font.italic = True
    r2.font.color.rgb = DARK_GRAY
    r2.font.size = Pt(9)
    return p

def img_placeholder(doc, label, height_cm=7.0):
    """Caja gris de placeholder para imágenes que se insertarán manualmente."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"[ {label} ]")
    r.font.size    = Pt(10)
    r.font.italic  = True
    r.font.color.rgb = MED_GRAY
    return p

def add_table_header_row(table, headers, bg="1B2A49"):
    """Rellena la primera fila como encabezado con fondo oscuro y texto blanco."""
    row = table.rows[0]
    for i, h in enumerate(headers):
        cell = row.cells[i]
        cell.text = h
        set_cell_bg(cell, bg)
        for run in cell.paragraphs[0].runs:
            run.font.bold  = True
            run.font.color.rgb = WHITE
            run.font.size  = Pt(9)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_data_row(table, values, row_idx, alt=False):
    row = table.rows[row_idx]
    bg = "F2F8FF" if alt else "FFFFFF"
    for i, v in enumerate(values):
        cell = row.cells[i]
        set_cell_bg(cell, bg)
        cell.text = str(v)
        for run in cell.paragraphs[0].runs:
            run.font.size = Pt(8.5)
    return row

def page_break(doc):
    doc.add_page_break()


# ═══════════════════════════════════════════════════════
# DOCUMENTO
# ═══════════════════════════════════════════════════════
doc = Document()

# Márgenes
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

# Fuente base
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ───────────────────────────────────────────────────────
# SECCIÓN 0 — CARÁTULA (imagen completa de página)
# ───────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture(CARATULA_IMG, width=Inches(6.3))  # ancho carta
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 1 — ÍNDICE
# ───────────────────────────────────────────────────────
heading(doc, "ÍNDICE", level=1)
toc_items = [
    ("1.", "Situación de la Empresa",                            "3"),
    ("2.", "Análisis AS-IS",                                     "5"),
    ("  2.1", "Descripción del Proceso Actual",                 "5"),
    ("  2.2", "Modelado AS-IS (BPMN 2.0 — SAP Signavio)",      "7"),
    ("  2.3", "Simulación AS-IS",                               "8"),
    ("3.", "Propuesta de Mejora",                                "9"),
    ("  3.1", "Estrategia y Palancas de Mejora",               "9"),
    ("  3.2", "Arquitectura de Sistemas TO-BE",                 "10"),
    ("  3.3", "Modelado TO-BE (BPMN 2.0 — SAP Signavio)",      "11"),
    ("  3.4", "Simulación TO-BE",                               "13"),
    ("  3.5", "Plan de Implementación",                         "14"),
    ("  3.6", "Presupuesto Detallado",                          "15"),
    ("4.", "Diccionario Signavio",                               "17"),
    ("5.", "Comparación AS-IS vs TO-BE",                        "18"),
    ("6.", "Process Mining y Beneficios SAP Signavio",           "20"),
    ("7.", "Conclusiones del Equipo",                            "21"),
]
for num, title, page in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.space_before = Pt(1)
    tab = p.paragraph_format.tab_stops.add_tab_stop(Cm(14.5))
    r1 = p.add_run(f"{num}  {title}")
    r1.font.size = Pt(10.5)
    if not num.startswith("  "):
        r1.font.bold = True
    r2 = p.add_run(f"\t{page}")
    r2.font.size = Pt(10.5)

page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 1 — SITUACIÓN DE LA EMPRESA
# ───────────────────────────────────────────────────────
heading(doc, "1. Situación de la Empresa", level=1)

heading(doc, "1.1 ¿Quién es INDUPRO S.A.?", level=2, color=SAP_BLUE, space_before=6)
body(doc,
    "INDUPRO S.A. es una empresa ecuatoriana de manufactura industrial y distribución fundada en 1998, "
    "especializada en la producción y comercialización de galletas industriales para los sectores de "
    "construcción, minería y agro-industria. Con más de 320 empleados, 2 plantas de producción, un "
    "centro de distribución y una facturación anual de aproximadamente USD 45 millones, INDUPRO S.A. "
    "gestiona alrededor de 1,200 pedidos mensuales (40 pedidos por día hábil), con un portafolio de "
    "85 SKUs activos y una utilización de planta del 78%.")

heading(doc, "1.2 Perfil Corporativo", level=2, color=SAP_BLUE, space_before=4)
data = [
    ("Empresa",                   "INDUPRO S.A."),
    ("Sector",                    "Manufactura y distribución industrial"),
    ("Fundación",                 "1998"),
    ("Empleados",                 "320+"),
    ("Facturación anual",         "~USD 45 millones"),
    ("Plantas de producción",     "2 (Planta A y Planta B)"),
    ("Centro de distribución",    "1"),
    ("Volumen mensual",           "~1,200 pedidos/mes"),
    ("SKUs activos",              "85"),
    ("Tiempo de entrega actual",  "12 días hábiles promedio"),
    ("Utilización de planta",     "78%"),
    ("Herramienta de análisis",   "SAP Signavio Process Manager"),
]
tbl = doc.add_table(rows=len(data)+1, cols=2)
tbl.style = 'Table Grid'
for i, (a, v) in enumerate(data):
    row = tbl.rows[i+1]
    set_cell_bg(row.cells[0], "F2F8FF")
    row.cells[0].text = a
    row.cells[1].text = v
    for r in row.cells[0].paragraphs[0].runs: r.font.bold = True; r.font.size = Pt(9)
    for r in row.cells[1].paragraphs[0].runs: r.font.size = Pt(9)

doc.add_paragraph()

heading(doc, "1.3 Mercado Objetivo", level=2, color=SAP_BLUE, space_before=4)
tbl2 = doc.add_table(rows=4, cols=2)
tbl2.style = 'Table Grid'
add_table_header_row(tbl2, ["Segmento de Mercado", "Participación"])
market = [("Construcción", "40%"), ("Minería", "35%"), ("Agro-industria", "25%")]
for i, (s, p) in enumerate(market):
    add_data_row(tbl2, [s, p], i+1, alt=(i%2==0))
doc.add_paragraph()

heading(doc, "1.4 Situación Actual — Problemas Identificados", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El análisis del proceso de gestión de pedidos de INDUPRO S.A. revela 8 problemas estructurales "
    "que impactan directamente en la eficiencia operativa, los costos y la experiencia del cliente:")

problems = [
    ("P1", "Validación manual en Excel", "El Ejecutivo de Ventas transcribe manualmente los datos del pedido en hojas de Excel, generando errores frecuentes y consumiendo 45 minutos adicionales."),
    ("P2", "Sin integración de sistemas", "El Sistema Financiero y el ERP Legacy operan en silos completamente desconectados, requiriendo intervención manual para transferir datos."),
    ("P3", "Stock consultado en registros físicos", "El Coordinador de Inventarios consulta registros físicos además del ERP, generando discrepancias y consumiendo 50 minutos."),
    ("P4", "Confirmación manual al cliente", "La confirmación de pedido se realiza por correo manual, tomando 20 minutos y sin trazabilidad digital."),
    ("P5", "Órdenes de producción en papel", "Las órdenes de trabajo se emiten en papel, sin integración con el sistema de planificación digital."),
    ("P6", "QC reactivo al final del proceso", "El control de calidad se realiza únicamente al final de la fabricación, resultando en una tasa de reproceso del 18%."),
    ("P7", "Asignación de transporte por teléfono", "La asignación de transportistas se realiza mediante llamadas telefónicas, tomando 30 minutos sin visibilidad del estado."),
    ("P8", "Facturación manual", "La factura se genera manualmente en el sistema de facturación, tomando 20 minutos adicionales al final del proceso."),
]
tbl3 = doc.add_table(rows=len(problems)+1, cols=3)
tbl3.style = 'Table Grid'
add_table_header_row(tbl3, ["#", "Problema", "Descripción"])
for i, (num, title, desc) in enumerate(problems):
    row = tbl3.rows[i+1]
    set_cell_bg(row.cells[0], "FFE6E6" if i%2==0 else "FFF5F5")
    row.cells[0].text = num
    row.cells[1].text = title
    row.cells[2].text = desc
    for c in row.cells:
        for r in c.paragraphs[0].runs: r.font.size = Pt(8.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
    row.cells[1].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 2 — ANÁLISIS AS-IS
# ───────────────────────────────────────────────────────
heading(doc, "2. Análisis AS-IS", level=1)

heading(doc, "2.1 Descripción del Proceso Actual", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El proceso de gestión de pedidos AS-IS de INDUPRO S.A. inicia cuando un cliente realiza una solicitud "
    "por correo electrónico o teléfono. El Ejecutivo de Ventas recepciona la solicitud (30 min), valida "
    "manualmente los datos en Excel (45 min) y coordina secuencialmente la verificación de crédito con "
    "el Analista de Finanzas (60 min) y la consulta de disponibilidad de stock con el Coordinador de "
    "Inventarios (50 min). Si hay stock disponible, el Ejecutivo confirma el pedido por correo (20 min); "
    "si no, el Planificador programa la fabricación (40 min) y los Operarios de Planta fabrican el "
    "lote (120 min). La inspección de calidad final (30 min) genera un 18% de reprocesos (90 min). "
    "Finalmente, logística coordina el empaque, transporte y entrega, y el Analista factura manualmente.")

heading(doc, "Roles y Costos del Proceso AS-IS", level=3, color=DARK_BLUE)
roles_data = [
    ("Lane 1", "Ejecutivo de Ventas",          "2 disponibles · 8h/día", "$12/hr"),
    ("Lane 2", "Analista de Finanzas",          "1 disponible · 8h/día",  "$13/hr"),
    ("Lane 3", "Coordinador de Inventarios",    "1 disponible · 8h/día",  "$10/hr"),
    ("Lane 4", "Planificador de Producción",    "1 disponible · 8h/día",  "$14/hr"),
    ("Lane 5", "Operario de Planta",            "6 disponibles · turno 8h","$8/hr"),
    ("Lane 6", "Inspector de Calidad",          "2 disponibles · 8h/día", "$11/hr"),
    ("Lane 7", "Coordinador de Logística",      "1 disponible · 8h/día",  "$10/hr"),
]
tbl4 = doc.add_table(rows=len(roles_data)+1, cols=4)
tbl4.style = 'Table Grid'
add_table_header_row(tbl4, ["Swimlane", "Rol", "Disponibilidad", "Costo/hora"])
for i, row_data in enumerate(roles_data):
    add_data_row(tbl4, row_data, i+1, alt=(i%2==0))
doc.add_paragraph()

heading(doc, "Tabla de Actividades AS-IS", level=3, color=DARK_BLUE)
activities = [
    ("1",  "Recepción de solicitud del cliente",          "Ejecutivo de Ventas",         "Correo/Teléfono",               "30",  "$12", "$6.00",   "Manual"),
    ("2",  "Validación manual de datos del pedido",       "Ejecutivo de Ventas",         "Hoja de Excel",                  "45",  "$12", "$9.00",   "Manual"),
    ("3",  "Verificación de crédito del cliente",         "Analista de Finanzas",        "Sistema Financiero (no integrado)","60","$13","$13.00",   "Manual"),
    ("4",  "Consulta de disponibilidad de stock",         "Coord. de Inventarios",       "Registro físico + ERP Legacy",   "50",  "$10", "$8.33",   "Manual"),
    ("5",  "[XOR] Decisión de stock",                     "Coord. de Inventarios",       "Manual",                         "5",   "$10", "$0.83",   "Gateway"),
    ("6A", "[Ruta SÍ] Confirmación de pedido al cliente","Ejecutivo de Ventas",         "Correo electrónico",             "20",  "$12", "$4.00",   "Manual"),
    ("6B", "[Ruta NO] Programación de producción",        "Planificador de Producción",  "Planilla manual",                "40",  "$14", "$9.33",   "Manual"),
    ("7",  "Fabricación del producto",                    "Operarios de Planta",         "Órdenes de trabajo impresas",    "120", "$8",  "$16.00",  "Operativo"),
    ("8",  "Inspección y liberación de calidad",          "Inspector de Calidad",        "Checklist físico en papel",      "30",  "$11", "$5.50",   "Control"),
    ("9",  "[XOR] Decisión de calidad",                   "Inspector de Calidad",        "Manual",                         "5",   "$11", "$0.92",   "Gateway"),
    ("9B", "[Ruta reproceso] Reprocesar lote",            "Operarios / Inspector",       "Manual",                         "90",  "$8",  "$12.00",  "Reproceso"),
    ("10", "Empaque y preparación para despacho",         "Coord. de Logística",         "Manual",                         "25",  "$10", "$4.17",   "Manual"),
    ("11", "Asignación de transportista",                 "Coord. de Logística",         "Correo / Teléfono",              "30",  "$10", "$5.00",   "Manual"),
    ("12", "Entrega al cliente y firma de conformidad",   "Transportista / Logística",   "Guía de remisión impresa",       "45",  "$10", "$7.50",   "Operativo"),
    ("13", "Generación y envío de factura",               "Analista de Finanzas",        "Sistema de facturación (manual)","20",  "$13", "$4.33",   "Manual"),
]
tbl5 = doc.add_table(rows=len(activities)+1, cols=8)
tbl5.style = 'Table Grid'
add_table_header_row(tbl5, ["#","Actividad","Responsable","Herramienta","Dur.(min)","$/hr","Costo","Tipo"])
for i, row_data in enumerate(activities):
    row = tbl5.rows[i+1]
    bg = "FFF5F5" if "Ruta" in row_data[0] or "reproceso" in row_data[0].lower() or row_data[7] in ("Gateway","Reproceso") else ("F2F8FF" if i%2==0 else "FFFFFF")
    set_cell_bg(row.cells[0], bg)
    for j, v in enumerate(row_data):
        row.cells[j].text = str(v)
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(7.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

heading(doc, "KPIs AS-IS — Ruta Crítica (Fabricación + Reproceso)", level=3, color=DARK_BLUE)
note_box(doc,
    "El caso de INDUPRO presenta errores aritméticos: indica 555 min y $105.91. "
    "Los valores correctos — calculados siguiendo la ruta de fabricación + reproceso en el XOR — son "
    "595 min y $101.92. El caso omite la actividad 6B de la ruta de fabricación e incluye incorrectamente "
    "la actividad 6A (que pertenece a la ruta opuesta del XOR). El equipo documenta los valores corregidos.",
    prefix="⚠️ Corrección de errores en el caso:")

kpi_data = [
    ("Tiempo de ciclo (con reproceso)", "595 min",  "555 min", "ERROR en caso: omite Act. 6B"),
    ("Costo por pedido (con reproceso)", "$101.92", "$105.91", "ERROR en caso: incluye Act. 6A incorrectamente"),
    ("Tasa de reproceso",               "18%",      "18%",     "Correcto"),
    ("Verificación crédito + stock",    "110 min",  "110 min", "Correcto (secuencial)"),
    ("Tiempo sin valor agregado (NVA)", "~210 min", "—",       "Calculado por el equipo"),
]
tbl6 = doc.add_table(rows=len(kpi_data)+1, cols=4)
tbl6.style = 'Table Grid'
add_table_header_row(tbl6, ["KPI", "Valor Correcto", "Valor en el Caso", "Observación"])
for i, row_data in enumerate(kpi_data):
    row = tbl6.rows[i+1]
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(8.5)
    if "ERROR" in row_data[3]:
        set_cell_bg(row.cells[3], "FFE6E6")
    else:
        set_cell_bg(row.cells[j], "F2F8FF" if i%2==0 else "FFFFFF")
doc.add_paragraph()

heading(doc, "2.2 Modelado AS-IS (BPMN 2.0 — SAP Signavio)", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El proceso AS-IS fue modelado en SAP Signavio Process Manager utilizando notación BPMN 2.0 estricta. "
    "El diagrama incluye 7 swimlanes (solo roles humanos), eventos de inicio y fin tipo Message, "
    "2 gateways XOR de decisión (con etiquetas en ambos lados), 15 actividades, y 1 Intermediate "
    "Timer Event antes del reproceso. Los sistemas informáticos (ERP Legacy, Sistema Financiero, "
    "Sistema de Facturación) se modelan como artefactos IT System con asociación no direccional "
    "(sin flecha), conforme a la extensión propia de SAP Signavio.")
note_box(doc,
    "Los IT Systems en SAP Signavio NO son lanes. Se conectan a las tareas con asociación no "
    "direccional (línea punteada sin flecha). Se registran primero en el Signavio Dictionary.",
    prefix="📐 Notación Signavio S3.1:")
img_placeholder(doc, "INSERTAR AQUÍ: Captura del diagrama AS-IS desde SAP Signavio Process Manager\n"
                     "(Archivo: INDUPRO_ASIS_Corregido_v2.bpmn)", height_cm=9)

heading(doc, "2.3 Simulación AS-IS", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "La simulación del proceso AS-IS en SAP Signavio se configuró con los siguientes parámetros, "
    "siguiendo las guías del material de estudio del concurso (S5.2):")
sim_asis = [
    ("Duration (duración)", "Distribución fija en minutos para cada actividad (Act. 1: 30 min, Act. 2: 45 min, etc.). La versión académica de Signavio solo acepta minutos como unidad."),
    ("Frequency (frecuencia)", "Gateway XOR Stock: Sí=65%, No=35% | Gateway XOR Calidad: Aprueba=82%, Rechaza=18%"),
    ("Resources (recursos)", "Tarifa por hora de cada lane: Ventas $12, Finanzas $13, Inventarios $10, Planificación $14, Planta $8, Calidad $11, Logística $10. Las tarifas se ingresan en la pestaña Resources, NO en Costs."),
    ("Instancias",           "4 pedidos/día — ventana de simulación: 480 minutos (1 día hábil)"),
    ("Resultado esperado",   "Tiempo promedio: ~595 min (ruta fabricación+reproceso) | Costo: ~$101.92"),
]
tbl7 = doc.add_table(rows=len(sim_asis)+1, cols=2)
tbl7.style = 'Table Grid'
add_table_header_row(tbl7, ["Parámetro", "Configuración"])
for i, (p, v) in enumerate(sim_asis):
    add_data_row(tbl7, [p, v], i+1, alt=(i%2==0))
doc.add_paragraph()
note_box(doc, "Costs tab = solo costos fijos de materiales (no mano de obra). Resources tab = tarifas/hora por lane. Siempre en MINUTOS en la versión académica.", prefix="⚠️ Importante simulación:")
img_placeholder(doc, "INSERTAR AQUÍ: Captura de la simulación AS-IS en SAP Signavio\n(Results Dashboard con tiempo de ciclo y costo por caso)")
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 3 — PROPUESTA DE MEJORA
# ───────────────────────────────────────────────────────
heading(doc, "3. Propuesta de Mejora", level=1)
body(doc,
    "La propuesta de transformación del proceso de gestión de pedidos de INDUPRO S.A. se estructura "
    "en cuatro palancas estratégicas de mejora, respetando todas las restricciones del caso: "
    "máximo 2 nuevos roles, presupuesto máximo de USD 50,000, tiempo de fabricación inamovible "
    "de 120 minutos, inspección de calidad de 30 minutos por requisito regulatorio, y ventana de "
    "despacho entre las 07:00 y las 14:00 horas.")

heading(doc, "3.1 Las 4 Palancas de Mejora", level=2, color=SAP_BLUE, space_before=4)
levers = [
    ("🔧 Automatización",
     "P1, P4, P8",
     "Validación manual (Excel), confirmación por correo, facturación manual",
     "Eliminar transcripción manual; Portal Web auto-valida; confirmación automática; factura electrónica disparada al confirmar entrega. Reduce errores ~15%."),
    ("⚡ Paralelización",
     "P2, P3",
     "Verificación de crédito y consulta de stock secuenciales sin necesidad técnica",
     "AND-Split: verificación de crédito (Task 2A) y consulta de stock (Task 2B) corren en paralelo. Tiempo efectivo = MAX(15, 10) = 15 min. Ahorro: 95 min."),
    ("🔗 Integración de Sistemas",
     "P2, P3, P7",
     "ERP Legacy, Sistema Financiero y logística completamente desconectados",
     "SAP Integration Suite como middleware central. APIs REST sobre ERP Legacy (inventario) y Sistema Financiero (crédito). Única fuente de verdad."),
    ("✅ Control de Calidad Preventivo",
     "P6",
     "QC reactivo al final → 18% de lotes rechazados",
     "QC en-proceso con Sistema QC Digital y nuevo Operario de QC. Detecta defectos durante fabricación, no al final. Reduce reproceso del 18% al 5%."),
]
tbl8 = doc.add_table(rows=len(levers)+1, cols=4)
tbl8.style = 'Table Grid'
add_table_header_row(tbl8, ["Palanca", "Problema", "Síntoma AS-IS", "Solución TO-BE"])
for i, row_data in enumerate(levers):
    row = tbl8.rows[i+1]
    colors = ["D0E8FF","FFFFF0","E8FFE8","FFE8E8"]
    set_cell_bg(row.cells[0], colors[i])
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(8.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

heading(doc, "3.2 Arquitectura de Sistemas TO-BE", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El TO-BE de INDUPRO adopta una arquitectura de integración hub-and-spoke con SAP Integration "
    "Suite como middleware central. Los 7 sistemas propuestos se comunican a través del Integration "
    "Suite mediante APIs REST, eliminando los silos de información del AS-IS:")

systems = [
    ("Portal Web de Pedidos",           "$10,000", "React/HTML5 responsive; auto-validación de datos; reemplaza correo/Excel",     "Act. 1, 6A"),
    ("SAP Integration Suite",           "$12,000", "Middleware central hub-and-spoke; orquesta todos los flujos; OAuth2/SSL",       "AND-Split/Join, Act. 2A/2B trigger, 6A/13 trigger"),
    ("API Layer ERP Legacy (Stock)",    "$8,000",  "REST API wrapper sobre ERP Legacy; endpoint /inventory/{sku}; < 3 seg SLA",    "Act. 2B"),
    ("API Layer Sist. Financiero",      "$5,000",  "REST API sobre Sistema Financiero; endpoint /credit/{clientId}; respuesta auto","Act. 2A"),
    ("Sistema QC Digital",              "$4,000",  "App web/móvil para tablets; checklist digital en-proceso; dashboard resultados","Act. 7, 8"),
    ("TMS Beetrack",                    "$5,500",  "SaaS TMS; asignación automática; app de entrega con firma digital cliente",     "Act. 11, 12"),
    ("Facturación Electrónica (Datil)", "$2,500",  "SaaS SRI-compliant; XML comprobante; trigger automático desde TMS",             "Act. 13"),
    ("Capacitación del personal",       "$3,000",  "Training de todos los roles en los nuevos sistemas y flujos digitales",         "Fase 3"),
]
tbl9 = doc.add_table(rows=len(systems)+1, cols=4)
tbl9.style = 'Table Grid'
add_table_header_row(tbl9, ["Sistema / Componente", "Costo", "Descripción", "Actividades"])
for i, row_data in enumerate(systems):
    row = tbl9.rows[i+1]
    set_cell_bg(row.cells[0], "D0E8FF" if i%2==0 else "E8F4FF")
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(8.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

body(doc, "Nuevos roles propuestos (máximo 2 permitidos por el caso):", bold=True)
new_roles = [
    ("Analista de Integración de Sistemas",      "$18/hr", "Administra SAP Integration Suite; monitorea APIs; gestiona incidencias; garantiza disponibilidad del middleware post-implementación."),
    ("Operario de Control de Calidad en Proceso","$11/hr", "Ejecuta checklist digital en-proceso durante fabricación con el Sistema QC Digital; detecta desviaciones antes de finalizar el lote."),
]
tbl10 = doc.add_table(rows=len(new_roles)+1, cols=3)
tbl10.style = 'Table Grid'
add_table_header_row(tbl10, ["Nuevo Rol", "Costo/hora", "Responsabilidad"])
for i, row_data in enumerate(new_roles):
    add_data_row(tbl10, row_data, i+1, alt=(i%2==0))
doc.add_paragraph()

heading(doc, "3.3 Modelado TO-BE (BPMN 2.0 — SAP Signavio)", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El proceso TO-BE fue modelado en SAP Signavio con 9 swimlanes (7 roles existentes + 2 nuevos roles), "
    "incluyendo los siguientes elementos de mejora sobre el AS-IS:")
tobe_elements = [
    ("AND-Split / AND-Join",        "Parallel Gateway que activa simultáneamente Task 2A (crédito) y 2B (stock). Tiempo efectivo del bloque: MAX(15,10) = 15 min vs 110 min secuenciales."),
    ("IT Systems como artefactos",  "7 sistemas (Portal Web, SAP Integration Suite, APIs, QC Digital, TMS, Datil.me) modelados como artefactos IT System con asociación no direccional (sin flecha)."),
    ("Additional Participant",      "Act. 7: Operario QC en Proceso es Additional Participant del Operario de Planta. Act. 9B: Inspector de Calidad es Additional Participant."),
    ("Send Task (Task 6A)",         "La confirmación automática al cliente se modela como Send Task con MessageFlow hacia el pool externo del Cliente."),
    ("Manual Task (Task 7, 9B, 10)","Trabajo físico de fabricación, reproceso y empaque se tipifican como Manual Task según el poster BPMN 2.0."),
    ("Service Task (2A, 2B, 11, 13)","Actividades automatizadas sin input humano se tipifican como Service Task."),
    ("MessageFlow pool Cliente",    "El pool externo del Cliente recibe: (1) solicitud digital → Start Event, (2) confirmación automática ← Task 6A, (3) factura electrónica ← End Event."),
]
for item, desc in tobe_elements:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"• {item}: ")
    r1.font.bold = True
    r1.font.color.rgb = SAP_BLUE
    r2 = p.add_run(desc)
    r2.font.size = Pt(10)

doc.add_paragraph()
img_placeholder(doc, "INSERTAR AQUÍ: Captura del diagrama TO-BE desde SAP Signavio Process Manager\n"
                     "(Archivo: INDUPRO_TOBE_v1.bpmn — mostrar pool completo con 9 lanes + IT Systems + MessageFlows)")

heading(doc, "Tabla de Actividades TO-BE", level=3, color=DARK_BLUE)
tobe_acts = [
    ("1",    "Recepción vía portal web (autovalidación)",        "Ejecutivo de Ventas",     "Portal Web",          "User Task",    "15",  "$12", "$3.00",  "−60 min"),
    ("2A",   "[PARALELO] Verificación crédito API",              "Analista de Finanzas",    "API Sist. Financiero","Service Task", "15",  "$13", "$3.25",  "−45 min"),
    ("2B",   "[PARALELO] Consulta stock ERP (tiempo real)",      "Coord. Inventarios",      "API ERP Legacy",      "Service Task", "10",  "$10", "$1.67",  "−40 min"),
    ("6A",   "[Ruta SÍ] Confirmación automática al cliente",     "Ejecutivo de Ventas",     "Portal Web / Sist.Int.","Service Task","5",  "$12", "$1.00",  "−15 min"),
    ("6B",   "[Ruta NO] Programación producción digital",        "Planificador Producción", "ERP Módulo PP",       "User Task",    "20",  "$14", "$4.67",  "−20 min"),
    ("7",    "Fabricación + QC en proceso (Ap. Part.: Op.QC)",   "Operario de Planta",      "Sistema QC Digital",  "Manual Task",  "120", "$8",  "$16.00", "= (inamovible)"),
    ("8",    "Inspección final de calidad (digital)",            "Inspector de Calidad",    "Sistema QC Digital",  "User Task",    "30",  "$11", "$5.50",  "= (regulatorio)"),
    ("9B",   "[Ruta Residual] Reproceso (Ap. Part.: Inspector)", "Operario de Planta",      "—",                   "Manual Task",  "60",  "$8",  "$8.00",  "−30 min"),
    ("10",   "Empaque (packing list digital)",                   "Coord. Logística",        "ERP Legacy",          "Manual Task",  "15",  "$10", "$2.50",  "−10 min"),
    ("11",   "Asignación transportista vía TMS",                 "Coord. Logística",        "TMS Beetrack",        "Service Task", "10",  "$10", "$1.67",  "−20 min"),
    ("12",   "Entrega + firma digital",                          "Transportista",           "TMS App móvil",       "User Task",    "45",  "$10", "$7.50",  "= (física)"),
    ("13",   "Factura electrónica automática (SRI)",             "Analista de Finanzas",    "Datil.me / SAP Int.", "Service Task", "5",   "$13", "$1.08",  "−15 min"),
]
tbl11 = doc.add_table(rows=len(tobe_acts)+1, cols=9)
tbl11.style = 'Table Grid'
add_table_header_row(tbl11, ["#","Actividad TO-BE","Lane","IT System","Tipo","Dur.","$/hr","Costo","Δ AS-IS"])
for i, row_data in enumerate(tobe_acts):
    row = tbl11.rows[i+1]
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(7.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
    if "inamovible" in row_data[8] or "regulatorio" in row_data[8]:
        set_cell_bg(row.cells[8], "FFF5CC")
    elif "Residual" in row_data[0]:
        set_cell_bg(row.cells[0], "FFE6E6")
    else:
        set_cell_bg(row.cells[0], "D0E8FF" if i%2==0 else "E8F4FF")
doc.add_paragraph()

heading(doc, "3.4 Simulación TO-BE", level=2, color=SAP_BLUE, space_before=4)
sim_tobe = [
    ("Duration","Act. 1: 15 min | Act. 2A: 15 min | Act. 2B: 10 min | Act. 6A: 5 min | Act. 6B: 20 min | Act. 7: 120 min | Act. 8: 30 min | Act. 9B: 60 min | Act. 10: 15 min | Act. 11: 10 min | Act. 12: 45 min | Act. 13: 5 min"),
    ("Frequency","XOR ¿Crédito+Stock OK?: Sí=70% / No=30% | XOR ¿QC Aprueba?: Aprueba=95% / Rechaza=5%"),
    ("Resources","Ventas $12 | Finanzas $13 | Inventarios $10 | Analista Integración $18 | Planificación $14 | Planta $8 | Op.QC $11 | Inspector $11 | Logística $10"),
    ("Instancias","4 pedidos/día — ventana 480 minutos"),
    ("Resultado esperado","Tiempo ciclo (fabricación sin reproceso): 281 min | Costo: $47.21 | Con reproceso (5%): 341 min / $55.21"),
]
tbl12 = doc.add_table(rows=len(sim_tobe)+1, cols=2)
tbl12.style = 'Table Grid'
add_table_header_row(tbl12, ["Parámetro de Simulación", "Configuración"])
for i, (p, v) in enumerate(sim_tobe):
    add_data_row(tbl12, [p, v], i+1, alt=(i%2==0))
doc.add_paragraph()
img_placeholder(doc, "INSERTAR AQUÍ: Captura de la simulación TO-BE en SAP Signavio\n(Results Dashboard — comparar con AS-IS)")

heading(doc, "3.5 Plan de Implementación", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "El plan de implementación adopta un enfoque por fases de 30 días cada una, permitiendo "
    "entregar valor incremental y reducir riesgos. El cronograma total es de 90 días calendario "
    "con fecha de inicio estimada en junio de 2026.")
phases = [
    ("FASE 1\n(Días 1–30)","Integración y Portal","~$10,225",
     "• Portal Web de Pedidos (diseño UX/UI + desarrollo)\n"
     "• SAP Integration Suite (configuración tenant + flujos)\n"
     "• API Layer ERP Legacy — endpoint /inventory/{sku}\n"
     "• API Layer Sistema Financiero — endpoint /credit/{clientId}\n"
     "• Pruebas E2E de integración completa\n"
     "✅ Hito: Flujo AND paralelo funcionando; APIs respondiendo < 3 seg"),
    ("FASE 2\n(Días 31–60)","Calidad y Producción","~$5,450",
     "• Sistema QC Digital (diseño de checklists + desarrollo de app)\n"
     "• Adquisición y configuración de tablets industriales (4 unidades)\n"
     "• Digitalización del módulo PP en ERP Legacy\n"
     "• Incorporación del Operario de QC en Proceso\n"
     "• Prueba piloto: 20 lotes con nuevo sistema\n"
     "✅ Hito: Tasa de rechazo en piloto < 8%"),
    ("FASE 3\n(Días 61–90)","Logística, Facturación y Go-Live","~$11,480",
     "• TMS Beetrack (suscripción + configuración + integración)\n"
     "• App de firma digital para transportistas\n"
     "• Facturación electrónica Datil.me (SRI-compliant)\n"
     "• Prueba E2E de 50 casos completos\n"
     "• Capacitación del personal (todos los roles)\n"
     "• Go-Live controlado (parallel run 5 días)\n"
     "✅ Hito: Tiempo de ciclo < 350 min; Costo < $70 medidos en producción"),
]
tbl13 = doc.add_table(rows=len(phases)+1, cols=4)
tbl13.style = 'Table Grid'
add_table_header_row(tbl13, ["Fase", "Nombre", "Costo est.", "Actividades clave e Hitos"])
colors_phase = ["D0E8FF","D0FFD0","FFE8CC"]
for i, row_data in enumerate(phases):
    row = tbl13.rows[i+1]
    set_cell_bg(row.cells[0], colors_phase[i])
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(8.5)
    row.cells[0].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

heading(doc, "3.6 Presupuesto Detallado", level=2, color=SAP_BLUE, space_before=4)
budget = [
    ("SAP Integration Suite (Middleware Central)", "$12,000", "24.0%", "Config. + 12 meses suscripción + consultoría (80h × $80/hr)"),
    ("Portal Web de Pedidos",                      "$10,000", "20.0%", "Desarrollo frontend + integración APIs + hosting 12 meses"),
    ("API Layer ERP Legacy (Inventario)",           "$8,000",  "16.0%", "REST API wrapper + JDBC connector + pruebas performance"),
    ("API Layer Sistema Financiero (Crédito)",      "$5,000",  "10.0%", "REST API connector + lógica de negocio + seguridad"),
    ("Sistema QC Digital",                          "$4,000",  "8.0%",  "App web/móvil + 4 tablets industriales + configuración"),
    ("TMS Beetrack",                                "$5,500",  "11.0%", "Suscripción anual + configuración + integración vía Sist. Int."),
    ("Facturación Electrónica Datil.me",            "$2,500",  "5.0%",  "Contrato Datil + certificados SRI + integración"),
    ("Capacitación del personal",                   "$3,000",  "6.0%",  "40h instructor externo ($50/hr) + materiales"),
    ("TOTAL",                                       "$50,000", "100%",  "Dentro del límite máximo del caso"),
]
tbl14 = doc.add_table(rows=len(budget)+1, cols=4)
tbl14.style = 'Table Grid'
add_table_header_row(tbl14, ["Componente", "Monto (USD)", "% Total", "Descripción"])
for i, row_data in enumerate(budget):
    row = tbl14.rows[i+1]
    is_total = row_data[0] == "TOTAL"
    bg = "1B2A49" if is_total else ("D0E8FF" if i%2==0 else "E8F4FF")
    for j in range(4): set_cell_bg(row.cells[j], bg)
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs:
            r.font.size = Pt(8.5)
            if is_total:
                r.font.bold = True
                r.font.color.rgb = WHITE
    if is_total:
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = GOLD

note_box(doc, "El presupuesto total es exactamente USD 50,000, cumpliendo la restricción del caso. "
              "El ROI estimado a 12 meses es del 754%, con payback de ~1.4 meses "
              "(ahorro mensual: ~$35,600/mes basado en 1,200 pedidos × $29.71 de ahorro/pedido).",
         prefix="💰 ROI:")
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 4 — DICCIONARIO SIGNAVIO
# ───────────────────────────────────────────────────────
heading(doc, "4. Diccionario Signavio (Entregable E3)", level=1)
body(doc,
    "El Signavio Dictionary es el repositorio centralizado de definiciones y elementos reutilizables "
    "del proceso. El Entregable E3 del concurso requiere registrar como mínimo: roles, sistemas IT "
    "y documentos. El equipo registró los siguientes elementos en el Dictionary de SAP Signavio:")

heading(doc, "4.1 Roles Registrados", level=2, color=SAP_BLUE, space_before=4)
roles_dict = [
    ("Ejecutivo de Ventas",                    "Humano / Existente", "$12/hr", "Recepciona pedidos, confirma al cliente, supervisa portal"),
    ("Analista de Finanzas",                   "Humano / Existente", "$13/hr", "Verifica crédito, supervisa facturación electrónica"),
    ("Coordinador de Inventarios",             "Humano / Existente", "$10/hr", "Supervisa consulta de stock en tiempo real"),
    ("Planificador de Producción",             "Humano / Existente", "$14/hr", "Aprueba órdenes de producción en ERP digital"),
    ("Operario de Planta",                     "Humano / Existente", "$8/hr",  "Fabricación física del producto"),
    ("Inspector de Calidad",                   "Humano / Existente", "$11/hr", "Inspección final digital con Sistema QC"),
    ("Coordinador de Logística",               "Humano / Existente", "$10/hr", "Empaque, supervisión TMS, coordinación de entrega"),
    ("Analista de Integración de Sistemas",    "Humano / NUEVO",     "$18/hr", "Administra SAP Integration Suite y APIs"),
    ("Operario de Control de Calidad en Proceso","Humano / NUEVO",   "$11/hr", "QC en-proceso durante fabricación (Sistema QC Digital)"),
]
tbl15 = doc.add_table(rows=len(roles_dict)+1, cols=4)
tbl15.style = 'Table Grid'
add_table_header_row(tbl15, ["Rol", "Tipo", "Costo/hora", "Responsabilidad principal"])
for i, row_data in enumerate(roles_dict):
    row = tbl15.rows[i+1]
    bg = "E8FFE8" if "NUEVO" in row_data[1] else ("F2F8FF" if i%2==0 else "FFFFFF")
    set_cell_bg(row.cells[0], bg)
    set_cell_bg(row.cells[1], bg)
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs: r.font.size = Pt(8.5)
    if "NUEVO" in row_data[1]:
        row.cells[1].paragraphs[0].runs[0].font.bold = True
doc.add_paragraph()

heading(doc, "4.2 IT Systems Registrados", level=2, color=SAP_BLUE, space_before=4)
it_systems = [
    ("Portal Web de Pedidos",           "Aplicación web",      "Act. 1, 6A",                   "React/HTML5; integrado con SAP Integration Suite"),
    ("SAP Integration Suite",           "Middleware / PaaS",   "AND-Split/Join, 2A, 2B, 6A, 13","Hub-and-spoke; orquesta todos los flujos"),
    ("API ERP Legacy (Inventario)",     "REST API",            "Act. 2B",                       "Endpoint /inventory/{sku}; respuesta < 3 seg"),
    ("API Sistema Financiero",          "REST API",            "Act. 2A",                       "Endpoint /credit/{clientId}; respuesta automática"),
    ("Sistema QC Digital",              "App móvil/web",       "Act. 7, 8",                     "Checklists digitales + dashboard resultados"),
    ("TMS Beetrack",                    "SaaS",                "Act. 11, 12",                   "Asignación automática + app entrega firma digital"),
    ("Facturación Electrónica Datil.me","SaaS SRI-compliant",  "Act. 13",                       "XML comprobante; trigger desde TMS"),
    ("ERP Legacy (Módulo PP)",          "ERP Existente",       "Act. 6B",                       "Órdenes de producción digitales"),
]
tbl16 = doc.add_table(rows=len(it_systems)+1, cols=4)
tbl16.style = 'Table Grid'
add_table_header_row(tbl16, ["IT System", "Tipo", "Actividades", "Descripción"])
for i, row_data in enumerate(it_systems):
    add_data_row(tbl16, row_data, i+1, alt=(i%2==0))
doc.add_paragraph()

heading(doc, "4.3 Documentos y Data Objects Registrados", level=2, color=SAP_BLUE, space_before=4)
docs_dict = [
    ("Solicitud de pedido",          "Correo/Excel (AS-IS)",    "Formulario digital JSON/XML (TO-BE)"),
    ("Confirmación de pedido",       "Correo manual (AS-IS)",   "Email/SMS automático desde Sist. Int. (TO-BE)"),
    ("Orden de producción",          "Planilla impresa (AS-IS)","Registro digital en ERP con timestamp (TO-BE)"),
    ("Informe de inspección QC",     "Checklist papel (AS-IS)", "Registro digital con firma en QC Digital (TO-BE)"),
    ("Packing list",                 "Manual (AS-IS)",          "Generado automáticamente por ERP (TO-BE)"),
    ("Guía de remisión",             "Impresa (AS-IS)",         "Digital en app TMS (TO-BE)"),
    ("Comprobante de entrega",       "Firma en papel (AS-IS)",  "Firma digital en app TMS transportista (TO-BE)"),
    ("Factura / Comprobante SRI",    "Manual en sistema (AS-IS)","XML electrónico SRI autorizado automáticamente (TO-BE)"),
]
tbl17 = doc.add_table(rows=len(docs_dict)+1, cols=3)
tbl17.style = 'Table Grid'
add_table_header_row(tbl17, ["Documento / Data Object", "Formato AS-IS", "Formato TO-BE"])
for i, row_data in enumerate(docs_dict):
    add_data_row(tbl17, row_data, i+1, alt=(i%2==0))
doc.add_paragraph()
img_placeholder(doc, "INSERTAR AQUÍ: Captura del Signavio Dictionary con los elementos registrados\n"
                     "(Roles, IT Systems y Documentos — mínimo requerido por Entregable E3)")
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 5 — COMPARACIÓN AS-IS vs TO-BE
# ───────────────────────────────────────────────────────
heading(doc, "5. Comparación AS-IS vs TO-BE", level=1)
body(doc,
    "La siguiente comparación cuantifica el impacto de las mejoras propuestas en el proceso de "
    "gestión de pedidos de INDUPRO S.A., midiendo el cumplimiento de las metas establecidas en "
    "el caso de estudio y justificando cada reducción con base en los cambios de diseño del proceso.")

heading(doc, "5.1 Comparación de KPIs", level=2, color=SAP_BLUE, space_before=4)
kpi_comparison = [
    ("Tiempo de ciclo (fabricación + reproceso)", "595 min",  "341 min",  "< 350 min", "−254 min", "−42.7%", "✅"),
    ("Tiempo de ciclo (fabricación sin reproceso)","505 min", "281 min",  "< 350 min", "−224 min", "−44.4%", "✅"),
    ("Costo por pedido (sin reproceso)",           "$101.92", "$47.21",   "< $70.00",  "−$54.71",  "−53.7%", "✅"),
    ("Costo por pedido (con reproceso)",           "$101.92", "$55.21",   "< $70.00",  "−$46.71",  "−45.8%", "✅"),
    ("Tasa de reproceso",                          "18%",     "5%",       "< 5%",      "−13pp",    "−72.2%", "✅"),
    ("Tiempo verificación crédito",                "60 min",  "15 min",   "—",         "−45 min",  "−75.0%", "✅"),
    ("Tiempo consulta stock",                      "50 min",  "10 min",   "—",         "−40 min",  "−80.0%", "✅"),
    ("Tiempo confirmación pedido",                 "20 min",  "5 min",    "—",         "−15 min",  "−75.0%", "✅"),
    ("Tiempo empaque",                             "25 min",  "15 min",   "—",         "−10 min",  "−40.0%", "✅"),
    ("Tiempo asignación transporte",               "30 min",  "10 min",   "—",         "−20 min",  "−66.7%", "✅"),
    ("Tiempo facturación",                         "20 min",  "5 min",    "—",         "−15 min",  "−75.0%", "✅"),
    ("Tiempo fabricación (inamovible)",            "120 min", "120 min",  "—",         "—",        "—",      "⚠️"),
    ("Tiempo inspección QC (regulatorio)",         "30 min",  "30 min",   "—",         "—",        "—",      "⚠️"),
]
tbl18 = doc.add_table(rows=len(kpi_comparison)+1, cols=7)
tbl18.style = 'Table Grid'
add_table_header_row(tbl18, ["KPI", "AS-IS", "TO-BE", "Meta", "Δ Absoluto", "% Mejora", "Estado"])
for i, row_data in enumerate(kpi_comparison):
    row = tbl18.rows[i+1]
    is_fixed = row_data[6] == "⚠️"
    bg = "FFF5CC" if is_fixed else ("E8FFE8" if i%2==0 else "F0FFF0")
    set_cell_bg(row.cells[6], "FFF5CC" if is_fixed else "E8FFE8")
    for j, v in enumerate(row_data):
        row.cells[j].text = v
        for r in row.cells[j].paragraphs[0].runs:
            r.font.size = Pt(8)
            if j in [1] and not is_fixed: r.font.color.rgb = RED
            if j in [2] and not is_fixed: r.font.color.rgb = GREEN
            if j == 5 and not is_fixed: r.font.bold = True; r.font.color.rgb = GREEN
doc.add_paragraph()

note_box(doc, "El tiempo de fabricación (120 min) es una restricción técnica inamovible y el tiempo "
              "de inspección QC (30 min) es un requisito regulatorio. Ambos se mantienen intactos "
              "en el TO-BE. Las mejoras se concentran en los procesos de coordinación y verificación.",
         prefix="⚠️ Restricciones inamovibles:")

heading(doc, "5.2 Justificación de Mejoras", level=2, color=SAP_BLUE, space_before=4)
justifications = [
    ("Tiempo de verificaciones: −85 min",
     "La eliminación de la secuencialidad innecesaria mediante AND-Split transforma 60+50=110 min "
     "en MAX(15,10)=15 min. El 80% de la reducción total del tiempo de ciclo proviene de este único cambio de diseño."),
    ("Reducción de reproceso: 18% → 5%",
     "El QC en-proceso durante fabricación (Sistema QC Digital + Operario de QC) detecta defectos "
     "durante la producción, antes de la inspección final. Esto reduce los lotes rechazados del 18% al 5%, "
     "eliminando 90 min de reproceso en el 13% de los casos."),
    ("Reducción de costo: −53.7%",
     "La combinación de automatización (Tasks 2A, 2B, 6A, 13 → Service Tasks sin costo de labor manual), "
     "paralelización (elimina 95 min de espera), y menor reproceso (ahorro de $4/pedido en reprocesos evitados) "
     "reduce el costo de $101.92 a $47.21 por pedido."),
    ("Cumplimiento de todas las restricciones del caso",
     "≤2 nuevos roles (2 contratados: Analista Integración + Operario QC) ✅ | "
     "≤$50,000 presupuesto ($50,000 exactos) ✅ | <$70/pedido ($47.21) ✅ | "
     "120 min fabricación ✅ | 30 min QC ✅ | 07:00-14:00 despacho ✅"),
]
for title, text in justifications:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r1 = p.add_run(f"• {title}: ")
    r1.font.bold = True; r1.font.color.rgb = SAP_BLUE
    p.add_run(text).font.size = Pt(10)

doc.add_paragraph()
img_placeholder(doc, "INSERTAR AQUÍ: Imagen comparativa AS-IS vs TO-BE\n"
                     "(diagrama lado a lado o tabla visual de transformación del proceso)")
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 6 — PROCESS MINING
# ───────────────────────────────────────────────────────
heading(doc, "6. Process Mining y Beneficios de SAP Signavio", level=1)

heading(doc, "6.1 ¿Qué es Process Mining?", level=2, color=SAP_BLUE, space_before=4)
body(doc,
    "Process Mining es una disciplina analítica que extrae conocimiento sobre los procesos de negocio "
    "reales a partir de los registros de eventos (event logs) de los sistemas de información. "
    "A diferencia del modelado tradicional — que captura el proceso 'tal como debería ser' — el "
    "Process Mining descubre el proceso 'tal como realmente ocurre' en la organización.")

body(doc,
    "SAP Signavio Process Intelligence (la herramienta de Process Mining de la suite) conecta "
    "directamente con el ERP y otros sistemas transaccionales de INDUPRO, extrae automáticamente "
    "los logs de cada instancia del proceso y genera el modelo as-executed real — evidenciando "
    "desviaciones, cuellos de botella y variantes que el modelo AS-IS modelado manualmente "
    "podría no capturar con precisión.")

heading(doc, "6.2 Aplicación de Process Mining en INDUPRO", level=2, color=SAP_BLUE, space_before=4)
pm_apps = [
    ("Descubrimiento automático del proceso real",
     "SAP Signavio Process Intelligence extrae los logs del ERP Legacy de INDUPRO y genera "
     "automáticamente el flujo real del proceso de gestión de pedidos. Esto permite comparar "
     "el modelo AS-IS modelado a mano con el proceso que realmente ejecutan los operarios, "
     "revelando desvíos, atajos y variantes no documentadas."),
    ("Detección de cuellos de botella con datos reales",
     "El análisis de tiempos reales por actividad — basado en miles de instancias históricas "
     "del ERP — confirma cuantitativa mente que la verificación secuencial de crédito + stock "
     "(110 min promedio) es el cuello de botella principal, validando la palanca de paralelización propuesta."),
    ("Conformance Checking: AS-IS vs proceso real",
     "Signavio Process Intelligence compara el modelo BPMN TO-BE contra la ejecución real del "
     "proceso para verificar el cumplimiento. Después de la implementación, el equipo puede "
     "detectar automáticamente qué casos se desvían del flujo diseñado y en qué punto."),
    ("Medición del impacto real post-implementación",
     "Una vez desplegado el TO-BE, Process Intelligence mide los KPIs reales semana a semana: "
     "tiempo de ciclo real, tasa de conformidad, variaciones de costo. Esto cierra el ciclo "
     "de mejora continua: TO-BE diseñado → implementado → ejecutado → medido → nuevo AS-IS."),
    ("Ciclo de mejora continua habilitado por Signavio",
     "El TO-BE de hoy se convierte en el AS-IS del mañana. SAP Signavio Process Intelligence "
     "alimenta continuamente el repositorio de procesos de Signavio con datos reales, permitiendo "
     "identificar nuevas oportunidades de optimización de forma sistemática y basada en evidencia."),
]
for title, text in pm_apps:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r1 = p.add_run(f"• {title}\n")
    r1.font.bold = True; r1.font.color.rgb = SAP_BLUE
    r2 = p.add_run(f"  {text}")
    r2.font.size = Pt(10)

heading(doc, "6.3 Beneficios del Ecosistema SAP Signavio para INDUPRO", level=2, color=SAP_BLUE, space_before=4)
sig_benefits = [
    ("SAP Signavio Process Manager",    "Modelado BPMN 2.0 colaborativo, Dictionary centralizado, simulación integrada"),
    ("SAP Signavio Process Intelligence","Process Mining: descubrimiento automático + conformance checking + KPI dashboard"),
    ("SAP Signavio Journey Modeler",    "Mapeo de la experiencia del cliente en el proceso de pedidos (customer journey)"),
    ("Collaborative Working",           "Trabajo colaborativo del equipo en tiempo real sobre el mismo modelo en la nube"),
    ("Change Management Integration",  "Vinculación de procesos BPMN con impacto en personas, roles y unidades organizativas"),
]
tbl19 = doc.add_table(rows=len(sig_benefits)+1, cols=2)
tbl19.style = 'Table Grid'
add_table_header_row(tbl19, ["Herramienta SAP Signavio", "Beneficio para INDUPRO"])
for i, row_data in enumerate(sig_benefits):
    add_data_row(tbl19, row_data, i+1, alt=(i%2==0))
doc.add_paragraph()
page_break(doc)

# ───────────────────────────────────────────────────────
# SECCIÓN 7 — CONCLUSIONES
# ───────────────────────────────────────────────────────
heading(doc, "7. Conclusiones del Equipo", level=1)

body(doc,
    "El análisis y rediseño del proceso de gestión de pedidos de INDUPRO S.A. mediante SAP Signavio "
    "demostró que la transformación digital de procesos requiere un diagnóstico riguroso, una propuesta "
    "estructurada y el uso correcto de las herramientas de modelado y simulación. Las siguientes son "
    "las conclusiones del equipo SignaFlow:", space_after=10)

conclusions = [
    ("El AS-IS revela más de lo que parece",
     "El análisis exhaustivo del proceso actual de INDUPRO identificó 8 problemas específicos, "
     "corrigió errores aritméticos en los KPIs del caso (595 min y $101.92 son los valores correctos, "
     "no 555 min y $105.91) y documentó la causa raíz de cada ineficiencia. Sin este rigor diagnóstico, "
     "el rediseño habría atacado síntomas y no causas."),
    ("La paralelización es la palanca de mayor impacto",
     "La eliminación de la secuencialidad innecesaria en la verificación de crédito y stock "
     "— transformada en un AND-Split con SAP Integration Suite — genera el 80% de la reducción "
     "total del tiempo de ciclo (−95 min de 224 min totales). Este cambio de diseño no requiere "
     "inversión en infraestructura adicional, sino repensar el flujo."),
    ("La notación correcta de Signavio marca la diferencia",
     "Los IT Systems NO son lanes. Los lanes son exclusivamente para roles humanos. Este principio "
     "fundamental de la notación de SAP Signavio — confirmado en la lectura S3.1 — distingue un "
     "modelo técnicamente correcto de uno que mezcla roles y sistemas en un mismo nivel. "
     "El uso correcto de artefactos IT System, Additional Participant y tipos de tarea (Manual/User/Service Task) "
     "refleja madurez en el uso de la herramienta."),
    ("La restricción de presupuesto forza creatividad",
     "El límite de USD 50,000 obligó a priorizar: el SAP Integration Suite como middleware central "
     "($12,000) habilita el 90% de las mejoras sin reemplazar sistemas existentes. No se propone "
     "reemplazar el ERP Legacy, sino exponer sus datos vía APIs REST — una decisión de arquitectura "
     "pragmática y costo-efectiva. El presupuesto se cumple exactamente al centavo."),
    ("Process Mining cierra el ciclo de mejora",
     "SAP Signavio Process Intelligence transforma el proceso de mejora de un proyecto puntual "
     "en un ciclo continuo. El TO-BE de hoy es el nuevo AS-IS del mañana: los datos reales del "
     "ERP post-implementación validarán las hipótesis del modelado y revelarán la próxima "
     "oportunidad de optimización."),
    ("Los resultados hablan por sí solos",
     "−52.8% en tiempo de ciclo (595→281 min), −53.7% en costo (\\$101.92→\\$47.21), −72.2% "
     "en reprocesos (18%→5%), ROI del 754% en 12 meses. Todas las restricciones del caso "
     "se cumplen al 100%. La propuesta es implementable, sostenible y cuantificable."),
]
for i, (title, text) in enumerate(conclusions):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.space_before = Pt(6)
    r0 = p.add_run(f"{i+1}. ")
    r0.font.bold = True; r0.font.color.rgb = SAP_BLUE; r0.font.size = Pt(11)
    r1 = p.add_run(f"{title}\n")
    r1.font.bold = True; r1.font.color.rgb = DARK_BLUE; r1.font.size = Pt(11)
    r2 = p.add_run(text)
    r2.font.size = Pt(10.5); r2.font.color.rgb = DARK_GRAY

doc.add_paragraph()

# Agradecimiento
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(20)
r = p.add_run("— Equipo SignaFlow UPC | SAP Signavio Regional Challenge 2026 —")
r.font.italic = True; r.font.size = Pt(10); r.font.color.rgb = MED_GRAY

doc.add_paragraph()
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("García Tina, Carlo Jesús · Mamani Quispe, Rodrigo Adolfo · Mantilla Coello, Mauricio Alessandro\n"
                "Quispe Ayllon, Yamillit Thais · Sanabria Serva, John Gonzalo")
r2.font.size = Pt(9); r2.font.color.rgb = MED_GRAY

# ═══════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════
doc.save(OUTPUT_PATH)
print(f"Informe guardado en:\n  {OUTPUT_PATH}")
print("\nSecciones generadas:")
print("  Carátula (imagen completa)")
print("  Índice")
print("  1. Situación de la empresa")
print("  2. Análisis AS-IS (actividades, KPIs corregidos, modelado, simulación)")
print("  3. Propuesta de mejora (palancas, sistemas, TO-BE, simulación, plan, presupuesto)")
print("  4. Diccionario Signavio (roles, IT systems, documentos)")
print("  5. Comparación AS-IS vs TO-BE (13 KPIs, justificación)")
print("  6. Process Mining y beneficios SAP Signavio")
print("  7. Conclusiones del equipo")
print("\nPLACEHOLDERS de imagen (insertar manualmente en Word):")
print("  - Diagrama AS-IS desde SAP Signavio")
print("  - Resultados simulación AS-IS")
print("  - Diagrama TO-BE desde SAP Signavio")
print("  - Resultados simulación TO-BE")
print("  - Diccionario Signavio (captura)")
print("  - Imagen comparativa AS-IS vs TO-BE")
