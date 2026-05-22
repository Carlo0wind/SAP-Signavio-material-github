# Plan de Implementación — Transformación Digital del Proceso de Gestión de Pedidos
## INDUPRO S.A. | SAP Signavio Regional Challenge 2026

> **Versión:** 1.0  
> **Horizonte:** 90 días calendario  
> **Presupuesto total:** USD 50,000 (restricción del caso)  
> **Fecha de inicio estimada:** Junio 2026  

---

## 1. Visión General del Plan

El plan de implementación de INDUPRO S.A. adopta un **enfoque por fases** que permite entregar valor incremental, reducir riesgos y ajustarse al presupuesto de USD 50,000. La implementación se divide en **3 fases de 30 días** cada una, con priorización basada en el impacto en los KPIs críticos.

### Principio de priorización

```
Alta prioridad → Lo que reduce el tiempo de ciclo más rápidamente
Media prioridad → Lo que reduce costos sin impactar la operación
Baja prioridad → Mejoras de continuidad y optimización continua
```

### Fases del plan

| Fase | Nombre | Duración | Sistemas implementados | KPI objetivo |
|---|---|---|---|---|
| **Fase 1** | Integración y Portal | Días 1-30 | Portal Web + SAP Integration Suite + APIs ERP/Financiero | Eliminar pasos manuales 1-4 |
| **Fase 2** | Calidad y Producción | Días 31-60 | Sistema QC Digital + Mejora Módulo PP ERP | Reducir reproceso al 5% |
| **Fase 3** | Logística, Facturación y Estabilización | Días 61-90 | TMS + Facturación Electrónica + Capacitación + Go-Live | Proceso TO-BE completo en producción |

---

## 2. Roles Involucrados en la Implementación

### 2.1 Roles Internos (de INDUPRO — usando tarifas del caso)

| Rol | Costo/hora (caso) | Dedicación a implementación | Justificación |
|---|---|---|---|
| Ejecutivo de Ventas | $12/hr | 25% de su tiempo (2h/día) durante Fase 1 y 3 | Lidera el diseño del portal web y la capacitación de su área |
| Analista de Finanzas | $13/hr | 20% de su tiempo (1.6h/día) durante Fase 1 | Define reglas de negocio para la API de crédito |
| Coordinador de Inventarios | $10/hr | 20% de su tiempo (1.6h/día) durante Fase 1 | Define estructura de datos de stock para la API |
| Planificador de Producción | $14/hr | 20% de su tiempo (1.6h/día) durante Fase 2 | Valida el módulo digital de planificación de producción |
| Operario de Planta (ref.) | $8/hr | 10% de su tiempo durante Fase 2 | Pruebas piloto de las órdenes de trabajo digitales |
| Inspector de Calidad | $11/hr | 25% de su tiempo durante Fase 2 | Diseña checklists QC digital; lidera pruebas del sistema |
| Coordinador de Logística | $10/hr | 25% de su tiempo durante Fase 3 | Lidera implementación del TMS y capacitación logística |
| Analista de Finanzas | $13/hr | 15% de su tiempo durante Fase 3 | Configura y prueba el módulo de facturación electrónica |

> **Nota:** Los costos de dedicación interna forman parte del costo operativo existente de INDUPRO (nómina). No se suman al presupuesto de $50,000, pero se documentan para transparencia y justificación de la carga de cambio para el personal.

### 2.2 Nuevos Roles (contratados en la implementación)

| Rol | Costo/hora | Participación | Fase de inicio |
|---|---|---|---|
| **Analista de Integración de Sistemas** (Nuevo Rol 1) | $18/hr | 100% desde Semana 1; gestión del Integration Suite | Desde día 1 (contratación previa a inicio) |
| **Operario de Control de Calidad en Proceso** (Nuevo Rol 2) | $11/hr | Incorporación en Fase 2 | Día 31 |

### 2.3 Consultores Externos (incluidos en el presupuesto de $50,000)

