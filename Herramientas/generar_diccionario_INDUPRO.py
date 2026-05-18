"""
Generador del Diccionario INDUPRO para SAP Signavio
====================================================
Genera UN único archivo Excel listo para importar en SAP Signavio:

  Analisis/INDUPRO_Diccionario_Signavio.xlsx

Estructura por hoja (una por categoría, 11 en total):
  Fila 1 : cabeceras de columna  ← detectada automáticamente como header
  Fila 2+: datos del diccionario

Formato validado con el aviso de la plataforma SAP Signavio:
  "La herramienta detectará una fila de cabecera e importará todas las filas
  que queden en el diccionario, de acuerdo a un mapeado que será definido
  en el siguiente paso."

Cómo importar en Signavio (una vez por categoría):
  Explorer → Dictionary → seleccionar categoría
  → Import/Export → Import Excel → seleccionar este archivo
  → elegir la hoja correspondiente → mapear columnas → Import

Categorías:
  Organizational_Units | Roles | Departments | External_participants
  Documents | Activities | Events | IT_Systems | Risks | Controls | Others
"""

import os
import uuid
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "Analisis", "INDUPRO_Diccionario_Signavio.xlsx")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def new_id():
    return uuid.uuid4().hex  # 32-char hex, igual al formato Signavio

# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
CATEGORY_COLORS = {
    "Organizational_Units":  "1F3864",
    "Roles":                 "2E75B6",
    "Departments":           "00B050",
    "External_participants": "C55A11",
    "Documents":             "7030A0",
    "Activities":            "4472C4",
    "Events":                "ED7D31",
    "IT_Systems":            "404040",
    "Risks":                 "C00000",
    "Controls":              "375623",
    "Others":                "767171",
}

_thin = Side(style="thin", color="D0D0D0")
_BORDER = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
_ALT    = PatternFill("solid", fgColor="F4F4F4")

def _style_header(cell, hex_color):
    cell.fill      = PatternFill("solid", fgColor=hex_color)
    cell.font      = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border    = _BORDER

def _style_data(cell, row_idx):
    cell.font      = Font(name="Calibri", size=10)
    cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    cell.border    = _BORDER
    if row_idx % 2 == 0:
        cell.fill = _ALT

def _auto_width(ws, min_w=15, max_w=50):
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        best = max(
            (min(len(str(c.value or "")), max_w) for c in col),
            default=min_w,
        )
        ws.column_dimensions[letter].width = max(min_w, best + 3)

# ---------------------------------------------------------------------------
# Datos del Diccionario INDUPRO
# ---------------------------------------------------------------------------

# --- 1. Organizational_Units ---
ORG_UNITS_COLS = ["Title", "Description", "Relevant Documents", "Id"]
ORG_UNITS_DATA = [
    (
        "INDUPRO S.A.",
        "Empresa mediana de manufactura y distribución de productos industriales fundada en 1998. "
        "Sede principal en la ciudad capital, 2 plantas de producción en zonas industriales periféricas, "
        "1 centro de distribución. Más de 320 empleados, facturación ~USD 45 millones/año. "
        "Fabrica y distribuye componentes mecánicos, hidráulicos y eléctricos para los sectores "
        "de construcción (40%), minería (35%) y agro-industria (25%). +200 clientes activos.",
        "",
        new_id()
    ),
    (
        "Planta A",
        "Primera planta de producción de INDUPRO S.A. ubicada en zona industrial periférica. "
        "Dedicada a la fabricación de componentes mecánicos e hidráulicos. Utilización actual: ~78%.",
        "",
        new_id()
    ),
    (
        "Planta B",
        "Segunda planta de producción de INDUPRO S.A. ubicada en zona industrial periférica. "
        "Dedicada a la fabricación de componentes eléctricos e hidráulicos. Trabaja en coordinación con Planta A.",
        "",
        new_id()
    ),
    (
        "Centro de Distribución",
        "Centro de distribución principal de INDUPRO S.A. Gestiona el empaque, consolidación "
        "y despacho de productos terminados hacia los clientes. Ventana de despacho: 07:00-14:00 L-V.",
        "",
        new_id()
    ),
]

# --- 2. Roles ---
ROLES_COLS = ["Title", "Description", "Relevant Documents", "Responsible Mail Address", "Cost/Hour (USD)", "Quantity", "Id"]
ROLES_DATA = [
    (
        "Ejecutivo de Ventas",
        "Responsable de la recepción y validación de pedidos de clientes. Punto de contacto directo "
        "con el cliente para confirmación de pedidos, seguimiento y resolución de incidencias. "
        "Gestiona la comunicación por correo electrónico, teléfono y portal web.",
        "Solicitud de Compra del Cliente; Pedido Validado",
        "",
        "$12.00",
        "2 disponibles · 8h/día",
        new_id()
    ),
    (
        "Analista de Finanzas",
        "Responsable de la verificación de crédito del cliente y la generación/envío de facturas. "
        "Opera el sistema financiero y gestiona la cobranza. En el proceso TO-BE utiliza la integración "
        "API del sistema financiero para verificaciones automáticas de crédito.",
        "Factura; Reporte de Crédito",
        "",
        "$13.00",
        "1 disponible · 8h/día",
        new_id()
    ),
    (
        "Coordinador de Inventarios",
        "Responsable de la consulta y gestión de la disponibilidad de stock en bodega. "
        "En el proceso AS-IS consulta registros físicos y ERP legacy de forma separada. "
        "En el TO-BE utiliza el ERP integrado en tiempo real.",
        "Registro de Inventario; Consulta de Stock",
        "",
        "$10.00",
        "1 disponible · 8h/día",
        new_id()
    ),
    (
        "Planificador de Producción",
        "Responsable de la programación de órdenes de fabricación cuando no hay stock disponible. "
        "En el AS-IS usa planillas manuales. En el TO-BE utiliza el sistema ERP integrado con "
        "visibilidad de capacidad real de planta en tiempo real.",
        "Orden de Producción; Planilla de Producción",
        "",
        "$14.00",
        "1 disponible · 8h/día",
        new_id()
    ),
    (
        "Operario de Planta",
        "Responsable de la fabricación del producto según las órdenes de trabajo. Opera en Planta A "
        "o Planta B. Tiempo de fabricación estándar: 120 min/pedido (restricción técnica inamovible). "
        "En el TO-BE ejecuta también controles de calidad en-proceso (in-line QC).",
        "Orden de Trabajo; Checklist QC en-proceso",
        "",
        "$8.00",
        "6 disponibles · turno 8h",
        new_id()
    ),
    (
        "Inspector de Calidad",
        "Responsable de la inspección y liberación de productos terminados. Tiempo mínimo de inspección: "
        "30 min/pedido (requerimiento regulatorio interno inamovible). Tasa de aprobación AS-IS: 82%. "
        "Meta TO-BE: 95% de aprobación gracias al QC en-proceso durante manufactura.",
        "Checklist de Calidad; Reporte de Inspección",
        "",
        "$11.00",
        "2 disponibles · 8h/día",
        new_id()
    ),
    (
        "Coordinador de Logística",
        "Responsable del empaque, preparación para despacho, asignación de transportista y "
        "programación de entrega. En el AS-IS coordina por correo/teléfono. "
        "En el TO-BE utiliza el TMS para asignación automática de transportistas.",
        "Guía de Remisión; Lista de Empaque",
        "",
        "$10.00",
        "1 disponible · 8h/día (07:00-14:00 ventana despacho)",
        new_id()
    ),
    (
        "Gerente de Operaciones",
        "Responsable de la supervisión general del proceso de gestión de pedidos. "
        "Toma decisiones estratégicas sobre la planificación de producción, asignación de recursos "
        "y mejora continua del proceso. Rol de supervisión en ambos procesos AS-IS y TO-BE.",
        "",
        "",
        "$18.00",
        "1 disponible",
        new_id()
    ),
    (
        "Administrador de Sistemas (TO-BE)",
        "Nuevo rol propuesto en el proceso TO-BE. Administra el portal web de pedidos, monitorea "
        "el flujo digital del proceso y gestiona las integraciones API entre sistemas (ERP, TMS, "
        "sistema financiero). Uno de los 2 nuevos roles permitidos por las restricciones del desafío.",
        "",
        "",
        "$15.00",
        "1 nuevo rol · 8h/día",
        new_id()
    ),
    (
        "Técnico de Integración ERP (TO-BE)",
        "Nuevo rol propuesto en el proceso TO-BE. Mantiene las integraciones API y el ERP integrado "
        "en tiempo real. Brinda soporte técnico a los sistemas automatizados implementados. "
        "Segundo de los 2 nuevos roles permitidos por las restricciones del desafío.",
        "",
        "",
        "$14.00",
        "1 nuevo rol · 8h/día",
        new_id()
    ),
]

