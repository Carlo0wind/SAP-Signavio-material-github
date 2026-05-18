# Mapa de Teoría — SAP Signavio TTT
## Índice de Recursos y su Aplicación al Caso INDUPRO

> Guía de referencia rápida para navegar los materiales disponibles en `SAP Signavio TTT/`

---

## Estructura de Carpetas

```
SAP Signavio TTT/
├── 1. Slides/          → Presentaciones por sesión (S1-S5)
├── 2. Lectures/        → Lecturas detalladas por subtema
├── 3. Deliverables/    → Entregables de ejemplo de otros equipos
├── 4. Posters/         → Referencias visuales BPMN 2.0
├── 5. Recordings/      → (Grabaciones de sesiones)
├── 6. Handbooks/       → Manuales oficiales (BPMN 2.0, Signavio)
├── 7. Standards/       → Estándares industriales (SCOR, APQC PCF)
└── 9. Caso INDUPRO/    → Documentos del caso de estudio
```

---

## Índice de Lecturas (S2. Lectures/)

### Sesión 1 — Business Process Management

| Archivo | Contenido | Cuándo usar |
|---|---|---|
| `S1.1. Defining Business Process Management.docx` | Definición de BPM, ciclo de vida (diseño→modelado→ejecución→monitoreo→optimización), beneficios del BPM | Para la justificación teórica del análisis AS-IS y la propuesta TO-BE |
| `S1.2. Introduction to Business Process Modeling in Practice.docx` | Cómo modelar en práctica, convenciones, mejores prácticas | Para guiar el modelado correcto del proceso en Signavio |

### Sesión 2 — SAP Signavio Process Manager

| Archivo | Contenido | Cuándo usar |
|---|---|---|
| `S2.1. Understanding SAP Signavio Process Manager.docx` | Features: Explorer, Editor, Dictionary, Collaboration Hub, Simulation, Reporting. Diagrama Comparison. | **Guía principal de uso de la plataforma** |
| `S2.2. Using the QuickModel in SAP Signavio.docx` | QuickModel para crear modelos rápidos con texto estructurado | Para prototipar el proceso antes de modelar en detalle |

### Sesión 3 — BPMN 2.0

| Archivo | Contenido | Cuándo usar |
|---|---|---|
| `S3.1. An Introductory Guide to BPMN 2.0.docx` | **Guía completa de BPMN 2.0**: eventos, actividades, gateways (XOR/AND/OR), swimlanes, flujos, artefactos | **Referencia obligatoria para todo el modelado** |
| `S3.2. Responsibilities for Task Assignment (BPMN).docx` | Cómo asignar responsabilidades en swimlanes, roles en tareas, RACI en BPMN | Para asignar correctamente recursos en cada tarea |

### Sesión 4 — Arquitectura de Procesos y Reportes

| Archivo | Contenido | Cuándo usar |
|---|---|---|
| `S4.1. Explaining Process Architecture and Lifecycle.docx` | Niveles de proceso (L1-L4), arquitectura empresarial de procesos, lifecycle BPM | Para estructurar la jerarquía del proceso de INDUPRO |
| `S4.2. Understanding Signavio Reports.docx` | Cómo generar reportes en Signavio, análisis de atributos, exportación | Para evidencia documental y métricas adicionales |

### Sesión 5 — Simulación

| Archivo | Contenido | Cuándo usar |
|---|---|---|
| `S5.1. What is Modeling & Simulation.docx` | Tipos de simulación (system dynamics, discrete event, agent-based), herramientas, integración con BPI | Justificación teórica del uso de simulación |
| `S5.2. Performing Simulations in SAP Signavio.docx` | **Cómo simular en Signavio**: tabs Costs/Duration/Frequency/Resources, interpretar resultados, bottlenecks | **Guía paso a paso para configurar la simulación del caso** |

---

## Slides (S1. Slides/)

| Archivo | Sesión | Temas clave |
|---|---|---|
| `S1. Train-the-Trainer-de-SAP-Signavio-Process-Manager.pdf` | Sesión 1 | BPM fundamentos |
| `S2. Train-the-Trainer-de-SAP-Signavio-Process-Manager.pdf` | Sesión 2 | SAP Signavio features |
| `S3. Train-the-Trainer-de-SAP-Signavio-Process-Manager.pdf` | Sesión 3 | BPMN 2.0 |
| `S4. Train-the-Trainer-de-SAP-Signavio-Process-Manager.pdf` | Sesión 4 | Arquitectura y reportes |
| `S5. Train-the-Trainer-de-SAP-Signavio-Process-Manager.pdf` | Sesión 5 | Simulación |

---

## Posters de Referencia Rápida (S4. Posters/)

| Archivo | Uso |
|---|---|
| `BPMN and DMN-Poster-01.pdf` | Referencia visual rápida de todos los elementos BPMN 2.0 y DMN |
| `BPMN-2_2024-WEB-02.pdf` | Guía visual actualizada de BPMN 2.0 (2024) |
| `BPMN-2_2024-WEB-02.docx` | Versión editable del poster |

> **Consejo:** Tener abierto `BPMN and DMN-Poster-01.pdf` mientras se modela en Signavio para referencia inmediata de elementos.

