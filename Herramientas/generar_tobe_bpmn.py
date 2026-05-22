"""
Generador BPMN TO-BE INDUPRO S.A. — Version corregida v1
SAP Signavio Regional Challenge 2026

Correcciones sobre la plantilla base:
  1. Elimina lane "Sistema Automatico" → reemplaza por "Analista de Integracion de Sistemas" (nuevo rol)
  2. Agrega lane "Operario de Control de Calidad en Proceso" (nuevo rol) entre Planta y Calidad
  3. Desplaza lanes Calidad y Logistica -145px hacia abajo
  4. Corrige tipos de tarea: Task1=userTask, Task7=manualTask, Task9B=manualTask, Task10=manualTask
  5. Agrega IT Systems como textAnnotation con asociacion no direccional (non-directional association)
  6. Agrega Additional Participant annotations para Task7 y Task9B
"""

# ═══════════════════════════════════════════════════════════════
# LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════════
# 9 lanes x 145px = 1305px total pool height
# Pool INDUPRO: x=80, y=40, w=2560, h=1305
# Lane content area: x=130 to x=2640 (2510px wide)
# Pool Cliente: x=80, y=1365, h=60

POOL_X, POOL_Y, POOL_W = 80, 40, 2560
LANE_H = 145  # height of each lane
LANE_CONTENT_X = 130  # x start after pool label column

# Lane Y positions (top edge)
L_VENTAS       = 40    # Lane 1 — center_y=112
L_FINANZAS     = 185   # Lane 2 — center_y=257
L_INVENTARIOS  = 330   # Lane 3 — center_y=402
L_INTEGRACION  = 475   # Lane 4 — center_y=547  (replaces "Sistema Automatico")
L_PLANIFIC     = 620   # Lane 5 — center_y=692
L_PLANTA       = 765   # Lane 6 — center_y=837
L_QC_PROC      = 910   # Lane 7 — center_y=982  (NEW: Operario QC en Proceso)
L_CALIDAD      = 1055  # Lane 8 — center_y=1127 (was 910, shifted +145)
L_LOGISTICA    = 1200  # Lane 9 — center_y=1272 (was 1055, shifted +145)

POOL_H = L_LOGISTICA + LANE_H  # = 1345
CLIENTE_Y = POOL_Y + POOL_H + 20  # = 1385

def cy(lane_y): return lane_y + LANE_H // 2  # center y of a lane

# Task/event dimensions
EW, EH = 36, 36   # Event circle
TW, TH = 140, 70  # Task box (standard)
GW, GH = 40, 40   # Gateway diamond
ITW, ITH = 120, 45  # IT System annotation box
APW, APH = 150, 35  # Additional Participant annotation


# ═══════════════════════════════════════════════════════════════
# XML HELPERS
# ═══════════════════════════════════════════════════════════════
def bounds(x, y, w, h):
    return f'<omgdc:Bounds height="{h}" width="{w}" x="{x}" y="{y}"/>'

def wp(x, y):
    return f'<omgdi:waypoint x="{x}" y="{y}"/>'

def shape(elem_id, x, y, w, h, label_x=None, label_y=None, label_w=None, label_h=None,
          extra_attrs=""):
    lb = ""
    if label_x is not None:
        lb = f"""
        <bpmndi:BPMNLabel>{bounds(label_x, label_y, label_w, label_h)}</bpmndi:BPMNLabel>"""
    return f"""
      <bpmndi:BPMNShape bpmnElement="{elem_id}" id="{elem_id}_gui" {extra_attrs}>
        {bounds(x, y, w, h)}{lb}
      </bpmndi:BPMNShape>"""

def edge(elem_id, waypoints, label=None):
    wps = "\n        ".join(waypoints)
    lb = ""
    if label:
        lb = f"\n        <bpmndi:BPMNLabel>{bounds(*label)}</bpmndi:BPMNLabel>"
    return f"""
      <bpmndi:BPMNEdge bpmnElement="{elem_id}" id="{elem_id}_gui">
        {wps}{lb}
      </bpmndi:BPMNEdge>"""


# ═══════════════════════════════════════════════════════════════
# COORDINATE SHORTCUTS
# ═══════════════════════════════════════════════════════════════
# Centers of key elements (cx, cy)
START_CX, START_CY   = 200,  cy(L_VENTAS)        # 200, 112
T1_CX,    T1_CY      = 340,  cy(L_VENTAS)        # 340, 112
ANDS_CX,  ANDS_CY    = 510,  cy(L_INTEGRACION)   # 510, 547
T2A_CX,   T2A_CY     = 660,  cy(L_FINANZAS)      # 660, 257
T2B_CX,   T2B_CY     = 660,  cy(L_INVENTARIOS)   # 660, 402
ANDJ_CX,  ANDJ_CY    = 820,  cy(L_INTEGRACION)   # 820, 547
XORCS_CX, XORCS_CY   = 930,  cy(L_INTEGRACION)   # 930, 547
T6B_CX,   T6B_CY     = 1080, cy(L_PLANIFIC)      # 1080, 692
T7_CX,    T7_CY      = 1280, cy(L_PLANTA)        # 1280, 837
T8_CX,    T8_CY      = 1280, cy(L_CALIDAD)       # 1280, 1127
XORQC_CX, XORQC_CY   = 1480, cy(L_CALIDAD)       # 1480, 1127
T9B_CX,   T9B_CY     = 1620, cy(L_PLANTA)        # 1620, 837
XORJ_CX,  XORJ_CY    = 1780, cy(L_VENTAS)        # 1780, 112
T6A_CX,   T6A_CY     = 1920, cy(L_VENTAS)        # 1920, 112
T10_CX,   T10_CY     = 2060, cy(L_LOGISTICA)     # 2060, 1272
T11_CX,   T11_CY     = 2220, cy(L_LOGISTICA)     # 2220, 1272
T12_CX,   T12_CY     = 2380, cy(L_LOGISTICA)     # 2380, 1272
T13_CX,   T13_CY     = 2380, cy(L_FINANZAS)      # 2380, 257
END_CX,   END_CY     = 2540, cy(L_FINANZAS)      # 2540, 257