# --- 3. Departments ---
DEPTS_COLS = ["Title", "Description", "Relevant Documents", "Contact Persons", "Id"]
DEPTS_DATA = [
    (
        "Ventas y Servicio al Cliente",
        "Departamento responsable de la recepción y validación de pedidos de clientes, contacto directo "
        "con el cliente y gestión de la comunicación durante todo el proceso. Punto de entrada del "
        "proceso de gestión de pedidos de INDUPRO S.A. Cuenta con 2 Ejecutivos de Ventas.",
        "Solicitud de Compra del Cliente; Pedido Validado",
        "Ejecutivo de Ventas (2)",
        new_id()
    ),
    (
        "Planificación de Producción",
        "Departamento responsable de verificar inventarios y programar órdenes de fabricación. "
        "Coordina con Planta de Manufactura la capacidad disponible y los lotes de producción. "
        "Cuello de botella en AS-IS por programación manual sin visibilidad en tiempo real.",
        "Orden de Producción; Planilla de Producción",
        "Planificador de Producción (1)",
        new_id()
    ),
    (
        "Planta de Manufactura",
        "Departamento responsable de la fabricación de productos según órdenes de producción. "
        "Opera en Planta A y Planta B. Tiempo de fabricación estándar: 120 min/pedido (restricción técnica). "
        "Utilización actual: 78%. Capacidad: ~1,200 pedidos/mes con 85 SKUs activos.",
        "Orden de Trabajo; Ficha Técnica del Producto",
        "Operario de Planta (6)",
        new_id()
    ),
    (
        "Control de Calidad",
        "Departamento responsable de la inspección y liberación de productos terminados. "
        "Tiempo mínimo de inspección: 30 min/pedido (requerimiento regulatorio). "
        "Tasa de reproceso AS-IS: 18%. Meta TO-BE: reducir a <5% mediante QC en-proceso.",
        "Checklist de Calidad; Reporte de Inspección; Certificado de Calidad",
        "Inspector de Calidad (2)",
        new_id()
    ),
    (
        "Logística y Distribución",
        "Departamento responsable del empaque, consolidación, asignación de transportista "
        "y despacho al cliente. Ventana de despacho: 07:00-14:00 horas, lunes a viernes. "
        "En AS-IS asigna transportistas por llamadas telefónicas sin integración con tracking.",
        "Guía de Remisión; Lista de Empaque; Comprobante de Entrega",
        "Coordinador de Logística (1)",
        new_id()
    ),
    (
        "Finanzas y Facturación",
        "Departamento responsable de la verificación de crédito del cliente, generación de facturas "
        "y gestión de cobranza. En AS-IS la verificación de crédito es manual y secuencial (60 min). "
        "En TO-BE se integra con API para verificación automática (<15 min en paralelo).",
        "Factura; Reporte de Crédito; Orden de Cobro",
        "Analista de Finanzas (1)",
        new_id()
    ),
    (
        "Coordinación de Inventarios",
        "Departamento responsable de la consulta y gestión de disponibilidad de stock en bodega. "
        "En AS-IS consulta registros físicos y ERP legacy por separado (50 min, doble fuente). "
        "En TO-BE usa ERP integrado en tiempo real (10 min, fuente única).",
        "Registro de Inventario; Reporte de Stock",
        "Coordinador de Inventarios (1)",
        new_id()
    ),
]

# --- 4. External_participants ---
EXT_COLS = ["Title", "Description", "Relevant Documents", "Contact Mail Address", "Id"]
EXT_DATA = [
    (
        "Cliente - Sector Construcción",
        "Cliente del sector construcción. Representa el 40% del mercado objetivo de INDUPRO. "
        "Solicita componentes mecánicos e hidráulicos para proyectos de infraestructura. "
        "Punto de inicio del proceso: envía solicitud de compra por correo, teléfono o portal web.",
        "Solicitud de Compra del Cliente",
        "",
        new_id()
    ),
    (
        "Cliente - Sector Minería",
        "Cliente del sector minería. Representa el 35% del mercado objetivo de INDUPRO. "
        "Solicita componentes hidráulicos y eléctricos para operaciones mineras. "
        "Requiere tiempos de entrega cortos y trazabilidad del pedido.",
        "Solicitud de Compra del Cliente",
        "",
        new_id()
    ),
    (
        "Cliente - Sector Agro-industria",
        "Cliente del sector agro-industrial. Representa el 25% del mercado objetivo de INDUPRO. "
        "Solicita componentes mecánicos y eléctricos para maquinaria agrícola. "
        "Clientes estacionales con picos de demanda en épocas de cosecha.",
        "Solicitud de Compra del Cliente",
        "",
        new_id()
    ),
    (
        "Transportista Externo",
        "Empresa o persona responsable de la entrega física de los productos al cliente final. "
        "En AS-IS se asigna mediante llamadas telefónicas sin integración con tracking. "
        "En TO-BE se asigna automáticamente vía TMS. Firma la guía de remisión como evidencia de entrega.",
        "Guía de Remisión; Comprobante de Entrega",
        "",
        new_id()
    ),
    (
        "Proveedor de Materiales",
        "Proveedor externo de materias primas y materiales para el proceso de manufactura de INDUPRO. "
        "No forma parte directa del proceso de gestión de pedidos analizado, pero impacta en "
        "la disponibilidad de stock cuando no hay inventario suficiente.",
        "Orden de Compra a Proveedor",
        "",
        new_id()
    ),
]

