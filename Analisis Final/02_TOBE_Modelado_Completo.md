# TO-BE — Modelado Completo del Proceso Rediseñado
## INDUPRO S.A. | SAP Signavio Regional Challenge 2026

> **Versión:** 1.0  
> **Elaborado:** Mayo 2026  
> **Estrategia:** Automatización · Paralelización · Integración de Sistemas · Control Preventivo de Calidad

---

## ⚠️ Nota de Notación BPMN en SAP Signavio — Elementos Específicos

### A) IT Systems — NO son lanes

> **REGLA FUNDAMENTAL:** En SAP Signavio, los sistemas de IT **no son lanes (carriles)**. Los lanes representan exclusivamente actores humanos o departamentos.
>
> Los sistemas de IT (SAP Integration Suite, Portal Web, ERP Legacy, TMS, Datil.me, etc.) se modelan como **artefactos IT System** — extensión propia de SAP Signavio, similar a un *data object* o *data store*. Se colocan adyacentes a las tareas que soportan y se conectan mediante una **asociación no direccional** (línea punteada **sin flecha**), no mediante flujos de secuencia.
>
> 📘 *"The IT Systems element is a SAP Signavio-specific extension of BPMN. You use non-directional associations to connect them with activities instead of the directional associations you use for other artifacts."* — S3.1 BPMN Introductory Guide
>
> | Elemento | ¿Lane? | Cómo aparece en Signavio |
> |---|---|---|
> | Ejecutivo de Ventas | ✅ Sí | Carril horizontal del pool |
> | Analista de Finanzas | ✅ Sí | Carril horizontal del pool |
> | Operario de Planta | ✅ Sí | Carril horizontal del pool |
> | SAP Integration Suite | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
> | Portal Web de Pedidos | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
> | ERP Legacy | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
> | TMS (Beetrack) | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
> | Datil.me | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
> | Sistema QC Digital | ❌ No | Artefacto **IT System** — asociación no direccional a la tarea |
>
> Los IT Systems se registran primero en el **Signavio Dictionary** (Entregable E3) y luego se reutilizan en el diagrama arrastrando el elemento desde el Dictionary o la paleta de formas.

### B) Additional Participant — Participante Adicional

> Otra extensión de SAP Signavio. Se usa cuando una tarea tiene **un responsable principal (lane) y uno o más actores secundarios**. El activo secundario se conecta a la tarea mediante una asociación.
>
> Aplica en el TO-BE de INDUPRO:
> - **Actividad 7 (Fabricación + QC en proceso):** Responsable principal = Operario de Planta (lane). Participante adicional = **Operario de Calidad en Proceso** (nuevo rol).
> - **Actividad 9B (Reproceso residual):** Responsable principal = Operario de Planta. Participante adicional = Inspector de Calidad.

### C) Tipos de Tarea (Task Types) — BPMN Poster 2024

> Según el poster oficial BPMN 2.0 y la lectura S3.2, las tareas del TO-BE se tipifican así:
>
> | Actividad TO-BE | Tipo de tarea | Razón |
> |---|---|---|
> | 1 — Recepción vía portal | **User Task** | Persona interactúa con software (portal web) |
> | 2A — Verificación crédito API | **Service Task** | Actividad automática, sin input humano |
> | 2B — Consulta stock API | **Service Task** | Actividad automática, sin input humano |
> | 6A — Confirmación automática | **Service Task** | Email/SMS disparado automáticamente |
> | 6B — Programar producción digital | **User Task** | Planificador aprueba en el ERP |
> | 7 — Fabricación | **Manual Task** | Trabajo físico de planta (con QC digital in-proceso) |
> | 8 — Inspección QC digital | **User Task** | Inspector usa el Sistema QC Digital |
> | 10 — Empaque | **Manual Task** | Trabajo físico |
> | 11 — Asignación TMS | **Service Task** | Asignación automática por el TMS |
> | 12 — Entrega + firma digital | **User Task** | Transportista usa app TMS |
> | 13 — Factura electrónica | **Service Task** | Emisión automática, sin input humano |

### D) Signavio Dictionary — Entregable E3 obligatorio

> El caso exige como Entregable E3: *"Captura del Signavio Dictionary con los elementos registrados (mínimo: roles, sistemas, documentos)".*
>
> En el Dictionary se registran:
> - **Roles** (lanes): Ejecutivo de Ventas, Analista de Finanzas, etc.
> - **IT Systems**: SAP Integration Suite, Portal Web, ERP Legacy, Sistema QC Digital, TMS, Datil.me
> - **Documentos / Data Objects**: Formulario de pedido, Orden de producción, Informe QC digital, Packing list, Guía de remisión digital, Comprobante electrónico SRI

---

## 1. Estrategia de Rediseño — Las 4 Palancas de Mejora

El TO-BE de INDUPRO no es un catálogo de deseos tecnológicos. Es una **respuesta estructurada y directa a cada ineficiencia diagnosticada en el AS-IS**, construida dentro de las restricciones del caso.

| Palanca | Problema que resuelve | Impacto esperado |
|---|---|---|
| **1. Automatización** | Validación manual en Excel (P1); Confirmación manual (P4); Facturación manual (P8) | Eliminar tareas de transcripción y reducir errores ~15% |
| **2. Paralelización** | Pasos 3 y 4 secuenciales sin necesidad técnica (P4) | Reducir 50 min de espera innecesaria por pedido |
| **3. Integración de Sistemas** | Sistemas financiero, ERP legacy y logística desconectados (P2, P3, P7) | Única fuente de verdad; automatización de decisiones |
| **4. Control de Calidad Preventivo** | QC reactivo al final → 18% reproceso (P6) | Reducir tasa de rechazo del 18% al 5% |

---

## 2. Arquitectura de Sistemas TO-BE

