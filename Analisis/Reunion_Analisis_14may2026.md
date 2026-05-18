# Análisis de Reunión — SAP Signavio Contest
**Fecha de reunión:** 14 de mayo de 2026 · Grabación Teams  
**Archivo fuente:** `material-concurso/Reunión - SAP Signavio Contest-20260514_221426-Grabación de la reunión-es-MX.docx`  
**Elaborado:** 18 de mayo de 2026

---

## 1. Resumen Ejecutivo

La reunión fue una sesión de revisión del modelo AS-IS presentado al profesor asesor. El profesor identificó **errores de modelado BPMN** en el AS-IS (actividades que deberían ser Gateways), precisó la **lógica de negocio real** detrás de la verificación de crédito (módulo FI-AR de SAP), y lanzó **dos temas de investigación** que deben incorporarse al TO-BE: el **módulo CRP de SAP PP** y la **minería de procesos con SAP Signavio Process Intelligence**.

---

## 2. Correcciones al Modelo AS-IS — Lo que dijo el Profesor

### 2.1 Errores identificados en el BPMN AS-IS

| # | Elemento actual en el modelo | Corrección del profesor | Justificación |
|---|---|---|---|
| **C1** | Task "Validar datos del pedido manualmente (Excel)" | Debe ser **Gateway XOR**, no tarea | *"Cuando tú validas tienes 2 caminos; esa actividad tiene que ser un Gateway porque tú validas o verificas, si tienes línea de crédito o no"* |
| **C2** | Task "Verificar crédito del cliente" | Mantenerla como tarea, pero agregar **Gateway XOR de salida explícito** con evento de mensaje si crédito es rechazado | *"Acá sí tendríamos que ponerle como la validación de que al verificar se termina el proceso… pero más que termine, lo que tendría que hacer es notificar un mensaje… un evento de mensaje en rojo"* |
| **C3** | Task "Consultar disponibilidad de stock" | Tiene implícita una decisión; revisar si también corresponde Gateway | *"El gateway no es como pregunta, BPMN no hace que hagas preguntas así, ese es un gateway de exclusión"* |
| **C4** | Task "Reprocesar lote" | Considerar agregar un **Intermediate Timer Event** antes o durante el reproceso | *"Reprocesar lote que todos ustedes están colocando como actividad, pero hay un evento de tiempo"* |
| **C5** | Gateways XOR sin etiquetas en ambas salidas | **Etiquetar ambas salidas** de cada XOR (SÍ/NO, condición clara) | *"No puedes dejarlo así sin… está llegando uno u otro"* |

> **Posición del profesor sobre los cambios:** El equipo puede y debe hacer estas interpretaciones de modelado. *"Ustedes podrían decir: hemos recibido el caso, lo hemos modelado, consideramos que hay algunos puntos que se pueden mejorar a nivel de modelación y los colocan ahí."*

### 2.2 Lógica real de la verificación de crédito (detalle del profesor)

El profesor explicó que la verificación de crédito en un ERP real funciona así:

```
1. El cliente envía pedido
2. El sistema verifica que el cliente exista
3. El sistema consulta la LÍNEA DE CRÉDITO del cliente (monto máximo aprobado)
4. [Gateway XOR] ¿El pedido entra dentro de la línea de crédito disponible?
      └── SÍ → Se aprueba → Se genera la Orden de Producción
      └── NO → Se activa el módulo de Cuentas por Cobrar (FI-AR)
                → Se notifica al cliente (evento de mensaje)
                → El proceso se detiene / el cliente puede negociar
```

**Módulo SAP involucrado:** SD (Sales & Distribution) ↔ **FI-AR (Financial Accounting – Accounts Receivable)**

> *"Hay una conexión entre ventas y cuentas por cobrar, porque hay módulos que se integran. Investiguen, porque hay módulos que se integran."*

---

## 3. Propuestas del Profesor para el TO-BE

