# Configuración de Simulación AS-IS — SAP Signavio
## INDUPRO S.A. — Proceso de Gestión de Pedidos

> **Archivo BPMN base:** `Plantillas Base/INDUPRO_Gestion_Pedidos_ASIS.bpmn`
> **Regla crítica:** Todos los tiempos en **MINUTOS**. Nunca horas, nunca días.

---

## PASO 1 — Importar el modelo a SAP Signavio

1. Abrir **SAP Signavio Process Manager** → academic.signavio.com
2. En el **Explorer**, seleccionar la carpeta del equipo
3. Hacer clic en **New > Upload** → seleccionar `INDUPRO_Gestion_Pedidos_ASIS.bpmn`
4. Verificar que el diagrama se muestre con **7 swimlanes** y **2 gateways XOR**
5. Guardar con `Ctrl+S` antes de continuar

---

## PASO 2 — Verificar el Dictionary (antes de simular)

Ir a **Signavio Dictionary** y registrar los siguientes elementos:

### Roles (asignar a cada tarea del diagrama)

| Nombre del rol | Asignar a las tareas |
|----------------|---------------------|
| Ejecutivo de Ventas | Task 1, Task 2, Task 6A |
| Analista de Finanzas | Task 3, Task 13 |
| Coordinador de Inventarios | Task 4, GW-01 |
| Planificador de Producción | Task 6B |
| Operario de Planta | Task 7, Task 9B |
| Inspector de Calidad | Task 8, GW-02 |
| Coordinador de Logística | Task 10, Task 11 |
| Transportista | Task 12 |

### Sistemas/Herramientas

| Sistema | Tareas donde se usa |
|---------|---------------------|
| Correo electrónico / Teléfono | Task 1, Task 6A, Task 11 |
| Hoja de Excel | Task 2 |
| Sistema Financiero Manual | Task 3 |
| Registro físico / ERP legacy | Task 4 |
| Planilla de producción manual | Task 6B |
| Órdenes de trabajo impresas | Task 7 |
| Checklist físico de calidad | Task 8, Task 9B |
| Sistema de facturación | Task 13 |

---

## PASO 3 — Abrir el módulo de simulación

1. Abrir el diagrama AS-IS en el **Graphical Editor**
2. Ir al menú: **Edit → Simulate** (o botón de simulación en la barra)
3. Hacer clic en **"Create new scenario"**
4. Nombrar el escenario: `AS-IS Base`
5. Configurar las 4 pestañas en orden: Duration → Costs → Frequency → Resources

---

## PASO 4 — Pestaña DURATION

> Ingresar exactamente los siguientes valores. Tipo de distribución: **Fixed (fija)** en todos.

| Elemento del diagrama | ID en el BPMN | Duración (min) | Tipo |
|-----------------------|---------------|----------------|------|
| Recepcionar solicitud del cliente | `sid-task-1-recepcion` | **30** | Fixed |
| Validar datos del pedido manualmente | `sid-task-2-validacion` | **45** | Fixed |
| Verificar crédito del cliente | `sid-task-3-credito` | **60** | Fixed |
| Consultar disponibilidad de stock | `sid-task-4-stock` | **50** | Fixed |
| *(GW-01: ¿Hay stock?)* | `sid-gw-stock` | **5** | Fixed |
| Programar orden de producción | `sid-task-6b-planificacion` | **40** | Fixed |
| Fabricar el producto | `sid-task-7-fabricacion` | **120** | Fixed |
| Inspeccionar y liberar calidad | `sid-task-8-inspeccion` | **30** | Fixed |
| *(GW-02: ¿Pasa calidad?)* | `sid-gw-calidad` | **5** | Fixed |
| Reprocesar lote rechazado | `sid-task-9b-reproceso` | **90** | Fixed |
| Confirmar pedido al cliente | `sid-task-6a-confirmacion` | **20** | Fixed |
| Empacar y preparar para despacho | `sid-task-10-empaque` | **25** | Fixed |
| Asignar transportista y programar entrega | `sid-task-11-transportista` | **30** | Fixed |
| Entregar al cliente y firmar conformidad | `sid-task-12-entrega` | **45** | Fixed |
| Generar y enviar factura | `sid-task-13-factura` | **20** | Fixed |

**Suma de duración — ruta con fabricación y reproceso: 555 min**

---

## PASO 5 — Pestaña COSTS

> Los costos de mano de obra se configuran en la pestaña Resources (no aquí).
> En Costs se ingresan costos adicionales de materiales o herramientas.