| Perfil | Tarifa de mercado | Horas estimadas | Participación |
|---|---|---|---|
| Consultor SAP Integration Suite (Senior) | $80/hr | 80 horas | Fase 1: Arquitectura y configuración del middleware |
| Desarrollador Web / API (Full-stack) | $55/hr | 120 horas | Fases 1-2: Portal web + APIs ERP + APIs Financiero |
| Especialista TMS / Logística | $60/hr | 40 horas | Fase 3: Implementación TMS |
| Instructor de Capacitación | $50/hr | 40 horas | Fase 3: Training del personal |

---

## 3. Fase 1 — Integración y Portal (Días 1-30)

### Objetivo de Fase 1
Desplegar el Portal Web de Pedidos y establecer las integraciones API con el ERP Legacy (inventario) y el Sistema Financiero, permitiendo que las actividades 1, 2A y 2B del TO-BE funcionen de manera automatizada.

### Actividades de Fase 1

| ID | Actividad | Responsable | Duración | Horas estimadas | Costo asociado |
|---|---|---|---|---|---|
| F1.1 | **Levantamiento de requisitos técnicos** — Documentar la estructura de datos del ERP Legacy (inventario) y del Sistema Financiero (crédito) | Analista de Integración + Coordinador de Inventarios + Analista de Finanzas | 5 días | Analista Integración: 40h · Coord. Inv: 16h · Analista Fin: 16h | Interno (nómina) |
| F1.2 | **Configuración del tenant SAP Integration Suite** — Provisionar el ambiente en SAP BTP; configurar conectores; establecer políticas de seguridad (OAuth2, SSL) | Analista de Integración + Consultor SAP (externo) | 7 días | Analista Integración: 56h · Consultor SAP: 35h (×$80=$2,800) | $2,800 consultores |
| F1.3 | **Desarrollo API Layer ERP Legacy — Inventario** — Crear REST API wrapper sobre la base de datos del ERP legacy; endpoint: GET /inventory/{sku}; retorna: stock disponible, unidad, ubicación | Desarrollador Web (externo) | 8 días | Desarrollador: 40h (×$55=$2,200) · Analista Integración: 16h | $2,200 desarrollo |
| F1.4 | **Desarrollo API Layer Sistema Financiero — Crédito** — Crear REST API wrapper sobre el sistema financiero; endpoint: GET /credit/{clientId}; retorna: límite, utilizado, disponible, estado | Desarrollador Web (externo) | 6 días | Desarrollador: 30h (×$55=$1,650) · Analista de Finanzas: 16h | $1,650 desarrollo |
| F1.5 | **Desarrollo del Portal Web de Pedidos** — Diseño UX/UI del formulario; desarrollo frontend (HTML5/React); integración con APIs via Integration Suite; formulario de pedido con validación en tiempo real | Desarrollador Web (externo) | 12 días | Desarrollador: 50h (×$55=$2,750) · Ejecutivo de Ventas: 24h (revisión) | $2,750 desarrollo |
| F1.6 | **Pruebas de integración E2E (End-to-End)** — Prueba de flujo completo: solicitud portal → API inventario → API crédito → respuesta integrada | Analista de Integración + Ejecutivo de Ventas + Coord. de Inventarios + Analista de Finanzas | 5 días | Analista Integración: 40h · Resto: 8h c/u | Interno |
| F1.7 | **Ajustes y correcciones** — Corrección de bugs; ajuste de tiempos de respuesta de APIs (SLA: < 3 segundos); optimización de queries | Desarrollador Web + Analista de Integración | 3 días | Desarrollador: 15h (×$55=$825) · Analista Integración: 24h | $825 ajustes |
| **TOTAL FASE 1** | | | **30 días** | **~350 h totales** | **~$10,225** |

### Hito de cierre de Fase 1
> ✅ Portal Web funcional con validación automática en tiempo real  
> ✅ API de inventario respondiendo con datos en tiempo real del ERP Legacy  
> ✅ API de crédito respondiendo desde el Sistema Financiero  
> ✅ Flujo AND paralelo funcionando en Integration Suite  
> ✅ Tiempo de respuesta de APIs < 3 segundos