| # | Mejora propuesta | Descripción |
|---|---|---|
| **T1** | AND Gateway (paralelización) | Verificación de crédito (FI-AR) Y consulta de stock (MM) deben ocurrir en **paralelo**, no secuencial |
| **T2** | Integración con CRP de SAP | La planificación de producción debe usar el módulo **PP-CRP** para generar automáticamente fechas de entrega, balancear capacidad y gestionar órdenes |
| **T3** | Message End Event + notificación cliente | Al rechazar crédito: evento de mensaje al cliente, no un End Event opaco |
| **T4** | Automatización vía portal ERP | *"Lo que se debe abrir en el TO-BE es la automatización, que el sistema lo hace porque estás automatizando"* |
| **T5** | Minería de procesos (Process Mining) | Agregar **SAP Signavio Process Intelligence** como propuesta adicional al TO-BE para monitoreo continuo de cuellos de botella |

### 3.1 Entregables y plazos indicados

| Entregable | Fecha límite | Estado |
|---|---|---|
| Modelo TO-BE completo en Signavio | **22 de mayo de 2026** | En progreso |
| Cuadro comparativo AS-IS vs TO-BE (KPIs) | 22 de mayo | Pendiente |
| PPT: AS-IS datos + TO-BE datos + propuesta Process Mining | Sesión siguiente | Pendiente |
| **Próxima sesión con el profesor** | **Lunes 18 de mayo, 19:00** | Agendar en Teams |

---

## 4. Investigación Realizada

### 4.1 Módulo CRP de SAP (PP-CRP) — Capacity Requirements Planning

**¿Qué es?**  
CRP (Capacity Requirements Planning) es el sub-módulo de SAP PP que **valida si los centros de trabajo tienen la capacidad necesaria** para cumplir con la demanda de producción. Se ejecuta *después* del MRP (Material Requirements Planning).

**Secuencia lógica dentro de SAP PP:**

```
[Pedido de Cliente (SD)] 
        ↓
[MRP — Material Requirements Planning (PP-MRP)]
  • Descompone la demanda con la lista de materiales (BOM)
  • Verifica stock disponible y stock de seguridad
  • Genera propuestas de pedido/producción
        ↓
[CRP — Capacity Requirements Planning (PP-CRP)]
  • Evalúa la carga de cada centro de trabajo
  • Compara la carga total vs capacidad disponible
  • Detecta sobrecargas o subutilización
  • Realiza "Capacity Leveling" (redistribuye/reprograma)
  • Genera la FECHA DE ENTREGA automáticamente
        ↓
[Orden de Producción liberada]
        ↓
[QM — Quality Management] → Inspección final
        ↓
[SD — Shipping / WM — Warehouse] → Entrega al cliente
        ↓
[FI — Facturación automática]
```

**Lo que automatiza el CRP (vs proceso AS-IS de INDUPRO):**

| Proceso AS-IS (INDUPRO) | CRP en SAP TO-BE |
|---|---|
| Planificador llena planilla manual (40 min) | Sistema genera orden automáticamente |
| No hay visibilidad de capacidad real (78% utilización invisible) | Dashboard en tiempo real de carga por centro de trabajo |
| Fecha de entrega estimada manualmente | Fecha calculada automáticamente por el sistema según carga y BOM |
| Errores de planificación → reprocesos | Balanceo de carga (Capacity Leveling) previene sobrecargas |
| Sin integración con stock de materia prima | MRP verifica materias primas antes de lanzar orden |

**Transacciones SAP clave del CRP:**
- `CM01` — Capacity planning: Load of work centers
- `CM21` — Capacity leveling (reorganización de carga)
- `CM22` — Capacity leveling: SFC planning table
- `MD01` — MRP run (prerequisito del CRP)
- `CO01` — Create production order

