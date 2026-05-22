# AS-IS — Análisis Correcto del Proceso de Gestión de Pedidos
## INDUPRO S.A. | SAP Signavio Regional Challenge 2026

> **Versión:** 1.0 — Corrección Oficial  
> **Elaborado:** Mayo 2026  
> **Basado en:** `Caso_Estudio_INDUPRO_v1.pdf` + correcciones del feedback del jurado

---

## 1. Contexto General de la Empresa

| Atributo | Valor |
|---|---|
| Empresa | INDUPRO S.A. |
| Sector | Manufactura y distribución industrial |
| Fundación | 1998 |
| Empleados | 320+ |
| Facturación anual | ~USD 45 millones |
| Plantas de producción | 2 (Planta A y Planta B) |
| Centro de distribución | 1 |
| Volumen mensual | ~1,200 pedidos/mes |
| SKUs activos | 85 |
| Tiempo de entrega promedio actual | 12 días hábiles |
| Utilización de planta | 78% |

### Mercado objetivo de INDUPRO

| Segmento | Participación |
|---|---|
| Construcción | 40% |
| Minería | 35% |
| Agro-industria | 25% |

---

## 2. Alcance del Proceso Modelado

| Punto | Descripción |
|---|---|
| **Inicio** | Solicitud del cliente (correo electrónico / teléfono / portal web) |
| **Fin** | Entrega física al cliente + emisión y envío de factura |

### Departamentos involucrados (Swimlanes — solo roles humanos)

| Swimlane | Rol | Disponibilidad | Costo/hora |
|---|---|---|---|
| Lane 1 | Ejecutivo de Ventas | 2 disponibles · 8h/día | **$12/hr** |
| Lane 2 | Analista de Finanzas | 1 disponible · 8h/día | **$13/hr** |
| Lane 3 | Coordinador de Inventarios | 1 disponible · 8h/día | **$10/hr** |
| Lane 4 | Planificador de Producción | 1 disponible · 8h/día | **$14/hr** |
| Lane 5 | Operario de Planta | 6 disponibles · turno 8h | **$8/hr** |
| Lane 6 | Inspector de Calidad | 2 disponibles · 8h/día | **$11/hr** |
| Lane 7 | Coordinador de Logística | 1 disponible · 8h/día | **$10/hr** |

> Los costos por hora de los roles son los definidos explícitamente por el caso y se usan como base para todos los cálculos.

> ⚠️ **Notación Signavio — IT Systems:** Los sistemas informáticos (ERP Legacy, Sistema Financiero, Sistema de Facturación) **NO son lanes**. En SAP Signavio se modelan como artefactos **IT System** — extensión propia de Signavio, similar a un data object o data store — asociados a cada tarea mediante una **asociación no direccional** (línea punteada **sin flecha**). Los lanes son exclusivamente para actores humanos/roles.
>
> 📘 *Fuente S3.1:* "IT Systems also make an exception. You use non-directional associations to connect them with activities instead of the directional associations you use for other artifacts."
>
> **En el Dictionary del AS-IS deben registrarse** (Entregable E3): los 7 roles, los sistemas (ERP Legacy, Sistema Financiero, Sistema de Facturación), y los documentos (Solicitud de pedido, Checklist físico, Guía de remisión impresa, Factura manual).

---

## 3. Tabla de Actividades AS-IS — Descripción Completa

