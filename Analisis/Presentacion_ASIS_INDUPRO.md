# Presentación — Análisis AS-IS: INDUPRO S.A.
## SAP Signavio Regional Challenge 2026

---

# PARTE I — MODELADO AS-IS

---

## Slide 1 — Portada

**INDUPRO S.A.**
*Análisis y Modelado del Proceso de Gestión de Pedidos*

> SAP Signavio Regional Challenge 2026
> Modelado AS-IS · Identificación de Ineficiencias · Análisis Cuantitativo

---

## Slide 2 — ¿Qué es el modelado AS-IS y por qué importa?

El modelado **AS-IS** (*como está*) representa el proceso tal y como ocurre en la realidad — sin idealización ni mejoras.

### Su función analítica es triple:

| Propósito | Descripción |
|-----------|-------------|
| **Diagnóstico** | Expone cuellos de botella, actividades sin valor y flujos rotos |
| **Línea base cuantitativa** | Establece métricas medibles: tiempo, costo, frecuencia de fallo |
| **Fundamento del cambio** | Toda propuesta TO-BE debe justificarse contra el AS-IS |

> El AS-IS no describe el problema — lo **demuestra con datos**.

---

## Slide 3 — Empresa: INDUPRO S.A.

| Atributo | Valor |
|----------|-------|
| Sector | Manufactura y distribución industrial |
| Empleados | 320+ |
| Facturación anual | ~USD 45 millones |
| Plantas | 2 plantas de producción |
| Volumen operativo | ~1,200 pedidos/mes · 85 SKUs activos |

### Mercado objetivo

```
Construcción     ████████████████  40%
Minería         ██████████████    35%
Agroindustria   ██████████        25%
```

> El proceso que analizamos mueve el 100% de la operación comercial de la empresa.

---

## Slide 4 — Alcance del proceso modelado

**Proceso:** Gestión integral del pedido del cliente

| Punto de inicio | Punto de fin |
|-----------------|--------------|
| Solicitud del cliente (correo / teléfono / portal web) | Entrega física + emisión de factura |

### Áreas participantes — Swimlanes del modelo

| Swimlane | Rol representado |
|----------|-----------------|
| Lane 1 | Ventas y Servicio al Cliente |
| Lane 2 | Finanzas y Facturación |
| Lane 3 | Coordinación de Inventarios |
| Lane 4 | Planificación de Producción |
| Lane 5 | Planta de Manufactura |
| Lane 6 | Control de Calidad |
| Lane 7 | Logística y Distribución |

> Cada swimlane representa una **frontera de responsabilidad** — cruzarla implica una transferencia que puede convertirse en cuello de botella.

---

## Slide 5 — Estructura del modelo BPMN AS-IS

### Inventario de elementos del diagrama

| Elemento BPMN | Función | Cantidad |
|---------------|---------|----------|
| Start Event (Message) | Recepción de solicitud | 1 |
| End Event | Cierre del pedido | 1 |
| User Task | Actividades manuales con responsable | 12 |
| Exclusive Gateway (XOR) | Decisiones de bifurcación | 2 |
| Sequence Flow | Conexiones entre actividades | ~16 |
| Data Object | Pedido, orden de producción, factura | 3 |

### Los 2 gateways XOR son el corazón analítico del AS-IS

```
XOR #1 — ¿Hay stock disponible?
    SÍ: 65%  →  Ruta corta (solo logística)
    NO: 35%  →  Ruta larga (fabricación completa)

XOR #2 — ¿El lote aprueba el control de calidad?
    APRUEBA: 82%  →  Avanza al despacho
    RECHAZA: 18%  →  Reproceso (+90 min, +$12/caso)
```

> Las probabilidades de los gateways son datos reales de INDUPRO — no estimaciones.

---

## Slide 6 — Tabla de actividades AS-IS

### Flujo completo con métricas por actividad

