"""
Generador PPT — INDUPRO S.A.  |  Universidad Peruana de Ciencias Aplicadas
SAP Signavio Regional Challenge 2026
6 slides: Portada + 5 de contenido
Profesor responsable: Reyes Arce, Balmes Javier
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

# ─────────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────────
BASE       = r"c:\Users\drago\projects\ProyectoSAPSignavio"
UPC_LOGO   = BASE + r"\Entregables\UPC_logo_transparente.png"
IMG_ASIS   = BASE + r"\Analisis Final\Imagenes\AS-IS - Proceso de gestión de pedidos de INDUPRO S.A.png"
IMG_TOBE   = BASE + r"\Analisis Final\Imagenes\TO-BE - Proceso de gestión de pedidos de INDUPRO S.A.png"
SIM_ASIS   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 AS IS.png"
SIM_TOBE   = BASE + r"\Entregables\Resultados de Simulacion\Escenario 1 TO BE.png"
COMP_IMG   = BASE + r"\Entregables\Comparacion AS-IS vs TO-BE\Comparacion AS-IS TO-BE.png"
OUTPUT     = BASE + r"\Entregables\Informe Ejecutivo\INDUPRO_Presentacion_UPC.pptx"

# ─────────────────────────────────────────────────────────────────
# PALETA  (UPC rojo + blanco + SAP azules — sin saturar)
# ─────────────────────────────────────────────────────────────────
UPC_RED    = RGBColor(0xC8, 0x10, 0x2E)   # Rojo institucional UPC
SAP_BLUE   = RGBColor(0x00, 0x70, 0xF2)   # Azul SAP Signavio
DARK_BLUE  = RGBColor(0x1B, 0x2A, 0x49)   # Azul oscuro
GREEN      = RGBColor(0x1A, 0x7A, 0x3C)   # Verde éxito
AMBER      = RGBColor(0xF0, 0xAB, 0x00)   # Ámbar/dorado
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE  = RGBColor(0xF7, 0xF8, 0xFA)
LIGHT_GRAY = RGBColor(0xEE, 0xF2, 0xF7)
MED_GRAY   = RGBColor(0x8A, 0x99, 0xB0)
DARK_GRAY  = RGBColor(0x33, 0x3C, 0x4A)

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def rect(slide, l, t, w, h, fill, line=False):
    from pptx.util import Inches
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line: s.line.color.rgb = fill
    else: s.line.fill.background()
    return s

def tb(slide, text, l, t, w, h, size=10, bold=False, color=DARK_GRAY,
       align=PP_ALIGN.LEFT, italic=False):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.word_wrap = True
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return box

def multiline(slide, lines, l, t, w, h, size=9, default_color=DARK_GRAY):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.word_wrap = True
    tf = box.text_frame; tf.word_wrap = True
    first = True
    for item in lines:
        txt = item[0] if isinstance(item, (list,tuple)) else item
        bld = item[1] if isinstance(item,(list,tuple)) and len(item)>1 else False
        col = item[2] if isinstance(item,(list,tuple)) and len(item)>2 else default_color
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = txt
        r.font.size = Pt(size); r.font.bold = bld; r.font.color.rgb = col

def img(slide, path, l, t, w, h=None):
    if not os.path.exists(path): return
    from pptx.util import Inches
    if h: slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(w), Inches(h))
    else: slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(w))

def header(slide, title, sub=None):
    """Barra header: franja roja UPC fina + línea azul SAP + título"""
    rect(slide, 0, 0, 10, 0.06, UPC_RED)          # raya roja UPC
    rect(slide, 0, 0.06, 10, 0.9, DARK_BLUE)       # barra oscura
    rect(slide, 0, 0.06, 0.07, 0.9, UPC_RED)       # acento rojo izq
    rect(slide, 9.93, 0.06, 0.07, 0.9, SAP_BLUE)   # acento azul SAP der
    tb(slide, title, 0.2, 0.1, 8.6, 0.52, size=18, bold=True, color=WHITE)
    if sub:
        tb(slide, sub, 0.2, 0.63, 8.8, 0.3, size=8.5, color=MED_GRAY, italic=True)
    # Logo UPC pequeño en header
    img(slide, UPC_LOGO, 8.5, 0.1, 1.3, 0.7)

def footer(slide, num, total=5, extra=""):
    rect(slide, 0, 7.2, 10, 0.3, DARK_BLUE)
    tb(slide, f"SAP Signavio Regional Challenge 2026  ·  INDUPRO S.A.  ·  UPC  ·  Mgtr. Reyes Arce, Balmes Javier{extra}",
       0.2, 7.22, 8.5, 0.25, size=7, color=MED_GRAY)
    tb(slide, f"{num}/{total}", 9.3, 7.22, 0.6, 0.25, size=7.5, color=WHITE,
       align=PP_ALIGN.RIGHT, bold=True)

def kpi_card(slide, l, t, w, h, label, value, delta, val_color=SAP_BLUE, good=True):
    rect(slide, l, t, w, 0.05, val_color)
    rect(slide, l, t+0.05, w, h-0.05, LIGHT_GRAY)
    tb(slide, label, l+0.07, t+0.08, w-0.14, 0.22, size=7.5, color=MED_GRAY)
    tb(slide, value, l+0.07, t+0.3,  w-0.14, 0.32, size=13, bold=True, color=val_color)
    dcol = GREEN if good else UPC_RED
    tb(slide, delta, l+0.07, t+0.62, w-0.14, 0.22, size=7.5, bold=True, color=dcol)


# ─────────────────────────────────────────────────────────────────
# PRESENTACIÓN
# ─────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


# ══════════════════════════════════════════════════════════════════
# SLIDE 0 — PORTADA
# ══════════════════════════════════════════════════════════════════
s0 = prs.slides.add_slide(blank)

# Fondo partido: izquierda oscura, derecha blanca
rect(s0, 0,   0, 4.2, 7.5, DARK_BLUE)
rect(s0, 4.2, 0, 5.8, 7.5, WHITE)

# Franja roja UPC vertical en el borde entre las dos mitades
rect(s0, 4.0, 0, 0.18, 7.5, UPC_RED)

# Franja roja top
rect(s0, 0, 0, 4.2, 0.08, UPC_RED)

# Logo UPC (en zona blanca)
img(s0, UPC_LOGO, 4.5, 0.3, 5.0, 1.1)

# Título del concurso (zona blanca)
tb(s0, "SAP Signavio Regional\nChallenge 2026",
   4.5, 1.55, 5.2, 1.0, size=20, bold=True, color=DARK_BLUE)
rect(s0, 4.5, 2.58, 5.0, 0.06, SAP_BLUE)   # línea SAP azul

# Subtítulo caso
tb(s0, "Caso de Estudio: INDUPRO S.A.",
   4.5, 2.72, 5.2, 0.45, size=14, bold=True, color=UPC_RED)
tb(s0, "Transformación Digital del Proceso de Gestión de Pedidos\nmediante SAP Signavio Process Transformation Suite",
   4.5, 3.22, 5.2, 0.75, size=10, color=DARK_GRAY)

# Info equipo y profesor (zona blanca)
rect(s0, 4.5, 4.1, 5.0, 0.04, LIGHT_GRAY)
tb(s0, "Universidad Peruana de Ciencias Aplicadas",
   4.5, 4.18, 5.2, 0.3, size=9.5, bold=True, color=DARK_BLUE)
tb(s0, "Profesor responsable:  Mgtr. Reyes Arce, Balmes Javier",
   4.5, 4.5, 5.2, 0.28, size=9, color=DARK_GRAY)
tb(s0, "Mayo 2026",
   4.5, 4.82, 5.2, 0.25, size=9, color=MED_GRAY, italic=True)

# Zona izquierda oscura — contenido de la empresa
tb(s0, "INDUPRO S.A.", 0.3, 0.5, 3.7, 0.45, size=22, bold=True, color=WHITE)
rect(s0, 0.3, 1.0, 3.6, 0.05, UPC_RED)

# Resumen ejecutivo
multiline(s0, [
    ("Manufactura industrial — Ecuador", False, MED_GRAY),
    ("", False, MED_GRAY),
    ("AS-IS", True, AMBER),
    ("Tiempo de ciclo:   595 min", False, WHITE),
    ("Costo por pedido:  $101.92", False, WHITE),
    ("Tasa de reproceso: 35%", False, WHITE),
    ("", False, WHITE),
    ("TO-BE  (propuesta)", True, SAP_BLUE),
    ("Tiempo de ciclo:   252.5 min", False, WHITE),
    ("Costo por pedido:  $55.23", False, WHITE),
    ("Tasa de reproceso: 5%", False, WHITE),
    ("", False, WHITE),
    ("Reducción ciclo:   −57.6%", True, GREEN),
    ("Reducción costo:   −45.8%", True, GREEN),
    ("ROI a 12 meses:    1,118%", True, GREEN),
], 0.3, 1.1, 3.65, 4.5, size=10, default_color=WHITE)

# Verificado por Signavio
rect(s0, 0.2, 6.05, 3.75, 0.72, RGBColor(0x10,0x1E,0x38))
tb(s0, "✔  Verificado con simulación SAP Signavio\n    Escenario 1 · One Case · Mon–Fri",
   0.3, 6.1, 3.55, 0.6, size=8.5, color=SAP_BLUE, bold=False)

tb(s0, "0 / 5", 9.3, 7.22, 0.6, 0.25, size=7.5, color=MED_GRAY,
   align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — DIAGNÓSTICO: Empresa + Problemas + KPIs
# ══════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank)
rect(s1, 0, 0, 10, 7.5, WHITE)
header(s1, "Diagnóstico AS-IS — Empresa y Problemas Identificados",
       "INDUPRO S.A. · Manufactura industrial · Ecuador · 8 ineficiencias estructurales")

# ── Perfil empresa ──────────────────────────────────────────────
rect(s1, 0.2, 1.1, 4.55, 0.05, AMBER)
rect(s1, 0.2, 1.15, 4.55, 2.35, LIGHT_GRAY)
tb(s1, "PERFIL DE EMPRESA", 0.35, 1.2, 4.2, 0.28, size=9, bold=True, color=DARK_BLUE)
multiline(s1, [
    ("", False),
    ("Sector:     Manufactura y distribución industrial", False, DARK_GRAY),
    ("Empleados:  320+ · 2 plantas de producción", False, DARK_GRAY),
    ("Facturación: ~USD 45 millones anuales", False, DARK_GRAY),
    ("Volumen:    ~1,200 pedidos/mes  (40/día)", False, DARK_GRAY),
    ("SKUs:       85 activos", False, DARK_GRAY),
    ("Canal:      Correo y teléfono → Excel manual", False, DARK_GRAY),
    ("ERP:        Sistema legacy sin integración", False, DARK_GRAY),
], 0.35, 1.48, 4.3, 2.0, size=9.5)

# ── 8 Problemas ─────────────────────────────────────────────────
rect(s1, 5.0, 1.1, 4.75, 0.05, UPC_RED)
rect(s1, 5.0, 1.15, 4.75, 2.35, LIGHT_GRAY)
tb(s1, "8 PROBLEMAS IDENTIFICADOS", 5.15, 1.2, 4.5, 0.28, size=9, bold=True, color=UPC_RED)
multiline(s1, [
    ("P1  Validación manual en Excel → errores y demoras", False, DARK_GRAY),
    ("P2  Sin integración: Sist. Financiero ↔ ERP", False, DARK_GRAY),
    ("P3  Consulta de stock en registros físicos", False, DARK_GRAY),
    ("P4  Confirmación al cliente por correo manual", False, DARK_GRAY),
    ("P5  Órdenes de producción en planillas impresas", False, DARK_GRAY),
    ("P6  QC reactivo al final → 35% de lotes rechazados", False, UPC_RED),
    ("P7  Asignación de transporte por llamadas telefónicas", False, DARK_GRAY),
    ("P8  Facturación manual → 20 min adicionales", False, DARK_GRAY),
], 5.15, 1.5, 4.5, 2.0, size=9.5)

# ── KPI line ────────────────────────────────────────────────────
tb(s1, "KPIs AS-IS  —  Escenario 1 · One Case · Simulación SAP Signavio (datos reales)",
   0.2, 3.6, 9.6, 0.28, size=8.5, bold=True, color=DARK_BLUE)

kpi_card(s1, 0.2,  3.92, 2.35, 1.0, "Tiempo de ciclo total",  "595 min",  "⚠ Meta: < 350 min", UPC_RED, False)
kpi_card(s1, 2.7,  3.92, 2.35, 1.0, "Costo por pedido",       "$101.92",  "⚠ Meta: < $70.00",  UPC_RED, False)
kpi_card(s1, 5.2,  3.92, 2.35, 1.0, "Tasa de reproceso",      "35%",      "⚠ Meta: < 5%",      UPC_RED, False)
kpi_card(s1, 7.7,  3.92, 2.05, 1.0, "Bottlenecks Signavio",   "Ninguno",  "Recursos suficientes",SAP_BLUE, True)

# ── Nota ─────────────────────────────────────────────────────────
rect(s1, 0.2, 5.1, 9.6, 0.55, RGBColor(0xFF,0xF0,0xF0))
rect(s1, 0.2, 5.1, 0.06, 0.55, UPC_RED)
tb(s1, "Ruta crítica simulada: Fabricación + Reproceso (gateway QC: RECHAZADA=35%). "
        "Tiempo puro de ejecución: 9h 55m. Consumo de recursos: 9h 55m. "
        "SAP Signavio confirma el diagnóstico con datos objetivos.",
   0.32, 5.15, 9.4, 0.45, size=8, color=DARK_GRAY, italic=True)

footer(s1, 1)


# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — MODELADO AS-IS
# ══════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank)
rect(s2, 0, 0, 10, 7.5, WHITE)
header(s2, "Modelado AS-IS — BPMN 2.0 en SAP Signavio",
       "7 swimlanes · 15 actividades · 2 gateways XOR · Convención Signavio: IT Systems como artefactos")

# ── Imagen BPMN AS-IS ───────────────────────────────────────────
rect(s2, 0.15, 1.05, 9.7, 4.55, LIGHT_GRAY)
img(s2, IMG_ASIS, 0.15, 1.05, 9.7, 4.55)

# Anotaciones encima de la imagen
# Cuello de botella - crédito
rect(s2, 0.18, 1.08, 2.5, 0.72, RGBColor(0xC8,0x10,0x2E))  # fondo rojo
tb(s2, "CUELLO DE BOTELLA\nCrédito (60 min) + Stock (50 min)\n= 110 min secuencial",
   0.22, 1.12, 2.4, 0.65, size=7.5, color=WHITE, bold=False)

# Reproceso
rect(s2, 7.55, 1.08, 2.3, 0.72, RGBColor(0xC8,0x10,0x2E))
tb(s2, "REPROCESO 35%\nQC reactivo al final\n+90 min por pedido",
   7.58, 1.12, 2.22, 0.65, size=7.5, color=WHITE)

# ── Barra de métricas inferior ──────────────────────────────────
rect(s2, 0, 5.72, 10, 1.05, DARK_BLUE)
rect(s2, 0, 5.72, 10, 0.05, UPC_RED)

metrics = [
    (0.2,  "DURACIÓN (ruta crítica)", "595 min",  UPC_RED),
    (2.6,  "COSTO / PEDIDO",          "$101.92",  UPC_RED),
    (5.05, "REPROCESO",               "35%",      UPC_RED),
    (7.5,  "ACTIVIDADES MANUALES",    "12 de 15", MED_GRAY),
]
for lft, lbl, val, col in metrics:
    tb(s2, lbl, lft, 5.78, 2.2, 0.24, size=7, color=MED_GRAY)
    tb(s2, val, lft, 6.02, 2.2, 0.42, size=17, bold=True, color=col)

footer(s2, 2)


# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — PROPUESTA TO-BE
# ══════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank)
rect(s3, 0, 0, 10, 7.5, WHITE)
header(s3, "Propuesta TO-BE — 4 Palancas de Transformación",
       "$50,000 · 2 nuevos roles · 90 días · 7 IT Systems integrados via SAP Integration Suite")

# ── 4 Palancas de mejora ────────────────────────────────────────
palancas = [
    ("1\nAUTOMATIZACIÓN",    "Portal Web reemplaza\ncorreo/Excel. Confirmación\ny factura automáticas.",        SAP_BLUE),
    ("2\nDIGITALIZACIÓN",    "ERP + Sistema Financiero\nvía APIs REST. Stock y\ncrédito en tiempo real.",       DARK_BLUE),
    ("3\nINTEGRACIÓN",       "SAP Integration Suite\ncomo hub central.\nEliminación de silos.",                AMBER),
    ("4\nQC PREVENTIVO",     "Inspector + Operario QC\nen-proceso. Reproceso:\n35% → 5%.",                     GREEN),
]
for i, (title, body, col) in enumerate(palancas):
    lft = 0.2 + i * 2.43
    rect(s3, lft, 1.1, 2.3, 0.06, col)
    rect(s3, lft, 1.16, 2.3, 1.8, LIGHT_GRAY)
    tb(s3, title, lft+0.1, 1.2, 2.1, 0.6, size=9.5, bold=True, color=col, align=PP_ALIGN.CENTER)
    tb(s3, body,  lft+0.1, 1.82, 2.1, 1.1, size=9, color=DARK_GRAY)

# ── Stack tecnológico ───────────────────────────────────────────
rect(s3, 0.2, 3.08, 5.25, 0.05, SAP_BLUE)
rect(s3, 0.2, 3.13, 5.25, 2.45, LIGHT_GRAY)
tb(s3, "STACK TECNOLÓGICO — $50,000 total", 0.35, 3.18, 4.8, 0.28, size=9, bold=True, color=SAP_BLUE)

tech = [
    ("SAP Integration Suite",       "Middleware central  —  orquesta todos los sistemas",  "$12,000", SAP_BLUE),
    ("Portal Web de Pedidos",        "User Task: Act.1 (reemplaza correo/Excel)",           "$10,000", DARK_BLUE),
    ("API ERP Legacy (inventario)",  "Service Task: Act.3  —  stock tiempo real",           "$8,000",  DARK_BLUE),
    ("API Sistema Financiero",       "Service Task: Act.2  —  crédito automático",          "$5,000",  DARK_BLUE),
    ("Sistema QC Digital + tablets", "Act.5 en-proceso + Act.6 inspección final",           "$4,000",  GREEN),
    ("TMS Beetrack",                 "Service Task: Act.10  —  asignación automática",      "$5,500",  DARK_BLUE),
    ("Facturación Datil.me",         "Service Task: Act.12  —  SRI automático",             "$2,500",  DARK_BLUE),
    ("Capacitación del personal",    "40h instructor externo · gestión del cambio",         "$3,000",  MED_GRAY),
]
for i, (sys, desc, cost, col) in enumerate(tech):
    top = 3.5 + i * 0.255
    bg = WHITE if i % 2 == 0 else LIGHT_GRAY
    rect(s3, 0.2, top, 5.25, 0.255, bg)
    tb(s3, sys,  0.3,  top+0.04, 1.8, 0.2, size=7.5, bold=True, color=col)
    tb(s3, desc, 2.1,  top+0.04, 2.5, 0.2, size=7.5, color=DARK_GRAY)
    tb(s3, cost, 4.62, top+0.04, 0.8, 0.2, size=7.5, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

# ── 2 Nuevos roles ──────────────────────────────────────────────
rect(s3, 5.62, 3.08, 4.18, 0.05, UPC_RED)
rect(s3, 5.62, 3.13, 4.18, 2.45, LIGHT_GRAY)
tb(s3, "2 NUEVOS ROLES  (máx. permitido: 2)", 5.77, 3.18, 3.9, 0.28, size=9, bold=True, color=UPC_RED)

# Rol 1
rect(s3, 5.72, 3.52, 3.98, 0.05, SAP_BLUE)
rect(s3, 5.72, 3.57, 3.98, 0.9, WHITE)
tb(s3, "Analista de Integración de Sistemas", 5.82, 3.6, 3.7, 0.3, size=9, bold=True, color=SAP_BLUE)
tb(s3, "$18 / hora  ·  Act. todas (administra flujos SAP Integration Suite)\n"
        "Monitorea APIs, gestiona errores de integración, genera reportes KPI",
   5.82, 3.9, 3.7, 0.55, size=8.5, color=DARK_GRAY)

# Rol 2
rect(s3, 5.72, 4.54, 3.98, 0.05, GREEN)
rect(s3, 5.72, 4.59, 3.98, 0.9, WHITE)
tb(s3, "Operario de Control de Calidad en Proceso", 5.82, 4.62, 3.7, 0.3, size=9, bold=True, color=GREEN)
tb(s3, "$11 / hora  ·  Act. 5: QC digital durante fabricación\n"
        "Detecta defectos en tiempo real → reproceso 35% → 5%",
   5.82, 4.92, 3.7, 0.55, size=8.5, color=DARK_GRAY)

# Nota tipos de tarea Signavio
rect(s3, 5.62, 5.58, 4.18, 1.02, RGBColor(0xEE,0xF5,0xFF))
rect(s3, 5.62, 5.58, 0.06, 1.02, SAP_BLUE)
tb(s3, "TIPOLOGÍA DE TAREAS BPMN (Signavio):",
   5.73, 5.62, 3.9, 0.24, size=8, bold=True, color=SAP_BLUE)
tb(s3, "User Task: Portal, App QC, Entrega firma\n"
        "Service Task: API Crédito, API Stock, TMS, Factura\n"
        "Send Task: Confirmación automática al cliente\n"
        "Manual Task: Fabricación, Empaque, Reproceso",
   5.73, 5.88, 3.9, 0.7, size=8, color=DARK_GRAY)

footer(s3, 3)


# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — MODELADO TO-BE + RESULTADOS SIMULACIÓN
# ══════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank)
rect(s4, 0, 0, 10, 7.5, WHITE)
header(s4, "Modelado TO-BE + Resultados de Simulación Signavio",
       "BPMN 2.0 · 9 swimlanes · AND-Split/Join · IT System artifacts · Escenario 1 One Case")

# ── BPMN TO-BE imagen (izquierda) ──────────────────────────────
rect(s4, 0.15, 1.05, 6.3, 3.65, LIGHT_GRAY)
img(s4, IMG_TOBE, 0.15, 1.05, 6.3, 3.65)
rect(s4, 0.15, 1.05, 1.85, 0.32, GREEN)
tb(s4, "TO-BE  (rediseñado)", 0.22, 1.1, 1.72, 0.24, size=8, bold=True, color=WHITE)

# ── Tabla KPI comparativa (derecha) ────────────────────────────
tb(s4, "COMPARACIÓN KPIs — SIGNAVIO SIMULACIÓN",
   6.6, 1.05, 3.25, 0.3, size=8.5, bold=True, color=DARK_BLUE)

kpi_rows = [
    ("Tiempo de ciclo",   "595 min",  "252.5 min", "−57.6%"),
    ("Costo / pedido",    "$101.92",  "$55.23",    "−45.8%"),
    ("Reproceso QC",      "35%",      "5%",        "−85.7%"),
    ("Verif. crédito",    "60 min",   "5 min",     "−91.7%"),
    ("Consulta stock",    "50 min",   "5 min",     "−90.0%"),
    ("Confirmación",      "20 min",   "1 min",     "−95.0%"),
    ("Asig. transporte",  "30 min",   "5 min",     "−83.3%"),
    ("Facturación",       "20 min",   "0.5 min",   "−97.5%"),
    ("Bottlenecks",       "---",      "Ninguno",   "✔ OK"),
]
# Header tabla
row_h = 0.32
rect(s4, 6.6, 1.38, 3.25, row_h, DARK_BLUE)
for txt, lft_off, w in [("KPI", 0.05, 0.88), ("AS-IS", 0.95, 0.75), ("TO-BE", 1.72, 0.75), ("Δ", 2.5, 0.75)]:
    tb(s4, txt, 6.6+lft_off, 1.42, w, 0.26, size=7.5, bold=True, color=WHITE)

for i, (kpi, asis, tobe, delta) in enumerate(kpi_rows):
    top = 1.38 + (i+1)*row_h
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s4, 6.6, top, 3.25, row_h, bg)
    good = delta.startswith("−") or delta == "✔ OK"
    dcol = GREEN if good else UPC_RED
    acol = UPC_RED if asis not in ("---",) else MED_GRAY
    tcol = GREEN
    for txt, lft_off, w, col, bld in [
        (kpi, 0.05, 0.88, DARK_GRAY, False),
        (asis, 0.95, 0.75, acol, False),
        (tobe, 1.72, 0.75, tcol, True),
        (delta, 2.5, 0.75, dcol, True),
    ]:
        tb(s4, txt, 6.6+lft_off, top+0.06, w, 0.22, size=7.5, bold=bld, color=col)

# ── Captura simulación Signavio AS-IS ──────────────────────────
tb(s4, "SIMULACIÓN AS-IS — SAP Signavio Escenario 1", 0.15, 4.75, 4.8, 0.28,
   size=8.5, bold=True, color=DARK_BLUE)
rect(s4, 0.15, 5.05, 3.0, 1.8, LIGHT_GRAY)
img(s4, SIM_ASIS, 0.15, 5.05, 3.0, 1.8)

# ── Captura simulación Signavio TO-BE ──────────────────────────
tb(s4, "SIMULACIÓN TO-BE — SAP Signavio Escenario 1", 3.35, 4.75, 4.0, 0.28,
   size=8.5, bold=True, color=GREEN)
rect(s4, 3.35, 5.05, 3.0, 1.8, LIGHT_GRAY)
img(s4, SIM_TOBE, 3.35, 5.05, 3.0, 1.8)

# Leyenda simulación
rect(s4, 6.55, 4.75, 3.3, 2.1, RGBColor(0xEE,0xF5,0xFF))
rect(s4, 6.55, 4.75, 0.06, 2.1, SAP_BLUE)
tb(s4, "PARÁMETROS SIMULACIÓN:", 6.66, 4.8, 3.1, 0.26, size=8, bold=True, color=SAP_BLUE)
multiline(s4, [
    ("Duration: Min. 0:30 · Máx. 2:00 (fabricación)", False, DARK_GRAY),
    ("Frequency: Mon–Fri · 20 instancias total", False, DARK_GRAY),
    ("XOR Calidad: APROBADA 65% / RECHAZADA 35%", False, DARK_GRAY),
    ("XOR Stock: No hay stock 18% / Sí 82%", False, DARK_GRAY),
    ("TO-BE gateway QC: Aprueba 95% / Rechaza 5%", False, DARK_GRAY),
    ("Ventana despacho: 07:00–14:00 (restricción 4.1)", False, MED_GRAY),
    ("Bottlenecks detectados: NINGUNO en ambos", True, GREEN),
], 6.66, 5.08, 3.1, 1.7, size=8, default_color=DARK_GRAY)

footer(s4, 4)


# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — PLAN · PRESUPUESTO · CONCLUSIONES
# ══════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank)
rect(s5, 0, 0, 10, 7.5, WHITE)
header(s5, "Plan de Implementación · Presupuesto · Conclusiones",
       "3 fases · 90 días · $50,000 · ROI 1,118% · 5/5 KPIs del caso cumplidos")

# ── Presupuesto (izquierda top) ─────────────────────────────────
rect(s5, 0.2, 1.1, 4.55, 0.05, SAP_BLUE)
rect(s5, 0.2, 1.15, 4.55, 2.4, LIGHT_GRAY)
tb(s5, "PRESUPUESTO — USD $50,000 (límite exacto del caso)", 0.35, 1.2, 4.3, 0.28,
   size=9, bold=True, color=SAP_BLUE)

budget = [
    ("SAP Integration Suite",    "$12,000", "24%"),
    ("Portal Web de Pedidos",    "$10,000", "20%"),
    ("API ERP Legacy",           "$8,000",  "16%"),
    ("API Sistema Financiero",   "$5,000",  "10%"),
    ("TMS Beetrack",             "$5,500",  "11%"),
    ("Sistema QC Digital",       "$4,000",  "8%"),
    ("Datil.me (Facturación)",   "$2,500",  "5%"),
    ("Capacitación",             "$3,000",  "6%"),
    ("TOTAL",                    "$50,000", "100%"),
]
for i, (item, cost, pct) in enumerate(budget):
    top = 1.52 + i * 0.223
    is_total = item == "TOTAL"
    bg = DARK_BLUE if is_total else (WHITE if i%2==0 else LIGHT_GRAY)
    rect(s5, 0.2, top, 4.55, 0.223, bg)
    fc = WHITE if is_total else DARK_GRAY
    tb(s5, item, 0.3,  top+0.03, 2.8,  0.17, size=7.5, bold=is_total, color=fc)
    tb(s5, cost, 3.12, top+0.03, 0.85, 0.17, size=7.5, bold=is_total,
       color=(AMBER if is_total else GREEN), align=PP_ALIGN.RIGHT)
    tb(s5, pct,  4.0,  top+0.03, 0.6,  0.17, size=7.5, color=MED_GRAY if not is_total else WHITE,
       align=PP_ALIGN.RIGHT)

# ── Plan implementación (derecha top) ───────────────────────────
rect(s5, 5.05, 1.1, 4.7, 0.05, GREEN)
rect(s5, 5.05, 1.15, 4.7, 2.4, LIGHT_GRAY)
tb(s5, "PLAN DE IMPLEMENTACIÓN — 90 DÍAS", 5.2, 1.2, 4.4, 0.28, size=9, bold=True, color=GREEN)

phases = [
    ("FASE 1\nDías 1–30", "Portal Web + SAP Integration Suite\n+ APIs ERP y Financiero\n→ Elimina trabajo manual inmediato", "$35,000", SAP_BLUE),
    ("FASE 2\nDías 31–60","Sistema QC Digital + tablets\n+ Nuevos roles: QC y Analista Int.\n→ Reproceso 35% → 5%",           "$9,000",  GREEN),
    ("FASE 3\nDías 61–90","TMS Beetrack + Datil.me\n+ Capacitación + Go-Live\n→ Proceso 100% automatizado",                 "$6,000",  AMBER),
]
for i, (ph, desc, cost, col) in enumerate(phases):
    top = 1.55 + i * 0.64
    rect(s5, 5.15, top, 1.1, 0.58, col)
    tb(s5, ph, 5.2, top+0.05, 1.0, 0.5, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(s5, desc, 6.35, top+0.05, 2.4, 0.5, size=8, color=DARK_GRAY)
    tb(s5, cost, 8.8, top+0.17, 0.9, 0.28, size=9.5, bold=True, color=col, align=PP_ALIGN.RIGHT)

# ── Process Mining ───────────────────────────────────────────────
rect(s5, 0.2, 3.68, 4.55, 0.05, DARK_BLUE)
rect(s5, 0.2, 3.73, 4.55, 1.6, LIGHT_GRAY)
tb(s5, "PROCESS MINING — SAP Signavio Process Intelligence",
   0.35, 3.78, 4.3, 0.28, size=9, bold=True, color=DARK_BLUE)
multiline(s5, [
    ("Extrae event logs del ERP para descubrir el proceso real", False, DARK_GRAY),
    ("(as-executed) y compara contra el modelo BPMN TO-BE.", False, DARK_GRAY),
    ("", False),
    ("✔  Detecta desviaciones: modelo vs. ejecución real", False, DARK_GRAY),
    ("✔  Cuantifica tiempos y cuellos de botella con datos reales", False, DARK_GRAY),
    ("✔  Conformance checking semana a semana post-implementación", False, DARK_GRAY),
    ("✔  Alimenta el ciclo de mejora continua (TO-BE → AS-IS futuro)", False, DARK_GRAY),
], 0.35, 4.1, 4.3, 1.2, size=9, default_color=DARK_GRAY)

# ── KPIs conclusivos ─────────────────────────────────────────────
rect(s5, 5.05, 3.68, 4.7, 0.05, UPC_RED)
rect(s5, 5.05, 3.73, 4.7, 1.6, LIGHT_GRAY)
tb(s5, "RESULTADOS — 5/5 KPIs DEL CASO CUMPLIDOS",
   5.2, 3.78, 4.4, 0.28, size=9, bold=True, color=UPC_RED)
multiline(s5, [
    ("✔  Tiempo ciclo:  595 → 252.5 min  (−57.6%)  <  Meta 350 min", True, GREEN),
    ("✔  Costo/pedido:  $101.92 → $55.23  (−45.8%)  <  Meta $70.00", True, GREEN),
    ("✔  Reproceso:     35% → 5%  (−85.7%)  ≤  Meta 5%", True, GREEN),
    ("✔  Nuevos roles:  2 de 2 (máx. permitido)", True, GREEN),
    ("✔  Presupuesto:   $50,000 exactos  ≤  Límite $50K", True, GREEN),
    ("", False),
    ("ROI 12 meses:  1,118%  ·  Payback: ~0.9 meses", True, SAP_BLUE),
    ("Ahorro mensual: $56,028  (1,200 pedidos × $46.69)", False, DARK_GRAY),
    ("Fabricación 120 min ✔  ·  QC 30 min ✔  ·  07:00–14:00 ✔", False, DARK_GRAY),
], 5.2, 4.1, 4.4, 1.2, size=9, default_color=GREEN)

# ── Banner final ─────────────────────────────────────────────────
rect(s5, 0, 5.42, 10, 0.06, UPC_RED)
rect(s5, 0, 5.48, 10, 1.0, DARK_BLUE)
tb(s5, "Universidad Peruana de Ciencias Aplicadas  ·  SAP Signavio Regional Challenge 2026",
   0.3, 5.54, 7.0, 0.3, size=9.5, bold=True, color=WHITE)
tb(s5, "Profesor: Mgtr. Reyes Arce, Balmes Javier",
   0.3, 5.85, 5.0, 0.28, size=9, color=MED_GRAY)
img(s5, UPC_LOGO, 7.8, 5.5, 1.9, 0.85)

footer(s5, 5)


# ─────────────────────────────────────────────────────────────────
# GUARDAR
# ─────────────────────────────────────────────────────────────────
prs.save(OUTPUT)
print(f"✅  Presentación guardada en:\n    {OUTPUT}")
print("\nSlides generados:")
print("  Slide 0 — PORTADA  (UPC + SAP Signavio + Resumen ejecutivo)")
print("  Slide 1 — Diagnóstico AS-IS  (Empresa · 8 problemas · KPIs reales)")
print("  Slide 2 — Modelado AS-IS  (BPMN PNG real · anotaciones · métricas)")
print("  Slide 3 — Propuesta TO-BE  (4 palancas · stack · 2 roles)")
print("  Slide 4 — Modelado TO-BE + Simulación  (BPMN PNG · KPI tabla · capturas)")
print("  Slide 5 — Plan · Presupuesto · Process Mining · Conclusiones")
