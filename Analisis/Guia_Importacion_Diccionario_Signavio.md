# Guía de Importación del Diccionario en SAP Signavio

## Contexto

Se generaron **dos archivos Excel** del diccionario INDUPRO:

| Archivo | Uso | Descripción |
|---|---|---|
| `INDUPRO_Diccionario_Signavio.xlsx` | Documentación / Referencia | Formato de exportación de Signavio (metadatos en filas 1-5, headers en fila 7) |
| `INDUPRO_Diccionario_Import.xlsx` | **Importar en Signavio** | Headers en fila 1, datos desde fila 2 — compatible con el importador oficial |

---

## ¿Por qué hay un archivo separado para importar?

Según la **Sección 19.7** del *SAP Signavio Process Manager User Guide* (2025-08-28):

> *"The import tool interprets the **first row with text** as the header."*
> *"You must start your dictionary file with the first column and fill in at least **three columns**."*

El archivo `INDUPRO_Diccionario_Signavio.xlsx` (que sigue el formato de exportación de Signavio) tiene metadatos en las filas 1-5:
- Fila 1: `"Dictionary"` | nombre del workspace ← solo 2 columnas → **falla el requisito de mínimo 3**
- El importador lo tomaría como header incorrecto

El archivo `INDUPRO_Diccionario_Import.xlsx` corrige esto:
- Fila 1: headers de columnas (ej. `Title`, `Description`, etc.)
- Fila 2+: datos de las entradas

---

## Instrucciones de Importación — Paso a Paso

> **Fuente oficial**: Sección 19.7, *SAP Signavio Process Manager User Guide*

### Pre-requisitos
- Tener acceso como **administrador o usuario con permisos de escritura** en el Dictionary
- Archivo listo: `Analisis/INDUPRO_Diccionario_Import.xlsx`
- Solo puede ejecutarse **un import a la vez** en el workspace

### Proceso (repetir para cada una de las 11 categorías)

**Paso 1 — Abrir el Dictionary**
```
SAP Signavio Explorer → clic en "Dictionary" (panel izquierdo)
```

**Paso 2 — Iniciar el import**
```
Barra de herramientas → Import/Export → Import Excel
```

**Paso 3 — Seleccionar el archivo**
- Clic en **Choose File**
- Seleccionar `INDUPRO_Diccionario_Import.xlsx`
- Clic en **Import**

**Paso 4 — Configurar el wizard de importación**

El wizard tiene 4 secciones:

| Sección | Configuración |
|---|---|
| **Modo de importación** | `Create new entries for all rows` |
| **Hoja a importar** | Seleccionar la hoja correspondiente (ej. `Organizational_Units`) |
| **Atributo identificador** | No aplica (se están creando entradas nuevas) |
| **Mapeo de columnas** | Mapear cada columna del Excel al atributo del Dictionary |

**Paso 5 — Mapeo de columnas**

Al hacer clic en Import, aparecerá la pantalla de mapeo. Asignar:
- `Title` → **Title** *(obligatorio)*
- `Description` → **Description**
- `Relevant Documents` → **Relevant Documents**
- Las demás columnas → su atributo equivalente en Signavio

> Las columnas adicionales (como "Cost/Hour", "Process Step", "Risk Probability") se mapean a los **atributos personalizados** del Dictionary que existan en tu workspace.

**Paso 6 — Confirmar**
- Clic en **Import**
- Al terminar, Signavio muestra un resumen con un link para descargar el Excel con detalles del import

**Paso 7 — Repetir para las siguientes categorías**

Orden recomendado de importación:
1. `Organizational_Units` (4 entradas)
2. `Departments` (7 entradas)
3. `Roles` (10 entradas)
4. `External_participants` (5 entradas)
5. `Documents` (12 entradas)
6. `IT_Systems` (12 entradas)
7. `Risks` (9 entradas)
8. `Controls` (8 entradas)
9. `Activities` (13 entradas)
10. `Events` (7 entradas)
11. `Others` (14 entradas)

---

## Limitaciones Importantes

### ⚠️ Plataforma Académica (`academic.signavio.com`)

Según la Sección 4.2 del User Guide:
> *"The focus of the academic platform is process modeling. **Many advanced process management and collaboration features are not available**."*

**Posibilidad 1 — El import SÍ está disponible:**
Usa `INDUPRO_Diccionario_Import.xlsx` siguiendo el proceso anterior.

**Posibilidad 2 — El import NO está disponible en la versión académica:**
Ingresa las entradas manualmente:
```
Dictionary → seleccionar categoría → clic en "+" (Nueva entrada)
→ ingresar Title, Description y demás campos
```
Hay **84 entradas en total** — manejable en sesiones de trabajo.

### Límite por import
- Máximo **500 filas por hoja** (nuestras hojas tienen máx. 14 entradas — bien dentro del límite)

### Sin procesos BPMN requeridos
✅ Las entradas del Dictionary **pueden importarse sin haber creado ningún diagrama BPMN**. El diccionario existe independientemente de los modelos de proceso.

---

## Verificar la importación

Después de importar cada categoría:
1. En `Dictionary` → seleccionar la categoría importada
2. Verificar que las entradas aparecen listadas
3. Hacer clic en una entrada para revisar que `Title` y `Description` se importaron correctamente

---

## Resumen de las 11 categorías

| Categoría | Entradas | Descripción |
|---|---|---|
| `Organizational_Units` | 4 | INDUPRO S.A. + 2 plantas + 1 centro distribución |
| `Roles` | 10 | 8 roles AS-IS + 2 nuevos roles TO-BE |
| `Departments` | 7 | Ventas, Producción, Manufactura, QC, Logística, Finanzas, Inventarios |
| `External_participants` | 5 | 3 tipos de cliente + transportista + proveedor |
| `Documents` | 12 | Todos los documentos del proceso (Solicitud → Factura) |
| `Activities` | 13 | Las 13 actividades del proceso con tiempos AS-IS y TO-BE |
| `Events` | 7 | Inicio, fin e intermedios |
| `IT_Systems` | 12 | 5 sistemas AS-IS + 7 nuevos TO-BE con costos |
| `Risks` | 9 | Riesgos con matriz probabilidad/impacto |
| `Controls` | 8 | Controles con referencia al riesgo mitigado |
| `Others` | 14 | KPIs, restricciones, parámetros de simulación, análisis financiero |
| **Total** | **101** | |