| # | Actividad | Responsable | Herramienta | Duración (min) | Costo (USD) |
|---|-----------|-------------|-------------|----------------|-------------|
| 1 | Recepción de solicitud del cliente | Ejecutivo de Ventas | Correo / Teléfono | 30 | $6.00 |
| 2 | Validación manual de datos (cliente, productos, cantidades) | Ejecutivo de Ventas | **Hoja de Excel** | 45 | $9.00 |
| 3 | Verificación de crédito del cliente | Analista de Finanzas | Sistema financiero manual | 60 | $13.00 |
| 4 | Consulta de disponibilidad de stock | Coordinador de Inventarios | Registro físico / ERP legacy | 50 | $8.33 |
| 5 | **[XOR]** ¿Hay stock? | Coordinador de Inventarios | Manual | 5 | $0.83 |
| 6A | Confirmación de pedido al cliente | Ejecutivo de Ventas | Correo electrónico | 20 | $4.00 |
| 6B | Programación de orden de producción | Planificador | Planilla manual | 40 | $9.33 |
| 7 | Fabricación del producto | Operarios de Planta | Órdenes impresas | 120 | $16.00 |
| 8 | Inspección y liberación de calidad | Inspector de Calidad | Checklist físico | 30 | $5.50 |
| 9 | **[XOR]** ¿Pasa calidad? | Inspector de Calidad | Manual | 5 | $0.92 |
| 9B | Reproceso del lote (ruta rechazada) | Operarios / Inspector | Manual | 90 | $12.00 |
| 10 | Empaque y preparación para despacho | Logística | Manual | 25 | $4.17 |
| 11 | Asignación de transportista | Coordinador de Logística | Correo / Teléfono | 30 | $5.00 |
| 12 | Entrega al cliente y firma de conformidad | Transportista | Guía de remisión impresa | 45 | $7.50 |
| 13 | Generación y envío de factura | Analista de Finanzas | Sistema de facturación | 20 | $4.33 |

**TOTAL (ruta con fabricación + reproceso): 555 min · $105.91**

---

## Slide 7 — Flujo lógico AS-IS (vista analítica)

```
[INICIO] Solicitud del cliente
         │
         ▼
[1] Recepción (30 min) ──── VENTAS
         │
         ▼
[2] Validación Excel (45 min) ──── VENTAS  ← PROBLEMA: propenso a errores
         │
         ▼
[3] Verificación de crédito (60 min) ──── FINANZAS  ← CUELLO DE BOTELLA
         │
         ▼
[4] Consulta de stock (50 min) ──── INVENTARIOS  ← doble fuente de verdad
         │
         ▼
       [XOR] ¿Hay stock?
        /              \
    SÍ (65%)         NO (35%)
       │                │
       │         [6B] Prog. producción (40 min)
       │                │
       │         [7] Fabricación (120 min) ← RESTRICCIÓN TÉCNICA
       │                │
       │         [8] Inspección QC (30 min)
       │                │
       │              [XOR] ¿Pasa QC?
       │               /           \
       │         Sí (82%)       No (18%) ──→ [9B] Reproceso (90 min)
       │               \           /
       │                ▼         ▼ (vuelve a QC)
       │
[6A] Confirmación al cliente ◄────────────────┘
         │
         ▼
[10] Empaque (25 min) ──── LOGÍSTICA
         │
[11] Asignación transportista (30 min) ──── LOGÍSTICA  ← sin visibilidad
         │
[12] Entrega + firma (45 min) ──── TRANSPORTISTA
         │
[13] Factura (20 min) ──── FINANZAS
         │
       [FIN]
```

---

## Slide 8 — KPIs de la línea base AS-IS

### Lo que los datos muestran

| KPI | Valor AS-IS | Interpretación |
|-----|-------------|----------------|
| **Tiempo de ciclo total** | **555 min** | 9.25 horas hábiles — casi 2 jornadas completas |
| **Costo total por pedido** | **$105.91** | Incluye ruta con fabricación y reproceso |
| **Tiempo en espera / sin valor** | **~210 min** | El 38% del ciclo no agrega valor al cliente |
| **Cola — verificación de crédito** | **60 min** | Proceso bloqueado esperando aprobación financiera |
| **Cola — fabricación** | **120 min** | Restricción técnica; el proceso espera la planta |
| **Frecuencia de reproceso QC** | **18% de los lotes** | 1 de cada 5.5 lotes vuelve a producción |
| **Utilización de planta** | **78%** | Existe capacidad ociosa, pero mal planificada |