| # | Actividad | Responsable | Herramienta / Sistema | Duración (min) | Costo/hora | Costo actividad (USD) | Tipo |
|---|---|---|---|---|---|---|---|
| 1 | Recepción de solicitud del cliente | Ejecutivo de Ventas | Correo / Teléfono | 30 | $12 | **$6.00** | Manual |
| 2 | Validación manual de datos del pedido (cliente, productos, cantidades) | Ejecutivo de Ventas | Hoja de Excel | 45 | $12 | **$9.00** | Manual |
| 3 | Verificación de crédito del cliente | Analista de Finanzas | Sistema Financiero (manual, no integrado) | 60 | $13 | **$13.00** | Manual |
| 4 | Consulta de disponibilidad de stock en bodega | Coordinador de Inventarios | Registro físico + ERP Legacy (no integrado) | 50 | $10 | **$8.33** | Manual |
| 5 | **[Gateway XOR]** Decisión de stock | Coordinador de Inventarios | Manual | 5 | $10 | **$0.83** | Decisión |
| 6A | **[Ruta SÍ stock]** Confirmación de pedido al cliente | Ejecutivo de Ventas | Correo electrónico | 20 | $12 | **$4.00** | Manual |
| 6B | **[Ruta NO stock]** Programación de orden de producción | Planificador de Producción | Planilla de producción manual | 40 | $14 | **$9.33** | Manual |
| 7 | Fabricación del producto | Operarios de Planta | Órdenes de trabajo impresas | 120 | $8 | **$16.00** | Operativo |
| 8 | Inspección y liberación de calidad | Inspector de Calidad | Checklist físico en papel | 30 | $11 | **$5.50** | Control |
| 9 | **[Gateway XOR]** Decisión de calidad | Inspector de Calidad | Manual | 5 | $11 | **$0.92** | Decisión |
| 9B | **[Ruta reproceso]** Reprocesar lote | Operarios / Inspector | Manual | 90 | $8 | **$12.00** | Reproceso |
| 10 | Empaque y preparación para despacho | Operarios de Logística | Manual | 25 | $10 | **$4.17** | Manual |
| 11 | Asignación de transportista y programación de entrega | Coordinador de Logística | Correo / Teléfono | 30 | $10 | **$5.00** | Manual |
| 12 | Entrega al cliente y firma de conformidad | Transportista / Logística | Guía de remisión impresa | 45 | $10 | **$7.50** | Operativo |
| 13 | Generación y envío de factura | Analista de Finanzas | Sistema de facturación (manual) | 20 | $13 | **$4.33** | Manual |

---

## 4. ⚠️ ERRORES DETECTADOS EN EL CASO — KPIs AS-IS INCORRECTOS

> **IMPORTANTE:** El caso de INDUPRO presenta errores matemáticos en el cálculo de los KPIs de la ruta de fabricación + reproceso. Este apartado documenta los errores detectados y establece los valores correctos.

### Error 1 — Tiempo de ciclo incorrecto (555 min)

**Lo que afirma el caso:**
> El tiempo total de la ruta con reproceso y fabricación es **555 minutos**.

**Por qué es incorrecto:**  
Para calcular 555 minutos, el caso **omitió las actividades 6A y 6B** del cómputo total. Lo que hicieron fue sumar TODAS las actividades del proceso (incluyendo ambas rutas del XOR de stock) y luego restar 6A y 6B:

```
Suma de TODAS las actividades: 615 minutos
615 - 20 (actividad 6A) - 40 (actividad 6B) = 555 minutos
```

Pero esto no tiene lógica de proceso: si se toma la **ruta de fabricación** (NO hay stock), se transita por la actividad **6B** (Programar producción, 40 min), NO por 6A. Entonces, 6B sí debe estar incluida en el cómputo de esa ruta.

**El tiempo correcto para la ruta fabricación + reproceso:**

| # | Actividad | Duración (min) |
|---|---|---|
| 1 | Recepción de solicitud | 30 |
| 2 | Validación manual Excel | 45 |
| 3 | Verificación de crédito | 60 |
| 4 | Consulta de stock | 50 |
| 5 | Gateway XOR (decisión stock) | 5 |
| 6B | Programación de producción | 40 |
| 7 | Fabricación del producto | 120 |
| 8 | Inspección y liberación calidad | 30 |
| 9 | Gateway XOR (decisión calidad) | 5 |
| 9B | Reproceso del lote | 90 |
| 10 | Empaque y preparación | 25 |
| 11 | Asignación transportista | 30 |
| 12 | Entrega al cliente | 45 |
| 13 | Generación y envío de factura | 20 |
| **TOTAL CORRECTO** | | **595 min** |

> ✅ **Tiempo correcto para ruta fabricación + reproceso: 595 minutos** (no 555).

---

### Error 2 — Costo total incorrecto ($105.91)

**Lo que afirma el caso:**
> El costo total de la ruta con reproceso y fabricación es **$105.91**.