# --- 5. Documents ---
DOCS_COLS = ["Title", "Description", "Relevant Documents", "Process Step", "Format", "Id"]
DOCS_DATA = [
    (
        "Solicitud de Compra del Cliente",
        "Documento inicial del proceso. Solicitud formal de compra enviada por el cliente "
        "vía correo electrónico, teléfono o portal web. Contiene: nombre del cliente, "
        "productos solicitados (SKU), cantidades, dirección de entrega y fecha requerida.",
        "",
        "Paso 1 — Recepción de solicitud",
        "Email / Formulario web / Verbal",
        new_id()
    ),
    (
        "Pedido Validado",
        "Pedido del cliente una vez verificados y correctos: datos del cliente, "
        "productos, cantidades y condiciones comerciales. Generado por Ventas tras la validación. "
        "En AS-IS se registra en Excel. En TO-BE se genera automáticamente desde el portal web.",
        "Solicitud de Compra del Cliente",
        "Paso 2 — Validación del pedido",
        "Excel (AS-IS) / Digital Portal (TO-BE)",
        new_id()
    ),
    (
        "Reporte de Crédito del Cliente",
        "Resultado de la verificación del estado crediticio del cliente. Indica si el cliente "
        "tiene crédito aprobado para el monto del pedido. En AS-IS: proceso manual en sistema "
        "financiero (60 min). En TO-BE: integración API automática (<15 min).",
        "Pedido Validado",
        "Paso 3 — Verificación de crédito",
        "Sistema Financiero (impresión/digital)",
        new_id()
    ),
    (
        "Reporte de Disponibilidad de Stock",
        "Documento que indica la disponibilidad de inventario en bodega para los productos solicitados. "
        "En AS-IS: revisión en registros físicos + ERP legacy por separado (50 min). "
        "En TO-BE: consulta automática en ERP integrado en tiempo real (10 min).",
        "Pedido Validado",
        "Paso 4 — Consulta de stock",
        "Registro físico / ERP legacy (AS-IS) · ERP en tiempo real (TO-BE)",
        new_id()
    ),
    (
        "Confirmación de Pedido al Cliente",
        "Notificación al cliente confirmando la recepción y aceptación del pedido. "
        "Incluye número de pedido, fecha estimada de entrega y condiciones acordadas. "
        "En AS-IS: correo electrónico manual (20 min). En TO-BE: confirmación automática (5 min).",
        "Pedido Validado",
        "Paso 6A — Confirmación de pedido",
        "Email (AS-IS) / Email/SMS automático (TO-BE)",
        new_id()
    ),
    (
        "Orden de Producción",
        "Documento formal que autoriza la fabricación de un lote de productos. Contiene: "
        "SKU, cantidad, especificaciones técnicas, planta asignada (A o B) y fecha programada. "
        "En AS-IS: planilla manual. En TO-BE: generada digitalmente por el sistema ERP.",
        "Pedido Validado; Reporte de Disponibilidad de Stock",
        "Paso 6B — Programación de producción",
        "Planilla impresa (AS-IS) / ERP digital (TO-BE)",
        new_id()
    ),
    (
        "Orden de Trabajo",
        "Documento operativo entregado a los operarios de planta con las instrucciones de fabricación. "
        "Derivada de la Orden de Producción. Incluye: proceso de fabricación, materiales, tiempos "
        "estándar (120 min) y especificaciones de calidad.",
        "Orden de Producción",
        "Paso 7 — Fabricación",
        "Impresa (AS-IS) / Digital en tablet (TO-BE)",
        new_id()
    ),
    (
        "Checklist de Calidad",
        "Formulario de inspección que documenta los controles de calidad realizados al producto terminado. "
        "Registra los criterios evaluados, resultados y decisión de aprobación/rechazo. "
        "Tasa de rechazo AS-IS: 18%. Meta TO-BE: <5% con QC en-proceso.",
        "Orden de Trabajo",
        "Paso 8 — Inspección de calidad",
        "Físico impreso (AS-IS) / Sistema QC digital (TO-BE)",
        new_id()
    ),
    (
        "Reporte de Reproceso",
        "Documento que registra los lotes rechazados en control de calidad y el plan de reproceso. "
        "Incluye causa del rechazo, acciones correctivas y tiempo adicional de reproceso (90 min AS-IS, "
        "60 min TO-BE). Activa el ciclo de reproceso en el proceso.",
        "Checklist de Calidad",
        "Paso 9B — Reproceso del lote",
        "Manual (AS-IS) / Sistema QC digital (TO-BE)",
        new_id()
    ),
    (
        "Lista de Empaque (Packing List)",
        "Documento que detalla el contenido del paquete a despachar: productos, cantidades, "
        "peso, dimensiones y número de pedido. Acompaña la guía de remisión en el despacho.",
        "Pedido Validado; Checklist de Calidad",
        "Paso 10 — Empaque y preparación",
        "Manual (AS-IS) / Sistema etiquetado digital (TO-BE)",
        new_id()
    ),
    (
        "Guía de Remisión",
        "Documento legal que acompaña la mercadería durante el transporte. Registra: remitente, "
        "destinatario, productos, cantidades y condiciones de entrega. El cliente firma al recibir "
        "la mercadería. En TO-BE se implementa firma digital.",
        "Lista de Empaque",
        "Paso 12 — Entrega al cliente",
        "Impresa (AS-IS) / Firma digital en app móvil (TO-BE)",
        new_id()
    ),
    (
        "Factura",
        "Documento legal de cobro emitido tras la entrega del pedido al cliente. Contiene: "
        "detalle de productos, cantidades, precios y condiciones de pago. En AS-IS: generación "
        "manual en sistema de facturación (20 min). En TO-BE: factura electrónica automática (5 min).",
        "Guía de Remisión; Pedido Validado",
        "Paso 13 — Generación de factura",
        "PDF (AS-IS) / Factura Electrónica XML/PDF (TO-BE)",
        new_id()
    ),
]

