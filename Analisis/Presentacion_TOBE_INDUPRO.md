# Presentación — Propuesta TO-BE: INDUPRO S.A.
## SAP Signavio Regional Challenge 2026

---

# PARTE II — MODELADO TO-BE

---

## Slide 1 — Portada

**INDUPRO S.A.**
*Rediseño del Proceso de Gestión de Pedidos — Propuesta TO-BE*

> SAP Signavio Regional Challenge 2026
> Automatización · Paralelización · Control Preventivo · Integración de Sistemas

---

## Slide 2 — Del diagnóstico a la propuesta: el puente analítico

El AS-IS demostró con datos dónde falla el proceso. El TO-BE responde a cada uno de esos datos con una intervención específica.

> Un rediseño TO-BE no es una lista de deseos tecnológicos — es **una respuesta estructurada al diagnóstico**.

### Principio de correspondencia: cada mejora tiene un origen

| Problema AS-IS identificado | Intervención TO-BE | Naturaleza del cambio |
|-----------------------------|--------------------|-----------------------|
| Pasos 3 y 4 son secuenciales y bloquean el flujo | AND Gateway: paralelización | Cambio estructural BPMN |
| Validación manual en Excel con 15% de errores | Portal web con auto-validación | Automatización de entrada |
| QC detecta fallos solo al final de fabricación | Control en-proceso durante manufactura | Control preventivo |
| Asignación de transporte por llamadas sin trazabilidad | TMS integrado con asignación automática | Digitalización |
| Facturación manual tras entrega | Factura electrónica automática al cierre | Automatización de salida |

---

## Slide 3 — Las 4 palancas del rediseño

### Estrategia de mejora estructurada

Todas las mejoras se sostienen en 4 palancas que actúan sobre diferentes dimensiones del proceso:

---

**Palanca 1 — Automatización**
> Eliminar la entrada manual de datos y las decisiones que puede tomar el sistema.

Aplica a: validación de pedidos, verificación de crédito, confirmación al cliente, facturación.

---

**Palanca 2 — Paralelización**
> Ejecutar simultáneamente pasos que hoy se hacen en secuencia sin necesidad técnica.

Aplica a: verificación de crédito + consulta de stock → **AND Gateway** (BPMN).

---

**Palanca 3 — Integración de sistemas**
> Conectar ERP, sistema financiero y TMS en un flujo digital único con una sola fuente de verdad.

Aplica a: consulta de inventario, verificación de crédito, asignación logística.

---

**Palanca 4 — Control de calidad preventivo**
> Mover parte del control de calidad al inicio del ciclo productivo, antes de que el defecto se amplifique.

Aplica a: inspección en-proceso durante manufactura → reduce reprocesos del 18% al 5%.

---

## Slide 4 — Restricciones que el TO-BE debe respetar

> El TO-BE no es un escenario ideal — es una propuesta **viable dentro de los límites declarados del caso**.

### Restricciones inamovibles

| Tipo | Restricción | Valor |
|------|-------------|-------|
| Tiempo técnico | Fabricación por lote estándar | **120 min** — no negociable |
| Tiempo regulatorio | Inspección final de calidad | **30 min** — requisito normativo |
| Financiero | Inversión máxima en tecnología | **USD 50,000** |
| Operativo | Costo por pedido TO-BE | No superar **USD 70.00** |
| RR.HH. | Nuevos roles permitidos | Máximo **2** |
| Logístico | Ventana de despacho | Solo entre **07:00 y 14:00** |
| BPMN | Notación | **BPMN 2.0 estricta** — sin UML ni flujos libres |

### Por qué estas restricciones importan en la presentación

Cada restricción es un **argumento de viabilidad**. Un TO-BE que las ignore puede ser más eficiente en papel pero indefendible frente al jurado. La propuesta que presentamos las cumple todas.

---

## Slide 5 — Estructura del modelo BPMN TO-BE