---

## 4. Fase 2 — Calidad y Producción (Días 31-60)

### Objetivo de Fase 2
Implementar el Sistema QC Digital para control de calidad en-proceso y final, y digitalizar la planificación de producción. Estos cambios atacan directamente el mayor cuello de botella: el reproceso al 18%.

### Actividades de Fase 2

| ID | Actividad | Responsable | Duración | Horas estimadas | Costo asociado |
|---|---|---|---|---|---|
| F2.1 | **Diseño de checklists QC digitales** — Definir parámetros de calidad críticos (CTQ: Critical to Quality) durante fabricación; traducir el checklist físico actual a formato digital; definir alertas automáticas | Inspector de Calidad + Operario QC en-proceso (nuevo) | 5 días | Inspector: 40h · Op. QC: 40h | Interno/nuevo rol |
| F2.2 | **Desarrollo de la app Sistema QC Digital** — Aplicación web/móvil para tablets en planta; formularios de checklist por lote; registro de parámetros con timestamp; generación de informe digital de inspección; dashboard de resultados | Desarrollador Web (externo) | 12 días | Desarrollador: 60h (×$55=$3,300) · Analista Integración: 16h | $3,300 desarrollo |
| F2.3 | **Adquisición y configuración de tablets para planta** — 4 tablets industriales (1 por línea de producción + 1 para Inspector); configuración de acceso al Sistema QC Digital | Analista de Integración | 3 días | Compra: $1,600 · Configuración: 16h integración | $1,600 equipos |
| F2.4 | **Digitalización del módulo PP en ERP Legacy** — Configurar formularios digitales de órdenes de producción en el ERP Legacy; integrar con Integration Suite para recibir señal del portal cuando hay pedido sin stock | Analista de Integración + Planificador de Producción | 8 días | Analista Integración: 40h · Planificador: 16h (=$14×16=$224) | Interno (ERP config.) |
| F2.5 | **Prueba piloto del QC en-proceso** — Ejecutar 20 lotes piloto con el nuevo sistema QC digital; registrar resultados; comparar tasa de detección temprana vs. sistema anterior | Op. QC en-proceso + Inspector de Calidad + Operarios de Planta | 7 días | Op. QC: 56h · Inspector: 20h · Operarios: 10h c/u | Interno/nuevo rol |
| F2.6 | **Ajustes y validación** — Ajustar alertas y umbrales del sistema QC; validar que la tasa de rechazo en inspección final disminuya | Analista de Integración + Inspector | 5 días | Analista: 24h · Desarrollador: 10h (×$55=$550) | $550 ajustes |
| **TOTAL FASE 2** | | | **30 días** | **~300 h totales** | **~$5,450** |

### Hito de cierre de Fase 2
> ✅ Sistema QC Digital funcionando en planta con tablets industriales  
> ✅ Checklists digitales en-proceso durante fabricación  
> ✅ Inspección final con registro digital y trazabilidad de lote  
> ✅ Órdenes de producción digitales integradas con el ERP  
> ✅ Tasa de rechazo en prueba piloto < 8% (tendencia hacia meta del 5%)

---

## 5. Fase 3 — Logística, Facturación y Go-Live (Días 61-90)

### Objetivo de Fase 3
Implementar el TMS para logística automatizada, integrar el sistema de facturación electrónica, capacitar a todo el personal y realizar el Go-Live completo del proceso TO-BE.

### Actividades de Fase 3