# ═══════════════════════════════════════════════════════════════
# BUILD XML
# ═══════════════════════════════════════════════════════════════
def generate():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions
   xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
   xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC"
   xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI"
   xmlns:signavio="http://www.signavio.com"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   exporter="Signavio Process Editor, http://www.signavio.com"
   exporterVersion="26.18.0"
   expressionLanguage="http://www.w3.org/TR/XPath"
   id="sid-indupro-tobe-v1-definitions"
   targetNamespace="http://www.signavio.com"
   typeLanguage="http://www.w3.org/2001/XMLSchema"
   xml:lang="es-EC"
   xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL http://www.omg.org/spec/BPMN/2.0/20100501/BPMN20.xsd">

  <!--
    =====================================================================
    INDUPRO S.A. - Proceso de Gestion de Pedidos (TO-BE Corregido v1)
    SAP Signavio Regional Challenge 2026
    BPMN 2.0 - Modelado correcto segun feedback del profesor

    CORRECCIONES vs plantilla base:
      C1 - Lane "Sistema Automatico" eliminado.
           Gateways AND/XOR de orquestacion movidos a lane
           "Analista de Integracion de Sistemas" (nuevo rol).
      C2 - Lane "Operario de Control de Calidad en Proceso" agregado (nuevo rol).
           Se modela como Additional Participant de Task 7 via asociacion.
      C3 - Task 1: serviceTask -> userTask (Ejecutivo interactua con portal)
      C4 - Task 7: userTask -> manualTask (trabajo fisico de fabricacion)
      C5 - Task 9B: userTask -> manualTask (reproceso fisico)
      C6 - Task 10: userTask -> manualTask (empaque fisico)
      C7 - IT Systems agregados como textAnnotation con asociacion no direccional
           (non-directional association, sin flecha - per S3.1 lecture)
      C8 - Additional Participant notation para Task 7 y Task 9B

    NOTACION SIGNAVIO:
      IT Systems = textAnnotation con etiqueta [IT System: Nombre]
                   Conectados a tareas via association (associationDirection="None")
      Additional Participant = textAnnotation con etiqueta [Participante adicional]
                               Conectado a la tarea via association

    PARAMETROS DE SIMULACION:
      Duration: en MINUTOS (nunca horas/dias - version academica)
      Frequency: XOR-CreditStock: Si=70%, No=30% | XOR-QC: Aprueba=95%, Rechaza=5%
      Resources: tarifa/hora por lane (no en Costs tab)
      Resultado esperado: ~281 min / ~$47.21 por pedido (sin reproceso)
    =====================================================================
  -->

  <!-- Mensajes BPMN 2.0 -->
  <message id="msg-solicitud-pedido"    name="Solicitud de Pedido (portal web)"/>
  <message id="msg-confirmacion-orden"  name="Confirmacion de Orden"/>
  <message id="msg-factura-electronica" name="Factura Electronica"/>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- COLABORACION                                                -->
  <!-- ═══════════════════════════════════════════════════════════ -->
  <collaboration id="sid-collab-indupro-tobe-v1">
    <extensionElements>
      <signavio:signavioDiagramMetaData metaKey="revisionid" metaValue="INDUPRO-TOBE-v1-corregido"/>
    </extensionElements>

    <participant id="sid-pool-indupro-tobe" name="INDUPRO S.A."
                 processRef="sid-process-indupro-tobe">
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
    </participant>

    <participant id="sid-pool-cliente" name="Cliente">
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#f0f0f0"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#666666"/>
      </extensionElements>
    </participant>

    <!-- MessageFlow MF-01: Cliente -> INDUPRO (solicitud vía portal web) -->
    <messageFlow id="mf-solicitud-inicio"
       name="Solicitud de pedido&#10;(portal web)"
       sourceRef="sid-pool-cliente" targetRef="sid-start-tobe">
      <extensionElements>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#666666"/>
      </extensionElements>
    </messageFlow>

    <!-- MessageFlow MF-02: INDUPRO -> Cliente (confirmacion automatica) -->
    <messageFlow id="mf-confirmacion-cliente"
       name="Confirmacion automatica&#10;de pedido (email/SMS)"
       sourceRef="sid-task-6a-tobe" targetRef="sid-pool-cliente">
      <extensionElements>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#666666"/>
      </extensionElements>
    </messageFlow>

    <!-- MessageFlow MF-03: INDUPRO -> Cliente (factura electronica) -->
    <messageFlow id="mf-factura-cliente"
       name="Factura electronica&#10;(SRI-compliant)"
       sourceRef="sid-end-tobe" targetRef="sid-pool-cliente">
      <extensionElements>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#666666"/>
      </extensionElements>
    </messageFlow>

  </collaboration>

  <!-- ═══════════════════════════════════════════════════════════ -->
  <!-- PROCESO PRINCIPAL                                           -->
  <!-- ═══════════════════════════════════════════════════════════ -->
  <process id="sid-process-indupro-tobe"
     isClosed="false" isExecutable="false"
     name="Proceso de Gestion de Pedidos - TO-BE Corregido v1"
     processType="None">

    <extensionElements/>

    <!-- ─────────────────────────────────────────────────────────
         9 SWIMLANES — Solo roles humanos (NO sistemas)
         Los IT Systems se modelan como artefactos (textAnnotation)
         con asociacion no direccional a las tareas
         ───────────────────────────────────────────────────────── -->
    <laneSet id="sid-laneset-tobe-v1">

      <!-- Lane 1: Ejecutivo de Ventas -->
      <lane id="sid-lane-ventas" name="Ejecutivo de Ventas">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-start-tobe</flowNodeRef>
        <flowNodeRef>sid-task-1-tobe</flowNodeRef>
        <flowNodeRef>sid-gw-join-tobe</flowNodeRef>
        <flowNodeRef>sid-task-6a-tobe</flowNodeRef>
      </lane>

      <!-- Lane 2: Analista de Finanzas -->
      <lane id="sid-lane-finanzas" name="Analista de Finanzas">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-2a-tobe</flowNodeRef>
        <flowNodeRef>sid-task-13-tobe</flowNodeRef>
        <flowNodeRef>sid-end-tobe</flowNodeRef>
      </lane>

      <!-- Lane 3: Coordinador de Inventarios -->
      <lane id="sid-lane-inventarios" name="Coordinador de Inventarios">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-2b-tobe</flowNodeRef>
      </lane>

      <!-- Lane 4: Analista de Integracion de Sistemas (NUEVO ROL)
           Contiene los gateways AND y XOR de orquestacion de integracion.
           Los IT Systems (SAP Integration Suite, Portal Web, etc.) se
           adjuntan como artefactos con asociacion no direccional. -->
      <lane id="sid-lane-integracion" name="Analista de Integracion de Sistemas">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue="#f0f8ff"/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-gw-and-split-tobe</flowNodeRef>
        <flowNodeRef>sid-gw-and-join-tobe</flowNodeRef>
        <flowNodeRef>sid-gw-creditstock-tobe</flowNodeRef>
      </lane>

      <!-- Lane 5: Planificador de Produccion -->
      <lane id="sid-lane-planificacion" name="Planificador de Produccion">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-6b-tobe</flowNodeRef>
      </lane>

      <!-- Lane 6: Operario de Planta -->
      <lane id="sid-lane-planta" name="Operario de Planta">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-7-tobe</flowNodeRef>
        <flowNodeRef>sid-task-9b-tobe</flowNodeRef>
      </lane>

      <!-- Lane 7: Operario de Control de Calidad en Proceso (NUEVO ROL)
           Additional Participant de Task 7 (fabricacion con QC en proceso).
           Se conecta a Task 7 via asociacion no direccional. -->
      <lane id="sid-lane-qc-proceso" name="Operario de QC en Proceso">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue="#f0fff0"/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <!-- No tiene flowNodeRef propios - participa via Additional Participant en Task7 -->
      </lane>

      <!-- Lane 8: Inspector de Calidad -->
      <lane id="sid-lane-calidad" name="Inspector de Calidad">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-8-tobe</flowNodeRef>
        <flowNodeRef>sid-gw-qc-tobe</flowNodeRef>
      </lane>

      <!-- Lane 9: Coordinador de Logistica -->
      <lane id="sid-lane-logistica" name="Coordinador de Logistica">
        <extensionElements>
          <signavio:signavioMetaData metaKey="bgcolor" metaValue=""/>
          <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
        </extensionElements>
        <flowNodeRef>sid-task-10-tobe</flowNodeRef>
        <flowNodeRef>sid-task-11-tobe</flowNodeRef>
        <flowNodeRef>sid-task-12-tobe</flowNodeRef>
      </lane>

    </laneSet>

    <!-- ─────────────────────────────────────────────────────────
         EVENTOS
         ───────────────────────────────────────────────────────── -->

    <!-- START EVENT — Message Start (solicitud via portal web) -->
    <startEvent id="sid-start-tobe" name="Solicitud de pedido&#10;(portal web)">
      <documentation>
        Message Start Event. El cliente envia su solicitud a traves del portal web.
        [SIMULACION] Frecuencia: 4 pedidos/dia, ventana 480 min.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <outgoing>sf-tobe-01</outgoing>
      <messageEventDefinition id="sid-msgdef-start" messageRef="msg-solicitud-pedido"/>
    </startEvent>

    <!-- END EVENT — Message End (pedido entregado y facturado) -->
    <endEvent id="sid-end-tobe" name="Pedido entregado&#10;y facturado">
      <documentation>
        Message End Event. La firma digital dispara la factura electronica automatica.
        [SIMULACION TO-BE] Tiempo total: ~281 min | Costo: ~$47.21 (sin reproceso).
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-15</incoming>
      <messageEventDefinition id="sid-msgdef-end" messageRef="msg-factura-electronica"/>
    </endEvent>

    <!-- ─────────────────────────────────────────────────────────
         TAREAS
         ───────────────────────────────────────────────────────── -->

    <!-- TASK 1 — userTask (C3: corregido de serviceTask)
         Persona interactua con el Portal Web (User Task por definicion BPMN)
         IT System: Portal Web de Pedidos (textAnnotation it-portal) -->
    <userTask id="sid-task-1-tobe"
       name="Recepcionar pedido&#10;via portal web"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Ejecutivo de Ventas
        IT System: Portal Web de Pedidos (artefacto - asociacion no direccional)
        Tipo BPMN: User Task (persona interactua con software - portal web)
        Duracion: 15 min | Costo/hr: $12 | Costo: $3.00
        MEJORA vs AS-IS: Elimina recepcion por correo (30 min) + validacion Excel (45 min) = -60 min
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffcc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-01</incoming>
      <outgoing>sf-tobe-02</outgoing>
    </userTask>

    <!-- AND SPLIT — Parallel Gateway Diverging
         Inicia verificacion paralela de credito e inventario
         Lane: Analista de Integracion (gestiona la capa de integracion) -->
    <parallelGateway id="sid-gw-and-split-tobe"
       name="Inicio verificacion&#10;paralela"
       gatewayDirection="Diverging">
      <documentation>
        AND Split: Activa simultaneamente Task 2A (credito) y Task 2B (stock).
        Elimina la secuencialidad AS-IS (110 min secuencial -> 15 min paralelo).
        IT System: SAP Integration Suite orquesta las llamadas API en paralelo.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d5f5e3"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-02</incoming>
      <outgoing>sf-tobe-03a</outgoing>
      <outgoing>sf-tobe-03b</outgoing>
    </parallelGateway>

    <!-- TASK 2A — serviceTask (verificacion automatica via API)
         IT System: API Sistema Financiero / SAP Integration Suite -->
    <serviceTask id="sid-task-2a-tobe"
       name="Verificar credito del cliente&#10;via API financiera"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Analista de Finanzas (supervision de alertas)
        IT System: API Sistema Financiero via SAP Integration Suite
        Tipo BPMN: Service Task (automatizado - llamada API REST)
        Duracion: 15 min | Costo/hr: $13 | Costo: $3.25
        PARALELO con Task 2B.
        MEJORA: -45 min vs AS-IS (60 min manual -> 15 min automatizado)
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ccf2ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-03a</incoming>
      <outgoing>sf-tobe-04a</outgoing>
    </serviceTask>

    <!-- TASK 2B — serviceTask (consulta stock en tiempo real via ERP API)
         IT System: API ERP Legacy / SAP Integration Suite -->
    <serviceTask id="sid-task-2b-tobe"
       name="Consultar disponibilidad de stock&#10;en ERP (tiempo real)"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Coordinador de Inventarios (supervision)
        IT System: API ERP Legacy via SAP Integration Suite
        Tipo BPMN: Service Task (automatizado - consulta ERP)
        Duracion: 10 min | Costo/hr: $10 | Costo: $1.67
        PARALELO con Task 2A.
        MEJORA: -40 min vs AS-IS (50 min manual -> 10 min automatizado)
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ccf2ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-03b</incoming>
      <outgoing>sf-tobe-04b</outgoing>
    </serviceTask>

    <!-- AND JOIN — Parallel Gateway Converging -->
    <parallelGateway id="sid-gw-and-join-tobe"
       name="" gatewayDirection="Converging">
      <documentation>
        AND Join: Espera a que AMBAS verificaciones (2A y 2B) esten completas.
        Tiempo efectivo del bloque AND = MAX(15, 10) = 15 min.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d5f5e3"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-04a</incoming>
      <incoming>sf-tobe-04b</incoming>
      <outgoing>sf-tobe-05</outgoing>
    </parallelGateway>

    <!-- XOR 1 — Credito OK y Stock disponible?
         Decision automatica - Lane: Analista de Integracion -->
    <exclusiveGateway id="sid-gw-creditstock-tobe"
       name="Credito aprobado&#10;Y stock disponible?"
       gatewayDirection="Diverging">
      <documentation>
        XOR: Evalua resultado de 2A y 2B simultaneamente.
        [SIMULACION] Si (credito+stock OK): 70% | No (requiere produccion): 30%
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-05</incoming>
      <outgoing>sf-tobe-06-si</outgoing>
      <outgoing>sf-tobe-06-no</outgoing>
    </exclusiveGateway>

    <!-- TASK 6B — userTask (planificacion digital en ERP)
         IT System: ERP Legacy (modulo PP) -->
    <userTask id="sid-task-6b-tobe"
       name="Programar orden de produccion&#10;en ERP digital"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Planificador de Produccion
        IT System: ERP Legacy - Modulo PP (artefacto)
        Tipo BPMN: User Task (persona aprueba en el sistema)
        Duracion: 20 min | Costo/hr: $14 | Costo: $4.67
        Ruta: 30% de pedidos (requieren fabricacion)
        MEJORA: -20 min vs AS-IS (40 min manual -> 20 min con ERP)
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffcc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-06-no</incoming>
      <outgoing>sf-tobe-07</outgoing>
    </userTask>

    <!-- TASK 7 — manualTask (C4: corregido de userTask)
         Trabajo fisico de planta - no se usa software directamente
         Additional Participant: Operario de QC en Proceso (via asociacion)
         IT System: Sistema QC Digital (para registro de parametros en proceso) -->
    <manualTask id="sid-task-7-tobe"
       name="Fabricar el producto&#10;(con QC en proceso)"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable PRINCIPAL: Operario de Planta (lane)
        Additional Participant: Operario de QC en Proceso (asociacion no direccional)
        IT System: Sistema QC Digital (checklist en tablet durante fabricacion)
        Tipo BPMN: Manual Task (trabajo fisico - manufactura de galletas)
        Duracion: 120 min (RESTRICCION TECNICA INAMOVIBLE) | Costo/hr: $8 | Costo: $16.00
        MEJORA INTERNA: QC en proceso reduce tasa de rechazo 18% -> 5%
        RESTRICCION: El tiempo de fabricacion NO puede reducirse.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#fff0cc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-07</incoming>
      <outgoing>sf-tobe-08</outgoing>
    </manualTask>

    <!-- TASK 8 — userTask (inspector usa el Sistema QC Digital)
         IT System: Sistema QC Digital -->
    <userTask id="sid-task-8-tobe"
       name="Inspeccionar calidad&#10;del lote (digital)"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Inspector de Calidad
        IT System: Sistema QC Digital (checklist digital con trazabilidad)
        Tipo BPMN: User Task (persona usa el sistema QC Digital)
        Duracion: 30 min (REQUISITO REGULATORIO INAMOVIBLE) | Costo/hr: $11 | Costo: $5.50
        Recibe flujo de Task 7 (normal) y Task 9B (post-reproceso).
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffcc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-08</incoming>
      <incoming>sf-tobe-loop-9b</incoming>
      <outgoing>sf-tobe-09</outgoing>
    </userTask>

    <!-- XOR 2 — Pasa control de calidad? -->
    <exclusiveGateway id="sid-gw-qc-tobe"
       name="Pasa control&#10;de calidad?"
       gatewayDirection="Diverging">
      <documentation>
        [SIMULACION] Aprueba: 95% (vs 82% AS-IS, +13pp mejora) | Rechaza: 5% (vs 18% AS-IS)
        Duracion: 2 min | Costo: $0.37
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-09</incoming>
      <outgoing>sf-tobe-qc-aprueba</outgoing>
      <outgoing>sf-tobe-qc-rechaza</outgoing>
    </exclusiveGateway>

    <!-- TASK 9B — manualTask (C5: corregido de userTask)
         Reproceso fisico - trabajo manual
         Additional Participant: Inspector de Calidad -->
    <manualTask id="sid-task-9b-tobe"
       name="Reprocesar lote&#10;rechazado"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable PRINCIPAL: Operario de Planta (lane)
        Additional Participant: Inspector de Calidad (supervision del reproceso)
        Tipo BPMN: Manual Task (trabajo fisico correctivo - NVA residual)
        Duracion: 60 min (vs 90 min AS-IS, -33%) | Costo/hr: $8 | Costo: $8.00
        Ruta: 5% de lotes fabricados (vs 18% AS-IS - reduccion 72.2%)
        DOBLE MEJORA: Menos casos Y menos tiempo por caso.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffcccc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-qc-rechaza</incoming>
      <outgoing>sf-tobe-loop-9b</outgoing>
    </manualTask>

    <!-- XOR JOIN — Convergencia (stock disponible + fabricacion completada) -->
    <exclusiveGateway id="sid-gw-join-tobe"
       name="" gatewayDirection="Converging">
      <documentation>
        Converge: ruta Si (stock disponible, 70%) + ruta fabricacion-aprobada (95%x30%=28.5%)
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-06-si</incoming>
      <incoming>sf-tobe-qc-aprueba</incoming>
      <outgoing>sf-tobe-10</outgoing>
    </exclusiveGateway>

    <!-- TASK 6A — sendTask (confirmacion automatica al cliente)
         IT System: Portal Web / SAP Integration Suite -->
    <sendTask id="sid-task-6a-tobe"
       name="Enviar confirmacion&#10;automatica al cliente"
       messageRef="msg-confirmacion-orden"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Sistema Automatico (supervisado por Ejecutivo de Ventas)
        IT System: Portal Web / SAP Integration Suite (email/SMS automatico)
        Tipo BPMN: Send Task (envia MessageFlow al pool Cliente)
        Duracion: 5 min (vs 20 min AS-IS, -75%) | Costo/hr: $12 | Costo: $1.00
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ccccff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-10</incoming>
      <outgoing>sf-tobe-11</outgoing>
    </sendTask>

    <!-- TASK 10 — manualTask (C6: corregido de userTask)
         Empaque fisico con packing list digital
         IT System: ERP Legacy (packing list digital generado automaticamente) -->
    <manualTask id="sid-task-10-tobe"
       name="Empacar y preparar&#10;para despacho"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Coordinador de Logistica
        IT System: ERP Legacy (genera packing list digital automaticamente)
        Tipo BPMN: Manual Task (trabajo fisico de empaque)
        Duracion: 15 min (vs 25 min AS-IS, -40%) | Costo/hr: $10 | Costo: $2.50
        Restriccion: Despacho solo entre 07:00 y 14:00.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#fff0cc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-11</incoming>
      <outgoing>sf-tobe-12</outgoing>
    </manualTask>

    <!-- TASK 11 — serviceTask (asignacion automatica via TMS)
         IT System: TMS Beetrack -->
    <serviceTask id="sid-task-11-tobe"
       name="Asignar transportista&#10;via TMS automatizado"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Coordinador de Logistica (supervision)
        IT System: TMS Beetrack (asignacion automatica)
        Tipo BPMN: Service Task (automatizado - TMS selecciona transportista)
        Duracion: 10 min (vs 30 min AS-IS, -67%) | Costo/hr: $10 | Costo: $1.67
        Elimina llamadas telefonicas (P7).
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ccf2ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-12</incoming>
      <outgoing>sf-tobe-13</outgoing>
    </serviceTask>

    <!-- TASK 12 — userTask (entrega + firma digital)
         IT System: TMS Beetrack (app movil del transportista) -->
    <userTask id="sid-task-12-tobe"
       name="Entregar al cliente y registrar&#10;firma digital de conformidad"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Coordinador de Logistica / Transportista
        IT System: TMS Beetrack - App movil (firma digital)
        Tipo BPMN: User Task (persona usa app del TMS para registrar entrega)
        Duracion: 45 min | Costo/hr: $10 | Costo: $7.50
        Firma digital dispara automaticamente Task 13 (factura electronica).
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ffffcc"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-13</incoming>
      <outgoing>sf-tobe-14</outgoing>
    </userTask>

    <!-- TASK 13 — serviceTask (factura electronica automatica)
         IT System: Datil.me / SAP Integration Suite -->
    <serviceTask id="sid-task-13-tobe"
       name="Generar y enviar factura&#10;electronica automatica"
       completionQuantity="1" isForCompensation="false" startQuantity="1">
      <documentation>
        Responsable: Sistema Automatico (supervisado por Analista de Finanzas)
        IT System: Datil.me / SAP Integration Suite
        Tipo BPMN: Service Task (generacion y envio automatico SRI-compliant)
        Duracion: 5 min (vs 20 min AS-IS, -75%) | Costo/hr: $13 | Costo: $1.08
        Trigger: firma digital de Task 12 -> dispara automaticamente.
      </documentation>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#ccf2ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/>
      </extensionElements>
      <incoming>sf-tobe-14</incoming>
      <outgoing>sf-tobe-15</outgoing>
    </serviceTask>

    <!-- ─────────────────────────────────────────────────────────
         IT SYSTEMS — Como textAnnotation con asociacion no direccional
         Fuente S3.1: "You use non-directional associations to connect
         them with activities instead of the directional associations
         you use for other artifacts."
         ───────────────────────────────────────────────────────── -->

    <textAnnotation id="sid-it-portal-web">
      <text>IT System: Portal Web de Pedidos</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-integration-suite">
      <text>IT System: SAP Integration Suite (Middleware Central)</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-api-financiero">
      <text>IT System: API Sistema Financiero</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-erp-legacy">
      <text>IT System: ERP Legacy (API Stock + Modulo PP)</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-qc-digital">
      <text>IT System: Sistema QC Digital</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-tms-beetrack">
      <text>IT System: TMS Beetrack</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-it-datil">
      <text>IT System: Datil.me (SRI)</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d0e8ff"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#4090d0"/>
      </extensionElements>
    </textAnnotation>

    <!-- Additional Participant annotations -->
    <textAnnotation id="sid-ap-qc-proceso">
      <text>Additional Participant: Operario de QC en Proceso</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d5f5e3"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#27ae60"/>
      </extensionElements>
    </textAnnotation>

    <textAnnotation id="sid-ap-inspector">
      <text>Additional Participant: Inspector de Calidad</text>
      <extensionElements>
        <signavio:signavioMetaData metaKey="bgcolor" metaValue="#d5f5e3"/>
        <signavio:signavioMetaData metaKey="bordercolor" metaValue="#27ae60"/>
      </extensionElements>
    </textAnnotation>

    <!-- ─────────────────────────────────────────────────────────
         ASSOCIATIONS (no direccionales para IT Systems y Additional Participants)
         associationDirection="None" = linea punteada sin flecha
         ───────────────────────────────────────────────────────── -->

    <!-- IT Systems -> Tareas -->
    <association id="sid-assoc-portal-t1"  associationDirection="None"
       sourceRef="sid-it-portal-web"         targetRef="sid-task-1-tobe"/>
    <association id="sid-assoc-portal-t6a" associationDirection="None"
       sourceRef="sid-it-portal-web"         targetRef="sid-task-6a-tobe"/>
    <association id="sid-assoc-intsuit-gw" associationDirection="None"
       sourceRef="sid-it-integration-suite"  targetRef="sid-gw-and-split-tobe"/>
    <association id="sid-assoc-apifin-t2a" associationDirection="None"
       sourceRef="sid-it-api-financiero"     targetRef="sid-task-2a-tobe"/>
    <association id="sid-assoc-erp-t2b"    associationDirection="None"
       sourceRef="sid-it-erp-legacy"         targetRef="sid-task-2b-tobe"/>
    <association id="sid-assoc-erp-t6b"    associationDirection="None"
       sourceRef="sid-it-erp-legacy"         targetRef="sid-task-6b-tobe"/>
    <association id="sid-assoc-qc-t7"      associationDirection="None"
       sourceRef="sid-it-qc-digital"         targetRef="sid-task-7-tobe"/>
    <association id="sid-assoc-qc-t8"      associationDirection="None"
       sourceRef="sid-it-qc-digital"         targetRef="sid-task-8-tobe"/>
    <association id="sid-assoc-tms-t11"    associationDirection="None"
       sourceRef="sid-it-tms-beetrack"       targetRef="sid-task-11-tobe"/>
    <association id="sid-assoc-tms-t12"    associationDirection="None"
       sourceRef="sid-it-tms-beetrack"       targetRef="sid-task-12-tobe"/>
    <association id="sid-assoc-datil-t13"  associationDirection="None"
       sourceRef="sid-it-datil"              targetRef="sid-task-13-tobe"/>

    <!-- Additional Participants -> Tareas -->
    <association id="sid-assoc-ap-qcproc-t7"  associationDirection="None"
       sourceRef="sid-ap-qc-proceso"  targetRef="sid-task-7-tobe"/>
    <association id="sid-assoc-ap-insp-t9b"   associationDirection="None"
       sourceRef="sid-ap-inspector"   targetRef="sid-task-9b-tobe"/>

    <!-- ─────────────────────────────────────────────────────────
         SEQUENCE FLOWS
         ───────────────────────────────────────────────────────── -->
    <sequenceFlow id="sf-tobe-01" sourceRef="sid-start-tobe"        targetRef="sid-task-1-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-02" sourceRef="sid-task-1-tobe"       targetRef="sid-gw-and-split-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-03a" name="Verificar credito"
       sourceRef="sid-gw-and-split-tobe" targetRef="sid-task-2a-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-03b" name="Consultar stock"
       sourceRef="sid-gw-and-split-tobe" targetRef="sid-task-2b-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-04a" sourceRef="sid-task-2a-tobe"     targetRef="sid-gw-and-join-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-04b" sourceRef="sid-task-2b-tobe"     targetRef="sid-gw-and-join-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-05"  sourceRef="sid-gw-and-join-tobe" targetRef="sid-gw-creditstock-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-06-si" name="Si&#10;(credito OK + stock OK: 70%)"
       sourceRef="sid-gw-creditstock-tobe" targetRef="sid-gw-join-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
      <conditionExpression xsi:type="tFormalExpression">Credito aprobado Y stock disponible (70%)</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-06-no" name="No&#10;(requiere produccion: 30%)"
       sourceRef="sid-gw-creditstock-tobe" targetRef="sid-task-6b-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
      <conditionExpression xsi:type="tFormalExpression">Sin credito o sin stock (30%)</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-07"  sourceRef="sid-task-6b-tobe"     targetRef="sid-task-7-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-08"  sourceRef="sid-task-7-tobe"      targetRef="sid-task-8-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-09"  sourceRef="sid-task-8-tobe"      targetRef="sid-gw-qc-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-qc-aprueba" name="Aprueba&#10;(95%)"
       sourceRef="sid-gw-qc-tobe" targetRef="sid-gw-join-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
      <conditionExpression xsi:type="tFormalExpression">Lote aprueba inspeccion final (95%)</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-qc-rechaza" name="Rechaza&#10;(5%)"
       sourceRef="sid-gw-qc-tobe" targetRef="sid-task-9b-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
      <conditionExpression xsi:type="tFormalExpression">Lote rechazado - requiere reproceso (5%)</conditionExpression>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-loop-9b" name="Vuelve a&#10;inspeccion"
       sourceRef="sid-task-9b-tobe" targetRef="sid-task-8-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-10"  sourceRef="sid-gw-join-tobe"     targetRef="sid-task-6a-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-11"  sourceRef="sid-task-6a-tobe"     targetRef="sid-task-10-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-12"  sourceRef="sid-task-10-tobe"     targetRef="sid-task-11-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-13"  sourceRef="sid-task-11-tobe"     targetRef="sid-task-12-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-14"  sourceRef="sid-task-12-tobe"     targetRef="sid-task-13-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>
    <sequenceFlow id="sf-tobe-15"  sourceRef="sid-task-13-tobe"     targetRef="sid-end-tobe">
      <extensionElements><signavio:signavioMetaData metaKey="bordercolor" metaValue="#000000"/></extensionElements>
    </sequenceFlow>

  </process>

  <!-- ═══════════════════════════════════════════════════════════════
       BPMN DIAGRAM INTERCHANGE (DI) — Layout visual
       Canvas: 2560px wide x {POOL_H}px tall (INDUPRO) + 60px (Cliente)

       Lane Y positions (top edge):
         L1 Ventas          y={L_VENTAS}   center={cy(L_VENTAS)}
         L2 Finanzas        y={L_FINANZAS} center={cy(L_FINANZAS)}
         L3 Inventarios     y={L_INVENTARIOS} center={cy(L_INVENTARIOS)}
         L4 Integracion     y={L_INTEGRACION} center={cy(L_INTEGRACION)}
         L5 Planificacion   y={L_PLANIFIC} center={cy(L_PLANIFIC)}
         L6 Planta          y={L_PLANTA}   center={cy(L_PLANTA)}
         L7 QC en Proceso   y={L_QC_PROC}  center={cy(L_QC_PROC)}
         L8 Calidad         y={L_CALIDAD}  center={cy(L_CALIDAD)}
         L9 Logistica       y={L_LOGISTICA} center={cy(L_LOGISTICA)}
       ═══════════════════════════════════════════════════════════════ -->
  <bpmndi:BPMNDiagram id="sid-diagram-indupro-tobe-v1">
    <bpmndi:BPMNPlane bpmnElement="sid-collab-indupro-tobe-v1"
                      id="sid-plane-indupro-tobe-v1">

      <!-- ════ POOL SHAPES ════ -->

      <!-- Pool INDUPRO S.A. -->
      {shape("sid-pool-indupro-tobe", POOL_X, POOL_Y, POOL_W, POOL_H,
             POOL_X, POOL_Y, 24, POOL_H, 'isHorizontal="true"')}

      <!-- Pool Cliente (Black Box) -->
      {shape("sid-pool-cliente", POOL_X, CLIENTE_Y, POOL_W, 60,
             POOL_X, CLIENTE_Y, 24, 60, 'isHorizontal="true"')}

      <!-- ════ LANE SHAPES ════ -->
      {shape("sid-lane-ventas",      LANE_CONTENT_X, L_VENTAS,       2510, LANE_H, LANE_CONTENT_X+6, L_VENTAS+25,      12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-finanzas",    LANE_CONTENT_X, L_FINANZAS,     2510, LANE_H, LANE_CONTENT_X+6, L_FINANZAS+25,    12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-inventarios", LANE_CONTENT_X, L_INVENTARIOS,  2510, LANE_H, LANE_CONTENT_X+6, L_INVENTARIOS+25, 12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-integracion", LANE_CONTENT_X, L_INTEGRACION,  2510, LANE_H, LANE_CONTENT_X+6, L_INTEGRACION+25, 12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-planificacion",LANE_CONTENT_X, L_PLANIFIC,    2510, LANE_H, LANE_CONTENT_X+6, L_PLANIFIC+25,    12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-planta",      LANE_CONTENT_X, L_PLANTA,       2510, LANE_H, LANE_CONTENT_X+6, L_PLANTA+25,      12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-qc-proceso",  LANE_CONTENT_X, L_QC_PROC,      2510, LANE_H, LANE_CONTENT_X+6, L_QC_PROC+25,     12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-calidad",     LANE_CONTENT_X, L_CALIDAD,      2510, LANE_H, LANE_CONTENT_X+6, L_CALIDAD+25,     12, 96, 'isHorizontal="true"')}
      {shape("sid-lane-logistica",   LANE_CONTENT_X, L_LOGISTICA,    2510, LANE_H, LANE_CONTENT_X+6, L_LOGISTICA+25,   12, 96, 'isHorizontal="true"')}

      <!-- ════ EVENTS ════ -->

      <!-- Start Event (Message) — Lane Ventas -->
      {shape("sid-start-tobe",
             START_CX-EW//2, START_CY-EH//2, EW, EH,
             START_CX-45, START_CY+22, 90, 36)}

      <!-- End Event (Message) — Lane Finanzas -->
      {shape("sid-end-tobe",
             END_CX-EW//2, END_CY-EH//2, EW, EH,
             END_CX-45, END_CY+22, 90, 36)}

      <!-- ════ TASKS ════ -->

      <!-- Task 1 (userTask) — Lane Ventas -->
      {shape("sid-task-1-tobe",
             T1_CX-TW//2, T1_CY-TH//2, TW, TH,
             T1_CX-TW//2+5, T1_CY-TH//2+10, TW-10, 36)}

      <!-- Task 2A (serviceTask) — Lane Finanzas -->
      {shape("sid-task-2a-tobe",
             T2A_CX-TW//2, T2A_CY-TH//2, TW, TH,
             T2A_CX-TW//2+5, T2A_CY-TH//2+10, TW-10, 36)}

      <!-- Task 2B (serviceTask) — Lane Inventarios -->
      {shape("sid-task-2b-tobe",
             T2B_CX-TW//2, T2B_CY-TH//2, TW, TH,
             T2B_CX-TW//2+5, T2B_CY-TH//2+10, TW-10, 36)}

      <!-- Task 6B (userTask) — Lane Planificacion -->
      {shape("sid-task-6b-tobe",
             T6B_CX-TW//2, T6B_CY-TH//2, TW, TH,
             T6B_CX-TW//2+5, T6B_CY-TH//2+10, TW-10, 36)}

      <!-- Task 7 (manualTask) — Lane Planta -->
      {shape("sid-task-7-tobe",
             T7_CX-TW//2, T7_CY-TH//2, TW, TH,
             T7_CX-TW//2+5, T7_CY-TH//2+10, TW-10, 36)}

      <!-- Task 8 (userTask) — Lane Calidad -->
      {shape("sid-task-8-tobe",
             T8_CX-TW//2, T8_CY-TH//2, TW, TH,
             T8_CX-TW//2+5, T8_CY-TH//2+10, TW-10, 36)}

      <!-- Task 9B (manualTask) — Lane Planta -->
      {shape("sid-task-9b-tobe",
             T9B_CX-TW//2, T9B_CY-TH//2, TW, TH,
             T9B_CX-TW//2+5, T9B_CY-TH//2+10, TW-10, 36)}

      <!-- Task 6A (sendTask) — Lane Ventas -->
      {shape("sid-task-6a-tobe",
             T6A_CX-TW//2, T6A_CY-TH//2, TW, TH,
             T6A_CX-TW//2+5, T6A_CY-TH//2+10, TW-10, 36)}

      <!-- Task 10 (manualTask) — Lane Logistica -->
      {shape("sid-task-10-tobe",
             T10_CX-TW//2, T10_CY-TH//2, TW, TH,
             T10_CX-TW//2+5, T10_CY-TH//2+10, TW-10, 36)}

      <!-- Task 11 (serviceTask) — Lane Logistica -->
      {shape("sid-task-11-tobe",
             T11_CX-TW//2, T11_CY-TH//2, TW, TH,
             T11_CX-TW//2+5, T11_CY-TH//2+10, TW-10, 36)}

      <!-- Task 12 (userTask) — Lane Logistica -->
      {shape("sid-task-12-tobe",
             T12_CX-TW//2, T12_CY-TH//2, TW, TH,
             T12_CX-TW//2+5, T12_CY-TH//2+10, TW-10, 36)}

      <!-- Task 13 (serviceTask) — Lane Finanzas -->
      {shape("sid-task-13-tobe",
             T13_CX-TW//2, T13_CY-TH//2, TW, TH,
             T13_CX-TW//2+5, T13_CY-TH//2+10, TW-10, 36)}

      <!-- ════ GATEWAYS ════ -->

      <!-- AND SPLIT — Lane Integracion -->
      {shape("sid-gw-and-split-tobe",
             ANDS_CX-GW//2, ANDS_CY-GH//2, GW, GH,
             ANDS_CX-50, ANDS_CY+GH//2+5, 100, 30)}

      <!-- AND JOIN — Lane Integracion -->
      {shape("sid-gw-and-join-tobe",
             ANDJ_CX-GW//2, ANDJ_CY-GH//2, GW, GH)}

      <!-- XOR CreditStock — Lane Integracion -->
      {shape("sid-gw-creditstock-tobe",
             XORCS_CX-GW//2, XORCS_CY-GH//2, GW, GH,
             XORCS_CX-55, XORCS_CY+GH//2+5, 110, 36,
             'isMarkerVisible="true"')}

      <!-- XOR QC — Lane Calidad -->
      {shape("sid-gw-qc-tobe",
             XORQC_CX-GW//2, XORQC_CY-GH//2, GW, GH,
             XORQC_CX-50, XORQC_CY+GH//2+5, 100, 30,
             'isMarkerVisible="true"')}

      <!-- XOR JOIN — Lane Ventas -->
      {shape("sid-gw-join-tobe",
             XORJ_CX-GW//2, XORJ_CY-GH//2, GW, GH,
             label_x=None)}

      <!-- ════ IT SYSTEM ANNOTATIONS ════ -->

      <!-- Portal Web — Lane Ventas (above Task1) -->
      {shape("sid-it-portal-web",
             T1_CX-ITW//2-30, L_VENTAS+5, ITW, ITH)}

      <!-- SAP Integration Suite — Lane Integracion (above AND-Split) -->
      {shape("sid-it-integration-suite",
             ANDS_CX-80, L_INTEGRACION+5, 160, ITH)}

      <!-- API Sistema Financiero — Lane Finanzas (right of Task2A) -->
      {shape("sid-it-api-financiero",
             T2A_CX+TW//2+10, T2A_CY-ITH//2, 150, ITH)}

      <!-- ERP Legacy — Lane Inventarios (right of Task2B) -->
      {shape("sid-it-erp-legacy",
             T2B_CX+TW//2+10, T2B_CY-ITH//2, 150, ITH)}

      <!-- Sistema QC Digital — Lane Planta (above Task7) -->
      {shape("sid-it-qc-digital",
             T7_CX-ITW//2, L_PLANTA+5, ITW, ITH)}

      <!-- TMS Beetrack — Lane Logistica (above Task11) -->
      {shape("sid-it-tms-beetrack",
             T11_CX-ITW//2, L_LOGISTICA+5, ITW, ITH)}

      <!-- Datil.me — Lane Finanzas (above Task13) -->
      {shape("sid-it-datil",
             T13_CX-ITW//2, L_FINANZAS+5, ITW, ITH)}

      <!-- ════ ADDITIONAL PARTICIPANT ANNOTATIONS ════ -->

      <!-- QC en Proceso — Lane QC-PROC (connects to Task7) -->
      {shape("sid-ap-qc-proceso",
             T7_CX-APW//2, L_QC_PROC+55, APW, APH)}

      <!-- Inspector (Task9B) — Lane Calidad (connects to Task9B) -->
      {shape("sid-ap-inspector",
             T9B_CX-APW//2, L_CALIDAD+55, APW, APH)}

      <!-- ════ SEQUENCE FLOW EDGES ════ -->

      <!-- SF-01: Start -> Task1 (horizontal Ventas) -->
      {edge("sf-tobe-01", [
          wp(START_CX+EW//2, START_CY),
          wp(T1_CX-TW//2,    T1_CY)
      ])}

      <!-- SF-02: Task1 -> AND-Split (Ventas -> Integracion, down) -->
      {edge("sf-tobe-02", [
          wp(T1_CX+TW//2,  T1_CY),
          wp(ANDS_CX,      T1_CY),
          wp(ANDS_CX,      ANDS_CY-GH//2)
      ])}

      <!-- SF-03A: AND-Split -> Task2A (up to Finanzas) -->
      {edge("sf-tobe-03a", [
          wp(ANDS_CX,      ANDS_CY-GH//2),
          wp(ANDS_CX,      T2A_CY),
          wp(T2A_CX-TW//2, T2A_CY)
      ], label=(ANDS_CX+8, T2A_CY+30, 80, 14))}

      <!-- SF-03B: AND-Split -> Task2B (up to Inventarios) -->
      {edge("sf-tobe-03b", [
          wp(ANDS_CX+GW//2, ANDS_CY),
          wp(ANDS_CX+50,    ANDS_CY),
          wp(ANDS_CX+50,    T2B_CY),
          wp(T2B_CX-TW//2,  T2B_CY)
      ], label=(ANDS_CX+55, T2B_CY+20, 80, 14))}

      <!-- SF-04A: Task2A -> AND-Join (Finanzas down to Integracion) -->
      {edge("sf-tobe-04a", [
          wp(T2A_CX+TW//2, T2A_CY),
          wp(ANDJ_CX,      T2A_CY),
          wp(ANDJ_CX,      ANDJ_CY-GH//2)
      ])}

      <!-- SF-04B: Task2B -> AND-Join (Inventarios down to Integracion) -->
      {edge("sf-tobe-04b", [
          wp(T2B_CX+TW//2, T2B_CY),
          wp(ANDJ_CX-20,   T2B_CY),
          wp(ANDJ_CX-20,   ANDJ_CY),
          wp(ANDJ_CX-GW//2, ANDJ_CY)
      ])}

      <!-- SF-05: AND-Join -> XOR-CreditStock (horizontal Integracion) -->
      {edge("sf-tobe-05", [
          wp(ANDJ_CX+GW//2,  ANDJ_CY),
          wp(XORCS_CX-GW//2, XORCS_CY)
      ])}

      <!-- SF-06-SI: XOR-CreditStock -> XOR-Join (Integracion up to Ventas, long) -->
      {edge("sf-tobe-06-si", [
          wp(XORCS_CX,      XORCS_CY-GH//2),
          wp(XORCS_CX,      XORJ_CY),
          wp(XORJ_CX-GW//2, XORJ_CY)
      ], label=(XORCS_CX+8, XORCS_CY-GH//2-50, 130, 36))}

      <!-- SF-06-NO: XOR-CreditStock -> Task6B (down to Planificacion) -->
      {edge("sf-tobe-06-no", [
          wp(XORCS_CX,      XORCS_CY+GH//2),
          wp(XORCS_CX,      T6B_CY),
          wp(T6B_CX-TW//2,  T6B_CY)
      ], label=(XORCS_CX+8, XORCS_CY+GH//2+10, 120, 30))}

      <!-- SF-07: Task6B -> Task7 (Planificacion -> Planta, down) -->
      {edge("sf-tobe-07", [
          wp(T6B_CX+TW//2, T6B_CY),
          wp(T7_CX,        T6B_CY),
          wp(T7_CX,        T7_CY-TH//2)
      ])}

      <!-- SF-08: Task7 -> Task8 (Planta -> QC Proceso -> Calidad, straight down) -->
      {edge("sf-tobe-08", [
          wp(T7_CX, T7_CY+TH//2),
          wp(T7_CX, T8_CY-TH//2)
      ])}

      <!-- SF-09: Task8 -> XOR-QC (horizontal Calidad) -->
      {edge("sf-tobe-09", [
          wp(T8_CX+TW//2,    T8_CY),
          wp(XORQC_CX-GW//2, XORQC_CY)
      ])}

      <!-- SF-QC-APRUEBA: XOR-QC -> XOR-Join (up to Ventas, long) -->
      {edge("sf-tobe-qc-aprueba", [
          wp(XORQC_CX,       XORQC_CY-GH//2),
          wp(XORQC_CX,       XORJ_CY),
          wp(XORJ_CX-GW//2,  XORJ_CY)
      ], label=(XORQC_CX+8, XORQC_CY-200, 85, 24))}

      <!-- SF-QC-RECHAZA: XOR-QC -> Task9B (right, up to Planta) -->
      {edge("sf-tobe-qc-rechaza", [
          wp(XORQC_CX+GW//2, XORQC_CY),
          wp(T9B_CX,         XORQC_CY),
          wp(T9B_CX,         T9B_CY+TH//2)
      ], label=(XORQC_CX+GW//2+5, XORQC_CY-15, 70, 24))}

      <!-- SF-LOOP-9B: Task9B -> Task8 (left, down to Calidad - loop) -->
      {edge("sf-tobe-loop-9b", [
          wp(T9B_CX-TW//2, T9B_CY),
          wp(T8_CX,        T9B_CY),
          wp(T8_CX,        T8_CY-TH//2)
      ], label=(T8_CX+10, T9B_CY-20, 90, 24))}

      <!-- SF-10: XOR-Join -> Task6A (horizontal Ventas) -->
      {edge("sf-tobe-10", [
          wp(XORJ_CX+GW//2, XORJ_CY),
          wp(T6A_CX-TW//2,  T6A_CY)
      ])}

      <!-- SF-11: Task6A -> Task10 (Ventas down to Logistica) -->
      {edge("sf-tobe-11", [
          wp(T6A_CX, T6A_CY+TH//2),
          wp(T6A_CX, T10_CY),
          wp(T10_CX-TW//2, T10_CY)
      ])}

      <!-- SF-12: Task10 -> Task11 (horizontal Logistica) -->
      {edge("sf-tobe-12", [
          wp(T10_CX+TW//2, T10_CY),
          wp(T11_CX-TW//2, T11_CY)
      ])}

      <!-- SF-13: Task11 -> Task12 (horizontal Logistica) -->
      {edge("sf-tobe-13", [
          wp(T11_CX+TW//2, T11_CY),
          wp(T12_CX-TW//2, T12_CY)
      ])}

      <!-- SF-14: Task12 -> Task13 (Logistica up to Finanzas) -->
      {edge("sf-tobe-14", [
          wp(T12_CX+TW//2, T12_CY),
          wp(T13_CX,       T12_CY),
          wp(T13_CX,       T13_CY+TH//2)
      ])}

      <!-- SF-15: Task13 -> End (horizontal Finanzas) -->
      {edge("sf-tobe-15", [
          wp(T13_CX+TW//2,   T13_CY),
          wp(END_CX-EW//2,   END_CY)
      ])}

      <!-- ════ MESSAGE FLOW EDGES ════ -->

      <!-- MF-01: Pool-Cliente -> Start (solicitud via portal) -->
      {edge("mf-solicitud-inicio", [
          wp(START_CX, CLIENTE_Y),
          wp(START_CX, START_CY+EH//2)
      ], label=(START_CX+8, CLIENTE_Y-80, 100, 36))}

      <!-- MF-02: Task6A -> Pool-Cliente (confirmacion automatica) -->
      {edge("mf-confirmacion-cliente", [
          wp(T6A_CX, T6A_CY+TH//2),
          wp(T6A_CX, CLIENTE_Y)
      ], label=(T6A_CX+8, CLIENTE_Y-60, 110, 30))}

      <!-- MF-03: End -> Pool-Cliente (factura electronica) -->
      {edge("mf-factura-cliente", [
          wp(END_CX, END_CY+EH//2),
          wp(END_CX, CLIENTE_Y)
      ], label=(END_CX+8, CLIENTE_Y-50, 100, 30))}

      <!-- ════ ASSOCIATION EDGES (non-directional — IT Systems + Additional Participants) ════ -->

      <!-- Portal Web <-> Task1 -->
      {edge("sid-assoc-portal-t1", [
          wp(T1_CX-30, L_VENTAS+5+ITH),
          wp(T1_CX-30, T1_CY-TH//2)
      ])}

      <!-- Portal Web <-> Task6A -->
      {edge("sid-assoc-portal-t6a", [
          wp(T1_CX+ITW//2-30, L_VENTAS+5+ITH//2),
          wp(T6A_CX,          L_VENTAS+5+ITH//2)
      ])}

      <!-- SAP Integration Suite <-> AND-Split -->
      {edge("sid-assoc-intsuit-gw", [
          wp(ANDS_CX, L_INTEGRACION+5+ITH),
          wp(ANDS_CX, ANDS_CY-GH//2)
      ])}

      <!-- API Financiero <-> Task2A -->
      {edge("sid-assoc-apifin-t2a", [
          wp(T2A_CX+TW//2+10, T2A_CY),
          wp(T2A_CX+TW//2+10, T2A_CY)
      ])}

      <!-- ERP Legacy <-> Task2B -->
      {edge("sid-assoc-erp-t2b", [
          wp(T2B_CX+TW//2+10, T2B_CY),
          wp(T2B_CX+TW//2+10, T2B_CY)
      ])}

      <!-- ERP Legacy <-> Task6B -->
      {edge("sid-assoc-erp-t6b", [
          wp(T6B_CX+TW//2+10, T2B_CY+ITH//2),
          wp(T6B_CX+TW//2,    T6B_CY)
      ])}

      <!-- Sistema QC Digital <-> Task7 -->
      {edge("sid-assoc-qc-t7", [
          wp(T7_CX, L_PLANTA+5+ITH),
          wp(T7_CX, T7_CY-TH//2)
      ])}

      <!-- Sistema QC Digital <-> Task8 -->
      {edge("sid-assoc-qc-t8", [
          wp(T8_CX, L_CALIDAD+5),
          wp(T8_CX, T8_CY-TH//2)
      ])}

      <!-- TMS Beetrack <-> Task11 -->
      {edge("sid-assoc-tms-t11", [
          wp(T11_CX, L_LOGISTICA+5+ITH),
          wp(T11_CX, T11_CY-TH//2)
      ])}

      <!-- TMS Beetrack <-> Task12 -->
      {edge("sid-assoc-tms-t12", [
          wp(T11_CX+ITW//2, L_LOGISTICA+5+ITH//2),
          wp(T12_CX,        L_LOGISTICA+5+ITH//2)
      ])}

      <!-- Datil.me <-> Task13 -->
      {edge("sid-assoc-datil-t13", [
          wp(T13_CX, L_FINANZAS+5+ITH),
          wp(T13_CX, T13_CY-TH//2)
      ])}

      <!-- Additional Participant: QC en Proceso <-> Task7 (lane QC-PROC -> lane Planta) -->
      {edge("sid-assoc-ap-qcproc-t7", [
          wp(T7_CX,   L_QC_PROC+55+APH//2),
          wp(T7_CX,   T7_CY+TH//2)
      ])}

      <!-- Additional Participant: Inspector <-> Task9B (lane Calidad -> lane Planta) -->
      {edge("sid-assoc-ap-insp-t9b", [
          wp(T9B_CX, L_CALIDAD+55+APH//2),
          wp(T9B_CX, T9B_CY+TH//2)
      ])}

    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</definitions>
"""


# ═══════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    output_path = r"c:\Users\drago\projects\ProyectoSAPSignavio\Analisis\Modelados\INDUPRO_TOBE_v1.bpmn"
    xml = generate()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Archivo generado: {output_path}")
    print(f"\nEstructura TO-BE:")
    print(f"  9 Swimlanes: Ventas, Finanzas, Inventarios, Analista Integracion (NUEVO),")
    print(f"               Planificacion, Planta, Operario QC (NUEVO), Calidad, Logistica")
    print(f"  Tipos de tarea corregidos:")
    print(f"    Task 1  -> userTask   (Ejecutivo usa portal web)")
    print(f"    Task 2A -> serviceTask (API automatica)")
    print(f"    Task 2B -> serviceTask (API automatica)")
    print(f"    Task 6A -> sendTask    (confirmacion automatica)")
    print(f"    Task 6B -> userTask    (planificador aprueba en ERP)")
    print(f"    Task 7  -> manualTask  (fabricacion fisica)")
    print(f"    Task 8  -> userTask    (inspector usa QC Digital)")
    print(f"    Task 9B -> manualTask  (reproceso fisico)")
    print(f"    Task 10 -> manualTask  (empaque fisico)")
    print(f"    Task 11 -> serviceTask (TMS automatico)")
    print(f"    Task 12 -> userTask    (entrega con firma digital)")
    print(f"    Task 13 -> serviceTask (factura automatica)")
    print(f"  IT Systems (textAnnotation + asociacion no direccional):")
    print(f"    Portal Web, SAP Integration Suite, API Financiero,")
    print(f"    ERP Legacy, Sistema QC Digital, TMS Beetrack, Datil.me")
    print(f"  Additional Participants:")
    print(f"    Op. QC en Proceso -> Task7 | Inspector -> Task9B")
    print(f"  Gateways:")
    print(f"    AND-Split/Join + XOR-CreditStock (Si 70%/No 30%)")
    print(f"    XOR-QC (Aprueba 95%/Rechaza 5%)")