# --- 6. Activities ---
ACTS_COLS = ["Title", "Description", "Relevant Documents", "Responsible Role", "System/Tool", "Duration AS-IS (min)", "Duration TO-BE (min)", "Cost AS-IS (USD)", "Id"]
ACTS_DATA = [
    (
        "Recepción de solicitud del cliente",
        "Recibir y registrar la solicitud de compra enviada por el cliente vía correo electrónico, "
        "teléfono o portal web. En AS-IS: registro manual. En TO-BE: recepción automática por portal "
        "web con validación integrada de campos obligatorios.",
        "Solicitud de Compra del Cliente",
        "Ejecutivo de Ventas",
        "Correo / Teléfono (AS-IS) · Portal Web (TO-BE)",
        "30",
        "15",
        "$6.00",
        new_id()
    ),
    (
        "Validación manual de datos del pedido",
        "Verificar la completitud y corrección de los datos del pedido: datos del cliente, "
        "productos solicitados, cantidades y dirección de entrega. En AS-IS en Excel con alto "
        "riesgo de errores. En TO-BE fusionada con recepción (validación automática por portal).",
        "Solicitud de Compra del Cliente; Pedido Validado",
        "Ejecutivo de Ventas",
        "Hoja de Excel (AS-IS) · Portal Web automatizado (TO-BE)",
        "45",
        "0 (fusionada con paso 1)",
        "$9.00",
        new_id()
    ),
    (
        "Verificación de crédito del cliente",
        "Comprobar que el cliente tiene saldo disponible y crédito aprobado para el monto del pedido. "
        "AS-IS: proceso manual y secuencial (60 min, sin integración). "
        "TO-BE: consulta API automática al sistema financiero (<15 min, en paralelo con consulta de stock).",
        "Reporte de Crédito del Cliente",
        "Analista de Finanzas",
        "Sistema Financiero manual (AS-IS) · API Sistema Financiero (TO-BE)",
        "60",
        "15",
        "$13.00",
        new_id()
    ),
    (
        "Consulta de disponibilidad de stock en bodega",
        "Verificar si existe stock disponible en bodega para los productos del pedido. "
        "AS-IS: revisión en registros físicos + ERP legacy por separado (50 min, doble fuente de verdad). "
        "TO-BE: consulta automática en ERP integrado en tiempo real (10 min, en paralelo con crédito).",
        "Reporte de Disponibilidad de Stock",
        "Coordinador de Inventarios",
        "Registro físico / ERP Legacy (AS-IS) · ERP Integrado Tiempo Real (TO-BE)",
        "50",
        "10",
        "$8.33",
        new_id()
    ),
    (
        "Confirmación de pedido al cliente",
        "Notificar al cliente que su pedido ha sido recibido, validado y procesado exitosamente. "
        "Incluye número de pedido asignado y fecha estimada de entrega. "
        "AS-IS: correo manual (20 min). TO-BE: notificación automática por email/SMS (5 min).",
        "Confirmación de Pedido al Cliente",
        "Ejecutivo de Ventas",
        "Correo electrónico (AS-IS) · Portal Web / SMS automático (TO-BE)",
        "20",
        "5",
        "$4.00",
        new_id()
    ),
    (
        "Programación de orden de producción",
        "Planificar y programar la orden de fabricación cuando no hay stock disponible. "
        "AS-IS: planilla manual sin visibilidad de capacidad (40 min). "
        "TO-BE: sistema ERP con visibilidad en tiempo real de capacidad de Planta A y B (20 min).",
        "Orden de Producción",
        "Planificador de Producción",
        "Planilla de producción manual (AS-IS) · Sistema ERP Integrado (TO-BE)",
        "40",
        "20",
        "$9.33",
        new_id()
    ),
    (
        "Fabricación del producto",
        "Manufactura del lote de productos según la orden de trabajo en Planta A o B. "
        "Tiempo estándar: 120 min/pedido — restricción técnica inamovible. "
        "TO-BE: incorpora QC en-proceso (in-line quality control) para reducir tasa de rechazo.",
        "Orden de Trabajo; Checklist QC en-proceso",
        "Operario de Planta",
        "Órdenes de trabajo impresas (AS-IS) · Órdenes digitales + QC in-line (TO-BE)",
        "120",
        "120",
        "$16.00",
        new_id()
    ),
    (
        "Inspección y liberación de calidad",
        "Inspección final del producto terminado antes del despacho. "
        "Tiempo mínimo: 30 min/pedido — requerimiento regulatorio interno inamovible. "
        "AS-IS: checklist físico, tasa de aprobación 82%. TO-BE: sistema QC digital, meta 95% aprobación.",
        "Checklist de Calidad",
        "Inspector de Calidad",
        "Checklist físico impreso (AS-IS) · Sistema QC Digital (TO-BE)",
        "30",
        "30",
        "$5.50",
        new_id()
    ),
    (
        "Reproceso del lote",
        "Corrección y refabricación parcial del lote rechazado en inspección de calidad. "
        "AS-IS: 90 min (detectado tardíamente al final del proceso). "
        "TO-BE: 60 min (reducido gracias al QC en-proceso que detecta defectos durante manufactura). "
        "Tasa de activación: 18% AS-IS → <5% TO-BE.",
        "Reporte de Reproceso; Orden de Trabajo",
        "Operario de Planta / Inspector de Calidad",
        "Manual",
        "90",
        "60",
        "$12.00",
        new_id()
    ),
    (
        "Empaque y preparación para despacho",
        "Empacar, etiquetar y preparar los productos aprobados por QC para el despacho al cliente. "
        "Generar lista de empaque y organizar los paquetes según el pedido. "
        "AS-IS: manual (25 min). TO-BE: semi-automatizado con sistema de etiquetado digital (15 min).",
        "Lista de Empaque",
        "Operario de Logística",
        "Manual (AS-IS) · Sistema etiquetado + packing list digital (TO-BE)",
        "25",
        "15",
        "$4.17",
        new_id()
    ),
    (
        "Asignación de transportista y programación de entrega",
        "Seleccionar y asignar el transportista para la entrega, y programar la fecha/hora de despacho. "
        "AS-IS: llamadas telefónicas sin integración con tracking (30 min). "
        "TO-BE: asignación automática vía TMS con tracking integrado (10 min).",
        "Guía de Remisión",
        "Coordinador de Logística",
        "Correo / Teléfono (AS-IS) · TMS - Transport Management System (TO-BE)",
        "30",
        "10",
        "$5.00",
        new_id()
    ),
    (
        "Entrega al cliente y firma de conformidad",
        "Entrega física de los productos al cliente en su dirección. "
        "El cliente firma la guía de remisión como conformidad de recepción. "
        "AS-IS: firma física (45 min). TO-BE: firma digital en app móvil (45 min — tiempo físico inamovible).",
        "Guía de Remisión; Comprobante de Entrega",
        "Transportista Externo",
        "Guía de remisión impresa (AS-IS) · App móvil + firma digital (TO-BE)",
        "45",
        "45",
        "$7.50",
        new_id()
    ),
    (
        "Generación y envío de factura",
        "Emitir y enviar la factura al cliente una vez confirmada la entrega. "
        "AS-IS: generación manual en sistema de facturación (20 min). "
        "TO-BE: factura electrónica generada automáticamente al registrar la firma de entrega (5 min).",
        "Factura",
        "Analista de Finanzas",
        "Sistema de facturación (AS-IS) · Facturación electrónica automática ERP (TO-BE)",
        "20",
        "5",
        "$4.33",
        new_id()
    ),
]

