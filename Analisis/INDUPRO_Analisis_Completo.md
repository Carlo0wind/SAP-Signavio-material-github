# Análisis Completo — INDUPRO S.A.

## SAP Signavio Regional Challenge 2026

**Versión:** 1.0
**Fecha:** Mayo 2026
**Referencia:** `SAP Signavio TTT/9. Caso INDUPRO/Caso_Estudio_INDUPRO_v1.pdf`

---

## ÍNDICE

1. [Contexto del Reto](#1-contexto-del-reto)
2. [Empresa: INDUPRO S.A.](#2-empresa-indupro-sa)
3. [Proceso AS-IS — Análisis Detallado](#3-proceso-as-is--análisis-detallado)
4. [KPIs AS-IS vs. Metas TO-BE](#4-kpis-as-is-vs-metas-to-be)
5. [Ineficiencias Identificadas (causa raíz)](#5-ineficiencias-identificadas-causa-raíz)
6. [Restricciones del Desafío](#6-restricciones-del-desafío)
7. [Propuesta de Proceso TO-BE](#7-propuesta-de-proceso-to-be)
8. [Comparativa Cuantitativa AS-IS vs. TO-BE](#8-comparativa-cuantitativa-as-is-vs-to-be)
9. [Inversión y Viabilidad](#9-inversión-y-viabilidad)
10. [Requisitos BPMN en SAP Signavio](#10-requisitos-bpmn-en-sap-signavio)
11. [Guía de Simulación — Parámetros Exactos](#11-guía-de-simulación--parámetros-exactos)
12. [Entregables — Checklist Completo](#12-entregables--checklist-completo)
13. [Rúbrica y Criterios de Evaluación](#13-rúbrica-y-criterios-de-evaluación)
14. [Mapa de Teoría Disponible → Aplicación al Caso](#14-mapa-de-teoría-disponible--aplicación-al-caso)
15. [Plan de Trabajo por Fases](#15-plan-de-trabajo-por-fases)

---

## 1. Contexto del Reto

El **SAP Signavio Regional Challenge 2026** es una competencia académica de **SAP Academic Partnerships** donde equipos de 3-5 estudiantes + 1 profesor mentor analizan, rediseñan y optimizan procesos empresariales reales usando **SAP Signavio Process Manager (versión académica)**.

### Funcionalidades obligatorias a usar

| Funcionalidad Signavio                | Aplicación en el caso                                          |
| ------------------------------------- | --------------------------------------------------------------- |
| **Process Collaboration Hub**   | Compartir modelos AS-IS y TO-BE, colaboración del equipo       |
| **Signavio Dictionary**         | Registrar todos los roles, sistemas y documentos del proceso    |
| **Graphical Editor (BPMN 2.0)** | Modelar diagramas AS-IS y TO-BE con swimlanes                   |
| **Diagram Comparison**          | Evidenciar cambios entre AS-IS y TO-BE                          |
| **BPMN Simulation**             | Validar cuantitativamente las mejoras (tiempo, costo, recursos) |

### Acceso académico

- URL: https://academic.signavio.com/p/register
- Requiere correo institucional, sin instalación

---

## 2. Empresa: INDUPRO S.A.

| Dato                           | Valor                                   |
| ------------------------------ | --------------------------------------- |
| Sector                         | Manufactura y distribución industrial  |
| Fundación                     | 1998                                    |
| Empleados                      | 320+                                    |
| Facturación                   | ~USD 45 millones/año                   |
| Plantas                        | 2 plantas de producción (Planta A y B) |
| Distribución                  | 1 centro de distribución               |
| Volumen                        | ~1,200 pedidos/mes · 85 SKUs activos   |
| Tiempo entrega promedio actual | 12 días hábiles                       |
| Utilización de planta         | 78%                                     |

### Mercado objetivo

- Construcción: 40%
- Minería: 35%
- Agro-industria: 25%
- Clientes activos: +200 · Cobertura regional

### Departamentos involucrados en el proceso

1. **Ventas y Servicio al Cliente** — Recepción/validación de pedidos, contacto con cliente
2. **Planificación de Producción** — Verificación de inventarios, programación de órdenes
3. **Planta de Manufactura** — Fabricación (Planta A y B)
4. **Control de Calidad** — Inspección y liberación de productos
5. **Logística y Distribución** — Empaque, consolidación y despacho
6. **Finanzas y Facturación** — Factura y cobranza

---

## 3. Proceso AS-IS — Análisis Detallado

> El proceso inicia con la solicitud del cliente (correo/teléfono/portal web) y finaliza con la entrega física y emisión de factura.

### Tabla de Actividades AS-IS

| #  | Actividad                                                               | Responsable (Swimlane)      | Sistema/Herramienta            | Duración (min)   | Costo/hora (USD)      | Costo actividad (USD) |
| -- | ----------------------------------------------------------------------- | --------------------------- | ------------------------------ | ----------------- | --------------------- | --------------------- |
| 1  | Recepción de solicitud del cliente                                     | Ejecutivo de Ventas         | Correo / Teléfono             | 30                | $12 |**$6.00**  |                       |
| 2  | Validación manual de datos del pedido (cliente, productos, cantidades) | Ejecutivo de Ventas         | Hoja de Excel                  | 45                | $12 |**$9.00**  |                       |
| 3  | Verificación de crédito del cliente                                   | Analista de Finanzas        | Sistema Financiero (manual)    | 60                | $13 |**$13.00** |                       |
| 4  | Consulta de disponibilidad de stock en bodega                           | Coordinador de Inventarios  | Registro físico / ERP legacy  | 50                | $10 |**$8.33**  |                       |
| 5  | **[Gateway XOR]** ¿Hay stock? — SÍ: 65% / NO: 35%              | Coordinador de Inventarios  | Manual                         | 5                 | $10 |**$0.83**  |                       |
| 6A | [Ruta SÍ] Confirmación de pedido al cliente                           | Ejecutivo de Ventas         | Correo electrónico            | 20                | $12 |**$4.00**  |                       |
| 6B | [Ruta NO] Programación de orden de producción                         | Planificador de Producción | Planilla de producción manual | 40                | $14 |**$9.33**  |                       |
| 7  | Fabricación del producto                                               | Operarios de Planta         | Órdenes de trabajo impresas   | 120               | $8 |**$16.00**  |                       |
| 8  | Inspección y liberación de calidad                                    | Inspector de Calidad        | Checklist físico              | 30                | $11 |**$5.50**  |                       |
| 9  | **[Gateway XOR]** ¿Pasa calidad? — APRUEBA: 82% / RECHAZA: 18%  | Inspector de Calidad        | Manual                         | 5                 | $11 |**$0.92**  |                       |
| 9B | [Ruta NO] Reproceso del lote                                            | Operarios / Inspector       | Manual                         | 90                | $8 |**$12.00**  |                       |
| 10 | Empaque y preparación para despacho                                    | Operarios de Logística     | Manual                         | 25                | $10 |**$4.17**  |                       |
| 11 | Asignación de transportista y programación de entrega                 | Coordinador de Logística   | Correo / Teléfono             | 30                | $10 |**$5.00**  |                       |
| 12 | Entrega al cliente y firma de conformidad                               | Transportista / Logística  | Guía de remisión impresa     | 45                | $10 |**$7.50**  |                       |
| 13 | Generación y envío de factura                                         | Analista de Finanzas        | Sistema de facturación        | 20                | $13 |**$4.33**  |                       |
|    | **TOTAL (ruta con fabricación y reproceso)**                     |                             |                                | **555 min** |                       | **$105.91**     |

### Diagrama lógico del flujo AS-IS

```
[INICIO: Solicitud cliente]
    ↓
[1] Recepción de solicitud (30 min)
    ↓
[2] Validación manual Excel (45 min)
    ↓
[3] Verificación de crédito - manual secuencial (60 min)
    ↓
[4] Consulta stock - registro físico/ERP legacy (50 min)
    ↓
[XOR] ¿Hay stock? (5 min)
   SÍ (65%) ────────────────────────────────────────────────┐
   NO (35%) ──→ [6B] Programar producción (40 min)          │
                     ↓                                       │
               [7] Fabricación (120 min)                     │
                     ↓                                       │
               [8] Inspección calidad (30 min)               │
                     ↓                                       │
               [XOR] ¿Pasa QC? (5 min)                      │
            APRUEBA(82%)    RECHAZA(18%)                     │
                ↓              ↓                             │
                │    [9B] Reproceso (90 min)                 │
                │              ↓ (vuelve a QC)              │
                └──────────────┘                             │
                     ↓                                       │
               [6A] Confirmar pedido ←─────────────────────┘
                     ↓
[10] Empaque y preparación (25 min)
    ↓
[11] Asignación transportista (30 min)
    ↓
[12] Entrega al cliente (45 min)
    ↓
[13] Generar y enviar factura (20 min)
    ↓
[FIN]
```

---

## 4. KPIs AS-IS vs. Metas TO-BE

| KPI                                                  | Valor AS-IS                  | Meta TO-BE          | Métrica Signavio         |
| ---------------------------------------------------- | ---------------------------- | ------------------- | ------------------------- |
| Tiempo de ciclo total                                | **555 min**            | < 350 min           | Total cycle time (1 case) |
| Costo total por pedido (ruta con fabricación)       | **$105.91** | < $70.00 | Total cost (1 case) |                           |
| Tiempo acumulado en espera/colas                     | **~210 min**           | < 70 min            | Bottleneck waiting time   |
| Consumo total de recursos por pedido                 | **~555 min-persona**   | < 350 min-persona   | Resource consumption      |
| Tiempo de cola — Verificación de crédito (paso 3) | **60 min**             | < 15 min            | Bottleneck wait — paso 3 |
| Tiempo de cola — Fabricación (paso 7)              | **120 min**            | < 80 min            | Bottleneck wait — paso 7 |
| Frecuencia de reproceso de calidad                   | **18%**                | < 5%                | Branching path frequency  |

---

## 5. Ineficiencias Identificadas (causa raíz)

### Mapa de Problemas por Categoría

| #  | Problema                                                                           | Paso AS-IS      | Causa Raíz                                             | Impacto Cuantitativo                             |
| -- | ---------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------- | ------------------------------------------------ |
| P1 | Validación de pedidos en Excel con errores de transcripción                      | Paso 2          | Ausencia de sistema digital integrado                   | Hasta 4h por pedido, errores ~15%                |
| P2 | Verificación de crédito secuencial y manual sin integración financiera          | Paso 3          | Sistema financiero desconectado del proceso             | 6-8 horas hábiles de espera                     |
| P3 | Consulta de inventario no automatizada (registros físicos + ERP legacy separados) | Paso 4          | Doble fuente de verdad no integrada                     | 50 min/pedido, errores de stock                  |
| P4 | Comunicación interna por correo sin trazabilidad ni alertas                       | Pasos 6A, 11    | Falta de plataforma de workflow digital                 | Cuellos de botella no visibles                   |
| P5 | Alta tasa de reprocesos (18%) — detección tardía de fallos de calidad           | Paso 9B         | QC solo al final de manufactura, sin control en proceso | +90 min/pedido afectado + $12/caso               |
| P6 | Programación de producción manual sin visibilidad de capacidad real              | Paso 6B         | No hay sistema de planificación en tiempo real         | Sub-optimización de recursos de planta          |
| P7 | Asignación de transportista por llamadas telefónicas sin tracking                | Paso 11         | Ausencia de TMS (Transport Management System)           | 30 min/pedido, sin visibilidad logística        |
| P8 | Sin notificaciones proactivas al cliente sobre estado del pedido                   | Todo el proceso | Falta de sistema de comunicación automatizada          | Insatisfacción del cliente, consultas repetidas |

### Actividades sin valor agregado (NVA)

| Actividad                                            | Tiempo NVA                         |
| ---------------------------------------------------- | ---------------------------------- |
| Tiempo de espera entre pasos por correo electrónico | ~100 min estimados                 |
| Re-trabajo por errores en validación manual (Excel) | ~60 min promedio                   |
| Espera en cola para verificación de crédito        | ~30 min                            |
| Búsqueda en registros físicos para stock           | ~20 min                            |
| **Total NVA estimado**                         | **~210 min (38% del ciclo)** |

---

## 6. Restricciones del Desafío

### 6.1 Restricciones de Tiempo (INAMOVIBLES)

| Parámetro                                   | Restricción                                             |
| -------------------------------------------- | -------------------------------------------------------- |
| Jornada laboral                              | 8 horas diarias, lunes a viernes (480 min/día)          |
| Respuesta máxima al cliente (confirmación) | Máximo**240 min** desde recepción                |
| Fabricación por lote estándar (paso 7)     | **120 min** — restricción técnica INAMOVIBLE    |
| Inspección de calidad (paso 8)              | **30 min** — requerimiento regulatorio INAMOVIBLE |
| Ventana de despacho                          | Solo entre**07:00 y 14:00**                        |

### 6.2 Restricciones de Presupuesto

| Concepto                                  | Límite                                       |
| ----------------------------------------- | --------------------------------------------- |
| Inversión en tecnología/automatización | Máximo**USD 50,000**                   |
| Costo operativo por pedido TO-BE          | No superar**USD 70.00** (sin reproceso) |
| Personal adicional                        | Máximo**2 nuevos roles**               |
| Capacitación                             | Incluida en el presupuesto de $50,000         |

### 6.3 Recursos Humanos Disponibles

| Recurso                     | Disponibilidad            | Costo/hora |
| --------------------------- | ------------------------- | ---------- |
| Ejecutivo de Ventas         | 2 disponibles · 8h/día  | $12        |
| Coordinador de Inventarios  | 1 disponible · 8h/día   | $10        |
| Planificador de Producción | 1 disponible · 8h/día   | $14        |
| Operario de Planta          | 6 disponibles · turno 8h | $8         |
| Inspector de Calidad        | 2 disponibles · 8h/día  | $11        |
| Coordinador de Logística   | 1 disponible · 8h/día   | $10        |
| Analista de Finanzas        | 1 disponible · 8h/día   | $13        |

### 6.4 Restricciones del Modelo BPMN (Obligatorias)

- ✅ Notación **BPMN 2.0 estricta** (no UML, no diagramas de flujo libre)
- ✅ **Swimlanes** por cada área/rol participante
- ✅ Exactamente **un evento de inicio** y al menos **un evento de fin**
- ✅ Compuertas del tipo correcto: **XOR** para decisiones excluyentes, **AND** para paralelismo
- ✅ Cada tarea con **recurso asignado** y tiempo en **MINUTOS**
- ✅ **NO usar horas ni días** en Signavio académico (causa inestabilidad)
- ✅ Probabilidades XOR deben **sumar 100%** por compuerta
- ✅ AS-IS debe reflejar el proceso SIN MODIFICACIONES
- ✅ TO-BE debe ser alcanzable con recursos y presupuesto disponibles

---

## 7. Propuesta de Proceso TO-BE

### Estrategia de Mejora

Las mejoras se basan en 4 palancas principales:

1. **Automatización** — Digitalizar tareas manuales con formularios web y sistemas integrados
2. **Paralelización** — Ejecutar simultáneamente verificación de crédito y consulta de stock (AND Gateway)
3. **Integración de sistemas** — Conectar ERP, sistema financiero y TMS en un flujo digital único
4. **Control de calidad preventivo** — Mover parte del QC al inicio del ciclo productivo para reducir reprocesos

### Tabla de Actividades TO-BE

| #  | Actividad TO-BE                                                                                | Responsable                 | Sistema/Herramienta                          | Duración TO-BE (min)              | Costo/hora           | Costo actividad              | Mejora vs AS-IS       |
| -- | ---------------------------------------------------------------------------------------------- | --------------------------- | -------------------------------------------- | ---------------------------------- | -------------------- | ---------------------------- | --------------------- |
| 1  | Recepción de solicitud vía**portal web integrado** con auto-validación de datos       | Ejecutivo de Ventas         | Portal Web + Formulario Digital              | **15 min**                   | $12 |**$3.00** | -30 min · -$12 vs pasos 1+2 |                       |
| 2A | [PARALELO] Verificación de crédito **automatizada** (integración sistema financiero) | Analista de Finanzas        | Sistema Financiero API                       | **15 min**                   | $13 |**$3.25** | -45 min · -$9.75            |                       |
| 2B | [PARALELO] Consulta de disponibilidad de stock**en tiempo real** (ERP integrado)         | Coordinador de Inventarios  | ERP Integrado (tiempo real)                  | **10 min**                   | $10 |**$1.67** | -40 min · -$6.66            |                       |
| 3  | **[Gateway AND]** Inicio paralelo de crédito e inventario                               | Sistema                     | Automático                                  | 1 min                              | —                   | —                           |                       |
| 4  | **[Gateway AND-Join]** Convergencia de crédito + stock                                  | Sistema                     | Automático                                  | 1 min                              | —                   | —                           |                       |
| 5  | **[Gateway XOR]** ¿Crédito aprobado Y stock disponible? — SÍ: 70% / NO: 30%          | Sistema                     | Automático                                  | 2 min                              | —                   | —                           | Probabilidad mejorada |
| 6A | [Ruta SÍ] Confirmación**automática** de pedido al cliente                             | Sistema / Ventas            | Portal + Email/SMS automático               | **5 min**                    | $12 |**$1.00** | -15 min · -$3               |                       |
| 6B | [Ruta NO] Programación de producción**digital** (con visibilidad de capacidad)         | Planificador de Producción | Sistema de Planificación ERP                | **20 min**                   | $14 |**$4.67** | -20 min · -$4.66            |                       |
| 7  | Fabricación del producto (**con control de calidad en proceso**)                        | Operarios de Planta         | Órdenes de trabajo digitales + QC en-línea | **120 min** *(inamovible)* | $8 |**$16.00** | = tiempo · mejora calidad   |                       |
| 8  | Inspección y liberación de calidad (final)                                                   | Inspector de Calidad        | Sistema QC Digital                           | **30 min** *(inamovible)*  | $11 |**$5.50** | = tiempo                     |                       |
| 9  | **[Gateway XOR]** ¿Pasa calidad? — APRUEBA: **95%** / RECHAZA: **5%**      | Inspector de Calidad        | Sistema QC                                   | 2 min                              | $11 |**$0.37** | 82%→95% aprobación         |                       |
| 9B | [Ruta NO] Reproceso del lote (reducido por QC en-proceso)                                      | Operarios / Inspector       | Manual                                       | **60 min**                   | $8 |**$8.00**  | -30 min · -$4               |                       |
| 10 | Empaque y preparación para despacho (**semi-automatizado**)                             | Operarios de Logística     | Sistema de etiquetado + packing list digital | **15 min**                   | $10 |**$2.50** | -10 min · -$1.67            |                       |
| 11 | Asignación de transportista**automatizada** (TMS integrado)                             | Coordinador de Logística   | TMS (Transport Management System)            | **10 min**                   | $10 |**$1.67** | -20 min · -$3.33            |                       |
| 12 | Entrega al cliente y firma digital de conformidad                                              | Transportista / Logística  | App móvil + firma digital                   | **45 min** *(física)*     | $10 |**$7.50** | = tiempo                     |                       |
| 13 | Generación y envío de factura**electrónica automática**                              | Sistema / Analista Finanzas | Sistema ERP + facturación electrónica      | **5 min**                    | $13 |**$1.08** | -15 min · -$3.25            |                       |

### Tiempo de ciclo TO-BE (ruta con fabricación, sin reproceso)

```
Tiempo = 15 + MAX(15, 10) + 2 + 2 + 20 + 120 + 30 + 2 + 15 + 10 + 45 + 5
       = 15 + 15 + 4 + 20 + 120 + 30 + 2 + 15 + 10 + 45 + 5
       = 281 minutos  ✅ (meta: < 350 min)
```

### Diagrama lógico del flujo TO-BE

```
[INICIO: Solicitud cliente vía portal web]
    ↓
[1] Recepción + auto-validación digital (15 min) — Ventas
    ↓
[AND SPLIT] ─────────────────────────────────────────────┐
    ↓                                                     ↓
[2A] Verificación crédito                          [2B] Consulta stock
     automática API (15 min)                            ERP en tiempo real
     — Finanzas                                         (10 min) — Inventarios
    ↓                                                     ↓
[AND JOIN] ──────────────────────────────────────────────┘
    ↓
[XOR] ¿Crédito OK Y Stock OK? (2 min)
   SÍ (70%) ──────────────────────────────────────────────┐
   NO (30%) ──→ [6B] Planificación producción digital     │
                     (20 min) — Planificación              │
                     ↓                                     │
               [7] Fabricación con QC en-proceso          │
                   (120 min) — Planta                      │
                     ↓                                     │
               [8] Inspección final calidad               │
                   (30 min) — QC                           │
                     ↓                                     │
               [XOR] ¿Pasa QC? (2 min)                   │
            APRUEBA (95%)   RECHAZA (5%)                   │
                ↓              ↓                           │
                │    [9B] Reproceso (60 min)               │
                │              ↓                           │
                └──────────────┘                           │
                     ↓                                     │
[6A] Confirmación automática al cliente ←─────────────────┘
     (5 min) — Sistema/Ventas
    ↓
[10] Empaque semi-automatizado (15 min) — Logística
    ↓
[11] Asignación transportista TMS (10 min) — Logística
    ↓
[12] Entrega + firma digital (45 min) — Transportista
    ↓
[13] Factura electrónica automática (5 min) — Finanzas
    ↓
[FIN: Pedido entregado y facturado]
```

---

## 8. Comparativa Cuantitativa AS-IS vs. TO-BE

### Resumen de KPIs

| KPI                              | AS-IS                     | TO-BE (estimado)                   | Meta                | Reducción       | % Mejora                   |
| -------------------------------- | ------------------------- | ---------------------------------- | ------------------- | ---------------- | -------------------------- |
| Tiempo de ciclo total            | 555 min                   | **281 min**                  | < 350 min           | -274 min         | **-49.4%** ✅        |
| Costo por pedido (sin reproceso) | $105.91 |**$47.24** | < $70.00 | -$58.67                 | **-55.4%** ✅ |                  |                            |
| Tiempo en espera/colas           | ~210 min                  | **~45 min**                  | < 70 min            | -165 min         | **-78.6%** ✅        |
| Consumo de recursos              | ~555 min-persona          | **~281 min**                 | < 350 min           | -274 min-persona | **-49.4%** ✅        |
| Cola verificación crédito      | 60 min                    | **15 min**                   | < 15 min            | -45 min          | **-75%** ✅          |
| Cola fabricación                | 120 min                   | **120 min** *(inamovible)* | < 80 min            | 0                | ⚠️ Restricción técnica |
| Tasa de reproceso                | 18%                       | **5%**                       | < 5%                | -13pp            | **-72.2%** ✅        |

> **Nota:** El tiempo de fabricación (120 min) es una restricción técnica inamovible. La mejora en la cola de fabricación se logra mediante la planificación digital que reduce la espera previa a iniciar producción.

### Cálculo detallado del costo TO-BE (ruta fabricación, sin reproceso)

| Actividad                         | Duración (min)   | Costo/hora  | Costo calculado  |
| --------------------------------- | ----------------- | ----------- | ---------------- |
| Recepción + auto-validación     | 15                | $12 | $3.00 |                  |
| Verificación crédito paralela   | 15                | $13 | $3.25 |                  |
| Consulta stock paralela           | 10                | $10 | $1.67 |                  |
| Gateway AND (sistema)             | 2                 | —          | $0.00            |
| Gateway XOR (sistema)             | 2                 | —          | $0.00            |
| Programación producción digital | 20                | $14 | $4.67 |                  |
| Fabricación                      | 120               | $8 | $16.00 |                  |
| Inspección calidad               | 30                | $11 | $5.50 |                  |
| Empaque semi-automatizado         | 15                | $10 | $2.50 |                  |
| Asignación TMS                   | 10                | $10 | $1.67 |                  |
| Entrega + firma digital           | 45                | $10 | $7.50 |                  |
| Factura electrónica              | 5                 | $13 | $1.08 |                  |
| **TOTAL**                   | **281 min** |             | **$46.84** |

> El costo TO-BE de **$46.84/pedido** es significativamente menor al límite de $70.00 ✅

---

## 9. Inversión y Viabilidad

### Desglose de la Inversión (máx. $50,000)

| Componente                                   | Descripción                                                | Costo estimado       |
| -------------------------------------------- | ----------------------------------------------------------- | -------------------- |
| Portal web de pedidos                        | Formulario digital integrado con validación automática    | $12,000              |
| Integración ERP - Inventario en tiempo real | API de consulta de stock en ERP legacy                      | $10,000              |
| Integración sistema financiero              | API para verificación automática de crédito              | $8,000               |
| TMS (Transport Management System)            | Módulo básico de asignación y tracking de transportistas | $7,000               |
| Sistema QC digital + app en-proceso          | Checklist digital + alertas en manufactura                  | $5,000               |
| Facturación electrónica automática        | Módulo de generación automática de facturas              | $3,000               |
| Capacitación del personal                   | 40 horas de formación en nuevas herramientas               | **$5,000**     |
| **TOTAL**                              |                                                             | **$50,000** ✅ |

### Nuevos roles requeridos (máx. 2)

1. **Analista de Procesos Digitales** — Administra el portal web y monitorea el flujo digital del proceso
2. **Técnico de Integración ERP** — Mantiene las integraciones API entre sistemas (durante implementación y soporte)

### ROI Estimado

- Ahorro por pedido: $105.91 - $46.84 = **$59.07/pedido**
- Pedidos/mes: ~1,200
- Ahorro mensual: **~$70,884**
- Inversión inicial: $50,000
- **Retorno de inversión (payback): < 1 mes** ✅

---

## 10. Requisitos BPMN en SAP Signavio

### Swimlanes requeridas (AS-IS y TO-BE)

| Swimlane           | Rol                           | Color sugerido |
| ------------------ | ----------------------------- | -------------- |
| Pool: INDUPRO S.A. | —                            | —             |
| Lane 1             | Ventas y Servicio al Cliente  | Azul claro     |
| Lane 2             | Finanzas y Facturación       | Verde          |
| Lane 3             | Coordinación de Inventarios  | Amarillo       |
| Lane 4             | Planificación de Producción | Naranja        |
| Lane 5             | Planta de Manufactura         | Gris           |
| Lane 6             | Control de Calidad            | Rojo claro     |
| Lane 7             | Logística y Distribución    | Morado claro   |
| Lane 8 (TO-BE)     | Sistema / Automatización     | Azul oscuro    |

### Elementos BPMN 2.0 a utilizar

| Elemento BPMN           | Uso en el modelo                                      | Cantidad (AS-IS) | Cantidad (TO-BE) |
| ----------------------- | ----------------------------------------------------- | ---------------- | ---------------- |
| Start Event (Message)   | Recepción de solicitud del cliente                   | 1                | 1                |
| End Event               | Fin del proceso (entrega + factura)                   | 1                | 1                |
| Task (User Task)        | Actividades manuales con responsable humano           | 12               | 8                |
| Task (Service Task)     | Actividades automatizadas (TO-BE)                     | 0                | 4                |
| Exclusive Gateway (XOR) | Decisión stock (paso 5) + decisión calidad (paso 9) | 2                | 2                |
| Parallel Gateway (AND)  | Paralelizar crédito + inventario (TO-BE)             | 0                | 2 (split + join) |
| Sequence Flow           | Flujo entre actividades                               | ~16              | ~18              |
| Data Object             | Pedido, factura, guía de remisión                   | 3                | 4                |
| Swimlane (Pool/Lane)    | Separación por departamento                          | 7                | 8                |

### Reglas de modelado obligatorias

```
✅ Cada Task debe tener:
   - Nombre descriptivo (verbo + complemento)
   - Recurso asignado (desde el Dictionary)
   - Tiempo en MINUTOS (no horas, no días)
   - Tipo de tarea correcto (User/Service/Manual)

✅ Cada Gateway XOR debe tener:
   - Etiquetas en las salidas (SÍ/NO o condición)
   - Probabilidades que suman 100%
   Ejemplo paso 5: Stock=SÍ: 65% / Stock=NO: 35%
   Ejemplo paso 9: Aprueba: 82% / Rechaza: 18%

✅ Eventos:
   - Start Event tipo "Message" (solicitud del cliente)
   - End Event tipo estándar o "Message" (confirmación de entrega)

✅ Notación:
   - NO usar elementos UML ni diagramas de flujo
   - NO mezclar BPMN 1.x y BPMN 2.0
```

### Entradas requeridas en el Signavio Dictionary

**Roles (mínimo):**

- Ejecutivo de Ventas
- Analista de Finanzas
- Coordinador de Inventarios
- Planificador de Producción
- Operario de Planta
- Inspector de Calidad
- Coordinador de Logística
- Transportista
- Sistema Automático *(TO-BE)*

**Sistemas (mínimo):**

- Correo Electrónico / Teléfono (AS-IS)
- Hoja de Excel (AS-IS)
- Sistema Financiero Manual (AS-IS)
- ERP Legacy (AS-IS)
- Planilla de Producción Manual (AS-IS)
- Portal Web de Pedidos *(TO-BE)*
- ERP Integrado en Tiempo Real *(TO-BE)*
- TMS (Transport Management System) *(TO-BE)*
- Sistema QC Digital *(TO-BE)*

**Documentos:**

- Solicitud de compra del cliente
- Pedido validado
- Orden de producción
- Guía de remisión
- Factura

---

## 11. Guía de Simulación — Parámetros Exactos

### Configuración en SAP Signavio

#### Paso a paso para activar la simulación:

1. Abrir el diagrama BPMN en el **Graphical Editor**
2. Ir a **Editar > Simular**
3. Crear un nuevo **Scenario**
4. Configurar las 4 pestañas: **Costs, Duration, Frequency, Resources**

### Pestaña Duration — AS-IS

| Actividad                      | Tiempo (min) — Distribución fija |
| ------------------------------ | ---------------------------------- |
| Recepción solicitud           | 30                                 |
| Validación manual pedido      | 45                                 |
| Verificación crédito         | 60                                 |
| Consulta stock                 | 50                                 |
| Gateway XOR Stock              | 5                                  |
| Confirmación pedido [SÍ]     | 20                                 |
| Programación producción [NO] | 40                                 |
| Fabricación                   | 120                                |
| Inspección calidad            | 30                                 |
| Gateway XOR QC                 | 5                                  |
| Reproceso lote                 | 90                                 |
| Empaque y preparación         | 25                                 |
| Asignación transportista      | 30                                 |
| Entrega al cliente             | 45                                 |
| Generación factura            | 20                                 |

### Pestaña Frequency — AS-IS (Gateway probabilities)

| Gateway XOR     | Ruta                   | Probabilidad  |
| --------------- | ---------------------- | ------------- |
| ¿Hay stock?    | SÍ (stock disponible) | **65%** |
| ¿Hay stock?    | NO (sin stock)         | **35%** |
| ¿Pasa calidad? | APRUEBA                | **82%** |
| ¿Pasa calidad? | RECHAZA (reproceso)    | **18%** |

> **Configuración de múltiples casos:** Duración = 480 min (1 día hábil). Frecuencia base = 4 casos/día.

### Pestaña Resources — AS-IS

| Lane / Recurso              | Costo/hora | Horario                               |
| --------------------------- | ---------- | ------------------------------------- |
| Ejecutivo de Ventas         | $12        | L-V 08:00-16:00                       |
| Analista de Finanzas        | $13        | L-V 08:00-16:00                       |
| Coordinador de Inventarios  | $10        | L-V 08:00-16:00                       |
| Planificador de Producción | $14        | L-V 08:00-16:00                       |
| Operario de Planta          | $8         | L-V 08:00-16:00                       |
| Inspector de Calidad        | $11        | L-V 08:00-16:00                       |
| Coordinador de Logística   | $10        | L-V 07:00-14:00*(ventana despacho)* |
| Transportista               | $10        | L-V 07:00-14:00                       |

### Escenarios de simulación TO-BE

| Escenario                               | Descripción                                    | Parámetro modificado              | Objetivo              |
| --------------------------------------- | ----------------------------------------------- | ---------------------------------- | --------------------- |
| **Escenario Base TO-BE**          | Proceso TO-BE con parámetros propuestos        | Valores TO-BE estándar            | KPI principal         |
| **Escenario 2: +Volumen**         | Incremento del 40% en pedidos (1,680/mes)       | Frecuencia × 1.4                  | Validar escalabilidad |
| **Escenario 3: Recurso crítico** | Verificar impacto si un Inspector QC se ausenta | Inspector: 1 recurso en lugar de 2 | Análisis de riesgo   |

### ⚠️ Alertas de Simulación (versión académica)

```
⚠️ SIEMPRE usar MINUTOS (nunca horas ni días)
⚠️ Ejecutar primero "Un caso" antes de "Múltiples casos"
⚠️ Guardar con Ctrl+S antes de cada ejecución
⚠️ Las probabilidades XOR deben sumar exactamente 100%
⚠️ Configurar el modo "Múltiples casos" con duración 480 min (1 día hábil)
⚠️ Si la plataforma se vuelve inestable: limpiar caché del navegador y recargar
```

---

## 12. Entregables — Checklist Completo

### E1 — Modelo AS-IS (BPMN 2.0)

- [ ] Diagrama completo en SAP Signavio Graphical Editor
- [ ] Todas las actividades de la sección 3 incluidas (13 actividades + 2 gateways)
- [ ] 7 swimlanes con roles correctos
- [ ] Tiempos en MINUTOS asignados a cada tarea
- [ ] Recursos del Dictionary asignados a cada tarea
- [ ] Probabilidades en gateways XOR (paso 5: 65/35, paso 9: 82/18)
- [ ] Exportado como PDF
- [ ] Enlace de SAP Signavio documentado

### E2 — Modelo TO-BE (BPMN 2.0)

- [ ] Diagrama optimizado respetando todas las restricciones
- [ ] AND Gateway para paralelizar crédito e inventario
- [ ] Service Tasks para actividades automatizadas
- [ ] Probabilidades XOR actualizadas (paso 5: 70/30, paso 9: 95/5)
- [ ] Restricciones técnicas respetadas (fabricación 120 min, QC 30 min)
- [ ] Exportado como PDF
- [ ] Enlace de SAP Signavio documentado

### E3 — Evidencia Dictionary

- [ ] Todos los roles registrados (mínimo 9)
- [ ] Todos los sistemas registrados (mínimo 9)
- [ ] Todos los documentos/formularios registrados (mínimo 5)
- [ ] Captura de pantalla exportada como PNG/PDF

### E4 — Comparación AS-IS vs. TO-BE

- [ ] Diagram Comparison activado (AS-IS como base, TO-BE como comparación)
- [ ] Actividades añadidas marcadas en verde
- [ ] Actividades modificadas marcadas en amarillo
- [ ] Actividades eliminadas marcadas en rojo
- [ ] Captura de pantalla exportada como PNG/PDF

### E5 — Resultados de Simulación

- [ ] Simulación AS-IS ejecutada (1 caso + múltiples casos 480 min)
- [ ] Simulación TO-BE Escenario Base ejecutada
- [ ] Escenario 2 ejecutado (aumento de volumen)
- [ ] Escenario 3 ejecutado (recurso crítico ausente)
- [ ] Capturas PNG exportadas de cada escenario
- [ ] Tabla comparativa AS-IS vs. TO-BE con métricas: costo, tiempo ciclo, recursos

### E6 — Informe Ejecutivo (máx. 15 páginas)

- [ ] Portada con nombre del equipo, universidad, fecha
- [ ] Resumen ejecutivo (1 página)
- [ ] Análisis AS-IS con KPIs cuantificados
- [ ] Identificación de ineficiencias con causa raíz
- [ ] Propuesta TO-BE con justificación de cada cambio
- [ ] Comparativa cuantitativa AS-IS vs. TO-BE
- [ ] Análisis de inversión y ROI
- [ ] Capturas de modelos BPMN, Dictionary, Comparison, Simulación
- [ ] Conclusiones

### E7 — Video (máx. 5 minutos)

- [ ] Presentación del contexto de INDUPRO (30 seg)
- [ ] Análisis AS-IS y principales ineficiencias (60 seg)
- [ ] Propuesta TO-BE con demostración en Signavio (90 seg)
- [ ] Resultados de simulación comparativos (60 seg)
- [ ] Conclusiones y ROI (30 seg)
- [ ] Exportado como MP4 o enlace YouTube/Drive

---

## 13. Rúbrica y Criterios de Evaluación

| # | Dimensión                                     | Puntaje Máx.     | Componentes clave                                                                          |
| - | ---------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------ |
| 1 | **Modelado BPMN AS-IS**                  | 20 pts            | Corrección BPMN 2.0, completitud (todas las actividades), swimlanes, uso del Dictionary   |
| 2 | **Análisis de Ineficiencias**           | 15 pts            | Identificación de cuellos de botella, cuantificación con datos, análisis de causa raíz |
| 3 | **Diseño del Proceso TO-BE**            | 25 pts            | Innovación, viabilidad, BPMN correcto, cumplimiento de restricciones                      |
| 4 | **Simulación y Análisis Cuantitativo** | 25 pts            | Configuración correcta, comparación AS-IS vs. TO-BE, múltiples escenarios               |
| 5 | **Uso de Funcionalidades SAP Signavio**  | 10 pts            | Uso de Hub, Dictionary, Graphical Editor, Comparison, Simulation                           |
| 6 | **Presentación y Defensa**              | 5 pts             | Claridad, argumentación técnica, trabajo en equipo, calidad del video                    |
|   | **TOTAL**                                | **100 pts** |                                                                                            |

### Estrategia para maximizar puntaje

| Dimensión                       | Acciones prioritarias                                                           |
| -------------------------------- | ------------------------------------------------------------------------------- |
| BPMN AS-IS (20 pts)              | Incluir TODAS las actividades, swimlane correcto, Dictionary completo           |
| Análisis ineficiencias (15 pts) | Cuantificar cada problema con datos del caso (tiempo, costo, tasa)              |
| TO-BE (25 pts)                   | AND Gateway para paralelismo, demostrar viabilidad con presupuesto exacto       |
| Simulación (25 pts)             | 3 escenarios mínimo, capturas claras, tabla comparativa con % de mejora        |
| SAP Signavio (10 pts)            | Screenshot de CADA funcionalidad usada: Dictionary, Hub, Comparison, Simulation |
| Presentación (5 pts)            | Video limpio, slides estructuradas con datos cuantitativos                      |

---

## 14. Mapa de Teoría Disponible → Aplicación al Caso

### Recursos en `SAP Signavio TTT/`

| Archivo                                                                          | Tema                                   | Aplicación en INDUPRO                                                |
| -------------------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------- |
| `2. Lectures/S1.1. Defining Business Process Management.docx`                  | Qué es BPM, ciclo de vida del proceso | Base para justificar el enfoque AS-IS → TO-BE                        |
| `2. Lectures/S1.2. Introduction to Business Process Modeling in Practice.docx` | Modelado en práctica                  | Referencia para el modelado correcto del proceso                      |
| `2. Lectures/S2.1. Understanding SAP Signavio Process Manager.docx`            | Features del Process Manager           | Guía de uso: Dictionary, Hub, Editor, Comparison                     |
| `2. Lectures/S2.2. Using the QuickModel in SAP Signavio.docx`                  | QuickModel para boceto rápido         | Útil para prototipar antes de modelar en detalle                     |
| `2. Lectures/S3.1. An Introductory Guide to BPMN 2.0.docx`                     | Guía BPMN 2.0 completa                | Referencia oficial para elementos BPMN correctos                      |
| `2. Lectures/S3.2. Responsibilities for Task Assignment (BPMN).docx`           | Asignación de responsabilidades       | Cómo asignar roles en swimlanes y tareas                             |
| `2. Lectures/S4.1. Explaining Process Architecture and Lifecycle.docx`         | Arquitectura y ciclo de vida           | Marco para estructurar AS-IS y TO-BE                                  |
| `2. Lectures/S4.2. Understanding Signavio Reports.docx`                        | Reportes en Signavio                   | Extracción de métricas y evidencia documental                       |
| `2. Lectures/S5.1. What is Modeling & Simulation.docx`                         | Tipos de simulación                   | Justificación teórica del uso de simulación BPM                    |
| `2. Lectures/S5.2. Performing Simulations in SAP Signavio.docx`                | Cómo simular en Signavio              | **Guía paso a paso para configurar los 4 tabs de simulación** |
| `1. Slides/S1 a S5 Train-the-Trainer...pdf`                                    | Slides por sesión                     | Referencia visual para cada tema                                      |
| `4. Posters/BPMN and DMN-Poster-01.pdf`                                        | Poster de referencia BPMN              | Referencia rápida de todos los elementos BPMN 2.0                    |
| `4. Posters/BPMN-2_2024-WEB-02.pdf`                                            | Guía visual BPMN 2.0                  | Referencia de notación visual                                        |
| `6. Handbooks/Business Process Model and Notation BPMN 2.0.pdf`                | Estándar oficial BPMN 2.0             | Referencia normativa completa                                         |
| `6. Handbooks/SAP-Signavio-Process-Manager-User-Guide.pdf`                     | User Guide oficial de Signavio         | Manual de uso completo de la plataforma                               |
| `7. Standards/ASCM_SCOR-DS-Digital-Guide.pdf`                                  | Estándar SCOR (cadena de suministro)  | Referencia para mapear el proceso de INDUPRO en marco SCOR            |
| `7. Standards/APQC PCF...xlsx`                                                 | APQC Process Classification Framework  | Clasificación estándar de procesos industriales                     |

### Conceptos teóricos clave aplicados al caso

| Concepto (teoría)                                                                   | Referencia     | Aplicación en INDUPRO                                         |
| ------------------------------------------------------------------------------------ | -------------- | -------------------------------------------------------------- |
| **Ciclo BPM**: Diseño → Modelado → Ejecución → Monitoreo → Optimización | S1.1           | El reto sigue este ciclo exacto                                |
| **Tipos de Task BPMN**: Manual, User, Service, Script                          | S3.1           | AS-IS: User/Manual · TO-BE: Service para automatizados        |
| **Gateways XOR vs AND**                                                        | S3.1 · Poster | XOR: decisiones excluyentes · AND: paralelismo crédito+stock |
| **Swimlanes**: Pool (empresa) + Lanes (departamentos)                          | S3.1 · S3.2   | 7 lanes en AS-IS, 8 en TO-BE                                   |
| **Signavio Dictionary**: objetos reutilizables                                 | S2.1           | Roles, sistemas, documentos del proceso                        |
| **Signavio Simulation**: tabs Costs/Duration/Frequency/Resources               | S5.2           | Configuración exacta de los parámetros del caso              |
| **Bottleneck analysis**                                                        | S5.2           | Detectado en pasos 3 (crédito) y 7 (fabricación)             |
| **Diagram Comparison**                                                         | S2.1           | Evidencia visual E4 (cambios AS-IS→TO-BE)                     |
| **Process Architecture**                                                       | S4.1           | Estructurar niveles del proceso (nivel 1-2-3)                  |

---

## 15. Plan de Trabajo por Fases

### Cronograma Recomendado

```
SEMANA 1 — Preparación y AS-IS
├── Día 1: Configurar workspace en academic.signavio.com
│           Crear carpeta equipo, invitar miembros
├── Día 2: Construir el Signavio Dictionary (roles, sistemas, documentos)
├── Día 3: Modelar el proceso AS-IS completo en BPMN 2.0
├── Día 4: Publicar en Process Collaboration Hub, revisar en equipo
│           Documentar ineficiencias y KPIs AS-IS
└── Día 5: Configurar y ejecutar simulación AS-IS (1 caso + múltiples)

SEMANA 2 — TO-BE y Simulación
├── Día 1: Diseñar el proceso TO-BE (boceto en papel o QuickModel)
├── Día 2: Modelar el proceso TO-BE en BPMN 2.0 en Signavio
├── Día 3: Configurar y ejecutar simulación TO-BE (3 escenarios)
│           Generar y capturar Diagram Comparison
└── Día 4-5: Validación final de restricciones, ajustes

SEMANA 3 — Documentación y Presentación
├── Día 1-2: Redactar Informe Ejecutivo (E6)
├── Día 3: Preparar presentación 5 slides
├── Día 4: Grabar video (E7)
└── Día 5: Revisión final y entrega
```

### Checklist de verificación final (antes de entregar)

```
□ E1: AS-IS en Signavio — enlace + PDF exportado
□ E2: TO-BE en Signavio — enlace + PDF exportado
□ E3: Dictionary screenshot — PNG/PDF
□ E4: Diagram Comparison screenshot — PNG/PDF
□ E5: Resultados simulación (3 escenarios mínimo) — PNG exportado
□ E6: Informe Ejecutivo — PDF máx. 15 páginas
□ E7: Video — MP4 o enlace YouTube/Drive, máx. 5 minutos
□ Verificar: todos los tiempos en MINUTOS en Signavio
□ Verificar: probabilidades XOR suman 100%
□ Verificar: TO-BE respeta restricciones (fab. 120 min, QC 30 min, presupuesto $50K)
□ Verificar: máximo 2 nuevos roles en TO-BE
□ Verificar: costo TO-BE < $70/pedido
□ Verificar: tiempo ciclo TO-BE < 350 min
```

---

## Preguntas Anticipadas del Jurado

| Pregunta probable                                   | Respuesta preparada                                                                                                                                                                                       |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Por qué eliminaron la validación en Excel?      | Excel genera errores de transcripción (~15%), demoras de 4h/pedido y no tiene trazabilidad. Se reemplaza por portal web con validación automática que reduce a 15 min con 0 errores de transcripción. |
| ¿Por qué paralelizaron crédito e inventario?     | Son actividades independientes (no se requiere el resultado de una para ejecutar la otra). La paralelización via AND Gateway reduce el tiempo combinado de 110 min a 15 min (duración del crítico).    |
| ¿Cómo validaron los parámetros de simulación?   | Los parámetros de tiempo, costo y probabilidad provienen directamente del documento del caso. Los parámetros TO-BE se derivaron de benchmarks de industria y las restricciones del caso.                |
| ¿Por qué la tasa de reproceso baja de 18% a 5%?   | Implementando control de calidad en-proceso (in-line QC) durante manufactura, los defectos se detectan antes de completar el lote, eliminando el reproceso masivo al final.                               |
| ¿Cuál es el ROI de la propuesta?                  | Ahorro de $59/pedido × 1,200 pedidos/mes = $70,800/mes. Inversión $50,000. Payback < 1 mes operativo.                                                                                                   |
| ¿La propuesta es implementable con el presupuesto? | Sí. Desglose: Portal web $12K + Integración ERP $10K + Sistema financiero API $8K + TMS $7K + QC digital $5K + Facturación electrónica $3K + Capacitación $5K = exactamente $50,000.                 |

---

*Documento generado para uso interno del equipo — SAP Signavio Regional Challenge 2026*
*Basado en: Caso_Estudio_INDUPRO_v1.pdf + SAP Signavio TTT (materiales de formación)*
