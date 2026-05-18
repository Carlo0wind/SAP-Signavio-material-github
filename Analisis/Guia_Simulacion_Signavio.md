# Guía de Simulación — Parámetros Exactos para SAP Signavio
## Caso INDUPRO S.A. — AS-IS y TO-BE

> Esta guía contiene los valores exactos a ingresar en SAP Signavio para configurar la simulación.  
> **REGLA CRÍTICA: Todos los tiempos en MINUTOS. Nunca horas, nunca días.**

---

## SIMULACIÓN AS-IS

### Paso 1: Crear el escenario

1. Abrir el diagrama BPMN AS-IS en el Graphical Editor
2. Menú: **Editar → Simular**
3. Crear nuevo escenario: nombre `"AS-IS Base"`
4. Configurar las 4 pestañas:

---

### Pestaña DURATION (Duración)

| Actividad en el diagrama | Tiempo fijo (min) | Tipo distribución |
|---|---|---|
| Recepción de solicitud del cliente | `30` | Fija |
| Validación manual de datos del pedido | `45` | Fija |
| Verificación de crédito del cliente | `60` | Fija |
| Consulta de disponibilidad de stock | `50` | Fija |
| *(Gateway XOR ¿Hay stock?)* | `5` | Fija |
| Confirmación de pedido al cliente [SÍ] | `20` | Fija |
| Programación de orden de producción [NO] | `40` | Fija |
| Fabricación del producto | `120` | Fija |
| Inspección y liberación de calidad | `30` | Fija |
| *(Gateway XOR ¿Pasa calidad?)* | `5` | Fija |
| Reproceso del lote [RECHAZA] | `90` | Fija |
| Empaque y preparación para despacho | `25` | Fija |
| Asignación de transportista | `30` | Fija |
| Entrega al cliente y firma | `45` | Fija |
| Generación y envío de factura | `20` | Fija |

---

### Pestaña FREQUENCY (Frecuencia y probabilidades)

**Configuración de casos:**
```
Modo: Múltiples casos
Duración de simulación: 480 minutos (= 1 día hábil)
Frecuencia de inicio: 4 casos por día
```

**Probabilidades en Gateways XOR:**

| Gateway | Camino | Probabilidad |
|---|---|---|
| ¿Hay stock? | Sí (hay stock disponible) | `65` % |
| ¿Hay stock? | No (sin stock, ir a producción) | `35` % |
| ¿Pasa calidad? | APRUEBA | `82` % |
| ¿Pasa calidad? | RECHAZA (reproceso) | `18` % |

> ⚠️ Verificar que cada gateway sume exactamente 100%

---

### Pestaña RESOURCES (Recursos)

| Lane (Swimlane) | Recurso asignado | Costo/hora (USD) | Cantidad disponible | Horario |
|---|---|---|---|---|
| Ventas y Servicio al Cliente | Ejecutivo de Ventas | `12` | 2 | Lun-Vie 08:00-16:00 |
| Finanzas y Facturación | Analista de Finanzas | `13` | 1 | Lun-Vie 08:00-16:00 |
| Coordinación de Inventarios | Coordinador de Inventarios | `10` | 1 | Lun-Vie 08:00-16:00 |
| Planificación de Producción | Planificador de Producción | `14` | 1 | Lun-Vie 08:00-16:00 |
| Planta de Manufactura | Operario de Planta | `8` | 6 | Lun-Vie 08:00-16:00 |
| Control de Calidad | Inspector de Calidad | `11` | 2 | Lun-Vie 08:00-16:00 |
| Logística y Distribución | Coordinador de Logística | `10` | 1 | Lun-Vie 07:00-14:00 |

---

### Pestaña COSTS (Costos adicionales)

> En esta pestaña se ingresan costos de material/herramienta (NO mano de obra — esa va en Resources)

| Actividad | Costo adicional (USD) | Concepto |
|---|---|---|
| Fabricación del producto | `0` | Costos de materiales no incluidos en este nivel |
| Todas las demás | `0` | Solo costos de recurso humano |