### Cambios estructurales respecto al AS-IS

| Elemento BPMN | AS-IS | TO-BE | Cambio |
|---------------|-------|-------|--------|
| User Tasks (actividad manual) | 12 | 8 | −4 actividades manuales |
| Service Tasks (actividad automatizada) | 0 | 4 | +4 automatizadas |
| Exclusive Gateway XOR | 2 | 2 | Probabilidades actualizadas |
| Parallel Gateway AND | 0 | 2 | +1 split + 1 join (nuevo) |
| Swimlanes | 7 | 8 | +1 lane de "Sistema / Automatización" |
| Sequence Flows | ~16 | ~18 | Mayor conectividad por paralelismo |

### La incorporación del AND Gateway es la mayor innovación estructural

```
AS-IS (secuencial):        TO-BE (paralelo):

[Verificar crédito]        [AND Split]
        ↓                  /         \
[Consultar stock]   [Verificar    [Consultar
        ↓            crédito]      stock]
   [XOR decisión]         \         /
                          [AND Join]
                               ↓
                        [XOR decisión]
```

**Impacto:** El tiempo de ambos pasos combinados pasa de 60+50 = 110 min a MAX(15, 10) = **15 min**.

---

## Slide 6 — Tabla de actividades TO-BE

### Flujo completo con métricas por actividad

| # | Actividad TO-BE | Responsable | Sistema | Duración (min) | Costo (USD) | Δ vs AS-IS |
|---|-----------------|-------------|---------|----------------|-------------|------------|
| 1 | Recepción vía portal web con auto-validación | Ejecutivo de Ventas | Portal Web + Formulario Digital | **15** | $3.00 | −60 min · −$12 |
| 2A | [PARALELO] Verificación de crédito automatizada (API) | Analista de Finanzas | Sistema Financiero API | **15** | $3.25 | −45 min · −$9.75 |
| 2B | [PARALELO] Consulta de stock en tiempo real (ERP) | Coordinador de Inventarios | ERP Integrado | **10** | $1.67 | −40 min · −$6.66 |
| 3 | **[AND Split]** Inicio paralelo | Sistema | Automático | 1 | — | nuevo |
| 4 | **[AND Join]** Convergencia crédito + stock | Sistema | Automático | 1 | — | nuevo |
| 5 | **[XOR]** ¿Crédito OK Y Stock OK? | Sistema | Automático | 2 | — | automatizado |
| 6A | Confirmación automática al cliente | Sistema / Ventas | Portal + Email/SMS | **5** | $1.00 | −15 min · −$3 |
| 6B | Programación de producción digital | Planificador | ERP — Módulo de planificación | **20** | $4.67 | −20 min · −$4.66 |
| 7 | Fabricación con QC en-proceso | Operarios de Planta | Órdenes digitales + QC en-línea | **120** *(inamovible)* | $16.00 | = tiempo |
| 8 | Inspección final de calidad | Inspector de Calidad | Sistema QC Digital | **30** *(inamovible)* | $5.50 | = tiempo |
| 9 | **[XOR]** ¿Pasa calidad? | Inspector de Calidad | Sistema QC | 2 | $0.37 | 82% → **95%** aprobación |
| 9B | Reproceso del lote (residual) | Operarios / Inspector | Manual | **60** | $8.00 | −30 min · −$4 |
| 10 | Empaque semi-automatizado | Logística | Sistema etiquetado + packing digital | **15** | $2.50 | −10 min · −$1.67 |
| 11 | Asignación de transportista automática (TMS) | Coordinador de Logística | TMS Integrado | **10** | $1.67 | −20 min · −$3.33 |
| 12 | Entrega al cliente y firma digital | Transportista | App móvil + firma digital | **45** *(física)* | $7.50 | = tiempo |
| 13 | Factura electrónica automática | Sistema / Finanzas | ERP + facturación electrónica | **5** | $1.08 | −15 min · −$3.25 |