> **El indicador más revelador:** de 555 minutos totales, solo ~345 son trabajo activo. Los 210 restantes son esperas, traslados o rework.

---

## Slide 9 — Análisis de tiempo sin valor agregado (NVA)

### Descomposición de los 555 minutos del proceso

```
Tiempo con valor agregado (VA)
████████████████████████████████████  ~345 min (62%)

Tiempo sin valor agregado (NVA)
█████████████████████  ~210 min (38%)
```

### Detalle del tiempo NVA por categoría

| Categoría de NVA | Tiempo estimado | Causa |
|-----------------|-----------------|-------|
| Esperas entre pasos (correo / llamada) | ~100 min | Comunicación no integrada |
| Re-trabajo por errores en validación Excel | ~60 min | Entrada manual de datos |
| Espera en cola para crédito (paso 3) | ~30 min | Proceso secuencial sin automatización |
| Búsqueda en registros físicos para stock | ~20 min | Doble fuente de verdad |
| **Total NVA** | **~210 min** | **38% del tiempo de ciclo** |

> Un proceso eficiente tiene NVA < 15%. INDUPRO está en 38% — margen de mejora crítico.

---

## Slide 10 — Mapa de ineficiencias identificadas

### Diagnóstico por causa raíz

| # | Problema | Paso AS-IS | Causa Raíz | Impacto Cuantitativo |
|---|----------|------------|------------|---------------------|
| P1 | Validación de pedidos en Excel | Paso 2 | Sin sistema digital integrado | Errores ~15% · hasta 4h extra/pedido |
| P2 | Verificación de crédito secuencial | Paso 3 | Sistema financiero desconectado | 6-8h hábiles de espera |
| P3 | Consulta de inventario no automatizada | Paso 4 | Doble fuente de verdad (físico + ERP legacy) | 50 min/pedido + errores de stock |
| P4 | Comunicación interna por correo | Pasos 6A, 11 | Sin plataforma de workflow | Cuellos de botella no visibles |
| P5 | Alta tasa de reprocesos (18%) | Paso 9B | QC solo al final de manufactura | +90 min + $12/caso afectado |
| P6 | Planificación de producción manual | Paso 6B | Sin visibilidad de capacidad en tiempo real | Subutilización del 22% de planta |
| P7 | Asignación de transporte por teléfono | Paso 11 | Sin TMS | 30 min + sin trazabilidad logística |
| P8 | Sin notificaciones al cliente | Todo el proceso | Sin automatización de comunicación | Insatisfacción + consultas repetidas |

---

## Slide 11 — Los 3 cuellos de botella críticos

### Análisis de bottlenecks por impacto en el ciclo

---

### Cuello de botella #1 — Verificación de crédito (Paso 3)

**Tiempo:** 60 minutos · **Categoría:** Espera pura

El proceso completo se **detiene** mientras el Analista de Finanzas revisa manualmente el historial de crédito del cliente. Este paso no puede iniciarse hasta que los pasos 1 y 2 terminen — es estrictamente secuencial.

- No existe integración entre el flujo de ventas y el sistema financiero
- El cliente puede esperar hasta **8 horas hábiles** si el analista está ocupado
- Representa el **10.8% del tiempo total del ciclo**

---

### Cuello de botella #2 — Consulta de stock desincronizada (Paso 4)

**Tiempo:** 50 minutos · **Categoría:** Trabajo duplicado

El Coordinador de Inventarios consulta **dos fuentes separadas**: registros físicos en bodega y el ERP legacy. Estas fuentes frecuentemente no coinciden.

- Diferencias entre sistemas generan órdenes de producción innecesarias
- El 35% de los pedidos se va a fabricación — parte de ese porcentaje podría reducirse con un inventario preciso
- Si hubiera stock mal registrado, el error solo se descubre al llegar a la bodega

---

### Cuello de botella #3 — Reproceso por fallo de calidad (Paso 9B)

**Tiempo:** 90 minutos adicionales · **Frecuencia:** 18% de los casos · **Costo adicional:** $12.00