---

### Resultados esperados AS-IS (1 caso — ruta con producción + reproceso)

| Métrica | Valor esperado |
|---|---|
| Total cycle time | ~555 minutos |
| Total cost | ~$105.91 |
| Resource consumption | ~555 min-persona |
| Bottleneck | Paso 3 (Verificación Crédito) y Paso 7 (Fabricación) |

---

## SIMULACIÓN TO-BE

### Escenario 1: TO-BE Base

Crear nuevo escenario: `"TO-BE Base"`

### Pestaña DURATION — TO-BE

| Actividad en el diagrama | Tiempo fijo (min) | Tipo distribución |
|---|---|---|
| Recepción + auto-validación (portal web) | `15` | Fija |
| *(AND Split Gateway — inicio paralelo)* | `1` | Fija |
| Verificación crédito automatizada [PARALELO] | `15` | Fija |
| Consulta stock ERP tiempo real [PARALELO] | `10` | Fija |
| *(AND Join Gateway — convergencia)* | `1` | Fija |
| *(Gateway XOR ¿Crédito OK y Stock OK?)* | `2` | Fija |
| Confirmación automática pedido [SÍ] | `5` | Fija |
| Planificación producción digital [NO] | `20` | Fija |
| Fabricación (con QC en-proceso) | `120` | Fija *(inamovible)* |
| Inspección calidad final | `30` | Fija *(inamovible)* |
| *(Gateway XOR ¿Pasa calidad?)* | `2` | Fija |
| Reproceso del lote (reducido) | `60` | Fija |
| Empaque semi-automatizado | `15` | Fija |
| Asignación transportista TMS | `10` | Fija |
| Entrega al cliente + firma digital | `45` | Fija *(física)* |
| Factura electrónica automática | `5` | Fija |

### Pestaña FREQUENCY — TO-BE

| Gateway | Camino | Probabilidad |
|---|---|---|
| ¿Crédito OK y Stock OK? | Sí | `70` % |
| ¿Crédito OK y Stock OK? | No (producción) | `30` % |
| ¿Pasa calidad? | APRUEBA | `95` % |
| ¿Pasa calidad? | RECHAZA (reproceso) | `5` % |

**Configuración de casos:**
```
Modo: Múltiples casos
Duración de simulación: 480 minutos (= 1 día hábil)
Frecuencia de inicio: 4 casos por día (mismo que AS-IS para comparación)
```

### Pestaña RESOURCES — TO-BE

> Mismos recursos que AS-IS. El Lane de "Sistema / Automatización" tiene costo = $0 (automatizado)

| Lane | Recurso | Costo/hora | Cantidad | Horario |
|---|---|---|---|---|
| Ventas y Servicio al Cliente | Ejecutivo de Ventas | `12` | 2 | Lun-Vie 08:00-16:00 |
| Finanzas y Facturación | Analista de Finanzas | `13` | 1 | Lun-Vie 08:00-16:00 |
| Coordinación de Inventarios | Coordinador de Inventarios | `10` | 1 | Lun-Vie 08:00-16:00 |
| Planificación de Producción | Planificador de Producción | `14` | 1 | Lun-Vie 08:00-16:00 |
| Planta de Manufactura | Operario de Planta | `8` | 6 | Lun-Vie 08:00-16:00 |
| Control de Calidad | Inspector de Calidad | `11` | 2 | Lun-Vie 08:00-16:00 |
| Logística y Distribución | Coordinador de Logística | `10` | 1 | Lun-Vie 07:00-14:00 |
| Sistema / Automatización | Sistema Automático | `0` | — | 24/7 |

### Resultados esperados TO-BE (1 caso — ruta con producción, sin reproceso)

| Métrica | Valor esperado TO-BE | Valor AS-IS | Mejora |
|---|---|---|---|
| Total cycle time | **~281 minutos** | 555 min | **-49.4%** |
| Total cost | **~$46.84** | $105.91 | **-55.8%** |
| Resource consumption | **~281 min-persona** | ~555 min | **-49.4%** |