# --- 7. Events ---
EVTS_COLS = ["Title", "Description", "Relevant Documents", "Event Type", "BPMN Element", "Id"]
EVTS_DATA = [
    (
        "Solicitud de compra recibida",
        "Evento de inicio del proceso. Se activa cuando el cliente envía una solicitud de compra "
        "por cualquier canal: correo electrónico, teléfono o portal web. "
        "Desencadena el inicio del proceso de gestión de pedidos de INDUPRO S.A.",
        "Solicitud de Compra del Cliente",
        "Start Event",
        "Message Start Event (sobre con línea)",
        new_id()
    ),
    (
        "Pedido entregado y facturado",
        "Evento de fin del proceso. Se activa cuando el cliente ha recibido físicamente los productos "
        "y ha firmado la guía de remisión, y cuando se ha generado y enviado la factura correspondiente. "
        "Cierra el ciclo completo del proceso de gestión de pedidos.",
        "Guía de Remisión; Factura",
        "End Event",
        "Message End Event (sobre relleno)",
        new_id()
    ),
    (
        "Stock insuficiente detectado",
        "Evento intermedio que ocurre cuando la consulta de inventario indica que no hay stock "
        "suficiente para cubrir el pedido del cliente (probabilidad 35% en AS-IS, 30% en TO-BE). "
        "Desencadena la ruta de producción: programación de orden de fabricación.",
        "Reporte de Disponibilidad de Stock",
        "Intermediate Event",
        "Gateway XOR — resultado 'NO stock'",
        new_id()
    ),
    (
        "Lote rechazado por control de calidad",
        "Evento intermedio que ocurre cuando el Inspector de Calidad rechaza el lote de productos "
        "por no cumplir los estándares de calidad (probabilidad 18% AS-IS, 5% TO-BE). "
        "Desencadena el proceso de reproceso del lote.",
        "Checklist de Calidad; Reporte de Reproceso",
        "Intermediate Event",
        "Gateway XOR — resultado 'RECHAZA'",
        new_id()
    ),
    (
        "Crédito del cliente no aprobado",
        "Evento que ocurre cuando la verificación crediticia del cliente resulta negativa. "
        "En el proceso TO-BE, este evento se evalúa junto con la disponibilidad de stock "
        "en el Gateway XOR combinado (probabilidad de rechazo combinado: 30%).",
        "Reporte de Crédito del Cliente",
        "Intermediate Event",
        "Gateway XOR — resultado 'NO crédito'",
        new_id()
    ),
    (
        "Orden de producción emitida",
        "Evento que confirma la programación formal de la fabricación. Se genera la Orden de Producción "
        "que autoriza el inicio del proceso de manufactura en Planta A o B. "
        "Ocurre solo en la ruta 'sin stock disponible'.",
        "Orden de Producción",
        "Intermediate Event",
        "Intermediate Message Event",
        new_id()
    ),
    (
        "Producto liberado por QC",
        "Evento que confirma la aprobación del lote tras la inspección de calidad. "
        "Habilita el avance del proceso hacia el empaque y despacho. "
        "Ocurre con probabilidad 82% en AS-IS y 95% en TO-BE.",
        "Checklist de Calidad",
        "Intermediate Event",
        "Gateway XOR — resultado 'APRUEBA'",
        new_id()
    ),
]

# --- 8. IT_Systems ---
IT_COLS = ["Title", "Description", "Relevant Documents", "Process Phase", "Status (AS-IS / TO-BE)", "Estimated Cost (USD)", "Id"]
IT_DATA = [
    (
        "Correo Electrónico / Teléfono",
        "Canal de comunicación principal en el proceso AS-IS. Utilizado para: recepción de solicitudes, "
        "confirmación de pedidos al cliente, coordinación interna entre departamentos y asignación "
        "de transportistas. Principal fuente de falta de trazabilidad e ineficiencias.",
        "",
        "Recepción, Confirmación, Coordinación interna",
        "AS-IS (activo) · TO-BE (reemplazado por portal y notificaciones automáticas)",
        "$0 (existente)",
        new_id()
    ),
    (
        "Hoja de Excel (Validación de Pedidos)",
        "Sistema manual de registro y validación de datos de pedidos. Generador de errores "
        "de transcripción (~15% de pedidos con errores) y demoras de hasta 4 horas por pedido. "
        "Sin integración con otros sistemas. Será eliminado en el proceso TO-BE.",
        "Pedido Validado",
        "Validación de pedidos (Paso 2)",
        "AS-IS (activo) · TO-BE (eliminado — reemplazado por portal web)",
        "$0 (existente)",
        new_id()
    ),
    (
        "Sistema Financiero (Manual)",
        "Sistema financiero legado utilizado para la verificación manual de crédito del cliente. "
        "Sin integración API con el proceso. Requiere consulta manual de 60 min sin notificaciones. "
        "TO-BE: se expone mediante API para verificación automática en <15 min.",
        "Reporte de Crédito del Cliente",
        "Verificación de crédito (Paso 3)",
        "AS-IS (activo, sin integración) · TO-BE (con integración API)",
        "$8,000 (integración API)",
        new_id()
    ),
    (
        "ERP Legacy (Inventario)",
        "Sistema ERP legado utilizado para la consulta de inventario. Requiere consulta separada "
        "de registros físicos + ERP (doble fuente de verdad, 50 min). Sin visibilidad en tiempo real. "
        "TO-BE: se integra y actualiza a consulta en tiempo real (10 min).",
        "Reporte de Disponibilidad de Stock",
        "Consulta de inventario (Paso 4)",
        "AS-IS (activo, sin integración completa) · TO-BE (integrado en tiempo real)",
        "$10,000 (integración tiempo real)",
        new_id()
    ),
    (
        "Planilla de Producción Manual",
        "Sistema manual de programación de órdenes de producción. No considera la capacidad real "
        "disponible de cada planta en tiempo real. Genera sub-optimización de recursos. "
        "TO-BE: reemplazado por módulo de planificación en el ERP integrado.",
        "Orden de Producción",
        "Programación de producción (Paso 6B)",
        "AS-IS (activo) · TO-BE (eliminado — integrado en ERP)",
        "$0 (eliminado)",
        new_id()
    ),
    (
        "Portal Web de Pedidos (TO-BE)",
        "Nuevo sistema propuesto. Portal web integrado para recepción y auto-validación de solicitudes "
        "de compra. Reemplaza correo/teléfono/Excel para la entrada de pedidos. Incluye validación "
        "automática de campos y notificaciones automáticas al cliente.",
        "Solicitud de Compra del Cliente; Confirmación de Pedido",
        "Recepción y validación de pedidos (Pasos 1+2)",
        "TO-BE (nuevo) · Costo: $12,000",
        "$12,000",
        new_id()
    ),
    (
        "ERP Integrado en Tiempo Real (TO-BE)",
        "ERP actualizado con integración en tiempo real para consulta de stock e inventario. "
        "Proporciona visibilidad unificada de inventario (única fuente de verdad). "
        "También integra el módulo de planificación de producción con visibilidad de capacidad real.",
        "Reporte de Disponibilidad de Stock; Orden de Producción",
        "Consulta de stock (Paso 4) · Planificación (Paso 6B)",
        "TO-BE (actualización del ERP legacy) · Costo: $10,000",
        "$10,000",
        new_id()
    ),
    (
        "API Sistema Financiero (TO-BE)",
        "Integración API entre el proceso de gestión de pedidos y el sistema financiero "
        "para verificación automática de crédito. Reduce el tiempo de 60 min a <15 min "
        "y permite ejecución en paralelo con la consulta de inventario (AND Gateway).",
        "Reporte de Crédito del Cliente",
        "Verificación de crédito (Paso 3)",
        "TO-BE (nuevo) · Costo: $8,000",
        "$8,000",
        new_id()
    ),
    (
        "TMS - Transport Management System (TO-BE)",
        "Sistema de gestión de transporte para asignación automática de transportistas "
        "y tracking de entregas. Reemplaza la coordinación por llamadas telefónicas. "
        "Integrado con la generación de guías de remisión digitales.",
        "Guía de Remisión; Comprobante de Entrega",
        "Asignación de transportista (Paso 11)",
        "TO-BE (nuevo) · Costo: $7,000",
        "$7,000",
        new_id()
    ),
    (
        "Sistema QC Digital (TO-BE)",
        "Sistema digital para la gestión del control de calidad. Incluye: checklist digital, "
        "alertas en tiempo real durante manufactura (QC in-process), registro fotográfico "
        "de defectos y reportes automáticos. Objetivo: reducir tasa de rechazo de 18% a <5%.",
        "Checklist de Calidad; Reporte de Reproceso",
        "Inspección de calidad (Paso 8) · QC en-proceso (Paso 7)",
        "TO-BE (nuevo) · Costo: $5,000",
        "$5,000",
        new_id()
    ),
    (
        "Sistema de Facturación Electrónica (TO-BE)",
        "Módulo de generación automática de facturas electrónicas integrado con el ERP. "
        "Se activa automáticamente al registrar la firma digital de entrega. "
        "Reduce el tiempo de facturación de 20 min a 5 min. Genera factura en formato XML/PDF.",
        "Factura",
        "Generación de factura (Paso 13)",
        "TO-BE (nuevo) · Costo: $3,000",
        "$3,000",
        new_id()
    ),
    (
        "App Móvil de Entrega y Firma Digital (TO-BE)",
        "Aplicación móvil para el transportista que permite registrar la entrega y capturar "
        "la firma digital del cliente como conformidad de recepción. Reemplaza la guía de remisión impresa. "
        "Integrada con el TMS y el sistema de facturación electrónica.",
        "Guía de Remisión; Comprobante de Entrega",
        "Entrega al cliente (Paso 12)",
        "TO-BE (incluido en TMS) · Sin costo adicional",
        "$0 (incluido en TMS)",
        new_id()
    ),
]