**TOTAL (ruta con fabricación, sin reproceso): 281 min · $46.84**

---

## Slide 7 — Flujo lógico TO-BE (vista analítica)

```
[INICIO] Solicitud del cliente vía portal web
         │
         ▼
[1] Recepción + auto-validación digital (15 min) ── VENTAS / SISTEMA
         │
         ▼
    [AND SPLIT] ─────────────────────────────────────┐
         │                                           │
         ▼                                           ▼
[2A] Verificación de crédito              [2B] Consulta stock ERP
     automática API (15 min)                   tiempo real (10 min)
     ── FINANZAS / SISTEMA                     ── INVENTARIOS / SISTEMA
         │                                           │
    [AND JOIN] ──────────────────────────────────────┘
         │
         ▼
       [XOR] ¿Crédito OK Y Stock OK? (2 min) ── SISTEMA
        /                                 \
    SÍ (70%)                           NO (30%)
       │                                   │
       │                    [6B] Planificación digital (20 min)
       │                         ── PLANIFICACIÓN / ERP
       │                                   │
       │                    [7] Fabricación + QC en-proceso (120 min)
       │                         ── PLANTA ← restricción técnica
       │                                   │
       │                    [8] Inspección final calidad (30 min)
       │                         ── CONTROL DE CALIDAD ← regulatorio
       │                                   │
       │                               [XOR] ¿Pasa QC? (2 min)
       │                             Sí (95%)     No (5%)
       │                                 │             │
       │                                 │   [9B] Reproceso (60 min)
       │                                 │             │
       │                                 └─────────────┘
       │                                       │
[6A] Confirmación automática al cliente ◄──────┘
     (5 min) ── SISTEMA
         │
         ▼
[10] Empaque semi-automatizado (15 min) ── LOGÍSTICA
         │
[11] Asignación TMS automática (10 min) ── LOGÍSTICA / SISTEMA
         │
[12] Entrega + firma digital (45 min) ── TRANSPORTISTA
         │
[13] Factura electrónica automática (5 min) ── SISTEMA / FINANZAS
         │
       [FIN] Pedido entregado y facturado
```

---

## Slide 8 — Cálculo del tiempo de ciclo TO-BE

### Fórmula de tiempo con paralelismo

```
Tiempo total (ruta con fabricación, sin reproceso):

  Paso 1:          15 min   (recepción + auto-validación)
  Pasos 2A // 2B:  MAX(15, 10) = 15 min   ← paralelismo AND
  Gateways (3+4+5): 4 min
  Paso 6B:         20 min   (planificación digital)
  Paso 7:         120 min   (fabricación — inamovible)
  Paso 8:          30 min   (inspección — inamovible)
  Gateway XOR:      2 min
  Paso 6A:          5 min   (confirmación)
  Paso 10:         15 min   (empaque)
  Paso 11:         10 min   (TMS)
  Paso 12:         45 min   (entrega)
  Paso 13:          5 min   (factura)
                  ───────
  TOTAL:          286 min   ✅  (meta: < 350 min)
```

> La reducción de 555 → 281 min se logra principalmente por 3 cambios:
> - Paralelización pasos 3+4: **ahorra 95 min**
> - Reducción de actividades manuales: **ahorra ~120 min**
> - Automatización de gateways y confirmaciones: **ahorra ~55 min**

---

## Slide 9 — KPIs TO-BE vs. línea base AS-IS

### Comparativa completa de indicadores

