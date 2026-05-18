# SAP Signavio Regional Challenge 2026 — INDUPRO S.A.

Repositorio del proyecto de competencia **SAP Signavio Regional Challenge 2026**. Contiene los modelos BPMN, análisis, materiales de estudio y entregables del equipo para el caso de estudio **INDUPRO S.A.** — proceso de Gestión de Pedidos.

---

## Caso de Estudio

**INDUPRO S.A.** (Industrias Productivas S.A.) es una empresa manufacturera que requiere transformar digitalmente su proceso de Gestión de Pedidos con SAP.

| Indicador | AS-IS (actual) | TO-BE (objetivo) |
|-----------|---------------|-----------------|
| Tiempo total | 555 min | < 350 min |
| Costo por pedido | $105.91 | < $70.00 |
| Actividades sin valor agregado | ~120 min | < 70 min |
| Tasa de reproceso | ~18% | < 5% |

**Módulos SAP involucrados:** SD → FI-AR → MM → PP-MRP → PP-CRP → QM → WM → FI

---

## Estructura del Repositorio

```
ProyectoSAPSignavio/
│
├── Plantillas Base/                        # Modelos BPMN oficiales
│   ├── INDUPRO_Gestion_Pedidos_ASIS.bpmn   # Modelo AS-IS (entregable E1)
│   ├── INDUPRO_Gestion_Pedidos_TOBE.bpmn   # Modelo TO-BE (entregable E2)
│   ├── Diccionario Guía Exportado.xlsx     # Diccionario exportado de Signavio
│   ├── Proceso_Elaboracion_Galletas.bpmn   # Plantilla de referencia
│   └── Shipping of Goods.bpmn             # Plantilla de referencia
│
├── Analisis/                               # Documentación y análisis
│   ├── Modelados/
│   │   └── INDUPRO_ASIS_Corregido_v2.bpmn  # AS-IS con correcciones del profesor
│   ├── INDUPRO_Analisis_Completo.md        # Análisis integral del proceso
│   ├── Reunion_Analisis_14may2026.md       # Acta de reunión con el profesor (14 may)
│   ├── Presentacion_ASIS_INDUPRO.md        # Guía de presentación AS-IS
│   ├── Presentacion_TOBE_INDUPRO.md        # Guía de presentación TO-BE
│   ├── Configuracion_Simulacion_ASIS.md    # Parámetros de simulación AS-IS
│   ├── Guia_Simulacion_Signavio.md         # Cómo configurar la simulación en Signavio
│   ├── Guia_Importacion_Diccionario_Signavio.md  # Importar diccionario a Signavio
│   ├── Mapa_Teoria_SAP_Signavio_TTT.md     # Mapa de teoría SAP Signavio TTT
│   └── INDUPRO_Diccionario_Signavio.xlsx   # Diccionario de elementos del proceso
│
├── Herramientas/
│   └── generar_diccionario_INDUPRO.py      # Script Python para generar el diccionario
│
├── material-concurso/
│   └── Reunión - SAP Signavio Contest-20260514.docx  # Grabación/transcripción reunión
│
└── SAP Signavio TTT/                       # Material del Train-the-Trainer
    ├── 1. Slides/          # S1–S5: Presentaciones del programa TTT (PDF)
    ├── 2. Lectures/        # S1.1–S5.2: Lecturas de apoyo (DOCX)
    ├── 3. Deliverables/    # Entregables de referencia de otros equipos
    │   ├── Armijos_Alfredo_ESPOL/
    │   └── SAP & Furious_UMAD/
    ├── 4. Posters/         # Poster BPMN 2.0 y DMN
    ├── 5. Recordings/      # Grabaciones de sesiones (MP4, excluidas de git)
    ├── 6. Handbooks/       # Manuales BPMN 2.0 y SAP Signavio Process Manager
    ├── 7. Standards/       # Estándares APQC PCF y SCOR-DS
    ├── 8. Flyers/          # Quick Start Guide SAP Signavio
    ├── 9. Caso INDUPRO/    # Documentos oficiales del concurso
    │   ├── Caso_Estudio_INDUPRO_v1.pdf
    │   └── SAP_Signavio_Regional_Challenge_2026.pdf
    └── SAP_SIGNAVIO_PROCESS_TRANSFORMATION_SUITE/  # Documentación de la suite SAP Signavio
```