# --- 9. Risks ---
RISKS_COLS = [
    "Title", "Description", "Relevant Documents", "Cause", "Consequence",
    "Risk Probability (without controls)", "Extent of Damage (without controls)",
    "Risk Probability (residual risk)", "Extent of Damage (residual risk)",
    "Process Step", "Id"
]
RISKS_DATA = [
    (
        "Errores de transcripción en validación manual de pedidos",
        "El uso de hojas de cálculo Excel para la validación de pedidos genera errores de transcripción "
        "en datos del cliente, productos o cantidades. Impacta directamente en la calidad del pedido procesado.",
        "Pedido Validado",
        "Ausencia de sistema digital integrado con validación automática de datos",
        "Pedidos incorrectos, re-trabajo, insatisfacción del cliente, demoras de hasta 4h por pedido",
        "high",
        "high",
        "low",
        "low",
        "Paso 2 — Validación manual de pedidos",
        new_id()
    ),
    (
        "Verificación de crédito tardía o incorrecta",
        "La verificación de crédito manual y secuencial sin integración con el sistema financiero "
        "puede generar decisiones tardías (6-8h) o incorrectas que bloqueen pedidos válidos o "
        "aprueben pedidos con riesgo de impago.",
        "Reporte de Crédito del Cliente",
        "Sistema financiero desconectado del proceso de gestión de pedidos",
        "Bloqueo de pedidos legítimos, retrasos en el ciclo, riesgo crediticio no controlado",
        "normal",
        "high",
        "low",
        "normal",
        "Paso 3 — Verificación de crédito",
        new_id()
    ),
    (
        "Discrepancias en el inventario (doble fuente de verdad)",
        "La consulta de inventario en registros físicos separados del ERP legacy genera "
        "discrepancias entre ambas fuentes. Se puede confirmar stock disponible que en realidad "
        "no existe, o viceversa.",
        "Reporte de Disponibilidad de Stock",
        "No integración entre registros físicos y ERP legacy; falta de fuente única de verdad",
        "Pedidos confirmados sin stock real, paralizaciones en producción, incumplimiento de entrega",
        "normal",
        "high",
        "low",
        "low",
        "Paso 4 — Consulta de disponibilidad de stock",
        new_id()
    ),
    (
        "Alta tasa de reproceso por QC tardío (18%)",
        "El control de calidad realizado solo al final del proceso de manufactura detecta "
        "defectos tardíamente cuando ya se ha invertido todo el tiempo y costo de fabricación. "
        "El 18% de los lotes requiere reproceso (+90 min, +$12/caso).",
        "Checklist de Calidad; Reporte de Reproceso",
        "Ausencia de control de calidad en-proceso (in-line QC) durante la manufactura",
        "Incremento de costos (+$12/pedido afectado), retrasos de 90 min, insatisfacción del cliente",
        "high",
        "high",
        "low",
        "low",
        "Paso 9 — Inspección de calidad / Paso 9B — Reproceso",
        new_id()
    ),
    (
        "Falta de trazabilidad en comunicación interna",
        "La comunicación entre departamentos (Ventas, Planificación, Planta, Logística) por correo "
        "electrónico sin sistema de workflow genera falta de trazabilidad, pérdida de información "
        "y ausencia de alertas automáticas ante retrasos.",
        "",
        "Ausencia de plataforma de workflow digital integrada con el proceso",
        "Retrasos no detectados, pérdida de información, incapacidad de medir KPIs en tiempo real",
        "normal",
        "normal",
        "low",
        "low",
        "Todos los pasos de coordinación interna",
        new_id()
    ),
    (
        "Sub-optimización de planificación de producción",
        "La programación manual de órdenes de producción sin visibilidad de la capacidad real "
        "de cada planta en tiempo real genera ineficiencias en la asignación de recursos productivos.",
        "Orden de Producción",
        "Falta de sistema de planificación integrado con datos de capacidad real en tiempo real",
        "Uso ineficiente de capacidad productiva (78% actual vs >90% posible), cuellos de botella en planta",
        "normal",
        "normal",
        "low",
        "low",
        "Paso 6B — Programación de producción",
        new_id()
    ),
    (
        "Falla del ERP Legacy",
        "El sistema ERP legacy utilizado para consulta de inventario puede fallar o quedar no disponible "
        "durante el proceso, bloqueando la consulta de stock y paralizando la gestión de pedidos.",
        "Reporte de Disponibilidad de Stock",
        "Sistema legado sin plan de continuidad documentado ni integración redundante",
        "Paralización total de la consulta de inventario, imposibilidad de procesar pedidos",
        "low",
        "high",
        "low",
        "normal",
        "Paso 4 — Consulta de stock",
        new_id()
    ),
    (
        "Sin notificaciones proactivas al cliente",
        "La ausencia de un sistema de notificaciones automáticas impide que el cliente conozca "
        "el estado de su pedido durante el proceso, generando consultas repetidas y deterioro "
        "en la percepción del servicio.",
        "",
        "Falta de integración entre el proceso y un sistema de notificaciones al cliente",
        "Insatisfacción del cliente, incremento de llamadas de consulta, riesgo de cancelación de pedidos",
        "normal",
        "normal",
        "low",
        "low",
        "Todo el proceso — falta de visibilidad para el cliente",
        new_id()
    ),
    (
        "Transportista no disponible en ventana de despacho",
        "La asignación de transportistas por llamadas telefónicas sin sistema integrado puede "
        "resultar en que no haya transportista disponible dentro de la ventana de despacho (07:00-14:00), "
        "retrasando la entrega al siguiente día hábil.",
        "Guía de Remisión",
        "Sin sistema TMS para gestión anticipada de transportistas y tracking",
        "Retraso en entrega de 1 día hábil completo, insatisfacción del cliente, incumplimiento de SLA",
        "normal",
        "high",
        "low",
        "low",
        "Paso 11 — Asignación de transportista",
        new_id()
    ),
]