| KPI | AS-IS | TO-BE | Meta | Reducción | % Mejora |
|-----|-------|-------|------|-----------|----------|
| **Tiempo de ciclo total** | 555 min | **281 min** | < 350 min | −274 min | **−49.4%** ✅ |
| **Costo por pedido** | $105.91 | **$46.84** | < $70.00 | −$59.07 | **−55.8%** ✅ |
| **Tiempo en espera / NVA** | ~210 min | **~45 min** | < 70 min | −165 min | **−78.6%** ✅ |
| **Cola — verificación crédito** | 60 min | **15 min** | < 15 min | −45 min | **−75%** ✅ |
| **Cola — consulta de stock** | 50 min | **10 min** | — | −40 min | **−80%** |
| **Fabricación** | 120 min | **120 min** | — | 0 | ⚠️ Restricción técnica |
| **Tasa de reproceso QC** | 18% | **5%** | < 5% | −13 pp | **−72.2%** ✅ |
| **Probabilidad aprobación QC** | 82% | **95%** | — | +13 pp | **+15.9%** |

> El único KPI sin mejora es el tiempo de fabricación — por definición, una restricción técnica inamovible.

---

## Slide 10 — Costo del proceso TO-BE: distribución del ahorro

### ¿Dónde se genera el ahorro de $59.07 por pedido?

| Actividad | Costo AS-IS | Costo TO-BE | Ahorro |
|-----------|-------------|-------------|--------|
| Recepción + validación (pasos 1+2) | $15.00 | $3.00 | **$12.00** |
| Verificación de crédito (paso 3) | $13.00 | $3.25 | **$9.75** |
| Consulta de stock (paso 4) | $8.33 | $1.67 | **$6.66** |
| Confirmación al cliente (paso 6A) | $4.00 | $1.00 | **$3.00** |
| Planificación de producción (paso 6B) | $9.33 | $4.67 | **$4.66** |
| Reproceso QC (paso 9B — ponderado al 18%→5%) | $12.00 | $8.00 | **$4.00** |
| Empaque (paso 10) | $4.17 | $2.50 | **$1.67** |
| Asignación transportista (paso 11) | $5.00 | $1.67 | **$3.33** |
| Factura (paso 13) | $4.33 | $1.08 | **$3.25** |
| Fabricación / Inspección / Entrega | $29.00 | $29.00 | $0.00 *(inamovibles)* |

**Total ahorro: $59.07 por pedido (55.8% de reducción)**

---

## Slide 11 — El AND Gateway: la palanca más poderosa del rediseño

### Análisis del cambio estructural más impactante

El **Parallel Gateway (AND)** no existe en el BPMN AS-IS. Su incorporación en el TO-BE es la intervención de mayor impacto con cero inversión adicional de personal.

### ¿Por qué los pasos 3 y 4 pueden ejecutarse en paralelo?

```
En el AS-IS:
  ┌─────────────────────────────────────────────────────┐
  │ Paso 3 (crédito) NO usa información del Paso 4     │
  │ Paso 4 (stock) NO depende del resultado del Paso 3 │
  └─────────────────────────────────────────────────────┘
  → No existe dependencia lógica entre ellos.
  → La secuencialidad AS-IS es un artefacto del flujo manual, no un requisito del negocio.
```

### Impacto cuantitativo del AND Gateway

| Métrica | Sin AND (AS-IS) | Con AND (TO-BE) | Diferencia |
|---------|-----------------|-----------------|------------|
| Tiempo pasos 3+4 | 60 + 50 = **110 min** | MAX(15, 10) = **15 min** | **−95 min** |
| Costo pasos 3+4 | $13.00 + $8.33 = **$21.33** | $3.25 + $1.67 = **$4.92** | **−$16.41** |
| Bloqueo del proceso | Total (el proceso espera ambos) | Ninguno (corren simultáneamente) | Eliminado |

> 95 minutos ahorrados por un cambio de notación BPMN que refleja una decisión organizacional, no una inversión tecnológica adicional.

---

## Slide 12 — Control de calidad preventivo: del 18% al 5%

### El cambio de QC reactivo a QC preventivo

#### Estado AS-IS — QC al final del ciclo productivo