---

## Modelos BPMN

### AS-IS — Proceso Actual
- **Archivo:** `Plantillas Base/INDUPRO_Gestion_Pedidos_ASIS.bpmn`
- 7 carriles (Ventas, Crédito/Finanzas, Almacén, Planta, Calidad, Despacho, Cliente)
- 13 actividades numeradas, 2 gateways XOR (stock 65%/35%, calidad 82%/18%)
- Tiempo total: **555 min** | Costo: **$105.91**

### TO-BE — Proceso Optimizado con SAP
- **Archivo:** `Plantillas Base/INDUPRO_Gestion_Pedidos_TOBE.bpmn`
- 8 carriles (agrega "Sistema Automático")
- AND gateway para verificación paralela crédito+stock
- Service tasks para automatización SAP
- Objetivo: **< 350 min** | **< $70.00**

### AS-IS Corregido v2 (evidencia académica)
- **Archivo:** `Analisis/Modelados/INDUPRO_ASIS_Corregido_v2.bpmn`
- Incorpora correcciones del profesor: gateway validación de datos (C1), gateway crédito (C2), timer de reprogramación 15 min (C4), etiquetas explícitas en todos los gateways (C5)
- **Nota:** Este modelo es evidencia de calidad de modelado BPMN, no el entregable oficial de competencia

---

## Correcciones del Profesor (Reunión 14 May 2026)

| ID | Corrección | Descripción |
|----|-----------|-------------|
| C1 | Gateway validación de datos | XOR antes de verificación de crédito (85% correcto / 15% error) |
| C2 | Gateway aprobación de crédito | XOR explícito tras tarea de crédito (80% aprobado / 20% rechazado) |
| C4 | Timer de reprogramación | Intermediate Timer Event 15 min antes del reproceso de fabricación |
| C5 | Etiquetas en gateways | Ambas salidas de cada XOR etiquetadas explícitamente |

---

## Entregables del Concurso

| Entregable | Estado | Archivo |
|-----------|--------|---------|
| E1 — Modelo AS-IS | ✅ Completo | `Plantillas Base/INDUPRO_Gestion_Pedidos_ASIS.bpmn` |
| E2 — Modelo TO-BE | ✅ Completo | `Plantillas Base/INDUPRO_Gestion_Pedidos_TOBE.bpmn` |
| E3 — Simulación AS-IS | ⏳ Pendiente | Configurar en Signavio |
| E4 — Comparación de diagramas | ⏳ Pendiente | Crear en Signavio |

**Próximo hito:** Modelo TO-BE — entrega 22 de mayo de 2026  
**Próxima reunión con el profesor:** Lunes 18 de mayo 2026, 19:00

---

## Configuración del Entorno

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install python-docx pdfplumber openpyxl
```

> Las grabaciones de video (`.mp4`, ~1.2 GB total) están excluidas del repositorio por el límite de 100 MB de GitHub. Se almacenan localmente en `SAP Signavio TTT/5. Recordings/`.

---

## Tecnologías

- **SAP Signavio Process Manager** — Modelado y simulación BPMN 2.0
- **SAP Signavio Process Intelligence** — Process Mining para detección de variantes y cuellos de botella
- **BPMN 2.0** — Notación estándar de modelado de procesos
- **Python** — Automatización de diccionario y extracción de documentos
- **SAP Modules:** SD, FI-AR, MM, PP (MRP/CRP), QM, WM, FI