| Elemento | Costo adicional | Concepto |
|----------|----------------|----------|
| Todas las tareas | `$0` | Los costos son de recurso humano (van en Resources) |

*Dejar todos los campos en 0 para el escenario base.*

---

## PASO 6 — Pestaña FREQUENCY (Probabilidades de gateways)

### Configuración de instancias del proceso

```
Modo de simulación:   Multiple instances
Duración de ventana:  480 min  (= 1 día hábil de 8 horas)
Frecuencia de inicio: 4 casos por día
```

### Probabilidades en los Gateways XOR

> ⚠️ Verificar que cada gateway sume **exactamente 100%**

**Gateway GW-01 — ¿Hay stock disponible?**

| Sequence Flow de salida | Etiqueta | Probabilidad |
|------------------------|----------|--------------|
| `sf-gwstock-si-joinrutas` | Sí (hay stock) | **65** % |
| `sf-gwstock-no-task6b` | No (sin stock) | **35** % |
| **TOTAL** | | **100 %** ✅ |

**Gateway GW-02 — ¿Pasa control de calidad?**

| Sequence Flow de salida | Etiqueta | Probabilidad |
|------------------------|----------|--------------|
| `sf-gwcalidad-aprueba-joinrutas` | Aprueba | **82** % |
| `sf-gwcalidad-rechaza-task9b` | Rechaza | **18** % |
| **TOTAL** | | **100 %** ✅ |

---

## PASO 7 — Pestaña RESOURCES

> Un recurso por lane. Asignar cada recurso a las tareas de su swimlane.

| Lane | Nombre del recurso | Costo/hora (USD) | Cantidad | Horario |
|------|--------------------|-----------------|----------|---------|
| Ventas y Servicio al Cliente | Ejecutivo de Ventas | **12** | 2 | Lun–Vie 08:00–16:00 |
| Finanzas y Facturación | Analista de Finanzas | **13** | 1 | Lun–Vie 08:00–16:00 |
| Coordinación de Inventarios | Coordinador de Inventarios | **10** | 1 | Lun–Vie 08:00–16:00 |
| Planificación de Producción | Planificador de Producción | **14** | 1 | Lun–Vie 08:00–16:00 |
| Planta de Manufactura | Operario de Planta | **8** | 6 | Lun–Vie 08:00–16:00 |
| Control de Calidad | Inspector de Calidad | **11** | 2 | Lun–Vie 08:00–16:00 |
| Logística y Distribución | Coordinador de Logística | **10** | 1 | Lun–Vie 07:00–14:00 |

### Asignación de recursos a tareas

| Tarea | Recurso asignado |
|-------|-----------------|
| Task 1 — Recepcionar solicitud | Ejecutivo de Ventas |
| Task 2 — Validar datos (Excel) | Ejecutivo de Ventas |
| Task 3 — Verificar crédito | Analista de Finanzas |
| Task 4 — Consultar stock | Coordinador de Inventarios |
| Task 6B — Programar producción | Planificador de Producción |
| Task 7 — Fabricar producto | Operario de Planta |
| Task 8 — Inspeccionar calidad | Inspector de Calidad |
| Task 9B — Reprocesar lote | Operario de Planta |
| Task 6A — Confirmar pedido | Ejecutivo de Ventas |
| Task 10 — Empacar | Coordinador de Logística |
| Task 11 — Asignar transportista | Coordinador de Logística |
| Task 12 — Entregar al cliente | Coordinador de Logística |
| Task 13 — Generar factura | Analista de Finanzas |

---

## PASO 8 — Ejecutar la simulación

### Ejecución 1: Caso único (para verificar el modelo)

1. Seleccionar modo: **"Single instance"**
2. Hacer clic en **Run**
3. Verificar que el proceso complete sin errores
4. Revisar el resultado: tiempo de ciclo debería ser ~555 min (ruta con fabricación + reproceso)

### Ejecución 2: Múltiples casos (para obtener KPIs estadísticos)

1. Seleccionar modo: **"Multiple instances"**
2. Configurar duración: **480 min**
3. Frecuencia: **4 instancias al inicio del período**
4. Hacer clic en **Run**
5. Exportar resultados como PNG

---

## PASO 9 — Resultados esperados y KPIs de referencia

### Resultados de un caso único (ruta fabricación + reproceso)

