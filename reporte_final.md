# Reporte Ejecutivo de Análisis de Logs y Salud del Sistema

## 1. Resumen de Ejecución
- **Fecha y hora de análisis**: 2026-08-31 19:57:00
- **Motor de ingesta**: Python + SQLite (`datos/logs.db`)
- **Orquestador**: `scripts/pipeline_completo.sh`

---

## 2. Métricas del Servidor Web (`logs_acceso`)
- **Total de solicitudes procesadas**: 50 peticiones
- **Distribución HTTP**: 32 exitosas (HTTP 200), 18 incidencias (4xx / 5xx)
- **Rutas con mayor tasa de fallo**: `/login` (6 errores), `/inicio` (4 errores)

| Métrica | Visualización |
| :--- | :--- |
| **Distribución de Respuestas** | ![Distribución HTTP](datos/graficos/web_distribucion_http.png) |
| **Rutas más Solicitadas** | ![Rutas](datos/graficos/web_rutas_solicitadas.png) |
| **Direcciones IP Críticas** | ![Top IPs](datos/graficos/web_top_ips.png) |

---

## 3. Diagnóstico del Sistema Operativo (`logs_sistema`)
- **Total de eventos analizados**: 30 eventos
- **Servicios predominantes**: `nautilus` (14 eventos), `systemd` (13 eventos)
- **Alertas e incidentes detectados**: 12 eventos sospechosos/fallos

| Métrica | Visualización |
| :--- | :--- |
| **Proporción por Servicio** | ![Servicios](datos/graficos/sistema_eventos_servicios.png) |
| **Incidentes por Proceso** | ![Incidentes](datos/graficos/sistema_incidentes_servicio.png) |
| **Actividad por PID** | ![Carga por PID](datos/graficos/sistema_pids_actividad.png) |

---

## 4. Arquitectura del Pipeline
1. **Fase 1 (Origen)**: Generación y captura desatendida de logs planos.
2. **Fase 2 (Ingesta)**: Validación defensiva con Regex y almacenamiento relacional en SQLite.
3. **Fase 3 (Transformación)**: Extracción de métricas analíticas en SQL.
4. **Fase 4 (Presentación)**: Renderizado de dashboards gráficos con Seaborn/Matplotlib y exportación de este informe dinámico.