---

## Handbooks — Manuales Oficiales (S6. Handbooks/)

| Archivo | Contenido | Páginas clave |
|---|---|---|
| `Business Process Model and Notation BPMN 2.0.pdf` | **Estándar oficial BPMN 2.0 completo** (Object Management Group). Definición formal de todos los elementos. | Capítulo de Events, Activities, Gateways para validar uso correcto |
| `SAP-Signavio-Process-Manager-User-Guide.pdf` | **Manual de usuario completo de SAP Signavio Process Manager**. Todas las funcionalidades, paso a paso. | Secciones de Simulation, Dictionary, Collaboration Hub |

---

## Estándares Industriales (S7. Standards/)

| Archivo | Estándar | Aplicación en INDUPRO |
|---|---|---|
| `ASCM_SCOR-DS-Digital-Guide.pdf` | **SCOR (Supply Chain Operations Reference)** — Marco estándar para procesos de cadena de suministro | Mapear el proceso de gestión de pedidos de INDUPRO en el marco SCOR (Plan→Source→Make→Deliver) |
| `K014749_APQC PCF...xlsx` | **APQC Process Classification Framework (PCF)** — Taxonomía estándar cross-industria de procesos empresariales | Ubicar el proceso de INDUPRO en la jerarquía estándar (Grupo 4: Deliver Products and Services) |

### Mapeo SCOR para INDUPRO

| Proceso INDUPRO | Categoría SCOR |
|---|---|
| Recepción y validación de pedidos | **sO1** — Order Management |
| Verificación de crédito | **sO1.3** — Check Credit |
| Consulta de inventario | **sS1** — Source Stocked Product |
| Planificación de producción | **sP3** — Plan Make |
| Fabricación | **sM1** — Make-to-Stock |
| Control de calidad | **sM1.4** — Release Finished Product |
| Logística y despacho | **sD1** — Deliver Stocked Product |
| Facturación | **sD1.14** — Invoice |

---

## Entregables de Referencia (S3. Deliverables/)

> Carpetas de otros equipos como referencia de estructura y calidad:
- `Armijos_Alfredo_ESPOL/` — Entregables del equipo ESPOL
- `SAP & Furious_UMAD/` — Entregables del equipo UMAD

*(Actualmente vacías — se completarán con los trabajos de referencia)*

---

## Matriz de Teoría → Entregables del Caso

| Entregable | Archivo teoría principal | Archivo teoría de apoyo |
|---|---|---|
| E1: Modelo AS-IS | S3.1 BPMN 2.0 Guide | S3.2 Task Assignment · BPMN Poster |
| E2: Modelo TO-BE | S3.1 BPMN 2.0 Guide · S1.1 BPM | S4.1 Process Architecture |
| E3: Dictionary | S2.1 Understanding Signavio | Signavio User Guide |
| E4: Diagram Comparison | S2.1 Understanding Signavio | Signavio User Guide |
| E5: Simulación | **S5.2 Performing Simulations** | S5.1 What is Simulation |
| E6: Informe Ejecutivo | S1.1 BPM · S4.1 Architecture | SCOR Guide (contexto industrial) |
| E7: Video | S1 Slides (estructura presentación) | S2 Slides (demo Signavio) |

---

## Conceptos BPMN 2.0 Críticos para INDUPRO

### Elementos a usar (referencia: S3.1 + BPMN Poster)

```
EVENTOS
├── Start Event (Circle) → Inicio del proceso
│   └── Message Start (envelope) → Pedido del cliente
├── End Event (Thick circle) → Fin del proceso
│   └── Message End → Confirmación entrega + factura
└── Intermediate Events → No requeridos en este nivel

ACTIVIDADES
├── Task (Rounded rectangle)
│   ├── User Task (person icon) → Tareas humanas (AS-IS y TO-BE)
│   ├── Service Task (gear icon) → Automatizadas (TO-BE: crédito, stock, factura)
│   └── Manual Task (hand icon) → Sin sistema (fabricación física)
└── Sub-Process → No requerido en nivel 1

GATEWAYS
├── XOR Gateway (X) — Exclusive Decision
│   ├── ¿Hay stock? → SÍ (65%) / NO (35%)
│   └── ¿Pasa QC? → APRUEBA (82%) / RECHAZA (18%)
└── AND Gateway (+) — Parallel (TO-BE ONLY)
    ├── AND Split → Inicio paralelo crédito + inventario
    └── AND Join → Convergencia resultados paralelos

CONECTORES
├── Sequence Flow (solid arrow) → Flujo normal entre actividades
├── Message Flow (dashed arrow) → Entre pools diferentes
└── Association (dotted) → Anotaciones

SWIMLANES
├── Pool → INDUPRO S.A. (empresa completa)
└── Lane → Un carril por departamento/rol
    ├── Ventas y Servicio al Cliente
    ├── Finanzas y Facturación
    ├── Coordinación de Inventarios
    ├── Planificación de Producción
    ├── Planta de Manufactura
    ├── Control de Calidad
    └── Logística y Distribución
```

---

*Índice generado para el SAP Signavio Regional Challenge 2026 — Caso INDUPRO*