**Fuente:** [TutorialKart — What Is CRP in SAP PP](https://www.tutorialkart.com/what-is-capacity-requirement-planning-crp/) · [Rootstock — CRP & MRP](https://www.rootstock.com/cloud-erp-blog/an-introduction-to-how-capacity-planning-relates-to-material-requirements-planning/)

---

### 4.2 Integración de Módulos SAP involucrados en el proceso de INDUPRO

```
CLIENTE
   │  (Solicitud de pedido)
   ▼
[SD — Sales & Distribution]
   • Recepción de pedido de cliente
   • Verificación de precio y condiciones
   • Vincula con FI-AR para chequeo de crédito
   │
   ├──► [FI-AR — Financial Accounting: Accounts Receivable]
   │        • Verifica línea de crédito del cliente
   │        • Bloquea pedido si supera límite
   │        • Libera cuando crédito es aprobado
   │
   ▼ (crédito aprobado)
[MM — Materials Management]
   • Verifica stock en tiempo real (movimientos de material)
   • Si hay stock → despacho directo
   • Si no hay → dispara MRP
   │
   ▼ (sin stock)
[PP — Production Planning]
   ├── PP-MRP: explota BOM, verifica materia prima, genera propuesta
   └── PP-CRP: verifica capacidad de planta, asigna fechas, balancea carga
   │
   ▼ (orden de producción liberada)
[QM — Quality Management]
   • Inspección del lote (checklist digital)
   • Registro de resultados con trazabilidad
   │
   ▼ (lote aprobado)
[WM/LE — Warehouse / Logistics Execution]
   • Empaque y preparación con packing list digital
   • Asignación de transporte (TMS integrado)
   │
   ▼
[FI — Financial Accounting]
   • Generación automática de factura al confirmar entrega
   • Cierre del ciclo contable
```

**Módulos de SAP a mencionar en la PPT:**

| Módulo SAP | Nombre completo | Rol en el proceso |
|---|---|---|
| **SD** | Sales & Distribution | Gestión de pedidos de cliente |
| **FI-AR** | Financial Acc. – Accounts Receivable | Verificación y gestión de crédito |
| **MM** | Materials Management | Control de inventario en tiempo real |
| **PP-MRP** | Production Planning – Material Req. Planning | Planificación de necesidades de materiales |
| **PP-CRP** | Production Planning – Capacity Req. Planning | Planificación y balanceo de capacidad de planta |
| **QM** | Quality Management | Control de calidad digital con trazabilidad |
| **WM/LE** | Warehouse/Logistics Execution | Empaque, etiquetado y despacho |
| **FI** | Financial Accounting | Facturación electrónica automática |

---

### 4.3 SAP Signavio Process Intelligence — Process Mining

**¿Qué es Process Mining?**  
Es una metodología que extrae **huellas digitales** (event logs) de los sistemas ERP y de información para reconstruir automáticamente cómo se ejecutan los procesos realmente, detectar desviaciones, cuellos de botella y oportunidades de mejora.

**¿Qué hace SAP Signavio Process Intelligence?**

| Funcionalidad | Descripción |
|---|---|
| **Process Discovery** | Extrae event logs del ERP → genera automáticamente el diagrama BPMN real del proceso (no el diseñado, sino el ejecutado) |
| **Conformance Checking** | Compara el proceso ejecutado vs el modelo diseñado → detecta desviaciones |
| **Bottleneck Detection** | Identifica cuellos de botella de manera automática con datos reales |
| **Variant Analysis** | Muestra todas las variantes del proceso (caminos diferentes que toma cada instancia) |
| **KPI Dashboard** | Visualiza tiempos de ciclo, costos, frecuencias en tiempo real |
| **Integration con Build Process Automation** | Traduce hallazgos directamente en automatizaciones |

**Flujo propuesto para la PPT (como el profesor sugirió):**

```
[SAP ERP / Sistema INDUPRO]
  Genera event logs automáticamente
        ↓
[SAP Signavio Process Intelligence]
  Extrae → Transforma → Carga los datos
        ↓
  Genera diagrama de flujo real del proceso
        ↓
  Detecta: cuellos de botella, variantes, desviaciones
        ↓
[Acción] → Se alimenta de vuelta al modelo BPMN en Signavio
         → Se generan mejoras continuas
```

**Frase clave del profesor:**  
> *"Tu TO-BE tiene que estar acompañado de minería de proceso. Ahí les puedo explicar algunas cositas. El sistema extrae estos datos, los convierte en esto, se genera el proceso. Hagamos algo que se pueda rescatar."*

**Diferencia Process Insights vs Process Intelligence:**
- **SAP Signavio Process Insights** → visibilidad de alto nivel, KPIs, detección rápida de problemas
- **SAP Signavio Process Intelligence** → análisis profundo (deep-dive), variantes, causa raíz, minería completa

**Fuente:** [Signavio.com — Process Intelligence](https://www.signavio.com/es/products/process-intelligence/) · [Nagarro — Deep Dive Process Intelligence](https://www.nagarro.com/en/blog/unleashing-business-potential-sap-signavio-process-intelligence)

---

## 5. Impacto en los Modelos BPMN

### 5.1 Cambios pendientes en el AS-IS (correcciones del profesor)

> **Prioridad ALTA antes del 22 de mayo**

- [ ] **C1 — Convertir Task 2 (Validar datos) en Gateway XOR divergente**  
  Salidas: `Datos válidos (continúa)` / `Datos incompletos/incorrectos (notifica al cliente y termina o corrige)`

- [ ] **C2 — Agregar Gateway XOR de salida a la verificación de crédito**  
  Si crédito rechazado → `Send Task` (notificación al cliente) + posible `Message End Event` o loop de corrección

- [ ] **C5 — Etiquetar ambas salidas de TODOS los XOR gateways del AS-IS**  
  Actualmente los gateways de Stock y Calidad tienen etiquetas, pero revisar que sean explícitas en los 2 lados

### 5.2 Mejoras para el TO-BE (ya modeladas + pendientes)

| Elemento | Estado | Nota |
|---|---|---|
| AND Gateway (crédito ∥ stock) | ✅ Modelado | En `INDUPRO_Gestion_Pedidos_TOBE.bpmn` |
| ServiceTask verificación crédito API (FI-AR) | ✅ Modelado | Task 2A |
| ServiceTask consulta stock ERP (MM) | ✅ Modelado | Task 2B |
| Message Flow al cliente (confirmación) | ✅ Modelado | SendTask → Pool Cliente |
| Message Flow al cliente (factura) | ✅ Modelado | Message End Event |
| Gateway XOR si crédito rechazado + notificación | ⚠️ Pendiente | Agregar ruta de notificación de rechazo de crédito |
| Módulo PP-CRP en la planificación (Task 6B) | ⚠️ Pendiente | Mencionar en documentation + PPT como mejora estructural |
| Minería de procesos (Process Mining) | ❌ No modelado | Va en la PPT como propuesta adicional, no en el BPMN |

---

## 6. Plan de Acción Post-Reunión

| Tarea | Responsable | Fecha |
|---|---|---|
| Agendar reunión en Teams para lunes 18 mayo, 19:00 | Equipo | **Ya** |
| Ajustar modelo AS-IS (correcciones C1, C2, C5) | Modelador BPMN | 19 mayo |
| Agregar ruta de rechazo de crédito al TO-BE (XOR + notificación) | Modelador BPMN | 20 mayo |
| Actualizar `documentation` del Task 6B con referencia a PP-CRP | Equipo técnico | 20 mayo |
| Investigar y redactar slide de CRP para PPT | Investigador | 20 mayo |
| Investigar y redactar slide de Process Mining para PPT | Investigador | 21 mayo |
| Cuadro comparativo KPIs AS-IS vs TO-BE con valores de simulación | Todo el equipo | 21 mayo |
| TO-BE completo entregado al profesor | Equipo | **22 mayo** |

---

## 7. Citas Textuales del Profesor (Referencia de Criterios de Evaluación)

> *"Es importante detectar algo y eso es lo que quiere el jurado: una cosa que el proceso está definido, y hay cosas que ustedes tienen que mencionar que se puede modelar de esa manera."*

> *"Siempre tienen que resaltar a través de un cuadro comparativo los valores, es decir, los KPI que se obtiene del AS-IS. El TO-BE tiene que reducir, tienes que concluir algo: los cambios que has hecho han mejorado, han automatizado, han reducido, han aumentado las ventas, han reducido el tiempo de entrega."*

> *"Tu TO-BE tiene que estar acompañado de minería de proceso, y ahí les puedo explicar algunas cositas. El sistema extrae estos datos, los convierte en esto. Hagamos algo que se pueda rescatar."*

> *"Busquen esa información [CRP], eso es algo muy bueno. En base a la demanda, a la solicitud de un cliente, verifica prioridades y cómo explota la información, y se va generando la fecha de entrega."*

> *"Vayan investigando qué funcionalidades tiene Signavio con las que se puede conectar, resaltando la automatización del proceso. En su exposición tiene que ser eso: a través de Signavio permite poder esto, monitorea esto, y esto permite."*