| Métrica Signavio | Valor esperado AS-IS |
|-----------------|---------------------|
| **Total cycle time** | ~555 min |
| **Total cost** | ~$105.91 |
| **Resource consumption** | ~555 min-persona |
| **Bottleneck #1** | Task 3 — Verificar crédito (60 min bloqueante) |
| **Bottleneck #2** | Task 7 — Fabricación (120 min inamovible) |
| **Bottleneck #3** | Task 9B — Reproceso (18% de frecuencia × 90 min) |

### Distribución del costo por actividad (referencia)

| Actividad | Costo (USD) | % del total |
|-----------|-------------|-------------|
| Task 7 — Fabricación | $16.00 | 15.1% |
| Task 3 — Verificar crédito | $13.00 | 12.3% |
| Task 9B — Reproceso | $12.00 | 11.3% |
| Task 6B — Programar producción | $9.33 | 8.8% |
| Task 2 — Validar datos | $9.00 | 8.5% |
| Task 12 — Entregar al cliente | $7.50 | 7.1% |
| Task 4 — Consultar stock | $8.33 | 7.9% |
| Task 8 — Inspección calidad | $5.50 | 5.2% |
| Task 11 — Asignar transportista | $5.00 | 4.7% |
| Task 13 — Generar factura | $4.33 | 4.1% |
| Task 10 — Empacar | $4.17 | 3.9% |
| Task 6A — Confirmar pedido | $4.00 | 3.8% |
| Task 1 — Recepcionar solicitud | $6.00 | 5.7% |
| Gateways (XOR × 2) | $1.75 | 1.7% |
| **TOTAL** | **$105.91** | **100%** |

---

## PASO 10 — Exportar evidencias para los entregables

### Capturas requeridas (E5 del checklist)

| Evidencia | Dónde exportar | Formato |
|-----------|---------------|---------|
| Diagrama BPMN AS-IS completo | File → Export → PDF | PDF |
| Resultado simulación — caso único | Simulation results → Export | PNG |
| Resultado simulación — múltiples casos | Simulation results → Export | PNG |
| Vista de bottlenecks (color por tiempo) | Simulation heatmap view | PNG |
| Dictionary completo | Dictionary → Export | PNG / PDF |

---

## Alertas críticas para la versión académica de Signavio

```
⚠️  SIEMPRE usar MINUTOS — nunca horas, nunca días
    (la versión académica falla con unidades distintas a minutos)

⚠️  Ejecutar PRIMERO el modo "Single instance" para validar el modelo
    antes de correr múltiples casos

⚠️  Guardar con Ctrl+S antes de cada ejecución de simulación

⚠️  Las probabilidades de cada XOR deben sumar exactamente 100%
    GW-01: 65 + 35 = 100 ✅
    GW-02: 82 + 18 = 100 ✅

⚠️  Si la simulación muestra "0 cost" verificar que los recursos
    tienen el costo/hora ingresado (no dejar en blanco)

⚠️  Si la plataforma se vuelve inestable:
    → Limpiar caché del navegador (Ctrl+Shift+Del)
    → Recargar la página
    → Volver a abrir el diagrama desde el Explorer
```

---

## Escenarios adicionales de simulación (opcionales — mayor puntaje)

### Escenario 2: Aumento de volumen (+40%)

| Parámetro | Valor |
|-----------|-------|
| Nombre del escenario | `AS-IS + Volumen` |
| Frecuencia de inicio | **6 casos** por día (1,680 pedidos/mes) |
| Todo lo demás | Igual al escenario base |
| Objetivo | Mostrar que el cuello de botella del Analista de Finanzas (Task 3) colapsa |

### Escenario 3: Inspector de Calidad ausente

| Parámetro | Valor |
|-----------|-------|
| Nombre del escenario | `AS-IS Riesgo QC` |
| Inspector de Calidad | Reducir a **1 recurso** (de 2 a 1) |
| Todo lo demás | Igual al escenario base |
| Objetivo | Mostrar la fragilidad del proceso ante ausencias |

---

## Referencia cruzada con el Diagram Comparison

Una vez modelado también el TO-BE, activar:
1. Abrir el diagrama AS-IS
2. Menú: **Analyze → Compare with another diagram**
3. Seleccionar el diagrama TO-BE
4. Los cambios aparecerán marcados:
   - **Verde**: actividades nuevas en el TO-BE
   - **Amarillo**: actividades modificadas
   - **Rojo**: actividades eliminadas del AS-IS
5. Exportar la comparación como PNG para el entregable E4