**Por qué es incorrecto:**  
El valor $105.91 solo es alcanzable si se **incluye la actividad 6A** ($4.00 de Confirmación de pedido) en la ruta de fabricación. Pero 6A es la ruta contraria del XOR de stock (cuando SÍ hay stock). No puede estar simultáneamente en ambas rutas.

Además, el caso **truncó** el costo de actividades calculadas con decimales periódicos en lugar de redondear. Por ejemplo:
- Actividad 9 (Inspector QC, 5 min a $11/hr): 5/60 × $11 = $0.9166... → truncado a $0.91 (incorrecto) → redondeado a **$0.92** (correcto)
- Actividad 6B (Planificador, 40 min a $14/hr): 40/60 × $14 = $9.333... → redondeado a **$9.33**

**Costo correcto para la ruta fabricación + reproceso (con redondeo correcto a 2 decimales):**

| # | Actividad | Duración | $/hr | Cálculo | Costo |
|---|---|---|---|---|---|
| 1 | Recepción solicitud | 30 min | $12 | 30/60 × 12 | **$6.00** |
| 2 | Validación Excel | 45 min | $12 | 45/60 × 12 | **$9.00** |
| 3 | Verificación crédito | 60 min | $13 | 60/60 × 13 | **$13.00** |
| 4 | Consulta stock | 50 min | $10 | 50/60 × 10 | **$8.33** |
| 5 | Gateway XOR stock | 5 min | $10 | 5/60 × 10 | **$0.83** |
| 6B | Programar producción | 40 min | $14 | 40/60 × 14 = 9.333... | **$9.33** |
| 7 | Fabricación | 120 min | $8 | 120/60 × 8 | **$16.00** |
| 8 | Inspección calidad | 30 min | $11 | 30/60 × 11 | **$5.50** |
| 9 | Gateway XOR calidad | 5 min | $11 | 5/60 × 11 = 0.9166... | **$0.92** |
| 9B | Reproceso lote | 90 min | $8 | 90/60 × 8 | **$12.00** |
| 10 | Empaque | 25 min | $10 | 25/60 × 10 = 4.166... | **$4.17** |
| 11 | Asig. transportista | 30 min | $10 | 30/60 × 10 | **$5.00** |
| 12 | Entrega cliente | 45 min | $10 | 45/60 × 10 | **$7.50** |
| 13 | Factura | 20 min | $13 | 20/60 × 13 = 4.333... | **$4.33** |
| **TOTAL** | | 595 min | | | **$101.91** |

> ⚠️ **Nota sobre redondeo:** SAP Signavio aplica redondeo matemático a cada actividad individual antes de sumar. Dado que la actividad 9 da $0.9166... y Signavio redondea a $0.92, el total con Signavio sería **$101.92**. El caso lo truncó a $0.91, resultando en $101.91 (diferencia de $0.01). **En Signavio el valor correcto será $101.92.**

**Resumen de la discrepancia con el caso:**

| KPI | Valor en el caso | Valor CORRECTO | Error |
|---|---|---|---|
| Tiempo (ruta fabricación + reproceso) | 555 min | **595 min** | +40 min omitidos |
| Costo (ruta fabricación + reproceso) | $105.91 | **$101.92** | Incluye 6A incorrectamente |

---

### Error 3 — Ambigüedad en el flujo post-confirmación

**Lo que describe el caso:**  
No se especifica claramente qué sucede después de la "Confirmación de pedido al cliente" (Actividad 6A, ruta SÍ stock). La lógica mínima de negocio dicta que si existe stock, el proceso debería continuar directamente hacia **Empaque** (actividad 10) sin pasar por Fabricación. Sin embargo, el modelo del caso no lo aclara.

**Interpretación correcta:**  
- **Ruta SÍ stock** (65%): Confirmar pedido → Empaque → Asignación transportista → Entrega → Factura
- **Ruta NO stock** (35%): Programar producción → Fabricar → Inspección QC → (reproceso si aplica) → Empaque → Asignación transportista → Entrega → Factura

---

## 5. Flujo del Proceso AS-IS (Descripción Narrativa)

El proceso comienza cuando un cliente de INDUPRO realiza una solicitud de pedido a través de correo electrónico o llamada telefónica. El **Ejecutivo de Ventas** recibe la solicitud (30 min) y procede a validar manualmente los datos del pedido en una hoja de Excel (45 min), verificando que la información del cliente, los productos y las cantidades sean correctas.