# --- 10. Controls ---
CTRLS_COLS = [
    "Title", "Description", "Relevant Documents",
    "Control Aim", "Type of Control", "Documentation",
    "Responsible", "Control Frequency", "Status", "Risk Mitigated", "Id"
]
CTRLS_DATA = [
    (
        "Validación automática de datos de pedido (TO-BE)",
        "El portal web de pedidos realiza validación automática de todos los campos obligatorios "
        "al momento de la recepción: RUC/NIT del cliente, SKU de productos, cantidades, dirección. "
        "Impide que un pedido con datos incompletos avance en el proceso.",
        "Solicitud de Compra del Cliente; Pedido Validado",
        "Eliminar errores de transcripción y pedidos con datos incompletos",
        "Automático (sistema)",
        "Log de validación del portal web",
        "Administrador de Sistemas",
        "En cada pedido (100% de los casos)",
        "Propuesto (TO-BE)",
        "Errores de transcripción en validación manual de pedidos",
        new_id()
    ),
    (
        "Verificación automática de crédito vía API (TO-BE)",
        "Integración API con el sistema financiero que verifica automáticamente el estado crediticio "
        "del cliente en <15 minutos, en paralelo con la consulta de inventario. "
        "Elimina la dependencia de consultas manuales.",
        "Reporte de Crédito del Cliente",
        "Verificación oportuna y automática del estado crediticio sin intervención manual",
        "Automático (API)",
        "Log de respuesta API del sistema financiero",
        "Analista de Finanzas / Sistema Automático",
        "En cada pedido (100% de los casos)",
        "Propuesto (TO-BE)",
        "Verificación de crédito tardía o incorrecta",
        new_id()
    ),
    (
        "Fuente única de verdad para inventario - ERP en tiempo real (TO-BE)",
        "Integración del ERP con los registros de bodega para mantener una única fuente de verdad "
        "de inventario actualizada en tiempo real. Elimina la discrepancia entre registros físicos y ERP.",
        "Reporte de Disponibilidad de Stock",
        "Eliminar discrepancias de inventario y garantizar consultas precisas",
        "Automático (integración ERP)",
        "Registro de transacciones ERP; Reporte de inventario en tiempo real",
        "Coordinador de Inventarios / Técnico de Integración ERP",
        "Actualización continua en tiempo real",
        "Propuesto (TO-BE)",
        "Discrepancias en el inventario (doble fuente de verdad)",
        new_id()
    ),
    (
        "Control de calidad en-proceso — in-line QC (TO-BE)",
        "Implementación de puntos de control de calidad durante el proceso de manufactura "
        "(no solo al final). Permite detectar defectos en etapas tempranas del proceso productivo, "
        "reduciendo la tasa de rechazo de 18% a <5%.",
        "Checklist QC en-proceso; Checklist de Calidad",
        "Detectar defectos durante la manufactura para reducir reprocesos finales",
        "Manual + Digital (checklist digital en tablet)",
        "Registro en Sistema QC Digital; Reporte de QC en-proceso",
        "Inspector de Calidad / Operario de Planta",
        "Durante cada fabricación (en puntos críticos del proceso)",
        "Propuesto (TO-BE)",
        "Alta tasa de reproceso por QC tardío (18%)",
        new_id()
    ),
    (
        "Sistema de workflow digital con trazabilidad completa (TO-BE)",
        "Reemplazo de la comunicación por correo electrónico con un sistema de workflow digital "
        "integrado que registra cada paso del proceso, genera alertas automáticas ante retrasos "
        "y provee visibilidad en tiempo real a todos los departamentos.",
        "",
        "Garantizar trazabilidad completa del proceso y alertas proactivas",
        "Automático (sistema de workflow integrado en ERP)",
        "Log de actividades del proceso; Dashboard de KPIs en tiempo real",
        "Administrador de Sistemas",
        "Monitoreo continuo en tiempo real",
        "Propuesto (TO-BE)",
        "Falta de trazabilidad en comunicación interna",
        new_id()
    ),
    (
        "TMS con gestión anticipada de transportistas (TO-BE)",
        "Sistema de gestión de transporte que permite programar y confirmar transportistas "
        "con anticipación y rastrear entregas en tiempo real. Elimina la dependencia de "
        "llamadas telefónicas y garantiza disponibilidad en la ventana de despacho (07:00-14:00).",
        "Guía de Remisión; Comprobante de Entrega",
        "Garantizar disponibilidad de transportista en la ventana de despacho",
        "Automático (TMS)",
        "Registro de asignaciones y tracking en TMS",
        "Coordinador de Logística / TMS",
        "En cada pedido con despacho programado",
        "Propuesto (TO-BE)",
        "Transportista no disponible en ventana de despacho",
        new_id()
    ),
    (
        "Revisión periódica del ERP legacy y plan de continuidad (AS-IS)",
        "Mantenimiento preventivo y plan de continuidad para el ERP legacy utilizado para "
        "consulta de inventario. Incluye backup diario y procedimiento manual de contingencia.",
        "",
        "Minimizar el riesgo de falla del ERP legacy que paralice la consulta de stock",
        "Manual + Técnico",
        "Reporte de mantenimiento mensual; Plan de continuidad documentado",
        "Técnico de Integración ERP / Coordinador de Inventarios",
        "Mensual (mantenimiento preventivo)",
        "Activo (AS-IS)",
        "Falla del ERP Legacy",
        new_id()
    ),
    (
        "Notificaciones automáticas al cliente sobre estado del pedido (TO-BE)",
        "Sistema de notificaciones automáticas por email/SMS que informa al cliente sobre el "
        "estado de su pedido en cada hito clave: recepción, confirmación, fabricación, "
        "despacho y entrega.",
        "Confirmación de Pedido al Cliente",
        "Mejorar la experiencia del cliente con información proactiva y transparente",
        "Automático (portal web + sistema de notificaciones)",
        "Log de notificaciones enviadas; Reporte de satisfacción del cliente",
        "Sistema Automático / Ejecutivo de Ventas",
        "En cada hito del proceso (automático)",
        "Propuesto (TO-BE)",
        "Sin notificaciones proactivas al cliente",
        new_id()
    ),
]

