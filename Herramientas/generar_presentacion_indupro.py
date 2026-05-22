"""
Generador de presentación PPT — INDUPRO S.A.
SAP Signavio Regional Challenge 2026
5 diapositivas de contenido (sin portada ni cierre)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ──────────────────────────────────────────────────────────────────
# PALETA DE COLORES SAP / INDUPRO
# ──────────────────────────────────────────────────────────────────
SAP_BLUE      = RGBColor(0x00, 0x70, 0xF2)   # #0070F2
DARK_BLUE     = RGBColor(0x1B, 0x2A, 0x49)   # #1B2A49
GOLD          = RGBColor(0xF0, 0xAB, 0x00)   # #F0AB00  SAP Gold
GREEN         = RGBColor(0x2E, 0x8B, 0x57)   # #2E8B57
RED           = RGBColor(0xC0, 0x39, 0x2B)   # #C0392B
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY    = RGBColor(0xF2, 0xF4, 0xF8)
MED_GRAY      = RGBColor(0x8A, 0x99, 0xB0)
DARK_GRAY     = RGBColor(0x44, 0x44, 0x44)

# ──────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────
def add_rect(slide, left, top, width, height, fill_color, alpha=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    return shape

def add_text_box(slide, text, left, top, width, height,
                 font_size=12, bold=False, color=WHITE,
                 align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_text_multiline(slide, lines, left, top, width, height,
                       font_size=10, color=DARK_GRAY, bold_first=False,
                       line_spacing=None, align=PP_ALIGN.LEFT):
    """lines: list of (text, bold, color_override)"""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    txBox.word_wrap = True
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, str):
            txt, bld, col = item, False, color
        else:
            txt = item[0]
            bld = item[1] if len(item) > 1 else False
            col = item[2] if len(item) > 2 else color
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = txt
        run.font.size = Pt(font_size)
        run.font.bold = bld
        run.font.color.rgb = col
    return txBox

def slide_header(slide, title, subtitle=None, title_color=WHITE,
                 bar_color=DARK_BLUE, accent_color=SAP_BLUE):
    """Header bar con título y barra de acento izquierda"""
    add_rect(slide, 0, 0, 10, 1.1, bar_color)
    # Barra de acento izquierda
    add_rect(slide, 0, 0, 0.08, 1.1, accent_color)
    add_text_box(slide, title, 0.2, 0.08, 8.0, 0.6,
                 font_size=22, bold=True, color=title_color, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text_box(slide, subtitle, 0.2, 0.65, 9.0, 0.38,
                     font_size=10, bold=False, color=MED_GRAY, align=PP_ALIGN.LEFT)

def card(slide, left, top, width, height, title, fill=LIGHT_GRAY,
         title_color=DARK_BLUE, border_color=SAP_BLUE, title_size=10):
    """Card con título y borde superior coloreado"""
    add_rect(slide, left, top, width, 0.04, border_color)
    add_rect(slide, left, top+0.04, width, height-0.04, fill)
    add_text_box(slide, title, left+0.1, top+0.08, width-0.2, 0.28,
                 font_size=title_size, bold=True, color=title_color)

def kpi_box(slide, left, top, w, h, label, value, val_color=SAP_BLUE,
            delta=None, delta_good=True):
    add_rect(slide, left, top, w, h, LIGHT_GRAY)
    add_rect(slide, left, top, w, 0.04, val_color)
    add_text_box(slide, label, left+0.05, top+0.06, w-0.1, 0.22,
                 font_size=8, bold=False, color=MED_GRAY)
    add_text_box(slide, value, left+0.05, top+0.26, w-0.1, 0.3,
                 font_size=14, bold=True, color=val_color)
    if delta:
        dcol = GREEN if delta_good else RED
        add_text_box(slide, delta, left+0.05, top+0.55, w-0.1, 0.22,
                     font_size=8, bold=True, color=dcol)


# ──────────────────────────────────────────────────────────────────
# PRESENTACIÓN
# ──────────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]  # completamente en blanco


# ══════════════════════════════════════════════════════════════════
# SLIDE 1 — INDUPRO: Empresa y Situación Actual
# ══════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(blank_layout)
slide_header(s1, "INDUPRO S.A. — Empresa y Situación Actual",
             "SAP Signavio Regional Challenge 2026 · Caso de estudio",
             accent_color=GOLD)

# ── Columna izquierda: Perfil empresa ──────────────────────────
card(s1, 0.2, 1.25, 4.6, 2.6, "PERFIL DE EMPRESA", border_color=GOLD)
company_lines = [
    ("", False),
    ("🏭  Fabricante de galletas industriales — Ecuador", False, DARK_GRAY),
    ("📦  ~1,200 pedidos / mes  (40/día hábil)", False, DARK_GRAY),
    ("👥  Roles actuales: 8 departamentos en proceso", False, DARK_GRAY),
    ("💻  Sistemas actuales: ERP Legacy + Sist. Financiero", False, DARK_GRAY),
    ("     (sin integración entre ellos)", True, MED_GRAY),
    ("🔗  Pedidos vía correo/teléfono → digitación en Excel", False, DARK_GRAY),
    ("📋  QC reactivo al final → 18% de reproceso", False, DARK_GRAY),
]
add_text_multiline(s1, company_lines, 0.3, 1.5, 4.4, 2.3, font_size=9.5, color=DARK_GRAY)

# ── Columna derecha: Problemas identificados ───────────────────
card(s1, 5.1, 1.25, 4.7, 2.6, "8 PROBLEMAS IDENTIFICADOS (AS-IS)", border_color=RED)
problems = [
    ("", False),
    ("P1  Validación manual en Excel → errores frecuentes", False, DARK_GRAY),
    ("P2  Sin integración: Sistema Financiero ↔ ERP", False, DARK_GRAY),
    ("P3  Consulta de stock en registros físicos", False, DARK_GRAY),
    ("P4  Confirmación manual → 20 min de espera", False, DARK_GRAY),
    ("P5  Órdenes de producción en papel", False, DARK_GRAY),
    ("P6  QC reactivo al final → 18% de lotes rechazados", False, DARK_GRAY),
    ("P7  Asignación de transporte por llamadas telefónicas", False, DARK_GRAY),
    ("P8  Facturación manual → 20 min adicionales", False, DARK_GRAY),
]
add_text_multiline(s1, problems, 5.2, 1.5, 4.5, 2.3, font_size=9.5, color=DARK_GRAY)

# ── KPIs situación actual ──────────────────────────────────────
add_text_box(s1, "KPIs ACTUALES (ruta crítica: fabricación + reproceso)",
             0.2, 3.95, 9.6, 0.28, font_size=9, bold=True, color=DARK_BLUE)
kpi_box(s1, 0.2,  4.25, 2.4, 1.05, "Tiempo de ciclo",    "595 min",   RED,     "⚠ Objetivo: < 350 min", False)
kpi_box(s1, 2.75, 4.25, 2.4, 1.05, "Costo por pedido",   "$101.92",   RED,     "⚠ Objetivo: < $70.00", False)
kpi_box(s1, 5.3,  4.25, 2.4, 1.05, "Tasa de reproceso",  "18%",       RED,     "⚠ Objetivo: < 5%", False)
kpi_box(s1, 7.85, 4.25, 2.0, 1.05, "Sistemas integrados","0 de 4",    RED,     "⚠ Silos desconectados", False)

# ── Nota inferior ──────────────────────────────────────────────
add_rect(s1, 0, 5.5, 10, 0.04, GOLD)
add_text_box(s1, "📌  Nota: El caso documenta 555 min y $105.91 — valores que contienen errores aritméticos verificados. Valores correctos: 595 min / $101.92.",
             0.2, 5.58, 9.6, 0.4, font_size=7.5, color=MED_GRAY, italic=True)

# ── Slide number ───────────────────────────────────────────────
add_text_box(s1, "1 / 5", 9.2, 7.1, 0.7, 0.3, font_size=8, color=MED_GRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 2 — AS-IS Modelado
# ══════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(blank_layout)
slide_header(s2, "AS-IS — Proceso de Gestión de Pedidos (Estado Actual)",
             "BPMN 2.0 · SAP Signavio Process Manager · 7 swimlanes · 15 actividades",
             accent_color=RED)

# ── Área de imagen BPMN ────────────────────────────────────────
img_box = add_rect(s2, 0.2, 1.2, 9.6, 4.4, LIGHT_GRAY)
add_text_box(s2,
    "[ INSERTAR AQUÍ: Captura del diagrama AS-IS desde SAP Signavio ]\n"
    "Archivo: INDUPRO_ASIS_Corregido_v2.bpmn\n\n"
    "Exportar desde Signavio: Diagrama → Export → PNG/SVG → pegar aquí",
    0.2, 2.5, 9.6, 1.5,
    font_size=10, color=MED_GRAY, align=PP_ALIGN.CENTER, italic=True)

# ── Anotaciones sobre el diagrama ─────────────────────────────
# Top-right tag rojo: cuello de botella
rb = add_rect(s2, 7.5, 1.25, 2.2, 0.85, RED)
add_text_box(s2, "⏱ CUELLO DE BOTELLA\nVerif. crédito + stock: 110 min\n(sin integración, secuencial)",
             7.55, 1.3, 2.1, 0.75, font_size=7.5, bold=False, color=WHITE)

# Bottom-left: estadística de reproceso
rb2 = add_rect(s2, 0.2, 4.7, 2.3, 0.82, RED)
add_text_box(s2, "♻ REPROCESO\n18% de lotes rechazados en QC\n+90 min por pedido afectado",
             0.25, 4.75, 2.2, 0.72, font_size=7.5, color=WHITE)

# ── Barra de resumen inferior ──────────────────────────────────
add_rect(s2, 0, 5.6, 10, 1.0, DARK_BLUE)
summary_items = [
    (0.2,  "DURACIÓN TOTAL",  "595 min", RED),
    (2.55, "COSTO/PEDIDO",    "$101.92", RED),
    (4.9,  "TASA REPROCESO",  "18%",     RED),
    (7.25, "ERRORES MANUALES","Altos",   RED),
]
for lft, lbl, val, col in summary_items:
    add_text_box(s2, lbl, lft, 5.65, 2.2, 0.22, font_size=7, bold=False, color=MED_GRAY)
    add_text_box(s2, val, lft, 5.88, 2.2, 0.35, font_size=15, bold=True, color=col)

add_text_box(s2, "2 / 5", 9.2, 7.1, 0.7, 0.3, font_size=8, color=MED_GRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 3 — Propuesta TO-BE
# ══════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(blank_layout)
slide_header(s3, "Propuesta de Rediseño — TO-BE",
             "4 palancas de mejora · $50,000 · 2 nuevos roles · 90 días de implementación",
             accent_color=GREEN)

# ── 4 Palancas ─────────────────────────────────────────────────
palancas = [
    ("1. AUTOMATIZACIÓN", "Validaciones, confirmaciones\ny factura: 0 intervención humana", SAP_BLUE),
    ("2. PARALELIZACIÓN", "Crédito + Stock simultáneos\nvía AND-Split/Join: −50 min", GOLD),
    ("3. INTEGRACIÓN", "SAP Integration Suite como\nmiddleware central (hub-and-spoke)", GREEN),
    ("4. QC PREVENTIVO", "Control en-proceso: tasa\nde reproceso 18% → 5%", RED),
]
for i, (title, body, col) in enumerate(palancas):
    lft = 0.2 + i * 2.45
    add_rect(s3, lft, 1.2, 2.3, 0.04, col)
    add_rect(s3, lft, 1.24, 2.3, 1.7, LIGHT_GRAY)
    add_text_box(s3, title, lft+0.1, 1.28, 2.1, 0.3, font_size=9, bold=True, color=col)
    add_text_box(s3, body,  lft+0.1, 1.58, 2.1, 1.3, font_size=9, color=DARK_GRAY)

# ── Stack tecnológico ──────────────────────────────────────────
add_text_box(s3, "STACK TECNOLÓGICO", 0.2, 3.05, 5.0, 0.28,
             font_size=9, bold=True, color=DARK_BLUE)
tech_lines = [
    ("🔗  SAP Integration Suite — Middleware central (orquesta todo)", True, SAP_BLUE),
    ("🌐  Portal Web de Pedidos — Reemplaza correo/Excel (User Task)", False, DARK_GRAY),
    ("📡  API Layer ERP Legacy — Stock en tiempo real (Service Task)", False, DARK_GRAY),
    ("💳  API Sistema Financiero — Crédito automático (Service Task)", False, DARK_GRAY),
    ("📱  Sistema QC Digital — Checklist en-proceso + inspección final", False, DARK_GRAY),
    ("🚚  TMS Beetrack — Asignación automática + firma digital", False, DARK_GRAY),
    ("🧾  Datil.me — Factura electrónica SRI automática", False, DARK_GRAY),
]
add_text_multiline(s3, tech_lines, 0.2, 3.38, 5.2, 2.5, font_size=9, color=DARK_GRAY)

# ── Nuevos roles ───────────────────────────────────────────────
add_text_box(s3, "2 NUEVOS ROLES (máx. permitido)", 5.5, 3.05, 4.3, 0.28,
             font_size=9, bold=True, color=DARK_BLUE)

card(s3, 5.5, 3.38, 4.3, 1.0, "Analista de Integración de Sistemas", border_color=SAP_BLUE, title_size=8.5)
add_text_box(s3, "$18/hr · Administra SAP Integration Suite\nMonitorea APIs y flujos de integración", 5.6, 3.72, 4.1, 0.6,
             font_size=8.5, color=DARK_GRAY)

card(s3, 5.5, 4.52, 4.3, 1.0, "Operario de Control de Calidad en Proceso", border_color=GREEN, title_size=8.5)
add_text_box(s3, "$11/hr · Ejecuta QC digital durante fabricación\nReduce reproceso del 18% al 5%", 5.6, 4.86, 4.1, 0.6,
             font_size=8.5, color=DARK_GRAY)

# ── Nota IT Systems ────────────────────────────────────────────
add_rect(s3, 0, 5.65, 10, 0.9, DARK_BLUE)
add_text_box(s3,
    "📐  NOTACIÓN SIGNAVIO:  Los IT Systems (SAP Integration Suite, Portal Web, TMS, etc.) son ARTEFACTOS — NO son lanes. "
    "Se conectan a las tareas con asociación no direccional (línea punteada sin flecha). "
    "Registrar primero en el Signavio Dictionary (Entregable E3).",
    0.25, 5.72, 9.5, 0.75, font_size=8.5, color=WHITE)

add_text_box(s3, "3 / 5", 9.2, 7.1, 0.7, 0.3, font_size=8, color=MED_GRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 4 — TO-BE Modelado + KPIs + Simulación
# ══════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(blank_layout)
slide_header(s4, "TO-BE — Proceso Rediseñado + Comparación KPIs",
             "BPMN 2.0 · AND-Split/Join · IT System artifacts · Additional Participant · Tipos de tarea",
             accent_color=GREEN)

# ── Área imagen BPMN TO-BE ─────────────────────────────────────
add_rect(s4, 0.2, 1.2, 6.5, 3.6, LIGHT_GRAY)
add_text_box(s4,
    "[ INSERTAR: Diagrama TO-BE desde SAP Signavio ]\n\n"
    "Incluir: AND-Split antes de Act.2A/2B · IT Systems como artefactos\n"
    "Additional Participant en Act.7 (Op.QC) y Act.9B (Inspector)",
    0.2, 2.5, 6.5, 1.2,
    font_size=9.5, color=MED_GRAY, align=PP_ALIGN.CENTER, italic=True)

# Etiqueta verde sobre el área de imagen
add_rect(s4, 0.2, 1.2, 2.0, 0.32, GREEN)
add_text_box(s4, "TO-BE (rediseñado)", 0.25, 1.23, 1.9, 0.26,
             font_size=8, bold=True, color=WHITE)

# ── Tabla KPIs comparativa ─────────────────────────────────────
add_text_box(s4, "COMPARACIÓN DE KPIs", 6.85, 1.2, 3.0, 0.28,
             font_size=9, bold=True, color=DARK_BLUE)

kpis = [
    ("Tiempo ciclo",     "595 min",  "281 min",   "−52.8%", True),
    ("Con reproceso",    "595 min",  "341 min",   "−42.7%", True),
    ("Costo / pedido",   "$101.92",  "$47.21",    "−53.7%", True),
    ("Con reproceso",    "$101.92",  "$55.21",    "−45.8%", True),
    ("Tasa reproceso",   "18%",      "5%",        "−72.2%", True),
    ("Tiempo verif.",    "110 min",  "15 min",    "−86.4%", True),
    ("Facturación",      "20 min",   "5 min",     "−75.0%", True),
]

# Header de la tabla
row_tops = [1.55 + i * 0.38 for i in range(len(kpis) + 1)]
add_rect(s4, 6.85, row_tops[0], 3.0, 0.35, DARK_BLUE)
for col_txt, col_lft in [("KPI", 6.88), ("AS-IS", 8.1), ("TO-BE", 8.72), ("Δ", 9.45)]:
    add_text_box(s4, col_txt, col_lft, row_tops[0]+0.04, 0.65, 0.27,
                 font_size=7.5, bold=True, color=WHITE)

for i, (kpi, asis, tobe, delta, good) in enumerate(kpis):
    row_bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    add_rect(s4, 6.85, row_tops[i+1], 3.0, 0.36, row_bg)
    dcol = GREEN if good else RED
    for txt, lft in [(kpi, 6.88), (asis, 8.08), (tobe, 8.7), (delta, 9.42)]:
        fcol = DARK_GRAY
        if txt == asis:  fcol = RED
        if txt == tobe:  fcol = GREEN
        if txt == delta: fcol = dcol
        add_text_box(s4, txt, lft, row_tops[i+1]+0.06, 0.65, 0.26,
                     font_size=7.5, bold=(txt == delta), color=fcol)

# ── Simulación Signavio ────────────────────────────────────────
add_rect(s4, 0.2, 4.9, 6.5, 0.04, SAP_BLUE)
add_text_box(s4, "SIMULACIÓN EN SAP SIGNAVIO", 0.2, 4.98, 4.0, 0.28,
             font_size=9, bold=True, color=DARK_BLUE)

sim_cols = [
    ("Duration\n(minutos)", "1→15, 2A→15, 2B→10\n7→120, 8→30, 9B→60\n12→45, 13→5"),
    ("Frequency\n(gateways)", "¿Stock+Crédito OK?\nSÍ 70% / NO 30%\n¿QC OK? 95% / 5%"),
    ("Resources\n(tarifas/hr)", "Ventas $12 · Finanzas $13\nPlanta $8 · QC $11\nIntegración $18"),
    ("Resultado\nesperado", "TO-BE: ~281 min\n$47.21 / pedido\n(sin reproceso)"),
]
for i, (lbl, val) in enumerate(sim_cols):
    lft = 0.2 + i * 1.625
    add_rect(s4, lft, 5.32, 1.55, 0.04, SAP_BLUE)
    add_rect(s4, lft, 5.36, 1.55, 1.18, LIGHT_GRAY)
    add_text_box(s4, lbl, lft+0.06, 5.4, 1.42, 0.3, font_size=7.5, bold=True, color=SAP_BLUE)
    add_text_box(s4, val,  lft+0.06, 5.7, 1.42, 0.78, font_size=7.5, color=DARK_GRAY)

add_text_box(s4, "⚠ Usar siempre MINUTOS · Costs tab = costos fijos (no labor) · Resources tab = tarifas/hora",
             0.2, 6.55, 6.5, 0.3, font_size=7.5, color=MED_GRAY, italic=True)

add_text_box(s4, "4 / 5", 9.2, 7.1, 0.7, 0.3, font_size=8, color=MED_GRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# SLIDE 5 — Process Mining + Presupuesto + Conclusiones
# ══════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(blank_layout)
slide_header(s5, "Process Mining · Presupuesto · Conclusiones",
             "SAP Signavio Process Intelligence · $50,000 · ROI 754% a 12 meses",
             accent_color=SAP_BLUE)

# ──── PROCESS MINING (left-top) ────────────────────────────────
add_rect(s5, 0.2, 1.2, 4.55, 0.04, SAP_BLUE)
add_rect(s5, 0.2, 1.24, 4.55, 2.1, LIGHT_GRAY)
add_text_box(s5, "🔍  PROCESS MINING — SAP Signavio Process Intelligence",
             0.3, 1.28, 4.35, 0.3, font_size=9, bold=True, color=SAP_BLUE)
pm_lines = [
    ("El sistema extrae datos transaccionales del ERP y genera", False, DARK_GRAY),
    ("automáticamente el proceso real (as-executed) vs. el modelo.", False, DARK_GRAY),
    ("", False),
    ("✔  Detecta desviaciones entre el proceso modelado y el real", False, DARK_GRAY),
    ("✔  Identifica cuellos de botella con datos reales de producción", False, DARK_GRAY),
    ("✔  Alimenta el ciclo de mejora continua (TO-BE → nuevo AS-IS)", False, DARK_GRAY),
    ("✔  Fuente de datos: ERP Legacy + logs del SAP Integration Suite", False, DARK_GRAY),
    ("", False),
    ('📖  "Tu TO-BE tiene que estar acompañado de mineria de proceso.', False, MED_GRAY),
    ('     El sistema extrae datos, genera el proceso." -- Prof. Jimmy', True, MED_GRAY),
]
add_text_multiline(s5, pm_lines, 0.3, 1.62, 4.35, 1.6, font_size=8.5, color=DARK_GRAY)

# ──── PRESUPUESTO (right-top) ──────────────────────────────────
add_rect(s5, 5.0, 1.2, 4.8, 0.04, GOLD)
add_rect(s5, 5.0, 1.24, 4.8, 2.1, LIGHT_GRAY)
add_text_box(s5, "💰  PRESUPUESTO — USD $50,000 (límite exacto)",
             5.1, 1.28, 4.6, 0.3, font_size=9, bold=True, color=DARK_BLUE)

budget_rows = [
    ("SAP Integration Suite (config + flujos)", "$10,000"),
    ("Portal Web de Pedidos (UX + dev + deploy)", "$10,000"),
    ("API ERP Legacy (inventario tiempo real)",   "$8,000"),
    ("API Sistema Financiero (crédito auto)",     "$5,000"),
    ("Sistema QC Digital (app + tablets)",        "$4,000"),
    ("TMS Beetrack (suscripción + integración)",  "$5,500"),
    ("Factura Electrónica Datil.me",              "$2,500"),
    ("Capacitación y gestión del cambio",         "$5,000"),
    ("TOTAL",                                     "$50,000"),
]
for i, (item, cost) in enumerate(budget_rows):
    top = 1.62 + i * 0.178
    is_total = (item == "TOTAL")
    bg = DARK_BLUE if is_total else (LIGHT_GRAY if i%2==0 else WHITE)
    fc = WHITE if is_total else DARK_GRAY
    cc = GOLD if is_total else (GREEN if i<8 else GREEN)
    add_rect(s5, 5.0, top, 4.8, 0.175, bg)
    add_text_box(s5, item, 5.05, top+0.02, 3.4, 0.14, font_size=7.5, bold=is_total, color=fc)
    add_text_box(s5, cost, 8.45, top+0.02, 1.3, 0.14, font_size=7.5, bold=is_total, color=GOLD if is_total else GREEN,
                 align=PP_ALIGN.RIGHT)

# ──── PLAN DE IMPLEMENTACIÓN (left-bottom) ────────────────────
add_rect(s5, 0.2, 3.45, 4.55, 0.04, GREEN)
add_rect(s5, 0.2, 3.49, 4.55, 1.85, LIGHT_GRAY)
add_text_box(s5, "📅  PLAN DE IMPLEMENTACIÓN — 90 DÍAS",
             0.3, 3.53, 4.35, 0.28, font_size=9, bold=True, color=GREEN)
phases = [
    ("FASE 1  (Días 1-30)", "Middleware + Portal Web + APIs\n→ $33,000 · Elimina trabajo manual inmediato", SAP_BLUE),
    ("FASE 2  (Días 31-60)", "Sistema QC Digital + nuevos roles\n→ $4,000 · Reduce reproceso 18%→5%", GOLD),
    ("FASE 3  (Días 61-90)", "TMS + Facturación + Capacitación\n→ $13,000 · Proceso 100% automatizado", GREEN),
]
for i, (ph, desc, col) in enumerate(phases):
    top = 3.85 + i * 0.48
    add_rect(s5, 0.3, top, 1.4, 0.42, col)
    add_text_box(s5, ph, 0.33, top+0.04, 1.34, 0.38, font_size=7.5, bold=True, color=WHITE)
    add_text_box(s5, desc, 1.75, top+0.04, 2.9, 0.38, font_size=7.5, color=DARK_GRAY)

# ──── CONCLUSIONES / ROI (right-bottom) ───────────────────────
add_rect(s5, 5.0, 3.45, 4.8, 0.04, SAP_BLUE)
add_rect(s5, 5.0, 3.49, 4.8, 1.85, LIGHT_GRAY)
add_text_box(s5, "✅  CONCLUSIONES Y ROI",
             5.1, 3.53, 4.6, 0.28, font_size=9, bold=True, color=DARK_BLUE)

conc_lines = [
    ("", False),
    ("📉  −52.8% tiempo ciclo:  595 → 281 min (< meta 350 min)", True, GREEN),
    ("💵  −53.7% costo/pedido:  $101.92 → $47.21 (< meta $70)", True, GREEN),
    ("♻  −72.2% reproceso:  18% → 5% (meta cumplida)", True, GREEN),
    ("", False),
    ("💡  Ahorro mensual estimado: ~$35,600/mes", False, DARK_GRAY),
    ("🔄  Payback: ~1.4 meses sobre inversión de $50,000", False, DARK_GRAY),
    ("📈  ROI a 12 meses: 754%", True, SAP_BLUE),
    ("📦  TCO 3 años: $71,200 costo vs $1.28M en ahorros", False, DARK_GRAY),
    ("", False),
    ("⚙  Todas las restricciones del caso se cumplen al 100%:", False, DARK_GRAY),
    ("    ≤2 nuevos roles ✓ · ≤$50K presupuesto ✓ · <$70/pedido ✓", False, GREEN),
    ("    120 min fabricación ✓ · 30 min QC ✓ · 07:00-14:00 ✓", False, GREEN),
]
add_text_multiline(s5, conc_lines, 5.1, 3.83, 4.6, 1.4, font_size=8.5, color=DARK_GRAY)

# ──── Footer ───────────────────────────────────────────────────
add_rect(s5, 0, 5.45, 10, 0.04, SAP_BLUE)
add_text_box(s5, "SAP Signavio Regional Challenge 2026 · INDUPRO S.A. · Equipo ESPOL",
             0.2, 5.52, 9.6, 0.3, font_size=9, bold=False, color=MED_GRAY, align=PP_ALIGN.CENTER)

add_text_box(s5, "5 / 5", 9.2, 7.1, 0.7, 0.3, font_size=8, color=MED_GRAY, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════
# GUARDAR
# ══════════════════════════════════════════════════════════════════
output_path = r"c:\Users\drago\projects\ProyectoSAPSignavio\Analisis Final\INDUPRO_Presentacion_5Slides.pptx"
prs.save(output_path)
print(f"✅ Presentación guardada en:\n   {output_path}")
print(f"\nDiapositivas generadas:")
print("  Slide 1 — INDUPRO: Empresa y Situación Actual")
print("  Slide 2 — AS-IS: Proceso Actual (con área para imagen BPMN)")
print("  Slide 3 — Propuesta TO-BE: Palancas + Stack + Roles")
print("  Slide 4 — TO-BE: Modelado + KPIs comparativa + Simulación")
print("  Slide 5 — Process Mining + Presupuesto + Plan + Conclusiones")