El control de calidad ocurre **solo al final de la fabricación**. Si un lote falla, ya se consumieron 120 minutos de fabricación. El reproceso agrega 90 minutos más antes de que el lote vuelva a la inspección.

- 18 de cada 100 lotes pasan por este ciclo — frecuencia inaceptable
- El costo acumulado de reprocesos a escala mensual: 1,200 pedidos × 35% (ruta fabricación) × 18% × $12 ≈ **$907/mes en reprocesos**
- La detección tardía multiplica el impacto: mismo defecto detectado en-proceso costaría < $3

---

## Slide 12 — Lectura analítica del modelo BPMN: los gateways como diagnóstico

> En BPMN, un **gateway XOR** no es solo una decisión — es un **punto de riesgo cuantificado**.

### Gateway #1: ¿Hay stock disponible? (Paso 5)

```
Probabilidad SÍ: 65%  →  Ruta: ~185 min · ~$45
Probabilidad NO: 35%  →  Ruta: ~375 min · ~$82
```

**Implicación analítica:** El 35% de los pedidos consume el doble de tiempo. Si la precisión del inventario mejorara y se descubriera que parte de ese 35% realmente tiene stock disponible, el impacto sería directo sobre el tiempo de ciclo sin cambiar ningún otro paso.

### Gateway #2: ¿Pasa el control de calidad? (Paso 9)

```
Probabilidad APRUEBA: 82%  →  Proceso continúa
Probabilidad RECHAZA: 18%  →  +90 min · +$12 · vuelve al XOR
```

**Implicación analítica:** Un proceso con 18% de tasa de rechazo al final del ciclo productivo no tiene control preventivo. El costo del rechazo se amplifica porque ya se invirtió el tiempo completo de fabricación.

> Cambiar las probabilidades de estos gateways — a través de mejoras upstream — es la palanca más poderosa del rediseño.

---

## Slide 13 — Costo del proceso: dónde va el dinero

### Distribución del costo de $105.91 por pedido (ruta completa)

| Actividad | Costo | % del total |
|-----------|-------|-------------|
| Fabricación (paso 7) | $16.00 | 15.1% |
| Verificación de crédito (paso 3) | $13.00 | 12.3% |
| Reproceso QC (paso 9B — ponderado) | $12.00 | 11.3% |
| Validación Excel (paso 2) | $9.00 | 8.5% |
| Programación producción (paso 6B) | $9.33 | 8.8% |
| Entrega al cliente (paso 12) | $7.50 | 7.1% |
| Inspección calidad (paso 8) | $5.50 | 5.2% |
| Asignación transportista (paso 11) | $5.00 | 4.7% |
| Consulta stock (paso 4) | $8.33 | 7.9% |
| Recepción solicitud (paso 1) | $6.00 | 5.7% |
| Confirmación pedido (paso 6A) | $4.00 | 3.8% |
| Empaque (paso 10) | $4.17 | 3.9% |
| Factura (paso 13) | $4.33 | 4.1% |
| Gateways (XOR) | $1.75 | 1.7% |

> Los 3 cuellos de botella identificados representan **$41.33 (39%)** del costo total del pedido.

---

## Slide 14 — Lo que el modelo BPMN revela que la narración no puede

| Dimensión | Lo que el texto dice | Lo que el modelo demuestra |
|-----------|---------------------|---------------------------|
| Secuencialidad | "Se verifican crédito e inventario antes de confirmar" | Los pasos 3 y 4 son **completamente secuenciales** — podrían paralelizarse sin riesgo |
| Probabilidad de fallo | "Hay rechazos de calidad frecuentes" | El **18% de frecuencia** multiplicado por **1,200 pedidos/mes** genera 216 reprocesos mensuales |
| Transferencias entre áreas | "Varios departamentos intervienen" | Hay **7 cambios de swimlane** — cada uno es un punto potencial de pérdida de información o espera |
| Impacto del gateway de stock | "A veces hay stock, a veces no" | El **35% de pedidos** activa la ruta larga — cada punto porcentual reducido ahorra $1.30/pedido promedio |
| Visibilidad del cliente | "El cliente espera la confirmación" | No hay ningún evento de notificación intermedia — el cliente está ciego durante todo el proceso |