A continuación, el **Analista de Finanzas** realiza una verificación manual del crédito disponible del cliente consultando el sistema financiero, que no está integrado con el resto del proceso (60 min). Este paso es secuencial y no puede comenzar hasta que el anterior finalice.

Paralelamente —o más bien, de forma consecutiva— el **Coordinador de Inventarios** consulta la disponibilidad de stock revisando registros físicos y el ERP Legacy, sistemas que tampoco están integrados entre sí (50 min). Se toma la decisión mediante un Gateway XOR (5 min):

- **Si HAY stock (65%):** El Ejecutivo de Ventas confirma el pedido al cliente por correo (20 min) y se procede directamente al empaque.
- **Si NO hay stock (35%):** El Planificador de Producción programa manualmente la orden de producción en una planilla (40 min), los Operarios de Planta fabrican el producto con órdenes impresas (120 min, tiempo inamovible por restricción técnica), y el Inspector de Calidad realiza la inspección del lote (30 min, tiempo inamovible por requisito regulatorio). Un segundo Gateway XOR decide:
  - **Si APRUEBA calidad (82%):** El proceso continúa.
  - **Si RECHAZA calidad (18%):** Los operarios reprocean el lote (90 min) y se regresa a la inspección.

Independientemente de la ruta, el proceso converge en el empaque (25 min), la asignación del transportista por teléfono/correo (30 min), la entrega física al cliente con firma de conformidad en papel (45 min) y la generación manual de la factura (20 min).

---

## 6. Caracterización del Proceso AS-IS

### 6.1 Ficha de Proceso

| Campo | Descripción |
|---|---|
| **Nombre del proceso** | Gestión de Pedidos del Cliente — AS-IS |
| **Alcance** | Solicitud del cliente → Entrega y facturación |
| **Propietario del proceso** | Gerencia de Ventas y Operaciones |
| **Frecuencia** | ~1,200 casos/mes (40 pedidos/día laboral) |
| **Jornada laboral** | 8 horas diarias, lunes a viernes (480 min/día) |
| **Notación** | BPMN 2.0 |
| **Herramienta de modelado** | SAP Signavio Process Manager (académico) |

### 6.2 Entradas y Salidas del Proceso

| Elemento | Descripción |
|---|---|
| **Entrada principal** | Solicitud de pedido del cliente (correo/teléfono) |
| **Entrada secundaria** | Información del cliente (crédito, historial) |
| **Salida principal** | Producto entregado + firma de conformidad |
| **Salida secundaria** | Factura emitida |

### 6.3 Recursos del Proceso

| Recurso | Tipo | Costo/hora | Participación en el proceso |
|---|---|---|---|
| Ejecutivo de Ventas | Humano | $12/hr | Actividades 1, 2, 6A |
| Analista de Finanzas | Humano | $13/hr | Actividades 3, 13 |
| Coordinador de Inventarios | Humano | $10/hr | Actividad 4, Gateway 5 |
| Planificador de Producción | Humano | $14/hr | Actividad 6B |
| Operario de Planta | Humano | $8/hr | Actividades 7, 9B |
| Inspector de Calidad | Humano | $11/hr | Actividades 8, 9, 9B (supervisión) |
| Coordinador de Logística | Humano | $10/hr | Actividades 10, 11 |
| Transportista | Humano externo | $10/hr | Actividad 12 |

### 6.4 Sistemas del Proceso AS-IS

| Sistema | Tipo | Actividades donde se usa | Problema identificado |
|---|---|---|---|
| Correo electrónico | Canal de comunicación | 1, 6A, 11 | Sin trazabilidad, sin alertas automáticas |
| Teléfono | Canal de comunicación | 1, 11 | Sin registro digital |
| Hoja de Excel | Herramienta manual | 2 | Propenso a errores (~15% error rate), sin validación |
| Sistema Financiero | ERP financiero legacy | 3 | No integrado con el proceso comercial |
| ERP Legacy | ERP de operaciones | 4 | Datos de inventario no en tiempo real; doble fuente de verdad |
| Planilla de producción | Hoja de cálculo manual | 6B | Sin visibilidad de capacidad real |
| Órdenes de trabajo impresas | Documento físico | 7 | Sin trazabilidad digital |
| Checklist físico | Documento papel | 8, 9 | Sin registro histórico digitalizado |
| Guía de remisión impresa | Documento físico | 12 | Sin tracking de entrega |
| Sistema de facturación | Módulo ERP | 13 | Manual, no automatizado |