### 2.1 Problema de partida: Silos de Sistemas (AS-IS)

```
AS-IS — Sistemas desconectados:

[Cliente] ──► [Correo/Teléfono] ──► [Excel] ──► [Sistema Financiero]
                                                         ↓ (manual)
                                              [ERP Legacy Inventario]
                                                         ↓ (manual)
                                          [Planilla Producción Manual]
                                                         ↓ (manual)
                                             [Órdenes de trabajo impresas]
                                                         ↓ (manual)
                                              [Sistema de Facturación]

★ RESULTADO: 4 silos independientes, sin integración, sin visibilidad
```

### 2.2 Arquitectura TO-BE: Integración vía Middleware Central

```
TO-BE — Arquitectura integrada:

[CLIENTE]
    │ (solicitud digital)
    ▼
[PORTAL WEB DE PEDIDOS] ◄──────────────────────────────────┐
    │                                                        │
    ▼                                                        │
╔═══════════════════════════════════════════════════╗       │
║     SAP INTEGRATION SUITE (MIDDLEWARE CENTRAL)    ║       │
║  ┌────────────────────────────────────────────┐  ║       │
║  │ Orquestación · APIs · Transformación · Log │  ║       │
║  └────────────────────────────────────────────┘  ║       │
╚════════╤══════════╤══════════╤═══════════╤════════╝       │
         │          │          │           │                 │
         ▼          ▼          ▼           ▼                 │
  [ERP LEGACY] [SISTEMA    [SISTEMA     [TMS           [FACTURA-
  [INVENTARIO] [FINANCIERO] [QC DIGITAL] TRANSPORTE]  CIÓN ELECTR.]
   (API REST)   (API REST)  (App Móvil)  (API REST)   (SRI-Compliant)

★ RESULTADO: Middleware único como "traductor universal" entre sistemas
```

---

## 3. Stack Tecnológico TO-BE — Definición Precisa de Herramientas

> **Principio rector del profesor:** *"Para que se conecten sistemas existe una conexión que se llama Middleware. El Middleware convierte los datos en un mismo lenguaje de un sistema. Vas a tener sistemas Legacy (los core) y los sistemas que administra el ERP. Lo que te piden es que los integres."*

### Sistema 1 — SAP Integration Suite (Middleware Central)