| ID | Actividad | Responsable | Duración | Horas estimadas | Costo asociado |
|---|---|---|---|---|---|
| F3.1 | **Contratación e integración del TMS (Beetrack)** — Contratar suscripción anual de Beetrack; configurar pool de transportistas; definir reglas de asignación automática (zona, capacidad, disponibilidad); integrar vía Integration Suite | Analista de Integración + Coord. Logística + Especialista TMS (externo) | 8 días | Analista: 40h · Coord. Logística: 24h · Especialista TMS: 40h (×$60=$2,400) | $2,400 consultoría + $2,500 suscripción |
| F3.2 | **Configuración de firma digital y app de entrega** — Configurar app móvil Beetrack para transportistas; habilitar firma digital del cliente en la app; integrar confirmación de entrega con trigger de facturación | Analista de Integración + Especialista TMS | 5 días | Analista: 24h · Especialista TMS: 24h (×$60=$1,440) | $1,440 consultoría |
| F3.3 | **Integración del Sistema de Facturación Electrónica (Datil.me)** — Contratar Datil.me; configurar cuenta empresarial SRI; mapear datos del pedido al formato XML de comprobante electrónico; programar trigger automático desde confirmación de entrega TMS | Analista de Integración + Analista de Finanzas | 6 días | Analista Integración: 32h · Analista Finanzas: 16h (=$13×16=$208) | Interno + $2,500 Datil suscripción |
| F3.4 | **Prueba de integración completa del flujo TO-BE** — Ejecutar 50 casos de prueba E2E: desde solicitud en portal hasta emisión de factura electrónica; documentar tiempos reales por actividad; validar contra KPIs objetivo | Todos los roles involucrados | 7 días | Analista Integración: 56h · Todos los roles: 8h c/u | Interno |
| F3.5 | **Capacitación del personal** — Capacitar: Ejecutivos de Ventas (portal), Analistas de Finanzas (dashboard crédito), Coord. Inventarios (monitoreo API stock), Planificador (PP digital), Inspectores QC (sistema digital), Coord. Logística (TMS) | Instructor externo + Analista de Integración | 5 días | Instructor: 40h (×$50=$2,000) · Analista Integración: 40h · Todos los roles: 4h c/u | $2,000 capacitación |
| F3.6 | **Go-Live controlado (parallel run)** — Operar en paralelo (manual + digital) durante 5 días para validar que el sistema digital funciona correctamente antes de desconectar procesos manuales | Analista de Integración + todos los roles | 5 días | Analista Integración: 40h · Todos los roles: 4h/día c/u | Interno |
| F3.7 | **Documentación y handover** — Documentar arquitectura final; manuales de usuario; procedimientos de contingencia; traspaso formal al Analista de Integración como responsable permanente | Analista de Integración + Consultor SAP | 4 días | Analista: 32h · Consultor SAP: 8h (×$80=$640) | $640 documentación |
| **TOTAL FASE 3** | | | **30 días** | **~400 h totales** | **~$11,480** |

### Hito de cierre de Fase 3 (Go-Live)
> ✅ TMS funcionando con asignación automática de transportistas  
> ✅ Firma digital de entrega integrada con trigger de facturación  
> ✅ Factura electrónica generada automáticamente al confirmar entrega  
> ✅ Personal capacitado en todos los nuevos sistemas  
> ✅ Proceso TO-BE completo en producción  
> ✅ Tiempo de ciclo medido y validado < 350 min  
> ✅ Costo por pedido medido y validado < $70.00  

---

## 6. Cronograma General (Gantt)

```
SEMANA →    1    2    3    4  ║  5    6    7    8  ║  9   10   11   12
            ◄──── FASE 1 ────►  ◄──── FASE 2 ────►  ◄──── FASE 3 ────►

F1.1  Levantamiento requisitos     ████
F1.2  Config. Integration Suite        █████
F1.3  API ERP Legacy (inventario)      ████████
F1.4  API Sistema Financiero               ██████
F1.5  Portal Web de Pedidos            ████████████
F1.6  Pruebas integración E2E                    ████
F1.7  Ajustes y correcciones                         ███

                               ║
F2.1  Diseño checklists QC                        ████
F2.2  Desarrollo app QC Digital                       ████████████
F2.3  Tablets para planta                          ███
F2.4  Digitalización módulo PP ERP                     ████████
F2.5  Prueba piloto QC en-proceso                               ███████
F2.6  Ajustes y validación QC                                       ████

                                                  ║
F3.1  Integración TMS (Beetrack)                               ████████
F3.2  App firma digital y entrega                                  █████
F3.3  Integración facturación electrónica                           ██████
F3.4  Prueba integración E2E completa                                    ███████
F3.5  Capacitación del personal                                              ████
F3.6  Go-Live controlado (parallel run)                                          ████
F3.7  Documentación y handover                                               ████

ENTREGABLES CLAVE:
  Fin Semana 4:  ► Portal + API Inventario + API Crédito FUNCIONANDO
  Fin Semana 8:  ► Sistema QC Digital + PP Digital FUNCIONANDO
  Fin Semana 12: ► TMS + Facturación + Capacitación + GO-LIVE COMPLETO
```

