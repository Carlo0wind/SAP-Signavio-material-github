# Análisis Final — INDUPRO S.A.
## SAP Signavio Regional Challenge 2026

> **Equipo:** ESPOL  
> **Fecha:** Mayo 2026  
> **Estado:** Entrega final

---

## Contenido de esta carpeta

| Archivo | Descripción | KPIs clave |
|---|---|---|
| [01_ASIS_Analisis_Correcto.md](./01_ASIS_Analisis_Correcto.md) | Análisis detallado del proceso AS-IS con **corrección de los errores del caso** | 595 min / $101.92 (correcto) |
| [02_TOBE_Modelado_Completo.md](./02_TOBE_Modelado_Completo.md) | TO-BE completo: stack tecnológico, caracterización, flujo, mapeo sistema→actividad | 281 min / $47.21 |
| [03_Plan_Implementacion.md](./03_Plan_Implementacion.md) | Plan de 90 días, 3 fases, roles, horas, actividades y cronograma | 3 fases · 90 días |
| [04_Presupuesto_Detallado.md](./04_Presupuesto_Detallado.md) | Presupuesto desglosado por sistema, rol, hora y fase | USD $50,000 exactos |

---

## Síntesis Ejecutiva

### El Problema (AS-IS Correcto)

> ⚠️ **Los KPIs del caso tienen errores matemáticos:**
> - El caso dice **555 min / $105.91** para la ruta fabricación + reproceso
> - El valor **correcto es 595 min / $101.92** (el caso omitió 6B y sumó 6A indebidamente)
> - Ver detalle completo en `01_ASIS_Analisis_Correcto.md`, Sección 4

El proceso actual de INDUPRO opera con:
- **4 sistemas completamente desconectados** (ERP legacy, sistema financiero, logística, facturación)
- **Flujo 100% secuencial** — verificación de crédito y consulta de stock en serie, no en paralelo
- **Control de calidad reactivo** → 18% de lotes rechazados → 90 min de reproceso por lote
- **Sin visibilidad** de estado del pedido para el cliente

### La Solución (TO-BE)

**Arquitectura basada en Middleware Central:**

```
CLIENTE → Portal Web → SAP Integration Suite (Middleware)
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   API ERP Legacy      API Sistema          Sistema QC
   (Inventario)        Financiero           Digital
                              │
                   TMS (Beetrack) + Facturación Electrónica (Datil.me)
```

**Stack tecnológico preciso:**

| Sistema | Herramienta | Costo |
|---|---|---|
| Middleware | **SAP Integration Suite** (SAP BTP) | $12,000 |
| Portal de pedidos | **Aplicación web** (SAP BTP Build Apps / custom) | $10,000 |
| API inventario | **REST API Layer** sobre ERP Legacy vía Integration Suite | $8,000 |
| API crédito | **REST API Layer** sobre Sistema Financiero | $5,000 |
| Control de calidad | **Sistema QC Digital** (app móvil/web + tablets) | $4,000 |
| Logística | **TMS Beetrack** (SaaS LATAM) | $5,500 |
| Facturación | **Datil.me** (SRI Ecuador compliant) | $2,500 |
| Capacitación | Instructor externo + materiales | $3,000 |
| **TOTAL** | | **$50,000 ✅** |

### Resultados Esperados

| KPI | AS-IS (correcto) | TO-BE | Mejora |
|---|---|---|---|
| Tiempo de ciclo (fab. + reproceso) | **595 min** | **341 min** | −42.7% ✅ |
| Tiempo de ciclo (fab. sin reproceso) | **505 min** | **281 min** | −44.4% ✅ |
| Costo por pedido (sin reproceso) | **$101.91** | **$47.21** | −53.7% ✅ |
| Tasa de reproceso | **18%** | **5%** | −72.2% ✅ |
| Tiempo de verificación crédito | **60 min** | **15 min (paralelo)** | −75% ✅ |

### ROI del Proyecto

| Indicador | Valor |
|---|---|
| Inversión total | $50,000 |
| Ahorro mensual estimado | ~$35,602/mes |
| Payback | **1.4 meses** ✅ |
| ROI a 12 meses | **754%** |

---

## Restricciones del Caso — Cumplimiento

| Restricción | Límite | Propuesta | Estado |
|---|---|---|---|
| Presupuesto | $50,000 | $50,000 exactos | ✅ |
| Costo por pedido | < $70.00 | $47.21 (sin rep.) / $55.21 (con rep.) | ✅ |
| Nuevos roles | Máximo 2 | 2 (Analista Integración + Op. QC) | ✅ |
| Fabricación | 120 min INAMOVIBLE | 120 min mantenido | ✅ |
| Inspección QC | 30 min INAMOVIBLE | 30 min mantenido | ✅ |
| Tiempo total | < 350 min | 281 / 341 min | ✅ |

---

*SAP Signavio Regional Challenge 2026 · ESPOL*