---

## ESCENARIO 2: TO-BE + Aumento de Volumen (+40%)

**Objetivo:** Validar que el proceso TO-BE soporta el crecimiento del negocio.

Crear escenario: `"TO-BE Escenario 2 - Volumen +40%"`

**Cambio único respecto a TO-BE Base:**
```
Pestaña Frequency:
  Frecuencia de inicio: 5.6 casos por día  (4 × 1.4 = +40%)
```

**Todos los demás parámetros IDÉNTICOS al TO-BE Base.**

**Pregunta a responder:** ¿Los recursos actuales pueden manejar 5.6 pedidos/día sin cuello de botella crítico?

---

## ESCENARIO 3: TO-BE + Recurso Crítico Ausente

**Objetivo:** Análisis de riesgo — ¿qué pasa si un Inspector de Calidad falta?

Crear escenario: `"TO-BE Escenario 3 - Inspector QC -1"`

**Cambio único respecto a TO-BE Base:**
```
Pestaña Resources:
  Inspector de Calidad: cambiar de 2 → 1 disponible
```

**Todos los demás parámetros IDÉNTICOS al TO-BE Base.**

**Pregunta a responder:** ¿El tiempo de ciclo TO-BE sigue < 350 min con solo 1 Inspector?

---

## Tabla Comparativa Final de Escenarios

| Escenario | Frecuencia | Inspector QC | Ciclo esperado | Costo esperado |
|---|---|---|---|---|
| AS-IS Base | 4/día | 2 disponibles | **555 min** | **$105.91** |
| TO-BE Base | 4/día | 2 disponibles | **~281 min** | **~$46.84** |
| TO-BE Escenario 2 (Vol +40%) | 5.6/día | 2 disponibles | ~320 min? | ~$46.84 |
| TO-BE Escenario 3 (Inspector -1) | 4/día | 1 disponible | ~310 min? | ~$46.84 |

> Los valores de Escenario 2 y 3 se obtendrán de la simulación real. Los "~?" son estimaciones a verificar.

---

## Cómo Exportar Resultados de Simulación

### Capturas requeridas (por escenario):
1. **Panel de resultados** (derecha): Total cycle time, Total cost, Resource consumption
2. **Diagrama con blue dots** (bottlenecks): Actividades con puntos azules de espera
3. **Gráfico de utilización de recursos** (si disponible)

### Pasos para exportar en Signavio:
1. Ejecutar la simulación
2. En el panel de resultados (derecha), hacer captura de pantalla (`Windows + Shift + S`)
3. Guardar como PNG en la carpeta `Analisis/` del proyecto
4. Nombrar: `Sim_ASIS_Base.png`, `Sim_TOBE_Base.png`, `Sim_TOBE_Vol.png`, `Sim_TOBE_QC.png`

---

## Checklist de Simulación

```
□ Simulación AS-IS:
  □ Escenario "AS-IS Base" creado
  □ Todos los tiempos en MINUTOS ingresados
  □ Probabilidades XOR configuradas (65/35 · 82/18)
  □ Recursos y costos/hora ingresados
  □ Ejecutado "1 caso" primero (verificación)
  □ Ejecutado "Múltiples casos" (480 min, 4/día)
  □ Captura de resultados guardada (Sim_ASIS_Base.png)
  □ Bottlenecks identificados y documentados

□ Simulación TO-BE:
  □ Escenario "TO-BE Base" creado
  □ AND Gateway configurado (crédito + inventario paralelo)
  □ Probabilidades XOR actualizadas (70/30 · 95/5)
  □ Ejecutado y capturado (Sim_TOBE_Base.png)

□ Escenarios adicionales:
  □ Escenario 2 (Volumen +40%) ejecutado y capturado
  □ Escenario 3 (Inspector QC -1) ejecutado y capturado

□ Tabla comparativa AS-IS vs. TO-BE completada con % mejora
```

---

*Guía de simulación — SAP Signavio Regional Challenge 2026 — Caso INDUPRO*