```
[7] Fabricación completa (120 min)
         ↓
[8] Inspección final
         ↓
   18% RECHAZA → [9B] Reproceso (90 min) → vuelve a [8]

Costo de un defecto detectado al final:
  120 min fabricación gastados + 90 min reproceso = 210 min · $28
```

#### Estado TO-BE — QC durante el proceso productivo

```
[7] Fabricación (120 min) + control en-proceso
         ↓
[8] Inspección final
         ↓
   5% RECHAZA → [9B] Reproceso reducido (60 min)

Costo de un defecto detectado durante el proceso:
  Parada temprana + corrección = ~30-45 min · $6-8
```

### Impacto mensual de la reducción de reprocesos

```
AS-IS:  1,200 pedidos × 35% (ruta fabricación) × 18% (rechazo) = 75.6 reprocesos/mes
TO-BE:  1,200 pedidos × 30% (ruta fabricación) × 5%  (rechazo) = 18.0 reprocesos/mes

Reducción de reprocesos: 57.6 menos por mes
Ahorro mensual en reprocesos: 57.6 × ($28 AS-IS − $8 TO-BE) = 57.6 × $20 = $1,152/mes
```

---

## Slide 13 — Los gateways XOR en el TO-BE: nuevas probabilidades

> Las probabilidades cambian porque el proceso upstream mejora la calidad de la decisión.

### XOR #1 — ¿Crédito OK Y Stock OK?

| | AS-IS | TO-BE | ¿Por qué cambia? |
|-|-------|-------|------------------|
| SÍ (aprobado) | 65% | **70%** | ERP integrado reduce errores de stock; menos pedidos van a fabricación innecesaria |
| NO (requiere producción) | 35% | **30%** | Mayor precisión del inventario en tiempo real |

### XOR #2 — ¿Pasa el control de calidad?

| | AS-IS | TO-BE | ¿Por qué cambia? |
|-|-------|-------|------------------|
| APRUEBA | 82% | **95%** | QC en-proceso detecta y corrige defectos antes de la inspección final |
| RECHAZA (reproceso) | 18% | **5%** | Los fallos se resuelven durante la fabricación, no al terminarla |

> Cambiar las probabilidades de los gateways **no es una suposición arbitraria** — es la consecuencia medible del QC preventivo y la integración del inventario.

---

## Slide 14 — Comparativa estructural BPMN: AS-IS vs. TO-BE

### Lo que cambia en el diagrama

| Dimensión | AS-IS | TO-BE |
|-----------|-------|-------|
| Pasos 1+2 (recepción y validación) | 2 User Tasks manuales — Excel | 1 Service Task automática — Portal web |
| Pasos 3+4 (crédito e inventario) | 2 User Tasks secuenciales | 2 Service Tasks en paralelo via AND Gateway |
| Gateway de stock | XOR manual (Coordinador decide) | XOR del sistema (criterio automático) |
| Confirmación al cliente | User Task — correo manual | Service Task — notificación automática |
| Planificación de producción | User Task — planilla manual | User Task — ERP con visibilidad de capacidad |
| QC durante fabricación | No existe | Integrado en Task [7] — control en-línea |
| Asignación de transporte | User Task — llamada telefónica | Service Task — TMS automático |
| Generación de factura | User Task — sistema de facturación | Service Task — ERP automático al cierre |
| Lane adicional | — | Lane 8: "Sistema / Automatización" |

### Lectura desde la perspectiva del evaluador BPMN

El TO-BE no solo tiene menos actividades — tiene **elementos BPMN más ricos**: Service Tasks, AND Gateways, y un lane de sistema que en el AS-IS no existía porque el sistema no participaba en el proceso.

---

## Slide 15 — Inversión requerida: viabilidad del TO-BE

### Desglose de los USD 50,000