---

## Slide 15 — Síntesis del diagnóstico AS-IS

### Los números que definen el problema

```
555 minutos por pedido      →  2 jornadas completas de trabajo
38% de tiempo sin valor     →  210 minutos que no agregan nada al cliente
18% de rechazos QC          →  216 reprocesos mensuales · $2,592/mes en rework
35% de pedidos a fabricación →  Parcialmente evitable con mejor gestión de inventario
7 cambios de swimlane       →  7 puntos de transferencia de responsabilidad
$105.91 por pedido          →  $0.48 de costo operativo por dólar de margen
```

### Síntesis de la causa raíz estructural

> INDUPRO opera con **procesos del siglo XX en la economía del siglo XXI**: validación manual, sistemas desconectados, control de calidad reactivo y comunicación por correo electrónico. El resultado es un proceso que genera su propia complejidad.

---

## Slide 16 — Metodología analítica aplicada

### ¿Cómo llegamos a estos números?

| Paso metodológico | Herramienta utilizada | Resultado |
|-------------------|-----------------------|-----------|
| 1. Levantamiento de actividades | Análisis del caso INDUPRO v1 | Tabla de 13 actividades con tiempos y costos |
| 2. Modelado estructural | BPMN 2.0 en SAP Signavio | Diagrama con swimlanes, gateways y flujos |
| 3. Análisis de gateways | Probabilidades declaradas en el caso | Cuantificación de rutas y su frecuencia |
| 4. Cálculo de KPIs | Fórmulas de tiempo de ciclo y costo | Métricas de la línea base AS-IS |
| 5. Identificación NVA | Clasificación VA / NVA por actividad | 38% del ciclo sin valor agregado |
| 6. Análisis de bottlenecks | Tiempo y costo por paso | 3 cuellos críticos identificados con impacto cuantitativo |
| 7. Simulación de escenarios | SAP Signavio Simulation Module | Validación de parámetros y distribución de recursos |

---

## Slide 17 — Cierre de la sección AS-IS

### ¿Por qué el análisis AS-IS precede a cualquier propuesta?

El modelado AS-IS no describe una situación problema — **la cuantifica, la localiza y la prioriza**.

Sin estos datos, una propuesta de mejora es una opinión.
**Con estos datos, es un argumento.**

---

### Lo que el AS-IS establece como línea base para el TO-BE:

| Dimensión | Línea base AS-IS | Meta cuantificada TO-BE |
|-----------|-----------------|------------------------|
| Tiempo de ciclo | 555 min | < 350 min |
| Costo por pedido | $105.91 | < $70.00 |
| Tiempo NVA | ~210 min (38%) | < 70 min |
| Tasa de reproceso QC | 18% | < 5% |
| Cola verificación crédito | 60 min | < 15 min |

> Cada meta TO-BE tiene un origen directo en el diagnóstico AS-IS. Eso es gestión de procesos basada en evidencia.

---

## Notas de presentación

### Estructura recomendada por bloque de tiempo

| Bloque | Slides | Tiempo sugerido | Foco |
|--------|--------|-----------------|------|
| Contexto y alcance | 1–4 | 3–4 min | Quién es INDUPRO, qué proceso analizamos |
| Estructura del modelo | 5–7 | 4–5 min | Qué modelamos, cómo se ve el flujo |
| Métricas y diagnóstico | 8–11 | 6–7 min | Los números del problema |
| Lectura analítica | 12–14 | 4–5 min | Qué revela el modelo más allá del texto |
| Síntesis y metodología | 15–17 | 3–4 min | Cierre y puente hacia el TO-BE |

### Recomendaciones de entrega

- Las tablas de actividades (Slides 6 y 15) son más efectivas como **handout** que como slide proyectado
- El flujo lógico del Slide 7 puede reemplazarse con el **diagrama BPMN exportado de Signavio**
- Los gateways (Slide 12) son el argumento más poderoso — dedicar tiempo a la discusión
- El Slide 16 (metodología) responde la pregunta implícita del jurado: *"¿Cómo saben que estos números son correctos?"*