---

## 7. Dedicación del Personal por Fase (Según Restricciones del Caso)

> Las tarifas por hora son las definidas por el caso de INDUPRO. Las horas de dedicación son estimadas según el porcentaje de tiempo dedicado al proyecto.

### Fase 1 — Horas internas de personal INDUPRO

| Rol | Tarifa (caso) | Horas en Fase 1 | Costo interno estimado |
|---|---|---|---|
| Ejecutivo de Ventas (×2 disponibles) | $12/hr | 24h (3 días equiv.) | $288 |
| Analista de Finanzas | $13/hr | 16h (2 días equiv.) | $208 |
| Coordinador de Inventarios | $10/hr | 16h (2 días equiv.) | $160 |
| Analista de Integración (nuevo) | $18/hr | 160h (20 días completos) | $2,880 (costo del nuevo rol) |
| **Total Fase 1 — dedicación interna** | | **216 h** | **$3,536** |

> ⚠️ El costo del Analista de Integración SÍ es un costo nuevo (nuevo rol), considerado dentro del presupuesto de implementación.

### Fase 2 — Horas internas de personal INDUPRO

| Rol | Tarifa (caso) | Horas en Fase 2 | Costo interno estimado |
|---|---|---|---|
| Inspector de Calidad | $11/hr | 60h (7.5 días equiv.) | $660 |
| Planificador de Producción | $14/hr | 16h (2 días equiv.) | $224 |
| Operario de Planta (ref.) | $8/hr | 10h | $80 |
| Analista de Integración (nuevo) | $18/hr | 136h (17 días) | $2,448 |
| Operario QC en-proceso (nuevo) | $11/hr | 136h (17 días) | $1,496 |
| **Total Fase 2 — dedicación** | | **358 h** | **$4,908** |

### Fase 3 — Horas internas de personal INDUPRO

| Rol | Tarifa (caso) | Horas en Fase 3 | Costo interno estimado |
|---|---|---|---|
| Coordinador de Logística | $10/hr | 24h (3 días equiv.) | $240 |
| Analista de Finanzas | $13/hr | 16h (2 días equiv.) | $208 |
| Todos los roles (capacitación) | promedio $10.43/hr | 8h c/u × 8 roles = 64h | $668 |
| Analista de Integración (nuevo) | $18/hr | 200h (25 días) | $3,600 |
| Operario QC en-proceso (nuevo) | $11/hr | 160h (20 días) | $1,760 |
| **Total Fase 3 — dedicación** | | **464 h** | **$6,476** |

---

## 8. Resumen de Horas por Actividad con Costos Justificados