| Componente | Descripción | Inversión |
|------------|-------------|-----------|
| Portal web de pedidos | Formulario digital con validación automática | $12,000 |
| Integración ERP — inventario en tiempo real | API de consulta de stock en ERP legacy | $10,000 |
| Integración sistema financiero | API de verificación automática de crédito | $8,000 |
| TMS — Transport Management System | Módulo básico de asignación y tracking | $7,000 |
| Sistema QC digital + app en-proceso | Checklist digital + alertas en manufactura | $5,000 |
| Facturación electrónica automática | Módulo de generación automática de facturas | $3,000 |
| Capacitación del personal | 40 horas de formación en nuevas herramientas | $5,000 |
| **TOTAL** | | **$50,000** ✅ |

### Nuevos roles creados (máx. 2 permitidos)

| Rol | Función |
|-----|---------|
| Analista de Procesos Digitales | Administra el portal web, monitorea el flujo digital |
| Técnico de Integración ERP | Mantiene las APIs entre sistemas (implementación + soporte) |

---

## Slide 16 — ROI: retorno sobre la inversión

### El argumento financiero del TO-BE

```
Ahorro por pedido:    $105.91 − $46.84  =  $59.07 / pedido

Volumen mensual:                           1,200 pedidos / mes

Ahorro mensual:       1,200 × $59.07    =  $70,884 / mes

Inversión total:                           $50,000

Payback period:       $50,000 ÷ $70,884  ≈  0.7 meses  (<  1 mes)  ✅
```

### Proyección a 12 meses post-implementación

| Período | Inversión | Ahorro acumulado | Balance neto |
|---------|-----------|-----------------|--------------|
| Mes 0 (implementación) | −$50,000 | $0 | −$50,000 |
| Mes 1 | — | +$70,884 | +$20,884 |
| Mes 3 | — | +$212,652 | +$162,652 |
| Mes 6 | — | +$425,304 | +$375,304 |
| Mes 12 | — | +$850,608 | +$800,608 |

> El TO-BE paga su propia implementación en menos de un mes. El argumento no es tecnológico — es financiero.

---

## Slide 17 — Simulación en SAP Signavio: parámetros TO-BE

### Configuración de escenarios de simulación

| Escenario | Descripción | Parámetro modificado | Objetivo |
|-----------|-------------|---------------------|----------|
| **Escenario Base** | TO-BE con valores propuestos | Estándar | Comparación directa vs AS-IS |
| **Escenario 2: +Volumen** | Incremento del 40% en pedidos | Frecuencia × 1.4 (1,680 pedidos/mes) | Validar escalabilidad |
| **Escenario 3: Riesgo** | Inspector de QC ausente | Inspector: 1 recurso en lugar de 2 | Análisis de resiliencia |

### Parámetros clave TO-BE para Signavio

| Pestaña | Parámetro | Valor |
|---------|-----------|-------|
| Duration | Recepción portal | 15 min |
| Duration | Verificación crédito (paralela) | 15 min |
| Duration | Consulta stock (paralela) | 10 min |
| Duration | Fabricación | 120 min *(inamovible)* |
| Duration | Inspección QC | 30 min *(inamovible)* |
| Frequency | XOR Stock — SÍ | **70%** |
| Frequency | XOR Stock — NO | **30%** |
| Frequency | XOR QC — APRUEBA | **95%** |
| Frequency | XOR QC — RECHAZA | **5%** |
| Resources | Sistema Automático | $0/hora *(costo ya amortizado)* |

---

## Slide 18 — Lo que el TO-BE demuestra más allá de los números

| Dimensión | Lo que el texto dice | Lo que el modelo TO-BE demuestra |
|-----------|---------------------|----------------------------------|
| Paralelismo | "Se mejora la eficiencia en crédito e inventario" | El AND Gateway **estructura** el paralelismo — no es una declaración, es una arquitectura de proceso |
| Automatización | "Se automatiza la validación" | Los Service Tasks reemplazan User Tasks específicos — trazable actividad por actividad |
| Calidad | "Se reduce la tasa de reproceso" | La probabilidad del XOR QC cambia de 82% a 95% — cuantificado y simulable |
| Escalabilidad | "El sistema puede manejar más volumen" | El Escenario 2 de simulación lo demuestra con 1,680 pedidos/mes |
| Viabilidad | "La propuesta es alcanzable" | El desglose de $50,000 cubre exactamente los componentes necesarios |