---

## 7. Diagrama Lógico del Flujo AS-IS

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCESO AS-IS — INDUPRO S.A.                     │
└─────────────────────────────────────────────────────────────────────┘

[INICIO] ──► Solicitud del cliente (correo/teléfono)
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ VENTAS   [1] Recepción de solicitud       (30 min/$6)   │
│          [2] Validación manual en Excel   (45 min/$9)   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ FINANZAS [3] Verificación de crédito      (60 min/$13)  │
│              (secuencial — Sistema financiero legacy)    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ INVENTARIOS [4] Consulta de stock        (50 min/$8.33) │
│                 (registros físicos + ERP legacy)         │
│             [5] Gateway XOR: ¿Hay stock? (5 min/$0.83)  │
└──────────┬──────────────────────────────┬───────────────┘
           │                              │
       SÍ (65%)                       NO (35%)
           │                              │
           │              ┌───────────────┘
           │              ▼
           │  ┌──────────────────────────────────────────────────┐
           │  │ PLANIF.  [6B] Programar orden (40 min / $9.33)  │
           │  │ PLANTA   [7]  Fabricación     (120 min / $16.00) │
           │  │              ⚠️ RESTRICCIÓN TÉCNICA INAMOVIBLE   │
           │  │ CALIDAD  [8]  Inspección QC   (30 min / $5.50)   │
           │  │              ⚠️ REQUERIMIENTO REGULATORIO         │
           │  │          [9]  Gateway XOR: ¿Pasa QC?             │
           │  │                (5 min / $0.92)                   │
           │  │           APRUEBA (82%)    RECHAZA (18%)         │
           │  │               │               │                  │
           │  │               │   [9B] Reproceso lote            │
           │  │               │       (90 min / $12.00)          │
           │  │               │        ⚠️ CUELLO DE BOTELLA       │
           │  │               └───────────────┘                  │
           │  └──────────────────────┬───────────────────────────┘
           │                         │
           ▼                         ▼
┌─────────────────────────────────────────────────────────┐
│ VENTAS   [6A] Confirmación al cliente  (20 min / $4.00) │
│               (solo ruta SÍ stock)                       │
└──────────────────────────┬──────────────────────────────┘
                           │ (convergencia de rutas)
                           ▼
┌─────────────────────────────────────────────────────────┐
│ LOGÍSTICA [10] Empaque y preparación  (25 min / $4.17)  │
│           [11] Asignación transportista (30 min / $5.00) │
│                (por correo/teléfono — sin trazabilidad)  │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ ENTREGA  [12] Entrega + firma remisión (45 min / $7.50) │
│               (guía en papel — sin tracking)             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ FINANZAS [13] Generar y enviar factura (20 min / $4.33) │
│               (manual — sistema no integrado)            │
└──────────────────────────┬──────────────────────────────┘
                           │
                        [FIN]
```

---

## 8. KPIs del Proceso AS-IS — Valores Correctos

### 8.1 Ruta con fabricación + reproceso (CORRECTA)

| KPI | Valor CORRECTO | ~~Valor del caso~~ | Diferencia |
|---|---|---|---|
| **Tiempo de ciclo** | **595 min** | ~~555 min~~ | Error: +40 min (omisión de 6B) |
| **Costo total (Signavio)** | **$101.92** | ~~$105.91~~ | Error: incluía 6A indebidamente |
| **Costo total (exacto)** | **$101.91** | ~~$105.91~~ | — |

### 8.2 Ruta con fabricación sin reproceso

| KPI | Valor |
|---|---|
| Tiempo de ciclo | **505 min** (595 − 90 min de 9B) |
| Costo total | **$89.92** (sin actividad 9B) |

### 8.3 Ruta directa de stock (sin fabricación, sin reproceso)

| KPI | Valor |
|---|---|
| Tiempo de ciclo | **330 min** (actividades 1-5 + 6A + 10-13) |
| Costo total | **$57.33** |

### 8.4 Tiempo promedio ponderado (considerando probabilidades XOR)

```
E[T] = P(stock SÍ) × T_stock + P(stock NO) × [P(QC OK) × T_fab + P(QC NO) × T_fab+rep]