| Actividad del TO-BE | Rol responsable | Tarifa (caso) | Tiempo en proceso (min) | Costo por instancia |
|---|---|---|---|---|
| 1. Recepción + autovalidación portal | Ejecutivo de Ventas | $12/hr | 15 min | $3.00 |
| 2A. Verificación crédito API | Analista de Finanzas (monitoreo) | $13/hr | 15 min | $3.25 |
| 2B. Consulta stock API | Coordinador de Inventarios (monitoreo) | $10/hr | 10 min | $1.67 |
| 6A. Confirmación automática cliente | Sistema / Ejecutivo Ventas (supervisión) | $12/hr | 5 min | $1.00 |
| 6B. Programar producción digital | Planificador de Producción | $14/hr | 20 min | $4.67 |
| 7. Fabricación + QC en-proceso | Operarios de Planta + Op. QC (nuevo) | $8/hr + $11/hr | 120 min | $16.00 (operarios) |
| 8. Inspección final digital | Inspector de Calidad | $11/hr | 30 min | $5.50 |
| 9B. Reproceso residual | Operarios / Inspector | $8/hr | 60 min (si aplica) | $8.00 |
| 10. Empaque digital | Coordinador de Logística | $10/hr | 15 min | $2.50 |
| 11. Asignación TMS | Coordinador de Logística (supervisión) | $10/hr | 10 min | $1.67 |
| 12. Entrega + firma digital | Transportista | $10/hr | 45 min | $7.50 |
| 13. Factura electrónica automática | Sistema / Analista de Finanzas (supervisión) | $13/hr | 5 min | $1.08 |
| **TOTAL TO-BE (sin reproceso)** | | | **281 min** | **$47.84** |
| **TOTAL TO-BE (con reproceso)** | | | **341 min** | **$55.84** |

> **Justificación:** Los tiempos de supervisión en actividades automatizadas (2A, 2B, 6A, 13) se contabilizan porque el rol humano monitorea el proceso y puede intervenir si hay error del sistema. El costo refleja la fracción del tiempo del rol dedicada a esa actividad específica.

---

## 9. Gestión de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| APIs del ERP Legacy no disponibles o sin acceso a la BD | Media | Alto | Levantamiento técnico previo en F1.1; si no hay API nativa, usar conexión JDBC directa a la BD del ERP via Integration Suite |
| Sistema Financiero no tiene endpoints documentados | Media | Alto | El Analista de Finanzas lidera el mapeo de campos en F1.1; alternativa: acceso JDBC o extracción de datos |
| Resistencia del personal al cambio | Alta | Medio | Go-Live controlado con parallel run (F3.6); capacitación antes del Go-Live (F3.5) |
| Presupuesto insuficiente por alcance subestimado | Media | Alto | Contingencia del 4% en el presupuesto; priorización clara por fases |
| Performance lenta de las APIs en horas pico | Baja | Medio | SLA de respuesta < 3 segundos en pruebas F1.6; caché en Integration Suite para consultas frecuentes |
| El TMS no se integra con los transportistas actuales | Baja | Bajo | Beetrack tiene onboarding de transportistas sin costo; alternativa: integración manual inicial |

---

## 10. Criterios de Éxito del Proyecto

| Criterio | Indicador | Meta |
|---|---|---|
| Tiempo de ciclo del proceso | Medido en Signavio Simulation y operación real | < 350 minutos |
| Costo por pedido | Calculado con tarifas del caso | < $70.00 |
| Tasa de reproceso de calidad | % de lotes rechazados en inspección final | < 5% |
| Tiempo de respuesta del portal | Desde submit del pedido hasta confirmación/asignación | < 60 minutos |
| Disponibilidad del sistema | Uptime de Portal + Integration Suite | > 99% en horario laboral |
| Satisfacción del personal | Encuesta post-capacitación | > 80% de valoración positiva |
| ROI del proyecto | Ahorro mensual vs. inversión | Payback < 1 mes |

---

## 11. Estructura de Gobierno del Proyecto

| Rol de Proyecto | Persona / Cargo | Responsabilidad |
|---|---|---|
| **Sponsor del proyecto** | Gerente General / Gerente de Operaciones INDUPRO | Aprobación de fases; desbloqueo de recursos |
| **Líder técnico** | Analista de Integración de Sistemas (nuevo rol) | Responsable de la implementación técnica del middleware y APIs |
| **Líder funcional** | Gerente de Ventas | Responsable de la adopción del portal y los nuevos flujos de negocio |
| **Gestor de calidad** | Inspector de Calidad (existente) | Responsable del diseño y adopción del Sistema QC Digital |
| **Consultores externos** | Consultor SAP Integration Suite + Desarrolladores | Implementación técnica dentro del presupuesto |

---

*Documento elaborado como parte del SAP Signavio Regional Challenge 2026*  
*Equipo participante — ESPOL*