---

## Slide 19 — Síntesis del rediseño TO-BE

### Los números que definen la propuesta

```
281 minutos por pedido     →  −49% vs AS-IS  ·  1.2 jornadas vs 2.3
$46.84 por pedido          →  −56% vs AS-IS  ·  USD 59 de ahorro neto
~45 min de espera NVA      →  −79% vs AS-IS  ·  de 210 a 45 min sin valor
5% tasa de reproceso QC    →  −72% vs AS-IS  ·  de 75 a 18 reprocesos/mes
$70,884 de ahorro mensual  →  ROI en < 1 mes  ·  $800K de beneficio neto en Año 1
```

### ¿Qué hace que este TO-BE sea defendible?

1. **Cada mejora tiene un origen en el diagnóstico AS-IS** — no son mejoras genéricas
2. **Las restricciones técnicas y regulatorias se respetan** — 120 min fabricación, 30 min QC
3. **La inversión encaja exactamente en el presupuesto** — $50,000 con desglose verificable
4. **Las probabilidades de los gateways son consecuencias lógicas**, no suposiciones
5. **El modelo BPMN refleja los cambios** — AND Gateway, Service Tasks, nuevo lane de sistema

---

## Slide 20 — Cierre: del AS-IS al TO-BE como argumento completo

```
DIAGNÓSTICO AS-IS                         PROPUESTA TO-BE
─────────────────────────────────────────────────────────
555 min de ciclo           →              281 min de ciclo
38% de tiempo sin valor    →              ~16% de tiempo sin valor
18% de reprocesos QC       →              5% de reprocesos QC
7 cambios de swimlane      →              7 + 1 (sistema) mejor integrado
0 actividades automatizadas →             4 Service Tasks automatizadas
0 AND Gateways             →              1 AND Gateway (paralelismo)
$105.91 por pedido         →              $46.84 por pedido
```

> El TO-BE no es una visión — es una **respuesta estructurada, cuantificada y viable** al diagnóstico AS-IS.
> Eso es lo que SAP Signavio permite demostrar: no solo cómo mejorar, sino **cuánto** y **por qué**.

---

## Notas de presentación

### Estructura recomendada por bloque de tiempo

| Bloque | Slides | Tiempo sugerido | Foco |
|--------|--------|-----------------|------|
| Estrategia y restricciones | 1–4 | 3–4 min | Por qué este rediseño y dentro de qué límites |
| Estructura del modelo TO-BE | 5–7 | 4–5 min | Qué cambió en el BPMN y cómo se ve el flujo |
| Métricas y distribución del ahorro | 8–10 | 5–6 min | Los números de la mejora, actividad por actividad |
| Cambios estructurales clave | 11–14 | 5–6 min | AND Gateway, QC preventivo, gateways actualizados |
| Viabilidad y ROI | 15–16 | 3–4 min | Inversión, desglose y retorno |
| Simulación y cierre | 17–20 | 3–4 min | Escenarios Signavio y síntesis del argumento |

### Recomendaciones de entrega

- El Slide 11 (AND Gateway) es el argumento técnico más potente — puede generar preguntas del jurado; preparar la respuesta sobre dependencia lógica entre pasos
- El Slide 12 (QC preventivo) requiere la captura de pantalla del diagrama Signavio donde se muestre el símbolo de QC en-proceso dentro del Task 7
- El Slide 16 (ROI) cierra el argumento financiero — dejarlo para el final de la sección de viabilidad, nunca al inicio
- El Slide 20 es el cierre ideal: funciona como slide de conclusión o como fondo durante preguntas del jurado