| Atributo | Detalle |
|---|---|
| **Herramienta** | SAP Integration Suite (Cloud Integration + API Management) |
| **Proveedor** | SAP SE (oficial) |
| **Tipo** | Platform as a Service (PaaS) — basado en SAP Business Technology Platform (SAP BTP) |
| **Rol en el proceso** | Middleware central que conecta: Portal Web ↔ ERP Legacy ↔ Sistema Financiero ↔ QC Digital ↔ TMS ↔ Facturación |
| **Funciones clave** | Orquestación de flujos de integración; transformación de formatos de datos; exposición de APIs; gestión de autenticación; logging y auditoría |
| **Actividades soportadas** | 2A (verificación crédito API); 2B (consulta stock API); 6A (confirmación automática); 6B (lanzar orden producción en ERP); 13 (trigger factura) |
| **Connectors disponibles** | REST/SOAP adapters para ERPs legacy; OData connectors; SFTP; E-mail; JDBC para bases de datos |
| **Fuente oficial** | [SAP Integration Suite — help.sap.com](https://help.sap.com/docs/integration-suite) |
| **Costo de implementación** | $10,000 (configuración, flujos, conectores) — ver Presupuesto |

**¿Por qué SAP Integration Suite y no MuleSoft u otras alternativas?**  
SAP Integration Suite es la solución oficial de SAP para conectar sistemas legacy con el ecosistema SAP. Dado que INDUPRO ya usa un ERP Legacy (posiblemente con componentes SAP) y utiliza SAP Signavio para modelado, la integración nativa con SAP BTP minimiza riesgos y tiempo de implementación. Incluye pre-built integration packs para sistemas SAP, reduciendo el costo de desarrollo.

---

### Sistema 2 — Portal Web de Pedidos

| Atributo | Detalle |
|---|---|
| **Herramienta** | Aplicación Web (construida sobre SAP Build Apps o desarrollo custom HTML5/Node.js) |
| **Proveedor** | SAP BTP Build Apps (low-code) o proveedor de desarrollo local |
| **Tipo** | Aplicación web responsiva (accesible desde browser/tablet) |
| **Rol en el proceso** | Canal de entrada de pedidos del cliente con validación automática en tiempo real |
| **Funciones clave** | Formulario estructurado de pedido; validación automática de datos (cliente, SKU, cantidades); notificación de confirmación/rechazo; visualización del estado del pedido |
| **Integración** | Se conecta al ERP Legacy y al Sistema Financiero vía SAP Integration Suite (APIs REST) |
| **Actividades soportadas** | Actividad 1 (recepción + autovalidación) |
| **Fuente oficial** | [SAP Build Apps — community.sap.com](https://community.sap.com/topics/build-apps) |
| **Costo de implementación** | $10,000 (diseño UX + desarrollo + despliegue) |

---

### Sistema 3 — API Layer del ERP Legacy (Inventario en Tiempo Real)

| Atributo | Detalle |
|---|---|
| **Herramienta** | REST API wrapper sobre el ERP Legacy existente (no se reemplaza el ERP — se expone) |
| **Tipo** | Capa de integración (API Gateway via SAP Integration Suite) |
| **Rol en el proceso** | Consultar stock disponible en tiempo real sin intervención manual |
| **Funciones clave** | Endpoint GET /inventory/{SKU} que retorna disponibilidad en tiempo real; sincronización de datos de stock entre el ERP y el Portal |
| **Integración** | SAP Integration Suite actúa como API Gateway; el ERP Legacy expone sus datos de inventario sin ser reemplazado |
| **Actividades soportadas** | Actividad 2B (consulta stock paralela) |
| **Fuente oficial** | [SAP API Business Hub](https://api.sap.com/) |
| **Costo de implementación** | $8,000 (desarrollo del API wrapper + configuración del Integration Suite connector) |

---

### Sistema 4 — API Layer del Sistema Financiero (Verificación de Crédito)

| Atributo | Detalle |
|---|---|
| **Herramienta** | REST API connector para el Sistema Financiero existente (no se reemplaza) |
| **Tipo** | Integración API via SAP Integration Suite |
| **Rol en el proceso** | Verificación automática del límite de crédito del cliente sin intervención humana |
| **Funciones clave** | Endpoint GET /credit/{clientId} que retorna: límite de crédito, crédito utilizado, crédito disponible, estado (aprobado/bloqueado); lógica de negocio: si crédito disponible ≥ monto del pedido → aprobado automáticamente |
| **Módulo conceptual** | Equivalente funcional al módulo FI-AR de SAP (Cuentas por Cobrar) |
| **Actividades soportadas** | Actividad 2A (verificación crédito paralela) |
| **Fuente oficial** | [SAP FI-AR Documentation](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/b249d650b15e4b3d9fc2077ee921abd0) |
| **Costo de implementación** | $5,000 (desarrollo API connector + reglas de negocio) |

---

### Sistema 5 — Sistema QC Digital (Control de Calidad)

| Atributo | Detalle |
|---|---|
| **Herramienta** | Aplicación web/móvil de checklists de calidad (SAP BTP Build Apps o equivalente) |
| **Tipo** | Aplicación móvil con formularios digitales + dashboard de resultados |
| **Rol en el proceso** | Control de calidad EN PROCESO durante fabricación + inspección final digital |
| **Funciones clave** | Checklist digital por lote; registro de parámetros de calidad durante fabricación; alertas automáticas si se detecta anomalía en proceso; generación de informe digital de inspección; historial de resultados por lote (trazabilidad) |
| **Impacto en el cuello de botella** | Al implementar QC en-proceso, los defectos se detectan y corrigen durante fabricación → reduce la necesidad de reproceso al finalizar → tasa de rechazo baja del 18% al 5% |
| **Actividades soportadas** | Actividades 7 (QC en-proceso durante fabricación) + 8 (inspección final digital) |
| **Nuevo rol requerido** | Operario de Calidad en-proceso (uno de los 2 nuevos roles permitidos) |
| **Costo de implementación** | $4,000 (desarrollo app + tablets para planta) |

---

### Sistema 6 — TMS (Transport Management System)

| Atributo | Detalle |
|---|---|
| **Herramienta** | Módulo TMS básico integrado vía SAP Integration Suite |
| **Opciones concretas** | SAP TM Basic (si se amplía SAP) / SaaS TMS regional (ej. Beetrack, DispatchTrack para LATAM) |
| **Tipo** | SaaS con APIs de integración |
| **Rol en el proceso** | Asignación automática de transportista disponible + tracking de entrega en tiempo real |
| **Funciones clave** | Pool de transportistas disponibles con disponibilidad en tiempo real; asignación automática basada en zona de entrega y capacidad; tracking GPS del pedido; notificación automática al cliente al despachar; firma digital de conformidad via app móvil |
| **Actividades soportadas** | Actividades 11 (asignación TMS automática) + 12 (entrega + firma digital) |
| **Fuente oficial** | [Beetrack — beetrack.com](https://www.beetrack.com/) / [SAP TM — help.sap.com](https://help.sap.com/docs/SAP_TM) |
| **Costo de implementación** | $5,500 (suscripción anual + configuración + integración) |

---

### Sistema 7 — Facturación Electrónica (SRI-Compliant)

| Atributo | Detalle |
|---|---|
| **Herramienta** | Módulo de facturación electrónica compatible con SRI (Ecuador) |
| **Opciones concretas** | Datil.me (Ecuador), Xerogroup, o extensión del sistema financiero existente |
| **Tipo** | SaaS con APIs REST |
| **Rol en el proceso** | Generación automática de comprobante electrónico al confirmar la entrega del pedido |
| **Funciones clave** | Trigger automático desde el TMS al confirmar entrega (firma digital); generación XML del comprobante; validación y autorización ante el SRI; envío automático al correo del cliente; archivado digital por 7 años |
| **Actividades soportadas** | Actividad 13 (factura electrónica automática) |
| **Fuente oficial** | [Datil — datil.co](https://datil.co) / [SRI Ecuador — sri.gob.ec](https://www.sri.gob.ec) |
| **Costo de implementación** | $2,500 (configuración + certificados + integración) |

---

## 4. Nuevos Roles Propuestos (Máx. 2 permitidos)

### Rol 1 — Analista de Integración de Sistemas

| Atributo | Detalle |
|---|---|
| **Nombre del rol** | Analista de Integración de Sistemas |
| **Costo/hora** | $18/hr |
| **Disponibilidad** | 1 disponible · 8h/día |
| **Responsabilidad** | Administrar y monitorear el SAP Integration Suite; configurar y mantener los flujos de integración entre sistemas; gestionar incidencias de API; generar reportes de rendimiento de la integración |
| **Actividades que soporta (TO-BE)** | Monitoreo de actividades 2A, 2B (APIs paralelas); troubleshooting de 6A (confirmación automática); soporte de 13 (facturación electrónica) |
| **Participación en implementación** | Lidera la configuración técnica de SAP Integration Suite (Fase 1 y 2) |
| **Justificación** | El middleware requiere administración técnica continua post-implementación; no puede depender de consultores externos indefinidamente |

### Rol 2 — Operario de Control de Calidad en Proceso

| Atributo | Detalle |
|---|---|
| **Nombre del rol** | Operario de Control de Calidad en Proceso |
| **Costo/hora** | $11/hr (misma tarifa que Inspector de Calidad) |
| **Disponibilidad** | 1 disponible · turno de 8h |
| **Responsabilidad** | Ejecutar checklist digital de calidad durante el proceso de fabricación (QC en-proceso); registrar parámetros en el Sistema QC Digital; alertar sobre desviaciones antes de finalizar el lote |
| **Actividades que soporta (TO-BE)** | Actividad 7 (QC en-proceso durante fabricación — en paralelo con operarios de planta) |
| **Justificación** | La reducción de la tasa de reproceso del 18% al 5% requiere un operario dedicado al control en-proceso. El caso permite 2 roles nuevos; este es el segundo. |
| **ROI del rol** | Ahorro mensual por reducción de reprocesos: (18%-5%) × 35% × 1,200 pedidos × $12 = $654/mes; costo del rol: $11/hr × 8h/día × 22 días = $1,936/mes → El ahorro en reprocesos cubre ~34% del costo del rol, más el impacto en capacidad de planta. |

---

## 5. Tabla de Actividades TO-BE — Completa con Herramientas y Tipos de Tarea

> **Nota Signavio:** Cada tarea debe tener el tipo correcto asignado en el editor. Los IT Systems se adjuntan como **artefactos IT System** mediante asociación no direccional. El Operario QC en-proceso se modela como **Additional Participant** en la Actividad 7 (no es un lane separado).

| # | Actividad TO-BE | Lane (responsable principal) | **IT System (artefacto)** | **Tipo de tarea** | Duración (min) | Costo/hr | Costo (USD) | Δ vs AS-IS |
|---|---|---|---|---|---|---|---|---|
| 1 | Recepción de solicitud vía **portal web** con auto-validación | Ejecutivo de Ventas | **Portal Web** | User Task | **15** | $12 | **$3.00** | −60 min · −$12 |
| AND-S | **[AND Split]** Inicio paralelo de verificaciones | — | **SAP Integration Suite** | Gateway AND | 1 | — | — | Nuevo elemento |
| 2A | **[PARALELO]** Verificación de crédito automática via API | Analista de Finanzas | **API Sistema Financiero / SAP Integration Suite** | Service Task | **15** | $13 | **$3.25** | −45 min · −$9.75 |
| 2B | **[PARALELO]** Consulta de stock en tiempo real via API | Coordinador de Inventarios | **ERP Legacy (API) / SAP Integration Suite** | Service Task | **10** | $10 | **$1.67** | −40 min · −$6.66 |
| AND-J | **[AND Join]** Convergencia de resultados | — | **SAP Integration Suite** | Gateway AND | 1 | — | — | Nuevo elemento |
| 5 | **[Gateway XOR]** ¿Crédito aprobado Y stock disponible? | — | **SAP Integration Suite** | Gateway XOR | 2 | — | — | Automatizado |
| 6A | **[Ruta SÍ]** Confirmación automática al cliente (email/SMS) | Ejecutivo de Ventas | **Portal Web / SAP Integration Suite** | Service Task | **5** | $12 | **$1.00** | −15 min · −$3 |
| 6B | **[Ruta NO]** Programación de producción digital | Planificador de Producción | **ERP Legacy (módulo PP)** | User Task | **20** | $14 | **$4.67** | −20 min · −$4.66 |
| 7 | Fabricación del producto **con QC en-proceso** *(Additional Participant: Op. QC en-proceso)* | Operario de Planta | **Sistema QC Digital** | Manual Task | **120** *(inamovible)* | $8 | **$16.00** | = tiempo; −13pp en rechazo |
| 8 | Inspección final de calidad | Inspector de Calidad | **Sistema QC Digital** | User Task | **30** *(inamovible)* | $11 | **$5.50** | = tiempo |
| 9 | **[Gateway XOR]** ¿Pasa calidad? | Inspector de Calidad | — | Gateway XOR | 2 | $11 | **$0.37** | 82% → **95%** aprobación |
| 9B | **[Ruta Residual]** Reproceso del lote *(Additional Participant: Inspector de Calidad)* | Operario de Planta | — | Manual Task | **60** | $8 | **$8.00** | −30 min · −$4 |
| 10 | Empaque y preparación para despacho | Coordinador de Logística | — | Manual Task | **15** | $10 | **$2.50** | −10 min · −$1.67 |
| 11 | Asignación de transportista **automática** | Coordinador de Logística | **TMS (Beetrack)** | Service Task | **10** | $10 | **$1.67** | −20 min · −$3.33 |
| 12 | Entrega al cliente + firma digital de conformidad | Transportista | **TMS (Beetrack) — App móvil** | User Task | **45** *(física)* | $10 | **$7.50** | = tiempo |
| 13 | Factura electrónica generada **automáticamente** al confirmar entrega | Analista de Finanzas | **Datil.me / SAP Integration Suite** | Service Task | **5** | $13 | **$1.08** | −15 min · −$3.25 |

---

## 6. Cálculo de KPIs TO-BE

### 6.1 Ruta con fabricación, sin reproceso (ruta principal)

```
Tiempo TO-BE = 15 + 1 (AND-S) + MAX(15, 10) [paralelo] + 1 (AND-J) + 2 (XOR) + 20 + 120 + 30 + 2 + 15 + 10 + 45 + 5
             = 15 + 1 + 15 + 1 + 2 + 20 + 120 + 30 + 2 + 15 + 10 + 45 + 5
             = 281 minutos ✅ (meta: < 350 min)
```

```
Costo TO-BE = $3.00 + $3.25 + $1.67 + $0 (AND) + $0 (XOR) + $4.67 + $16.00 + $5.50 + $0.37 + $2.50 + $1.67 + $7.50 + $1.08
            = $47.21 ✅ (meta: < $70.00)
```

### 6.2 Ruta con fabricación + reproceso (ruta residual, 5% de ocurrencia)

```
Tiempo = 281 + 60 (reproceso residual) = 341 minutos ✅ (< 350 min)
Costo  = $47.21 + $8.00 = $55.21 ✅ (< $70.00)
```

### 6.3 Comparativa KPIs AS-IS vs TO-BE

| KPI | AS-IS (correcto) | TO-BE | Meta | Reducción | % Mejora |
|---|---|---|---|---|---|
| **Tiempo de ciclo (fabricación + reproceso)** | 595 min | **341 min** | < 350 min | −254 min | **−42.7%** ✅ |
| **Tiempo de ciclo (fabricación sin reproceso)** | 505 min | **281 min** | < 350 min | −224 min | **−44.4%** ✅ |
| **Costo por pedido (sin reproceso)** | $101.91 | **$47.21** | < $70.00 | −$54.70 | **−53.7%** ✅ |
| **Costo por pedido (con reproceso)** | $101.91 | **$55.21** | < $70.00 | −$46.70 | **−45.8%** ✅ |
| **Tasa de reproceso** | 18% | **5%** | < 5% | −13pp | **−72.2%** ✅ |
| **Tiempo verificación crédito** | 60 min | **15 min (paralelo)** | < 15 min | −45 min | **−75%** ✅ |
| **Tiempo consulta stock** | 50 min | **10 min (paralelo)** | — | −40 min | **−80%** ✅ |
| **Tiempo empaque** | 25 min | **15 min** | — | −10 min | **−40%** ✅ |
| **Tiempo asignación transporte** | 30 min | **10 min** | — | −20 min | **−67%** ✅ |

> **El tiempo de fabricación (120 min) y la inspección final (30 min) son restricciones técnico-regulatorias inamovibles. Ambos se mantienen en el TO-BE.**

---

## 7. Explicación Narrativa del Proceso TO-BE

El proceso TO-BE de INDUPRO S.A. inicia cuando el cliente accede al **Portal Web de Pedidos**, una aplicación web integrada que reemplaza completamente el flujo de correo electrónico y hojas de Excel. El cliente ingresa los datos de su pedido (cliente, productos, cantidades) y el portal los valida automáticamente en tiempo real contra la base de datos del ERP Legacy vía API — sin intervención humana. Este paso dura **15 minutos** (reducción del 50% respecto a los 30+45 min del AS-IS).

Una vez recibida la solicitud validada, el **SAP Integration Suite** actúa como orquestador central y lanza en paralelo (Gateway AND) dos verificaciones simultáneas:

- **2A — Verificación de crédito automática:** Una API consulta al Sistema Financiero el límite de crédito disponible del cliente. Si el monto del pedido está dentro del límite, la aprobación es automática en **15 minutos** (vs 60 minutos manuales en el AS-IS). No requiere intervención del Analista de Finanzas para casos estándar.
- **2B — Consulta de stock en tiempo real:** Una API consulta al ERP Legacy el stock disponible de los SKUs del pedido en **10 minutos** (vs 50 minutos con registros físicos en el AS-IS).

El Gateway AND Join reúne ambos resultados. El sistema decide automáticamente (Gateway XOR):

**Si HAY crédito Y HAY stock disponible (70% de los casos):**  
El Portal Web envía automáticamente un correo de confirmación al cliente en **5 minutos** (vs 20 minutos manuales). El proceso pasa directamente al empaque.

**Si NO hay stock o NO hay crédito aprobado (30% de los casos):**  
El Planificador de Producción recibe en su pantalla la orden de producción ya pre-configurada por el ERP (con datos del pedido validados). Solo necesita revisar y aprobar en el sistema en **20 minutos** (vs 40 minutos llenando planillas manuales). Los Operarios de Planta reciben órdenes de trabajo digitales en sus terminales.

Durante la **Fabricación** (120 min — tiempo inamovible), el nuevo **Operario de Control de Calidad en Proceso** ejecuta el Sistema QC Digital para monitorear parámetros críticos en tiempo real. Las desviaciones se detectan y corrigen durante la fabricación, no al final. Esto reduce la probabilidad de rechazo en la inspección final del 18% al 5%.

La **Inspección Final de Calidad** (30 min — inamovible) se realiza con el Sistema QC Digital, generando un registro electrónico con trazabilidad completa del lote. Si el lote aprueba (95% de los casos), el proceso avanza. Si es rechazado (5% residual), el reproceso ahora dura **60 minutos** (vs 90 minutos en el AS-IS) porque gran parte de las correcciones ya se aplicaron durante la fabricación.

El **Empaque** (15 min) usa un sistema de packing list digital que genera automáticamente las etiquetas y la documentación del despacho. La **Asignación del transportista** (10 min) se hace automáticamente a través del TMS, que selecciona el transportista disponible según zona de entrega sin llamadas telefónicas.

La **Entrega** (45 min — físicamente inamovible) se confirma con firma digital del cliente en la app del transportista. Esta confirmación digital dispara automáticamente la **Factura Electrónica** (5 min) a través del sistema de facturación, que la envía en tiempo real al cliente y la registra ante la autoridad fiscal (SRI).

---

## 8. Caracterización del Proceso TO-BE

### 8.1 Ficha del Proceso TO-BE

| Campo | Descripción |
|---|---|
| **Nombre** | Gestión de Pedidos del Cliente — TO-BE |
| **Alcance** | Solicitud digital del cliente → Entrega confirmada + Factura electrónica |
| **Propietario** | Gerencia de Ventas y Operaciones / Analista de Integración (monitoreo digital) |
| **Frecuencia** | ~1,200 casos/mes (40 pedidos/día laboral) |
| **Jornada laboral** | 8 horas diarias, lunes a viernes (480 min/día) |
| **Notación** | BPMN 2.0 estricto |
| **Herramienta de modelado** | SAP Signavio Process Manager |

### 8.2 Entradas y Salidas del Proceso TO-BE

| Elemento | AS-IS | TO-BE |
|---|---|---|
| **Entrada principal** | Correo / Teléfono (no estructurado) | Portal Web con formulario estructurado |
| **Entrada secundaria** | Datos del cliente en Excel (manual) | Datos validados automáticamente por API del ERP |
| **Salida principal** | Producto entregado + firma en papel | Producto entregado + firma digital en app |
| **Salida secundaria** | Factura emitida manualmente (20 min) | Factura electrónica automática (5 min) |

### 8.3 Roles del Proceso TO-BE

| Rol | Tipo | Costo/hora | Actividades en TO-BE | Reducción de carga vs AS-IS |
|---|---|---|---|---|
| Ejecutivo de Ventas | Humano (existente) | $12/hr | 1 (portal web), 6A (supervisión) | Elimina transcripción manual en Excel |
| Analista de Finanzas | Humano (existente) | $13/hr | Monitoreo 2A; 13 (supervisión factura) | Elimina verificación manual de crédito |
| Coordinador de Inventarios | Humano (existente) | $10/hr | Monitoreo 2B | Elimina consulta manual de stock |
| Planificador de Producción | Humano (existente) | $14/hr | 6B (aprobación digital) | Elimina llenado manual de planilla |
| Operario de Planta | Humano (existente) | $8/hr | 7 (fabricación) | Sin cambio en fabricación |
| Inspector de Calidad | Humano (existente) | $11/hr | 8 (inspección digital), 9 (decisión QC) | Herramienta digital; trazabilidad |
| Coordinador de Logística | Humano (existente) | $10/hr | 10 (empaque digital), 11 (supervisión TMS) | Elimina llamadas telefónicas |
| Transportista | Humano externo | $10/hr | 12 (entrega + firma digital) | App de firma; sin papel |
| **Analista de Integración de Sistemas** | **Humano (NUEVO)** | **$18/hr** | Monitoreo middleware; APIs; incidencias | Nuevo rol habilitador del TO-BE |
| **Operario de Control de Calidad en Proceso** | **Humano (NUEVO)** | **$11/hr** | 7 (QC en-proceso paralelo a fabricación) | Nuevo rol para reducir reprocesos |

### 8.4 Sistemas del Proceso TO-BE

| Sistema | Tipo | Actividades | Integración |
|---|---|---|---|
| **Portal Web de Pedidos** | Aplicación web | 1 | Se conecta vía Integration Suite a ERP y Sistema Financiero |
| **SAP Integration Suite** | Middleware / PaaS | AND-Split, AND-Join, 2A trigger, 2B trigger, 6A trigger, 13 trigger | Núcleo de integración de todos los sistemas |
| **API ERP Legacy (Inventario)** | REST API | 2B | Expuesto vía Integration Suite |
| **API Sistema Financiero** | REST API | 2A | Expuesto vía Integration Suite |
| **ERP Legacy (Módulo PP)** | ERP (existente) | 6B | Recibe órdenes de producción vía Integration Suite |
| **Sistema QC Digital** | App móvil/web | 7, 8, 9 | Standalone + registro en ERP |
| **TMS (Beetrack/SAP TM)** | SaaS | 11, 12 | Integrado vía Integration Suite |
| **Sistema Facturación Electrónica** | SaaS (Datil.me) | 13 | Trigger automático desde TMS vía Integration Suite |

### 8.5 Documentos y Artefactos del Proceso TO-BE

| Documento | Formato AS-IS | Formato TO-BE |
|---|---|---|
| Solicitud de pedido | Correo/Excel | Formulario digital en portal (JSON/XML) |
| Confirmación de pedido | Correo manual | Email/SMS automático desde Integration Suite |
| Orden de producción | Planilla impresa | Registro digital en ERP con timestamp |
| Informe de inspección de calidad | Checklist papel | Registro digital en Sistema QC con firma digital |
| Packing list | Manual | Generado automáticamente por sistema logístico |
| Guía de remisión | Impresa | Digital en app TMS |
| Comprobante de entrega | Firma en papel | Firma digital en app transportista |
| Factura | Manual en sistema | Comprobante electrónico XML (SRI) enviado automáticamente |

---

## 9. Diagrama Lógico del Flujo TO-BE

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PROCESO TO-BE — INDUPRO S.A.                           │
│              Sistema central: SAP Integration Suite (Middleware)                │
└─────────────────────────────────────────────────────────────────────────────────┘

[CLIENTE] ──► (solicitud web)
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│ VENTAS    [1] Recepción + autovalidación en Portal Web         │
│               (15 min / $3.00)                                  │
│               ► Sistema: Portal Web + SAP Integration Suite    │
└─────────────────────────────┬──────────────────────────────────┘
                              │
                              ▼
                    [AND SPLIT — SAP Integration Suite]
                     ┌────────────────────────────────┐
                     │                                │
                     ▼                                ▼
┌─────────────────────────┐       ┌─────────────────────────────┐
│ FINANZAS                │       │ INVENTARIOS                 │
│ [2A] Verificación       │       │ [2B] Consulta stock         │
│ crédito automática      │       │ tiempo real                 │
│ (15 min / $3.25)        │       │ (10 min / $1.67)            │
│ ► API Sistema Financiero│       │ ► API ERP Legacy            │
│   vía Integration Suite │       │   vía Integration Suite     │
└─────────────────────────┘       └─────────────────────────────┘
                     │                                │
                     └────────────┬───────────────────┘
                                  │
                                  ▼
                    [AND JOIN — SAP Integration Suite]
                                  │
                                  ▼
                  [XOR] ¿Crédito OK Y Stock OK? (2 min — automático)
                         ┌────────────────────────────┐
                     SÍ (70%)                     NO (30%)
                         │                            │
                         │            ┌───────────────┘
                         │            ▼
                         │  ┌──────────────────────────────────────────────────┐
                         │  │ PLANIF. [6B] Programar producción digital         │
                         │  │             (20 min / $4.67)                      │
                         │  │             ► ERP Legacy Módulo PP                │
                         │  │                                                   │
                         │  │ PLANTA  [7]  Fabricación + QC en-proceso          │
                         │  │             (120 min / $16.00)                    │
                         │  │             ⚠️ RESTRICCIÓN TÉCNICA INAMOVIBLE     │
                         │  │             ► Órdenes digitales + Sistema QC      │
                         │  │             ► Operario de Calidad en-proceso      │
                         │  │             ► Monitoreo continuo de parámetros    │
                         │  │                                                   │
                         │  │ CALIDAD [8]  Inspección final (digital)           │
                         │  │             (30 min / $5.50)                      │
                         │  │             ⚠️ REQUERIMIENTO REGULATORIO          │
                         │  │             ► Sistema QC Digital                  │
                         │  │                                                   │
                         │  │         [XOR] ¿Pasa calidad? (2 min / $0.37)     │
                         │  │          APRUEBA (95%)    RECHAZA (5%)            │
                         │  │              │               │                    │
                         │  │              │   [9B] Reproceso (60 min / $8.00) │
                         │  │              │        ▼                           │
                         │  │              └────────┘                           │
                         │  └──────────────────────┬─────────────────────────── │
                         │                         │
                         ▼                         ▼
            ┌─────────────────────────────────────────────────────┐
            │ VENTAS  [6A] Confirmación automática al cliente      │
            │              (5 min / $1.00)                         │
            │              ► Portal Web + Email API + Int. Suite   │
            └──────────────────────────┬──────────────────────────┘
                                       │ (convergencia de rutas)
                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ LOGÍSTICA [10] Empaque con packing list digital  (15 min/$2.50) │
│                ► Sistema etiquetado digital                       │
│                                                                   │
│           [11] Asignación transportista automática(10 min/$1.67) │
│                ► TMS (Beetrack/SAP TM)                           │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ ENTREGA   [12] Entrega + firma digital           (45 min/$7.50) │
│                ► App TMS móvil (transportista)                   │
│                ► Firma digital del cliente                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │ (trigger automático al confirmar entrega)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ FINANZAS  [13] Factura electrónica automática     (5 min/$1.08) │
│                ► Datil.me / Sistema Facturación SRI-Compliant   │
│                ► SAP Integration Suite (orquesta la emisión)    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                           [FIN] ── Pedido entregado + Factura SRI emitida
```

---

## 10. Mapeo "Sistema → Actividades" (Por solicitud del profesor)

> *"Tienes que justificar: estas actividades van a ser administradas por este sistema. Señalas todas estas tareas, se va a automatizar, digamos, acá en este ejemplo. Todas estas se van a agrupar y se van a centralizar en este sistema."*

### Agrupación por sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│ PORTAL WEB DE PEDIDOS                                               │
│ ├── Actividad 1: Recepción + autovalidación de datos               │
│ └── Actividad 6A: Confirmación automática al cliente                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ SAP INTEGRATION SUITE (Middleware)                                  │
│ ├── AND Split/Join: Orquestación de paralelismo                     │
│ ├── Actividad 2A: Llamada a API del Sistema Financiero              │
│ ├── Actividad 2B: Llamada a API del ERP Legacy (inventario)        │
│ ├── Gateway XOR (crédito + stock): Decisión automática              │
│ ├── Actividad 6A: Trigger de confirmación por email/SMS             │
│ ├── Actividad 6B: Lanzamiento de orden en ERP Legacy               │
│ └── Actividad 13: Trigger de emisión de factura electrónica         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ERP LEGACY (API Inventario)                                         │
│ └── Actividad 2B: Responde disponibilidad de stock en tiempo real   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ API SISTEMA FINANCIERO (Crédito)                                    │
│ └── Actividad 2A: Retorna estado de crédito del cliente             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ ERP LEGACY (Módulo PP — Producción)                                 │
│ └── Actividad 6B: Gestión de orden de producción digital            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ SISTEMA QC DIGITAL (App móvil/web)                                  │
│ ├── Actividad 7: Checklist en-proceso durante fabricación           │
│ ├── Actividad 8: Inspección final digital con trazabilidad          │
│ └── Gateway 9: Resultado de calidad (dato digital para decisión)    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ TMS — TRANSPORT MANAGEMENT SYSTEM (Beetrack/SAP TM)                │
│ ├── Actividad 11: Asignación automática de transportista            │
│ └── Actividad 12: Tracking de entrega + firma digital               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ SISTEMA FACTURACIÓN ELECTRÓNICA (Datil.me)                          │
│ └── Actividad 13: Emisión automática de comprobante SRI             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11. Configuración de Simulación en SAP Signavio — TO-BE

> **Fuente:** S5.2 — Performing Simulations in SAP Signavio + Caso INDUPRO (Sección 4 y Fase 3)
>
> ⚠️ Usar **siempre minutos** en la versión académica — nunca horas ni días (puede causar inestabilidad). Ejecutar primero en modo **"Un caso"** para verificar, luego **"Múltiples casos"** con duración 480 min (1 día hábil).

### Tab Costs (Costos fijos por actividad — NO incluye labor)

> Los costos de mano de obra se configuran en **Resources**, no aquí. En Costs solo van costos fijos de materiales, licencias u otros gastos directos de la tarea.

| Actividad | Costo fijo por ejecución (USD) | Concepto |
|---|---|---|
| 1 — Recepción portal | $0 | Sin costo fijo adicional |
| 2A — Verificación crédito API | $0 | Servicio incluido en licencia Integration Suite |
| 2B — Consulta stock API | $0 | Servicio incluido en licencia Integration Suite |
| 6B — Programar producción | $0 | Sistema existente |
| 7 — Fabricación | $0 | Materiales no incluidos en proceso |
| 8 — Inspección QC | $0 | |
| 9B — Reproceso | $0 | |
| 10 — Empaque | $0 | |
| 11 — Asignación TMS | $0 | Incluido en suscripción Beetrack |
| 12 — Entrega | $0 | |
| 13 — Factura | $0 | Incluido en suscripción Datil.me |

### Tab Duration (Tiempos de ejecución en MINUTOS)

| Actividad | Duración (min) |
|---|---|
| 1 — Recepción portal | 15 |
| 2A — Verificación crédito (paralelo) | 15 |
| 2B — Consulta stock (paralelo) | 10 |
| 6A — Confirmación automática | 5 |
| 6B — Programar producción | 20 |
| 7 — Fabricación | 120 |
| 8 — Inspección QC | 30 |
| 9B — Reproceso | 60 |
| 10 — Empaque | 15 |
| 11 — Asignación TMS | 10 |
| 12 — Entrega | 45 |
| 13 — Factura | 5 |

### Tab Frequency (Probabilidades de gateways — deben sumar 100%)

| Gateway | Ruta | Probabilidad |
|---|---|---|
| XOR: ¿Crédito OK Y Stock OK? | Sí (hay crédito + stock) | **70%** |
| XOR: ¿Crédito OK Y Stock OK? | No (sin crédito o sin stock) | **30%** |
| XOR: ¿Pasa calidad? | Aprueba | **95%** |
| XOR: ¿Pasa calidad? | Rechaza (reproceso) | **5%** |

> Frecuencia de llegada: 4 pedidos/día (mismo que AS-IS para comparación directa)

### Tab Resources (Tarifas por hora — aquí se configura el costo laboral)

| Lane (carril) | Costo/hora (USD) | Horas/día | Días/semana |
|---|---|---|---|
| Ejecutivo de Ventas | $12 | 8 | L-V |
| Analista de Finanzas | $13 | 8 | L-V |
| Coordinador de Inventarios | $10 | 8 | L-V |
| Planificador de Producción | $14 | 8 | L-V |
| Operario de Planta | $8 | 8 | L-V |
| Inspector de Calidad | $11 | 8 | L-V |
| Coordinador de Logística | $10 | 8 | L-V |
| Transportista | $10 | 8 | L-V |
| Analista de Integración (nuevo) | $18 | 8 | L-V |
| Operario QC en Proceso (nuevo) | $11 | 8 | L-V |

> **Resultado esperado en simulación TO-BE (1 caso):** Tiempo ciclo ~281 min · Costo ~$47.21

---

## 12. Validación contra Restricciones del Caso

| Restricción del Caso | Valor | TO-BE | ¿Cumple? |
|---|---|---|---|
| Fabricación por lote estándar | 120 min INAMOVIBLE | 120 min mantenido | ✅ |
| Inspección final de calidad | 30 min INAMOVIBLE | 30 min mantenido | ✅ |
| Presupuesto máximo | USD 50,000 | USD 50,000 exactos | ✅ |
| Costo por pedido TO-BE | No superar $70.00 | $47.21 (sin reproceso) / $55.21 (con reproceso) | ✅ |
| Personal adicional máximo | 2 nuevos roles | 2 nuevos roles propuestos | ✅ |
| Ventana de despacho | 07:00 - 14:00 | TMS respeta ventana de despacho | ✅ |
| Jornada laboral | 8h/día, L-V | Todos los tiempos en minutos (nunca horas/días) | ✅ |
| Notación BPMN 2.0 | Estricta | BPMN 2.0 con swimlanes (solo roles) + IT System artifacts (sistemas) | ✅ |
| IT Systems como artefactos | No son lanes | IT Systems con asociación no direccional (sin flecha) | ✅ |
| Tiempo total < 350 min | Meta | 281 min (sin reproceso) / 341 min (con reproceso) | ✅ |

---

## 13. Propuesta Adicional — SAP Signavio Process Intelligence (Process Mining)

> *"Tu TO-BE tiene que estar acompañado de minería de proceso. El sistema extrae estos datos, los convierte en esto, se genera el proceso."* — Prof. Jimmy

Como propuesta complementaria al TO-BE, se propone implementar **SAP Signavio Process Intelligence** como capa de monitoreo continuo del proceso rediseñado.

| Funcionalidad | Aplicación en INDUPRO |
|---|---|
| **Process Discovery** | Extraer event logs del ERP Legacy y del Integration Suite para reconstruir automáticamente cómo se ejecuta el proceso TO-BE en la realidad |
| **Conformance Checking** | Comparar el proceso ejecutado vs el TO-BE modelado → detectar desviaciones antes de que generen cuellos de botella |
| **Bottleneck Detection** | Identificar automáticamente dónde se acumula tiempo en el flujo (ej: si el portal tiene alta latencia en horas pico) |
| **KPI Dashboard** | Visualizar en tiempo real: tiempo de ciclo promedio, tasa de reproceso, porcentaje de créditos aprobados, tiempo de entrega |
| **Variant Analysis** | Detectar variantes del proceso (pedidos que siguen rutas no esperadas) |

Esta capa de Process Mining garantiza que la mejora del TO-BE sea **sostenible y medible** en el tiempo, habilitando la mejora continua basada en datos reales.

---

*Documento elaborado como parte del SAP Signavio Regional Challenge 2026*  
*Equipo participante — ESPOL*