E[T] = 0.65 × 330 + 0.35 × [0.82 × 505 + 0.18 × 595]
E[T] = 214.5 + 0.35 × [414.1 + 107.1]
E[T] = 214.5 + 0.35 × 521.2
E[T] = 214.5 + 182.4 = 396.9 min ≈ 397 min promedio ponderado
```

---

## 9. Ineficiencias Identificadas (Análisis de Causa Raíz)

| # | Problema | Actividad AS-IS | Causa Raíz | Impacto Cuantitativo |
|---|---|---|---|---|
| **P1** | Validación manual de pedidos con ~15% de error | Paso 2 | Sin sistema digital con validación automática | 45 min/pedido; errores requieren corrección posterior |
| **P2** | Verificación de crédito secuencial, sin integración | Paso 3 | Sistema financiero desconectado del flujo de ventas | 60 min bloqueando el proceso completo |
| **P3** | Consulta de inventario manual con doble fuente de verdad | Paso 4 | ERP legacy sin API en tiempo real; registros físicos paralelos | 50 min; errores de stock ~10% |
| **P4** | Tareas 3 y 4 son SECUENCIALES sin necesidad técnica | Pasos 3 y 4 | Ausencia de gateway AND para paralelización | +50 min desperdiciados en espera innecesaria |
| **P5** | Programación de producción sin visibilidad de capacidad | Paso 6B | Sin sistema de planificación en tiempo real | 40 min; sub-optimización de planta al 78% |
| **P6** | Control de calidad solo al final de fabricación | Paso 9B | QC tardío; defectos no detectados durante producción | 90 min de reproceso; 18% de lotes rechazados |
| **P7** | Asignación de transportista por llamadas sin tracking | Paso 11 | Sin TMS (Transport Management System) | 30 min/pedido; sin visibilidad logística |
| **P8** | Facturación manual no integrada | Paso 13 | Sistema de facturación desconectado del cierre del pedido | 20 min; riesgo de errores y demoras |
| **P9** | Sin notificaciones proactivas al cliente | Todo el proceso | Sin portal de comunicación integrada | Insatisfacción del cliente; consultas repetidas |
| **P10** | Sin paralelización de ninguna tarea | Todo el proceso | Diseño secuencial puro | 210 min estimados de espera evitable |

### 9.1 Cuello de Botella Principal: Reproceso del Lote (Actividad 9B)

| Atributo | Valor |
|---|---|
| Tiempo de reproceso | 90 minutos |
| Probabilidad de ocurrencia | 18% de los lotes fabricados |
| Costo por evento de reproceso | $12.00 |
| Impacto mensual estimado | 0.35 × 1,200 × 0.18 × 90 min = 6,804 min/mes de reproceso |
| Costo mensual de reproceso | 0.35 × 1,200 × 0.18 × $12 = **$907.20/mes** |
| Causa raíz | Control de calidad reactivo (solo al final de la producción) |

---

## 10. Actividades sin Valor Agregado (NVA)

| Actividad | Tiempo NVA | Causa |
|---|---|---|
| Esperas entre pasos por correo electrónico | ~100 min estimados | Comunicación sin workflow digital |
| Re-trabajo por errores en validación Excel | ~60 min promedio | Validación manual propensa a errores |
| Espera en cola para verificación de crédito | ~30 min | Proceso secuencial no automatizado |
| Búsqueda en registros físicos de stock | ~20 min | Doble fuente de verdad no integrada |
| **Total NVA estimado** | **~210 min** | **38% del ciclo total** |

---

## 11. Restricciones Inamovibles Identificadas en el Caso

| Restricción | Valor | Tipo |
|---|---|---|
| Fabricación por lote estándar (Paso 7) | 120 minutos | Técnica inamovible |
| Inspección final de calidad (Paso 8) | 30 minutos | Regulatoria inamovible |
| Jornada laboral | 8 horas diarias, L-V | Operativa |
| Ventana de despacho | 07:00 - 14:00 | Operativa |
| Presupuesto máximo de inversión | USD 50,000 | Financiera |
| Costo por pedido TO-BE máximo | USD 70.00 | Financiera |
| Nuevos roles permitidos | Máximo 2 | RR.HH. |

---

## 12. Conclusión del Análisis AS-IS

El proceso actual de INDUPRO S.A. está caracterizado por una estructura **enteramente secuencial**, **dependiente de procesos manuales** y operando con **sistemas completamente desconectados entre sí**. Los tres problemas críticos que impactan directamente los KPIs son:

1. **La ausencia de paralelización:** Los pasos de verificación de crédito (60 min) y consulta de stock (50 min) se ejecutan en secuencia cuando podrían ocurrir simultáneamente, desperdiciando 50 minutos por pedido.

2. **El control de calidad reactivo:** Con un 18% de tasa de rechazo y 90 minutos de reproceso, el sistema de calidad solo detecta defectos al final del ciclo productivo, generando el mayor cuello de botella del proceso.

3. **La desintegración de sistemas:** El ERP legacy, el sistema financiero y los procesos logísticos operan en silos completamente separados, obligando a intervenciones manuales en cada transición.

> **Tiempo real de la ruta crítica (fabricación + reproceso): 595 minutos / $101.92**  
> **Objetivo TO-BE: < 350 minutos / < $70.00**

---

## 10. Configuración de Simulación AS-IS en SAP Signavio

> **Fuente:** S5.2 — Performing Simulations in SAP Signavio + Caso INDUPRO (Fase 3, pasos 11-13)
>
> ⚠️ Usar **siempre minutos**. Ejecutar primero **"Un caso"** para verificar, luego **"Múltiples casos"** con duración **480 min** (1 día hábil). Guardar (Ctrl+S) antes de cada ejecución.

### Tab Duration — Tiempos en minutos

| Actividad | Duración (min) |
|---|---|
| 1 — Recepción solicitud | 30 |
| 2 — Validación manual Excel | 45 |
| 3 — Verificación crédito | 60 |
| 4 — Consulta stock | 50 |
| 5 — Gateway XOR stock | 5 |
| 6A — Confirmación pedido | 20 |
| 6B — Programar producción | 40 |
| 7 — Fabricación | 120 |
| 8 — Inspección calidad | 30 |
| 9 — Gateway XOR calidad | 5 |
| 9B — Reproceso lote | 90 |
| 10 — Empaque | 25 |
| 11 — Asignación transportista | 30 |
| 12 — Entrega al cliente | 45 |
| 13 — Factura | 20 |

### Tab Frequency — Probabilidades de gateways (deben sumar 100%)

| Gateway | Ruta | Probabilidad |
|---|---|---|
| XOR: ¿Hay stock? (paso 5) | Sí — hay stock | **65%** |
| XOR: ¿Hay stock? (paso 5) | No — sin stock | **35%** |
| XOR: ¿Pasa calidad? (paso 9) | Aprueba | **82%** |
| XOR: ¿Pasa calidad? (paso 9) | Rechaza | **18%** |

> Frecuencia: 4 pedidos/día (valor por defecto en Signavio académico)

### Tab Resources — Tarifas por hora por lane (aquí va el costo laboral)

| Lane | Costo/hora (USD) | Horas/día | Días/semana |
|---|---|---|---|
| Ejecutivo de Ventas | $12 | 8 | L-V |
| Analista de Finanzas | $13 | 8 | L-V |
| Coordinador de Inventarios | $10 | 8 | L-V |
| Planificador de Producción | $14 | 8 | L-V |
| Operario de Planta | $8 | 8 | L-V |
| Inspector de Calidad | $11 | 8 | L-V |
| Coordinador de Logística | $10 | 8 | L-V |

> **Resultado esperado en simulación AS-IS (1 caso, ruta fabricación + reproceso):** Tiempo ciclo ~595 min · Costo ~$101.92

---

*Documento elaborado como parte del SAP Signavio Regional Challenge 2026*  
*Equipo participante — ESPOL*
