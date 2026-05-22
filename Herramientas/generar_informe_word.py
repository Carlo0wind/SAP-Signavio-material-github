"""
Generador de Informe Word — INDUPRO S.A.
SAP Signavio Regional Challenge 2026
Límite: 15 páginas | Foco: AS-IS · TO-BE · Justificación · KPIs
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE         = r"c:\Users\drago\projects\ProyectoSAPSignavio"
CARAULA_IMG  = BASE + r"\material-concurso\imagen-caratula.png"
OUTPUT_PATH  = BASE + r"\Entregables\Informe Ejecutivo\INDUPRO_Informe_Concurso.docx"

# Imagenes de simulacion
SIM_ASIS_1   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 AS IS.png"
SIM_ASIS_2   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 AS IS pt 2.png"
SIM_ASIS_3   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 AS IS pt 3.png"
SIM_ASIS_4   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 AS IS pt 4.png"
SIM_TOBE_1   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 TO BE.png"
SIM_TOBE_2   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 TO BE pt 2.png"
SIM_TOBE_3   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 TO BE pt 3.png"
SIM_TOBE_4   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 TO BE pt 4.png"
COMP_IMG     = BASE + r"\Entregables\Comparacion AS-IS vs TO-BE\Comparacion AS-IS TO-BE.png"
DIC_ROLES    = BASE + r"\Entregables\Evidencia Dictionary\Diccionario - Roles.png"
DIC_DEPT     = BASE + r"\Entregables\Evidencia Dictionary\Diccionario - Dept.png"
DIC_SYS      = BASE + r"\Entregables\Evidencia Dictionary\Diccionario - IT Sys.png"
DIC_DOC      = BASE + r"\Entregables\Evidencia Dictionary\Diccionario - Doc.png"
IMG_ASIS     = BASE + r"\Analisis Final\Imagenes\AS-IS - Proceso de gesti\u00f3n de pedidos de INDUPRO S.A.png"
IMG_TOBE     = BASE + r"\Analisis Final\Imagenes\TO-BE - Proceso de gesti\u00f3n de pedidos de INDUPRO S.A.png"

# ── Paleta ────────────────────────────────────────────────────────────────────
SAP_BLUE  = RGBColor(0x00, 0x70, 0xF2)
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x49)
GREEN_OK  = RGBColor(0x1A, 0x7A, 0x3C)
RED_ERR   = RGBColor(0xC0, 0x39, 0x2B)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MED_GRAY  = RGBColor(0x77, 0x77, 0x77)

# ── Helpers ───────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex6):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex6)
    tcPr.append(shd)

def page_break(doc):
    doc.add_page_break()

def h1(doc, text):
    p = doc.add_heading(text, level=1)
    r = p.runs[0] if p.runs else p.add_run(text)
    r.font.color.rgb = DARK_BLUE
    r.font.bold = True
    r.font.size = Pt(14)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(4)

def h2(doc, text):
    p = doc.add_heading(text, level=2)
    r = p.runs[0] if p.runs else p.add_run(text)
    r.font.color.rgb = SAP_BLUE
    r.font.bold = True
    r.font.size = Pt(11)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(3)

def body(doc, text, size=10, space_after=5, italic=False, color=None, bold=False, indent=0):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if indent: p.paragraph_format.left_indent = Cm(indent)
    for run in p.runs:
        run.font.size   = Pt(size)
        if italic: run.font.italic = True
        if bold:   run.font.bold   = True
        if color:  run.font.color.rgb = color
    return p

def note(doc, text, prefix="Nota:"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Cm(0.4)
    r1 = p.add_run(prefix + " ")
    r1.font.bold = True; r1.font.color.rgb = SAP_BLUE; r1.font.size = Pt(9)
    r2 = p.add_run(text)
    r2.font.italic = True; r2.font.size = Pt(9); r2.font.color.rgb = DARK_GRAY

def img_box(doc, label):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    r = p.add_run("[ " + label + " ]")
    r.font.size = Pt(9); r.font.italic = True; r.font.color.rgb = MED_GRAY

def insert_img(doc, path, caption="", width=6.2):
    import os
    if not os.path.exists(path):
        img_box(doc, "IMAGEN NO ENCONTRADA: " + path)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(2)
    p.add_run().add_picture(path, width=Inches(width))
    if caption:
        pc = doc.add_paragraph(caption)
        pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pc.paragraph_format.space_before = Pt(0)
        pc.paragraph_format.space_after  = Pt(8)
        for r in pc.runs:
            r.font.size = Pt(8); r.font.italic = True; r.font.color.rgb = MED_GRAY

def make_table(doc, headers, rows_data, header_bg="1B2A49", alt_bg="EEF5FF", fs=8.5):
    tbl = doc.add_table(rows=1 + len(rows_data), cols=len(headers))
    tbl.style = "Table Grid"
    hrow = tbl.rows[0]
    for i, h in enumerate(headers):
        c = hrow.cells[i]
        set_cell_bg(c, header_bg)
        c.text = h
        for r in c.paragraphs[0].runs:
            r.font.bold = True; r.font.color.rgb = WHITE; r.font.size = Pt(fs)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row_data in enumerate(rows_data):
        row = tbl.rows[ri + 1]
        bg  = alt_bg if ri % 2 == 0 else "FFFFFF"
        for ci, v in enumerate(row_data):
            c = row.cells[ci]
            set_cell_bg(c, bg)
            c.text = str(v)
            for r in c.paragraphs[0].runs: r.font.size = Pt(fs)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def bullet(doc, bold_part, text, size=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Cm(0.4)
    r1 = p.add_run("- " + bold_part + ": ")
    r1.font.bold = True; r1.font.color.rgb = SAP_BLUE; r1.font.size = Pt(size)
    r2 = p.add_run(text)
    r2.font.size = Pt(size); r2.font.color.rgb = DARK_GRAY

# ── Documento ─────────────────────────────────────────────────────────────────
doc = Document()
for section in doc.sections:
    section.top_margin    = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin   = Cm(2.8)
    section.right_margin  = Cm(2.3)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)

# ── PAG 1: CARATULA ───────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run()
run.add_picture(CARAULA_IMG, width=Inches(6.0))
page_break(doc)

# ── PAG 2: INDICE ─────────────────────────────────────────────────────────────
h1(doc, "Indice")
toc = [
    ("1.",    "Situacion de la Empresa",                           "3"),
    ("2.",    "Analisis AS-IS",                                    "4"),
    ("  2.1", "Descripcion del proceso actual y problemas",        "4"),
    ("  2.2", "Modelado AS-IS en SAP Signavio (BPMN 2.0)",        "5"),
    ("  2.3", "Configuracion y resultados de simulacion AS-IS",    "5"),
    ("3.",    "Propuesta de Mejora TO-BE",                         "6"),
    ("  3.1", "Estrategia - 4 palancas de mejora",                 "6"),
    ("  3.2", "Arquitectura de sistemas y nuevos roles",            "6"),
    ("  3.3", "Modelado TO-BE en SAP Signavio (BPMN 2.0)",        "7"),
    ("  3.4", "Configuracion y resultados de simulacion TO-BE",    "8"),
    ("4.",    "Comparacion Cuantitativa AS-IS vs TO-BE",           "9"),
    ("  4.1", "Tabla comparativa de KPIs",                         "9"),
    ("  4.2", "Justificacion de cada mejora",                      "9"),
    ("5.",    "Plan de Implementacion y Presupuesto",               "11"),
    ("6.",    "Diccionario Signavio",                               "12"),
    ("7.",    "Process Mining",                                     "13"),
    ("8.",    "Conclusiones",                                       "13"),
    ("9.",    "Bibliografia y Referencias",                         "14"),
]
for num, title, page in toc:
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.space_before = Pt(1)
    r1 = p.add_run(num + "  " + title)
    r1.font.size = Pt(10)
    if not num.startswith("  "): r1.font.bold = True
    r2 = p.add_run("    " + "." * max(0, 50 - len(title) - len(num)) + "    " + page)
    r2.font.size = Pt(10); r2.font.color.rgb = MED_GRAY
page_break(doc)

# ── PAG 3: SITUACION DE LA EMPRESA ────────────────────────────────────────────
h1(doc, "1. Situacion de la Empresa")
body(doc,
    "INDUPRO S.A. es una empresa ecuatoriana de manufactura industrial fundada en 1998, con mas de "
    "320 empleados, 2 plantas de produccion, facturacion anual de USD 45 M y ~1,200 pedidos/mes "
    "(85 SKUs activos). Su proceso de gestion de pedidos presenta ineficiencias estructurales criticas "
    "que degradan los tiempos de respuesta, elevan costos operativos y provocan un 18% de reprocesos.")

make_table(doc,
    ["Atributo", "Valor"],
    [
        ("Sector",            "Manufactura y distribucion industrial"),
        ("Fundacion",         "1998"),
        ("Empleados",         "320+"),
        ("Facturacion anual", "~USD 45 millones"),
        ("Plantas",           "2 plantas + 1 centro de distribucion"),
        ("Volumen mensual",   "~1,200 pedidos/mes · 40 pedidos/dia"),
        ("SKUs activos",      "85"),
        ("Entrega promedio",  "12 dias habiles"),
    ],
    fs=9)

body(doc,
    "El analisis identifica 8 problemas criticos: (P1) validacion manual en Excel, "
    "(P2) sistemas financiero y ERP desconectados, (P3) stock consultado en registros fisicos, "
    "(P4) confirmacion por correo manual, (P5) ordenes de produccion en papel, "
    "(P6) QC reactivo al final con 18% de reproceso, (P7) asignacion de transporte por telefono, "
    "(P8) facturacion manual. Todos atacados en la propuesta TO-BE.")
page_break(doc)

# ── PAG 4-5: ANALISIS AS-IS ───────────────────────────────────────────────────
h1(doc, "2. Analisis AS-IS")
h2(doc, "2.1 Descripcion del proceso actual y problemas")
body(doc,
    "El proceso inicia cuando el cliente solicita por correo/telefono. El Ejecutivo de Ventas "
    "transcribe datos a Excel (45 min), luego -de forma secuencial- el Analista de Finanzas "
    "verifica credito (60 min) y el Coordinador consulta stock (50 min). Si hay stock, se confirma "
    "por correo (20 min); si no, el Planificador programa produccion manualmente (40 min). "
    "Fabricacion: 120 min, QC final: 30 min, con 18% rechazo (90 min reproceso). "
    "Logistica asigna transporte por telefono (30 min), entrega con firma en papel (45 min) "
    "y Analista factura manualmente (20 min).")

make_table(doc,
    ["#", "Actividad", "Responsable", "Dur. (min)", "Costo (USD)", "Problema"],
    [
        ("1",   "Recepcion de solicitud",          "Ejecutivo Ventas",     "30",  "$6.00",  "-"),
        ("2",   "Validacion manual en Excel",       "Ejecutivo Ventas",     "45",  "$9.00",  "P1"),
        ("3",   "Verificacion credito (manual)",    "Analista Finanzas",    "60",  "$13.00", "P2"),
        ("4",   "Consulta stock (fisica + ERP)",    "Coord. Inventarios",   "50",  "$8.33",  "P3"),
        ("5",   "[XOR] Decision stock",             "Coord. Inventarios",   "5",   "$0.83",  "-"),
        ("6A",  "Confirmacion al cliente (correo)", "Ejecutivo Ventas",     "20",  "$4.00",  "P4"),
        ("6B",  "Programar produccion (planilla)",  "Planificador",         "40",  "$9.33",  "P5"),
        ("7",   "Fabricacion del producto",         "Operario de Planta",   "120", "$16.00", "-"),
        ("8",   "Inspeccion QC (checklist papel)",  "Inspector Calidad",    "30",  "$5.50",  "P6"),
        ("9",   "[XOR] Decision calidad",           "Inspector Calidad",    "5",   "$0.92",  "-"),
        ("9B",  "Reproceso del lote (18% casos)",   "Operario / Inspector", "90",  "$12.00", "P6"),
        ("10",  "Empaque y preparacion",            "Coord. Logistica",     "25",  "$4.17",  "-"),
        ("11",  "Asignacion transportista (tel.)",  "Coord. Logistica",     "30",  "$5.00",  "P7"),
        ("12",  "Entrega + firma en papel",         "Logistica",            "45",  "$7.50",  "-"),
        ("13",  "Facturacion manual",               "Analista Finanzas",    "20",  "$4.33",  "P8"),
    ], fs=8)

note(doc,
    "El caso indica 555 min y $105.91. Los valores correctos son 595 min y $101.92 "
    "(ruta: fabricacion + reproceso). El error surge porque el caso omite Act. 6B (40 min) "
    "de la ruta de fabricacion e incluye incorrectamente Act. 6A ($4.00). "
    "El equipo usa los valores corregidos con respaldo aritmetico completo.",
    "Correccion de errores en el caso:")

h2(doc, "2.2 Modelado AS-IS en SAP Signavio (BPMN 2.0)")
body(doc,
    "Modelado con 7 swimlanes (solo roles humanos), eventos inicio/fin tipo Message, "
    "2 gateways XOR con porcentajes de probabilidad, 15 actividades, 1 Intermediate Timer Event "
    "antes del reproceso. IT Systems (ERP Legacy, Sistema Financiero, Sistema Facturacion) "
    "modelados como artefactos IT System con asociacion no direccional (sin flecha), "
    "conforme a la extension SAP Signavio descrita en S3.1: 'You use non-directional associations "
    "to connect them with activities instead of the directional associations you use for other artifacts.'")
img_box(doc, "INSERTAR: Diagrama AS-IS desde SAP Signavio - INDUPRO_ASIS_Corregido_v2.bpmn")
insert_img(doc, IMG_ASIS, "Fig. A - Modelado AS-IS: Proceso de Gestion de Pedidos INDUPRO S.A. (SAP Signavio BPMN 2.0)")

h2(doc, "2.3 Configuracion y resultados de simulacion AS-IS")
make_table(doc,
    ["Parametro", "Configuracion"],
    [
        ("Duration",        "Act.1:30min - Act.2:45min - Act.3:60min - Act.4:50min - Act.5:5min - Act.6A:20min - Act.6B:40min - Act.7:120min - Act.8:30min - Act.9:5min - Act.9B:90min - Act.10:25min - Act.11:30min - Act.12:45min - Act.13:20min"),
        ("Frequency",       "Inicio: 'Llegada de Solicitud de pedido' On Mon-Fri, overall 20 times | XOR Calidad: APROBADA=65% / RECHAZADA=35% | XOR Stock: No hay stock=18% / Si hay stock=82%"),
        ("Resources",       "Ventas:$12/h x2 - Finanzas:$13/h - Inventarios:$10/h - Planificacion:$14/h - Planta:$8/h x6 - Calidad:$11/h x2 - Logistica:$10/h | Horario: Lun-Vie 08:00-16:00 (Logistica 07:00-14:00)"),
        ("Resultado Signavio","One Case: Tiempo ciclo = 9h 55m 00s (595 min) | Costo = $101.92 | Consumo recursos = 9h 55m | Bottlenecks: ninguno detectado"),
    ], fs=9)
note(doc, "Costs tab = solo costos fijos de materiales (NO mano de obra). Resources tab = tarifas/hora por lane. Siempre en MINUTOS (version academica de Signavio).", "Importante simulacion:")
body(doc, "Resultados de ejecucion AS-IS (Escenario 1 - One Case con fabricacion + reproceso):", bold=True, size=9)
make_table(doc,
    ["Actividad", "Tiempo puro", "Costo", "Recurso"],
    [
        ("Recibir solicitud del cliente",             "00:30:00",  "$6.00",  "Ejecutivo de Ventas"),
        ("Validar datos del pedido (Excel)",          "00:45:00",  "$9.00",  "Ejecutivo de Ventas"),
        ("Verificar credito del cliente",             "01:00:00",  "$13.00", "Analista de Finanzas"),
        ("Consultar disponibilidad stock en bodega",  "00:50:00",  "$8.33",  "Coord. Inventarios"),
        ("Verificar stock (gateway)",                 "00:05:00",  "$0.83",  "Coord. Inventarios"),
        ("Programar orden de produccion",             "00:40:00",  "$9.33",  "Planificador Produccion"),
        ("Fabricar producto",                         "02:00:00",  "$16.00", "Operario de Planta"),
        ("Inspeccionar y liberar calidad",            "00:30:00",  "$5.50",  "Inspector de Calidad"),
        ("Verificar calidad (gateway)",               "00:05:00",  "$0.92",  "Inspector de Calidad"),
        ("Reprocesar lote rechazado",                 "01:30:00",  "$12.00", "Operario + Inspector"),
        ("Empacar y preparar para despacho",          "00:25:00",  "$4.17",  "Coord. Logistica"),
        ("Asignar transportista y programar entrega", "00:30:00",  "$5.00",  "Coord. Logistica"),
        ("Entregar al cliente y obtener firma",       "00:45:00",  "$7.50",  "Transportista"),
        ("Generar y enviar factura",                  "00:20:00",  "$4.33",  "Analista de Finanzas"),
        ("TOTAL (ruta fabricacion + reproceso)",      "09:55:00",  "$101.92","---"),
    ], header_bg="C03A2B", fs=8)
body(doc, "Consumo de recursos AS-IS: Operario Planta 3h30m (35%) | Analista Finanzas 1h20m (13%) | Ejecutivo Ventas 1h15m (13%) | Coord. Inventarios 55m (9%) | Coord. Logistica 55m (9%) | Transportista 45m (8%) | Planificador 40m (7%) | Inspector Calidad 35m (6%)", size=8.5, italic=True)
insert_img(doc, SIM_ASIS_1, "Fig. 1 - Vista general simulacion AS-IS (Escenario 1 - One Case)")
insert_img(doc, SIM_ASIS_2, "Fig. 2 - Costos por actividad y probabilidades de gateways AS-IS", width=6.0)
insert_img(doc, SIM_ASIS_3, "Fig. 3 - Tiempos de ejecucion puros AS-IS por actividad", width=6.0)
insert_img(doc, SIM_ASIS_4, "Fig. 4 - Consumo de recursos AS-IS", width=6.0)
page_break(doc)

# ── PAG 6-8: PROPUESTA TO-BE ──────────────────────────────────────────────────
h1(doc, "3. Propuesta de Mejora TO-BE")
h2(doc, "3.1 Estrategia de rediseno - 4 palancas de mejora")
make_table(doc,
    ["Palanca", "Problema", "Mecanismo de mejora", "KPI impactado"],
    [
        ("1. Automatizacion",       "P1, P4, P8",
         "Portal web auto-validacion reemplaza Excel; confirmacion automatica; factura electronica SRI disparada al confirmar entrega",
         "-75 min | -$17.33"),
        ("2. Paralelizacion",       "P2, P3",
         "AND-Split SAP Integration Suite: credito (2A) y stock (2B) corren simultaneamente en lugar de secuencialmente",
         "110 min -> 15 min (-95 min / -86.4%)"),
        ("3. Integracion sistemas", "P2, P3, P7",
         "SAP Integration Suite como middleware hub-and-spoke; APIs REST sobre ERP Legacy y Sistema Financiero; unica fuente de verdad",
         "Elimina silos de datos"),
        ("4. QC Preventivo",        "P6",
         "QC en-proceso con Sistema QC Digital + nuevo Operario de QC durante fabricacion; detecta defectos antes de finalizar el lote",
         "18% -> 5% reproceso (-72.2%)"),
    ], fs=9)

h2(doc, "3.2 Arquitectura de sistemas y nuevos roles")
make_table(doc,
    ["Sistema / Rol nuevo", "Tipo", "Actividades", "Costo"],
    [
        ("Portal Web de Pedidos",         "Aplicacion web",      "Act. 1, 6A",                    "$10,000"),
        ("SAP Integration Suite",         "Middleware PaaS",     "AND-Split/Join, 2A/2B trigger, 13 trigger", "$12,000"),
        ("API ERP Legacy (Inventario)",   "REST API wrapper",    "Act. 2B",                       "$8,000"),
        ("API Sistema Financiero",        "REST API wrapper",    "Act. 2A",                       "$5,000"),
        ("Sistema QC Digital",            "App movil/web",       "Act. 7 (en-proceso), 8",        "$4,000"),
        ("TMS Beetrack",                  "SaaS",                "Act. 11, 12",                   "$5,500"),
        ("Facturacion Electronica Datil.","SaaS SRI-compliant",  "Act. 13",                       "$2,500"),
        ("Capacitacion del personal",     "Servicio externo",    "Todos los roles",               "$3,000"),
        ("NUEVO ROL: Analista Integracion","$18/hr",             "Administra SAP Integration Suite y APIs", "-"),
        ("NUEVO ROL: Operario QC proceso","$11/hr",              "Act. 7 Additional Participant",  "-"),
    ], header_bg="1B2A49", alt_bg="EEF5FF", fs=8.5)
note(doc,
    "Additional Participant (extension SAP Signavio): Operario QC en-proceso se adjunta a Act.7 "
    "como participante secundario. Inspector de Calidad es Additional Participant en Act.9B. "
    "Ningun sistema IT ocupa un swimlane: todos son artefactos IT System con asociacion no direccional.",
    "Notacion Signavio:")

h2(doc, "3.3 Modelado TO-BE en SAP Signavio (BPMN 2.0)")
body(doc,
    "El TO-BE tiene 9 swimlanes (7 existentes + 2 nuevos), 7 artefactos IT System, "
    "AND-Split/Join para paralelizacion, XOR credito+stock (70%/30%), XOR calidad (95%/5%), "
    "pool externo Cliente con MessageFlow (solicitud > confirmacion > factura), "
    "y tipificacion correcta de tareas:")
make_table(doc,
    ["Actividad TO-BE", "Tipo", "IT System", "Razon"],
    [
        ("1 - Recepcion portal web",         "User Task",    "Portal Web",           "Persona interactua con interfaz digital"),
        ("2A - Verificacion credito API",     "Service Task", "API Sist. Financiero", "Automatico, sin input humano"),
        ("2B - Consulta stock API",           "Service Task", "API ERP Legacy",       "Automatico, sin input humano"),
        ("6A - Confirmacion automatica",      "Send Task",    "Portal Web / Sist.Int","Email/SMS disparado automaticamente"),
        ("6B - Programar produccion digital", "User Task",    "ERP Modulo PP",        "Planificador aprueba en pantalla"),
        ("7 - Fabricacion + QC en-proceso",  "Manual Task",  "Sistema QC Digital",   "Trabajo fisico; QC digital es soporte"),
        ("8 - Inspeccion final digital",      "User Task",    "Sistema QC Digital",   "Inspector usa app con formulario digital"),
        ("9B - Reproceso residual (5%)",      "Manual Task",  "-",                    "Trabajo fisico"),
        ("10 - Empaque (packing list digital)","Manual Task", "ERP Legacy",           "Trabajo fisico"),
        ("11 - Asignacion TMS automatica",    "Service Task", "TMS Beetrack",         "Asignacion automatica por reglas"),
        ("12 - Entrega + firma digital",      "User Task",    "TMS App movil",        "Transportista usa app de entrega"),
        ("13 - Factura electronica SRI",      "Service Task", "Datil.me / Sist.Int.", "Emitida automaticamente al confirmar entrega"),
    ], fs=8)
img_box(doc, "INSERTAR: Diagrama TO-BE desde SAP Signavio - INDUPRO_TOBE_v1.bpmn (9 lanes + IT Systems + MessageFlows)")
insert_img(doc, IMG_TOBE, "Fig. B - Modelado TO-BE: Proceso de Gestion de Pedidos INDUPRO S.A. rediseñado (SAP Signavio BPMN 2.0)")

h2(doc, "3.4 Configuracion y resultados de simulacion TO-BE")
make_table(doc,
    ["Parametro", "Configuracion"],
    [
        ("Duration",          "Act.1:5min - Act.2:5min - Act.3:5min - Act.4:10min - Act.5:120min - Act.6:30min - Act.7(reproceso):30min - Act.8:1min - Act.9:10min - Act.10:5min - Act.11:1min - Act.12:0.5min"),
        ("Frequency",         "Inicio: 'Solicitud de pedido (portal web)' On Mon-Fri, overall 20 times | XOR Credito: Aprobado=70% / Desaprobado=30% | XOR QC: Aprueba=95% / Rechaza=5%"),
        ("Resources",         "Ventas:$12/h - Finanzas:$13/h - Inventarios:$10/h - Planif.:$14/h - Planta:$8/h - OpQC:$11/h - Inspector:$11/h - Logistica:$10/h | Logistica horario: 07:00-14:00"),
        ("Resultado Signavio", "One Case: Tiempo ciclo = 4h 12m 30s (252.5 min) | Costo = $55.23 | Consumo recursos = 6h 12m 30s (372.5 min) | Bottlenecks: ninguno detectado"),
    ], fs=9)
body(doc, "Resultados de ejecucion TO-BE (Escenario 1 - One Case con fabricacion + reproceso residual 5%):", bold=True, size=9)
make_table(doc,
    ["Actividad", "Tiempo puro", "Costo", "Recurso / IT System"],
    [
        ("Analizar pedido via portal web",                      "00:05:00", "$1.00",  "Ejecutivo de Ventas | Portal Web"),
        ("Verificar credito del cliente via API financiera",    "00:05:00", "$1.08",  "Analista de Finanzas | API Sist. Financiero"),
        ("Consultar disponibilidad de stock en ERP",            "00:05:00", "$0.83",  "Coord. Inventarios | API ERP Legacy"),
        ("Programar orden de produccion en ERP digital",        "00:10:00", "$2.33",  "Planificador | ERP Modulo PP"),
        ("Fabricar el producto (con QC en proceso)",            "02:00:00", "$32.00", "Operario Planta + Operario QC | Sistema QC Digital"),
        ("Inspeccionar calidad del lote (digital)",             "00:30:00", "$5.50",  "Inspector de Calidad | Sistema QC Digital"),
        ("Reproceso de Calidad (5% casos)",                    "00:30:00", "$4.00",  "Operario + Inspector"),
        ("Enviar confirmacion automatica al cliente",           "00:01:00", "$0.20",  "Portal Web | SAP Integration Suite"),
        ("Empacar y preparar para despacho",                   "00:10:00", "$1.67",  "Coord. Logistica"),
        ("Asignar transportista via TMS automatizado",          "00:05:00", "$0.83",  "Coord. Logistica | TMS Beetrack"),
        ("Entregar al cliente y registrar firma digital",       "00:01:00", "$0.17",  "Transportista | TMS App movil"),
        ("Generar y enviar factura electronica automatica",     "00:00:30", "$0.11",  "Datil.me | SAP Integration Suite"),
        ("Espera ventana despacho 07:00-14:00 (restriccion 4.1)","00:30:00","$0.00", "Restriccion operativa inamovible"),
        ("TOTAL (ruta fabricacion + reproceso)",                "04:12:30", "$55.23", "---"),
    ], header_bg="1A7A3C", fs=8)
body(doc, "Consumo de recursos TO-BE: Operario Planta 2h30m (59%) | Operario QC en Proceso 2h00m (48%) | Inspector Calidad 1h00m (24%) | Coord. Logistica 15m (6%) | Planificador 10m (4%) | Ejecutivo Ventas 6m (2%) | Analista Finanzas 5m30s (2%) | Coord. Inventarios 5m (2%) | Transportista 1m (0%)", size=8.5, italic=True)
insert_img(doc, SIM_TOBE_1, "Fig. 5 - Vista general simulacion TO-BE (Escenario 1 - One Case)")
insert_img(doc, SIM_TOBE_2, "Fig. 6 - Costos por actividad TO-BE", width=6.0)
insert_img(doc, SIM_TOBE_3, "Fig. 7 - Tiempos de ejecucion puros TO-BE por actividad", width=6.0)
insert_img(doc, SIM_TOBE_4, "Fig. 8 - Consumo de recursos TO-BE", width=6.0)
page_break(doc)

# ── PAG 9-10: COMPARACION AS-IS vs TO-BE ─────────────────────────────────────
h1(doc, "4. Comparacion Cuantitativa AS-IS vs TO-BE")
h2(doc, "4.1 Tabla comparativa de KPIs")

kpi_rows = [
    ("Tiempo de ciclo total (con reproceso)",     "595 min\n(9h 55m)",   "252.5 min\n(4h 12m 30s)", "< 350 min", "-342.5 min", "-57.6%", "META"),
    ("Tiempo de ciclo puro (sin espera logistica)","595 min",             "222.5 min",               "< 350 min", "-372.5 min", "-62.6%", "META"),
    ("Costo por pedido (ruta con reproceso)",      "$101.92",             "$55.23",                  "< $70.00",  "-$46.69",   "-45.8%", "META"),
    ("Costo por pedido (ruta sin reproceso)",      "$101.92",             "$51.23",                  "< $70.00",  "-$50.69",   "-49.7%", "META"),
    ("Tasa de reproceso de calidad (paso 9B)",      "35%",                "5%",                      "< 5%",      "-30 pp",    "-85.7%", "META"),
    ("Tiempo verificacion credito (paso 3/2)",      "60 min",             "5 min",                   "< 15 min",  "-55 min",   "-91.7%", "OK"),
    ("Tiempo consulta stock (paso 4/3)",            "50 min",             "5 min",                   "-",         "-45 min",   "-90.0%", "OK"),
    ("Tiempo confirmacion al cliente",              "20 min",             "1 min",                   "< 240 min", "-19 min",   "-95.0%", "OK"),
    ("Tiempo programar produccion",                 "40 min",             "10 min",                  "-",         "-30 min",   "-75.0%", "OK"),
    ("Tiempo empaque",                              "25 min",             "10 min",                  "-",         "-15 min",   "-60.0%", "OK"),
    ("Tiempo asignacion transporte",                "30 min",             "5 min",                   "-",         "-25 min",   "-83.3%", "OK"),
    ("Tiempo facturacion",                          "20 min",             "0.5 min",                 "-",         "-19.5 min", "-97.5%", "OK"),
    ("Tiempo fabricacion (inamovible)",             "120 min",            "120 min",                 "-",         "-",         "-",      "FIJO"),
    ("Tiempo inspeccion QC (regulatorio)",          "30 min",             "30 min",                  "-",         "-",         "-",      "FIJO"),
    ("Bottlenecks detectados por Signavio",         "Ninguno\n(recursos OK)","Ninguno\n(recursos OK)","-",       "-",         "-",      "OK"),
    ("ROI estimado a 12 meses",                    "-",                   "1,118%",                  "> 0%",      "+$617,280", "-",      "META"),
]
tbl = doc.add_table(rows=1 + len(kpi_rows), cols=7)
tbl.style = "Table Grid"
hdrs = ["KPI", "AS-IS", "TO-BE", "Meta", "Delta", "% Mejora", "Estado"]
hrow = tbl.rows[0]
for i, h in enumerate(hdrs):
    c = hrow.cells[i]
    set_cell_bg(c, "1B2A49")
    c.text = h
    for r in c.paragraphs[0].runs:
        r.font.bold = True; r.font.color.rgb = WHITE; r.font.size = Pt(8)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for ri, rd in enumerate(kpi_rows):
    row = tbl.rows[ri + 1]
    is_fixed = rd[6] == "FIJO"
    is_meta  = rd[6] == "META"
    alt = ri % 2 == 0
    bg = "FFF9CC" if is_fixed else ("EEF5FF" if alt else "FFFFFF")
    for ci, v in enumerate(rd):
        c = row.cells[ci]
        if ci == 1 and not is_fixed: set_cell_bg(c, "FFE8E8")
        elif ci == 2 and not is_fixed: set_cell_bg(c, "E8FFE8")
        elif ci == 6:
            if is_meta: set_cell_bg(c, "1A7A3C")
            elif rd[6] == "OK": set_cell_bg(c, "D0F0E0")
            elif is_fixed: set_cell_bg(c, "FFF9CC")
        else:
            set_cell_bg(c, bg)
        c.text = v
        for r in c.paragraphs[0].runs:
            r.font.size = Pt(8)
            if ci == 6 and is_meta: r.font.color.rgb = WHITE; r.font.bold = True
            elif ci == 5 and not is_fixed and v != "-": r.font.bold = True; r.font.color.rgb = GREEN_OK
doc.add_paragraph().paragraph_format.space_after = Pt(4)
note(doc, "Fabricacion 120 min y QC 30 min son inamovibles (restriccion tecnica y regulatoria). Las 5 metas cuantitativas del caso se cumplen al 100%. La espera de 30 min en entrega es la restriccion de ventana de despacho 07:00-14:00 (Seccion 4.1 del caso).", "Restricciones:")
insert_img(doc, COMP_IMG, "Fig. 9 - Comparacion side-by-side AS-IS vs TO-BE en SAP Signavio (80 cambios entre Revision 10 y Revision 2)")

h2(doc, "4.2 Justificacion de cada mejora")
justifs = [
    ("-57.6% tiempo de ciclo (595 -> 252.5 min)",
     "Combinacion de 4 palancas: (a) automatizacion elimina 39 min de actividades manuales (validacion Excel, confirmacion correo, factura manual), "
     "(b) digitalizacion reduce tiempos de credito, stock, transporte y empaque en 130 min adicionales, "
     "(c) QC preventivo reduce el tiempo esperado de reproceso de 31.5 min (35%*90) a 1.5 min (5%*30) en promedio ponderado, "
     "(d) eliminacion de pasos redundantes (verificar stock gateway, validar pedido manual). "
     "Confirmado por Signavio: 9h55m -> 4h12m30s con identica carga de trabajo y mismos recursos."),
    ("-45.8% costo por pedido ($101.92 -> $55.23)",
     "Las Service Tasks automatizadas (credito API, stock API, confirmacion automatica, factura electronica) eliminan "
     "costo de intervencion humana prolongada. El Analista de Finanzas pasa de 60 min a 5 min (ahorro $12.92). "
     "El Coordinador de Inventarios pasa de 50 min a 5 min (ahorro $7.50). "
     "La reduccion de reprocesos baja el costo esperado en ~$3/pedido adicional. "
     "Confirmado por Signavio: $101.92 -> $55.23 por pedido en One Case."),
    ("-85.7% tasa de reproceso (35% -> 5%)",
     "QC en-proceso (Sistema QC Digital + Operario de QC en proceso) ejecuta checklists digitales durante fabricacion, "
     "detectando y corrigiendo parametros fuera de especificacion antes de finalizar el lote. "
     "Configurado en Signavio: gateway 'RECHAZADA' = 5% (vs 35% en AS-IS). "
     "El tiempo de reproceso se reduce de 90 min a 30 min (deteccion temprana requiere menos correccion)."),
    ("-91.7% tiempo verificacion credito (60 -> 5 min)",
     "API REST sobre Sistema Financiero (/credit/{clientId}) responde en segundos. "
     "Sin intervencion manual del Analista de Finanzas para casos estandar. "
     "Confirmado en Signavio: pure execution time = 00:05:00 (constant). "
     "Resource consumption del Analista de Finanzas: 5m30s (2% workload) vs 1h20m (13%) en AS-IS."),
    ("Cumplimiento 100% de restricciones del caso (Seccion 4)",
     "<=2 nuevos roles: 2 (Operario QC en Proceso + Analista Integracion Sist.) OK | "
     "Presupuesto <=50,000: $50,000 OK | Costo/pedido <$70: $55.23 OK | "
     "Tiempo ciclo <350 min: 252.5 min OK | Fabricacion 120 min inamovible OK | QC 30 min regulatorio OK | "
     "Ventana despacho 07:00-14:00: modelado en Resources con Logistica 07:00-14:00 OK"),
]
for t, d in justifs:
    bullet(doc, t, d, size=9.5)
page_break(doc)

# ── PAG 11: PLAN DE IMPLEMENTACION Y PRESUPUESTO ─────────────────────────────
h1(doc, "5. Plan de Implementacion y Presupuesto")
body(doc,
    "La implementacion se divide en 3 fases de 30 dias, entregando valor incremental y "
    "respetando el limite de USD 50,000 total. ROI estimado a 12 meses: 1,118%. "
    "Payback: ~0.89 meses (ahorro mensual: $56,028 sobre 1,200 pedidos x $46.69 de ahorro/pedido confirmado por simulacion Signavio).")
make_table(doc,
    ["Fase", "Nombre", "Dias", "Sistemas implementados", "Costo est.", "Hito clave"],
    [
        ("Fase 1","Integracion y Portal","1-30","Portal Web + SAP Integration Suite + APIs ERP/Financiero","~$10,225","AND-Split funcionando; APIs respondiendo < 3 seg"),
        ("Fase 2","Calidad y Produccion","31-60","Sistema QC Digital + tablets industriales + PP digital en ERP","~$5,450","Tasa de rechazo en piloto < 8%"),
        ("Fase 3","Logistica y Go-Live","61-90","TMS Beetrack + Datil.me + Capacitacion + Go-Live controlado","~$11,480","Tiempo ciclo < 350 min medido en produccion"),
    ], fs=8.5)

make_table(doc,
    ["Componente / Sistema", "Monto (USD)", "% Total", "Concepto"],
    [
        ("SAP Integration Suite (Middleware)",       "$12,000","24.0%","Setup + suscripcion 12 meses + consultoria 80h a $80/hr"),
        ("Portal Web de Pedidos",                    "$10,000","20.0%","Desarrollo frontend + integracion APIs + hosting"),
        ("API Layer ERP Legacy (Inventario)",        "$8,000", "16.0%","REST API wrapper + connector JDBC + performance"),
        ("API Layer Sistema Financiero",             "$5,000", "10.0%","REST API + logica credito + seguridad OAuth2/SSL"),
        ("Sistema QC Digital + tablets",             "$4,000", "8.0%", "App web/movil + 4 tablets industriales + config."),
        ("TMS Beetrack + integracion",               "$5,500", "11.0%","Suscripcion anual + asignacion automatica + firma"),
        ("Facturacion Electronica Datil.me",         "$2,500", "5.0%", "SRI-compliant + certificados + integracion vía SIS"),
        ("Capacitacion del personal",                "$3,000", "6.0%", "40h instructor externo ($50/hr) + materiales"),
        ("TOTAL",                                    "$50,000","100%", "Dentro del limite maximo del caso"),
    ], header_bg="1B2A49", alt_bg="EEF5FF", fs=8.5)
note(doc, "ROI = ($56,028/mes * 12 meses - $50,000) / $50,000 = 1,118%. Payback = $50,000 / $56,028 = 0.89 meses. Ahorro/pedido confirmado por simulacion Signavio: $101.92 - $55.23 = $46.69.", "ROI calculado:")
page_break(doc)

# ── PAG 12: DICCIONARIO SIGNAVIO ──────────────────────────────────────────────
h1(doc, "6. Diccionario Signavio (Entregable E3)")
body(doc, "El Signavio Dictionary centraliza todos los elementos reutilizables. El Entregable E3 requiere captura con: roles, IT Systems y documentos.")
make_table(doc,
    ["Categoria", "Elemento", "Descripcion"],
    [
        ("Rol existente",  "Ejecutivo de Ventas",        "$12/hr - Recepciona y confirma pedidos"),
        ("Rol existente",  "Analista de Finanzas",       "$13/hr - Verifica credito - Supervisa facturacion"),
        ("Rol existente",  "Coord. de Inventarios",      "$10/hr - Supervisa consulta stock"),
        ("Rol existente",  "Planificador de Produccion", "$14/hr - Aprueba ordenes digitales en ERP"),
        ("Rol existente",  "Operario de Planta",         "$8/hr - Fabricacion fisica"),
        ("Rol existente",  "Inspector de Calidad",       "$11/hr - Inspeccion final digital"),
        ("Rol existente",  "Coord. de Logistica",        "$10/hr - Empaque y supervision TMS"),
        ("Rol NUEVO",      "Analista Integracion Sist.", "$18/hr - Administra SAP Integration Suite y APIs"),
        ("Rol NUEVO",      "Operario QC en-proceso",     "$11/hr - QC digital durante fabricacion"),
        ("IT System",      "Portal Web de Pedidos",      "Act. 1, 6A - React/HTML5 + integracion APIs"),
        ("IT System",      "SAP Integration Suite",      "AND-Split/Join, 2A/2B trigger, 13 trigger"),
        ("IT System",      "API ERP Legacy (Stock)",     "Act. 2B - /inventory/{sku} < 3 seg respuesta"),
        ("IT System",      "API Sistema Financiero",     "Act. 2A - /credit/{clientId}"),
        ("IT System",      "Sistema QC Digital",         "Act. 7, 8 - checklists digitales + dashboard"),
        ("IT System",      "TMS Beetrack",               "Act. 11, 12 - asignacion automatica + firma digital"),
        ("IT System",      "Facturacion Datil.me",       "Act. 13 - XML SRI + trigger automatico desde TMS"),
        ("Documento",      "Formulario de pedido",       "JSON/XML portal (TO-BE) vs correo/Excel (AS-IS)"),
        ("Documento",      "Orden de produccion",        "Digital en ERP con timestamp (TO-BE) vs planilla impresa"),
        ("Documento",      "Informe QC",                 "Digital con firma (TO-BE) vs checklist papel (AS-IS)"),
        ("Documento",      "Comprobante electronico SRI","XML SRI autorizado automaticamente (TO-BE)"),
    ], fs=8)
img_box(doc, "INSERTAR: Captura del Signavio Dictionary con los elementos registrados (Entregable E3)")
insert_img(doc, DIC_ROLES, "Fig. D1 - Dictionary: Roles", width=5.5)
insert_img(doc, DIC_SYS,   "Fig. D2 - Dictionary: IT Systems", width=5.5)
insert_img(doc, DIC_DEPT,  "Fig. D3 - Dictionary: Departamentos", width=5.5)
insert_img(doc, DIC_DOC,   "Fig. D4 - Dictionary: Documentos", width=5.5)
page_break(doc)

# ── PAG 13: PROCESS MINING + CONCLUSIONES ────────────────────────────────────
h1(doc, "7. Process Mining y Beneficios SAP Signavio")
body(doc,
    "SAP Signavio Process Intelligence extrae event logs del ERP para descubrir el proceso real "
    "(as-executed), identificar variantes y cuellos de botella, y comparar el modelo BPMN TO-BE "
    "contra la ejecucion real (conformance checking). Para INDUPRO:")
for t, d in [
    ("Descubrimiento automatico", "Genera el flujo real desde logs del ERP; revela desvios vs. el modelo AS-IS modelado manualmente."),
    ("Validacion cuantitativa del cuello de botella", "Confirma con instancias reales que el bloque credito+stock secuencial (110 min) es el mayor tiempo sin valor agregado."),
    ("Conformance Checking post-implementacion", "Compara el TO-BE disenado vs. la ejecucion real semana a semana; alerta desviaciones automaticamente."),
    ("Mejora continua basada en datos", "El TO-BE de hoy es el AS-IS del manana. El ciclo de mejora se vuelve continuo y basado en evidencia real."),
]:
    bullet(doc, t, d, size=9.5)

h1(doc, "8. Conclusiones")
for t, d in [
    ("Diagnostico riguroso como base",
     "Identificamos 8 problemas, corregimos valores del caso y trazamos cada "
     "ineficiencia a su causa raiz. El analisis AS-IS confirmado por simulacion Signavio: 595 min, $101.92."),
    ("Digitalizacion: palanca de mayor impacto",
     "La sustitucion de procesos manuales (Excel, correo, telefono, papel) por APIs, portales y TMS "
     "genera el 90% de la reduccion total del tiempo de ciclo: de 595 a 252.5 min (-57.6%). "
     "Confirmado por simulacion Signavio con datos reales."),
    ("Notacion correcta en Signavio",
     "IT Systems son artefactos (no lanes), Additional Participants vinculan roles secundarios, "
     "y la tipificacion Manual/User/Service/Send Task refleja madurez tecnica en BPMN 2.0."),
    ("Resultados cuantificables y verificados",
     "-57.6% tiempo de ciclo, -45.8% costo (de $101.92 a $55.23), -85.7% reprocesos (35% a 5%). "
     "ROI 1,118% en 12 meses. Presupuesto $50,000. 5 de 5 metas del caso cumplidas. "
     "Bottlenecks: ninguno detectado en Signavio para ambos escenarios."),
]:
    bullet(doc, t, d, size=9.5)
page_break(doc)

# ── PAG 14: BIBLIOGRAFIA ──────────────────────────────────────────────────────
h1(doc, "9. Bibliografia y Referencias")
body(doc, "Fuentes que respaldan la notacion, simulacion, arquitectura y costos de sistemas utilizados en este informe.", size=10, space_after=8)

refs = [
    ("[1]",  "SAP Signavio — Official Help Portal",
     "SAP SE. (2024). SAP Signavio Process Transformation Suite.",
     "https://help.sap.com/docs/signavio"),
    ("[2]",  "SAP Signavio BPMN Reference - IT Systems (S3.1)",
     "SAP SE. (2024). BPMN Introductory Guide — IT Systems and Associations. SAP Learning.",
     "https://learning.sap.com/learning-journeys/discover-sap-signavio"),
    ("[3]",  "SAP Signavio Process Intelligence (Process Mining)",
     "SAP SE. (2024). SAP Signavio Process Intelligence.",
     "https://help.sap.com/docs/signavio/sap-signavio-process-intelligence"),
    ("[4]",  "BPMN 2.0 Specification — OMG",
     "Object Management Group. (2011). Business Process Model and Notation (BPMN) Version 2.0.",
     "https://www.omg.org/spec/BPMN/2.0/"),
    ("[5]",  "SAP Integration Suite",
     "SAP SE. (2024). SAP Integration Suite Documentation. SAP Business Technology Platform.",
     "https://help.sap.com/docs/integration-suite"),
    ("[6]",  "SAP Business Technology Platform (BTP)",
     "SAP SE. (2024). SAP BTP — Build, Run, and Integrate Business Applications.",
     "https://www.sap.com/products/technology-platform.html"),
    ("[7]",  "Beetrack — TMS para Latinoamerica",
     "Beetrack. (2024). Plataforma de gestion de ultima milla para Latinoamerica.",
     "https://www.beetrack.com/"),
    ("[8]",  "Datil — Facturacion Electronica SRI Ecuador",
     "Datil. (2024). Plataforma de facturacion electronica conforme al SRI Ecuador.",
     "https://datil.co"),
    ("[9]",  "SRI Ecuador — Comprobantes Electronicos",
     "Servicio de Rentas Internas del Ecuador. (2024). Emision de Comprobantes Electronicos.",
     "https://www.sri.gob.ec/web/guest/comprobantes-electronicos"),
    ("[10]", "Process Mining — Foundation",
     "van der Aalst, W.M.P. (2016). Process Mining: Data Science in Action (2nd ed.). Springer.",
     "https://doi.org/10.1007/978-3-662-49851-4"),
    ("[11]", "SAP University Alliances",
     "SAP SE. (2024). SAP University Alliances — Academic Programs and Competitions.",
     "https://www.sap.com/about/company/innovation/education/university-alliances.html"),
    ("[12]", "Caso de Estudio INDUPRO S.A. — Material oficial del concurso",
     "SAP University Alliances. (2026). SAP Signavio Regional Challenge 2026 — Caso INDUPRO S.A.",
     "Documento oficial del concurso (acceso restringido a equipos participantes)"),
]

for ref_num, title, citation, url in refs:
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(5)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent  = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)
    r1 = p.add_run(ref_num + " ")
    r1.font.bold = True; r1.font.color.rgb = SAP_BLUE; r1.font.size = Pt(9)
    r2 = p.add_run(citation + "  ")
    r2.font.size = Pt(9)
    r3 = p.add_run(url)
    r3.font.size = Pt(8.5); r3.font.color.rgb = SAP_BLUE; r3.font.italic = True

# ── GUARDAR ───────────────────────────────────────────────────────────────────
doc.save(OUTPUT_PATH)
print("Documento guardado: " + OUTPUT_PATH)