# --- 11. Others ---
OTHERS_COLS = ["Title", "Description", "Relevant Documents", "Category", "Id"]
OTHERS_DATA = [
    (
        "KPI: Tiempo de Ciclo Total",
        "Indicador clave de rendimiento del proceso completo desde la recepción del pedido "
        "hasta la entrega al cliente. AS-IS: 555 minutos. Meta TO-BE: <350 minutos. "
        "Métrica Signavio: 'Total cycle time (1 case)'.",
        "",
        "KPI / Métricas del proceso",
        new_id()
    ),
    (
        "KPI: Costo Total por Pedido",
        "Costo total del proceso por pedido (ruta con fabricación). "
        "AS-IS: $105.91. Meta TO-BE: <$70.00. Costo estimado TO-BE: $46.84. "
        "Métrica Signavio: 'Total cost (1 case)'.",
        "",
        "KPI / Métricas del proceso",
        new_id()
    ),
    (
        "KPI: Tasa de Reproceso de Calidad",
        "Frecuencia de activación del reproceso por rechazo en control de calidad. "
        "AS-IS: 18% de los casos. Meta TO-BE: <5%. "
        "Métrica Signavio: 'Branching path frequency' (Gateway QC, ruta RECHAZA).",
        "",
        "KPI / Métricas del proceso",
        new_id()
    ),
    (
        "KPI: Tiempo en Espera / Colas (NVA)",
        "Tiempo acumulado en actividades de espera y cola sin valor agregado. "
        "AS-IS: ~210 minutos (38% del ciclo total). Meta TO-BE: <70 minutos. "
        "Métrica Signavio: 'Bottleneck waiting time'.",
        "",
        "KPI / Métricas del proceso",
        new_id()
    ),
    (
        "Restricción: Tiempo mínimo de fabricación",
        "Restricción técnica inamovible del proceso. El tiempo de fabricación por lote estándar "
        "es de 120 minutos por pedido. No puede reducirse en la propuesta TO-BE. "
        "Aplicable al Paso 7 del proceso.",
        "",
        "Restricciones del desafío",
        new_id()
    ),
    (
        "Restricción: Tiempo mínimo de inspección de calidad",
        "Requerimiento regulatorio interno inamovible. El tiempo de inspección de calidad es de "
        "mínimo 30 minutos por pedido. No puede reducirse en la propuesta TO-BE. "
        "Aplicable al Paso 8 del proceso.",
        "",
        "Restricciones del desafío",
        new_id()
    ),
    (
        "Restricción: Presupuesto máximo de inversión",
        "Límite máximo de inversión en tecnología y automatización para el proceso TO-BE: USD 50,000. "
        "Incluye implementación de todos los sistemas nuevos y capacitación del personal. "
        "Máximo 2 nuevos roles adicionales permitidos.",
        "",
        "Restricciones del desafío",
        new_id()
    ),
    (
        "Restricción: Ventana de despacho",
        "El despacho de productos solo puede realizarse entre las 07:00 y las 14:00 horas, "
        "de lunes a viernes. Pedidos listos fuera de este horario se despachan el siguiente día hábil.",
        "",
        "Restricciones del desafío",
        new_id()
    ),
    (
        "Parámetro simulación: Gateway XOR Stock AS-IS",
        "Configuración de probabilidades para la compuerta XOR de disponibilidad de stock en el AS-IS. "
        "SÍ (hay stock): 65% | NO (sin stock, ir a producción): 35%. "
        "Ingresar en pestaña Frequency de la simulación en SAP Signavio.",
        "",
        "Parámetros de simulación",
        new_id()
    ),
    (
        "Parámetro simulación: Gateway XOR Calidad AS-IS",
        "Configuración de probabilidades para la compuerta XOR de control de calidad en el AS-IS. "
        "APRUEBA: 82% | RECHAZA (reproceso): 18%. "
        "Ingresar en pestaña Frequency de la simulación en SAP Signavio.",
        "",
        "Parámetros de simulación",
        new_id()
    ),
    (
        "Parámetro simulación: Gateway XOR Stock TO-BE",
        "Configuración de probabilidades mejoradas para la compuerta XOR combinada de crédito+stock en el TO-BE. "
        "SÍ (crédito OK y stock OK): 70% | NO: 30%. "
        "Ingresar en pestaña Frequency de la simulación en SAP Signavio.",
        "",
        "Parámetros de simulación",
        new_id()
    ),
    (
        "Parámetro simulación: Gateway XOR Calidad TO-BE",
        "Configuración de probabilidades mejoradas para la compuerta XOR de calidad en el TO-BE. "
        "APRUEBA: 95% | RECHAZA: 5%. Mejora gracias al QC en-proceso implementado. "
        "Ingresar en pestaña Frequency de la simulación en SAP Signavio.",
        "",
        "Parámetros de simulación",
        new_id()
    ),
    (
        "Inversión TO-BE: Desglose por componente",
        "Desglose de la inversión total de $50,000: Portal Web $12,000 | Integración ERP $10,000 | "
        "API Sistema Financiero $8,000 | TMS $7,000 | Sistema QC Digital $5,000 | "
        "Facturación Electrónica $3,000 | Capacitación $5,000. Total: $50,000 exactos.",
        "",
        "Análisis financiero",
        new_id()
    ),
    (
        "ROI estimado del proceso TO-BE",
        "Retorno de inversión del proceso TO-BE. Ahorro por pedido: $105.91 - $46.84 = $59.07. "
        "Pedidos por mes: ~1,200. Ahorro mensual: ~$70,884. Inversión inicial: $50,000. "
        "Payback estimado: <1 mes operativo.",
        "",
        "Análisis financiero",
        new_id()
    ),
]

# ---------------------------------------------------------------------------
# Construcción del workbook
# ---------------------------------------------------------------------------

SHEETS = [
    {"name": "Organizational_Units",  "cols": ORG_UNITS_COLS, "data": ORG_UNITS_DATA},
    {"name": "Roles",                 "cols": ROLES_COLS,     "data": ROLES_DATA},
    {"name": "Departments",           "cols": DEPTS_COLS,     "data": DEPTS_DATA},
    {"name": "External_participants", "cols": EXT_COLS,       "data": EXT_DATA},
    {"name": "Documents",             "cols": DOCS_COLS,      "data": DOCS_DATA},
    {"name": "Activities",            "cols": ACTS_COLS,      "data": ACTS_DATA},
    {"name": "Events",                "cols": EVTS_COLS,      "data": EVTS_DATA},
    {"name": "IT_Systems",            "cols": IT_COLS,        "data": IT_DATA},
    {"name": "Risks",                 "cols": RISKS_COLS,     "data": RISKS_DATA},
    {"name": "Controls",              "cols": CTRLS_COLS,     "data": CTRLS_DATA},
    {"name": "Others",                "cols": OTHERS_COLS,    "data": OTHERS_DATA},
]

def build_workbook():
    """
    Un único archivo Excel, 11 hojas (una por categoría).
    Estructura de cada hoja:
      Fila 1  → cabeceras  (detectada automáticamente como header por Signavio)
      Fila 2+ → registros del diccionario
    Listo para importar: Explorer → Dictionary → Import/Export → Import Excel.
    """
    wb = Workbook()
    wb.remove(wb.active)

    for sheet_def in SHEETS:
        sname = sheet_def["name"]
        color = CATEGORY_COLORS[sname]
        ws    = wb.create_sheet(title=sname)
        cols  = sheet_def["cols"]

        # ── Fila 1: cabeceras ────────────────────────────────────────────
        for c_idx, col_name in enumerate(cols, start=1):
            _style_header(ws.cell(row=1, column=c_idx, value=col_name), color)
        ws.row_dimensions[1].height = 28

        # ── Filas 2+: datos ──────────────────────────────────────────────
        for r_off, row_data in enumerate(sheet_def["data"]):
            r_num = 2 + r_off
            for c_idx, value in enumerate(row_data, start=1):
                _style_data(ws.cell(row=r_num, column=c_idx, value=value), r_num)
            ws.row_dimensions[r_num].height = 28

        ws.freeze_panes = "A2"
        _auto_width(ws)

    return wb


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    wb = build_workbook()
    wb.save(OUTPUT_PATH)

    print(f"✅ Diccionario INDUPRO generado:")
    print(f"   {OUTPUT_PATH}")
    print(f"\n11 hojas (una por categoría) — fila 1 = cabecera, fila 2+ = datos:\n")
    total = 0
    for s in SHEETS:
        n = len(s["data"])
        total += n
        print(f"  • {s['name']:30s}  {n:>3} entradas")
    print(f"\n  Total: {total} entradas\n")
    print("Importar en Signavio (por categoría):")
    print("  Explorer → Dictionary → [categoría] → Import/Export → Import Excel")
    print("  Seleccionar hoja correspondiente → mapear columnas → Import")


if __name__ == "__main__":
    main()
