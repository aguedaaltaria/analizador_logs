#!/usr/bin/env python3
import datetime
import os
import sqlite3

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(DIRECTORIO_ACTUAL, "..", "datos", "logs.db")
RUTA_REPORTE = os.path.join(DIRECTORIO_ACTUAL, "..", "reporte_final.md")


def obtener_metricas():
    if not os.path.exists(RUTA_BD):
        print(f"Error: Base de datos no encontrada en {RUTA_BD}")
        return None

    conexion = sqlite3.connect(RUTA_BD)
    cursor = conexion.cursor()

    datos = {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_web": 0,
        "http_200": 0,
        "http_errores": 0,
        "rutas_fallidas": [],
        "total_sistema": 0,
        "top_servicios": [],
        "total_alertas": 0,
    }

    # 1. Métricas Web (logs_acceso)
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='logs_acceso'"
    )
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM logs_acceso")
        datos["total_web"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM logs_acceso WHERE codigo = 200")
        datos["http_200"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM logs_acceso WHERE codigo >= 400")
        datos["http_errores"] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT ruta, COUNT(*) 
            FROM logs_acceso 
            WHERE codigo >= 400 
            GROUP BY ruta 
            ORDER BY COUNT(*) DESC 
            LIMIT 2
        """)
        datos["rutas_fallidas"] = [
            f"`{r[0]}` ({r[1]} errores)" for r in cursor.fetchall()
        ]

    # 2. Métricas Sistema Operativo (logs_sistema)
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='logs_sistema'"
    )
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM logs_sistema")
        datos["total_sistema"] = cursor.fetchone()[0]

        # Inspeccionar nombres de columnas reales en la base de datos
        cursor.execute("PRAGMA table_info(logs_sistema)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        # Buscar la columna que contiene el nombre del proceso/servicio
        if "servicio" in columnas:
            col_servicio = "servicio"
        elif "programa" in columnas:
            col_servicio = "programa"
        elif "proceso" in columnas:
            col_servicio = "proceso"
        else:
            col_servicio = columnas[2]

        cursor.execute(f"""
            SELECT {col_servicio}, COUNT(*) 
            FROM logs_sistema 
            GROUP BY {col_servicio} 
            ORDER BY COUNT(*) DESC 
            LIMIT 2
        """)
        datos["top_servicios"] = [
            f"`{s[0]}` ({s[1]} eventos)" for s in cursor.fetchall()
        ]

        # Cálculo de alertas e incidentes sospechosos
        cursor.execute("""
            SELECT COUNT(*) 
            FROM logs_sistema 
            WHERE mensaje LIKE '%failed%' 
               OR mensaje LIKE '%error%' 
               OR mensaje LIKE '%warning%' 
               OR mensaje LIKE '%denied%'
        """)
        datos["total_alertas"] = cursor.fetchone()[0]

    conexion.close()
    return datos


def generar_markdown(datos):
    if not datos:
        return

    rutas_str = (
        ", ".join(datos["rutas_fallidas"])
        if datos["rutas_fallidas"]
        else "Ninguna ruta crítica detectada"
    )
    servicios_str = (
        ", ".join(datos["top_servicios"])
        if datos["top_servicios"]
        else "Sin datos suficientes"
    )

    plantilla = f"""# Reporte Ejecutivo de Análisis de Logs y Salud del Sistema

## 1. Resumen de Ejecución
- **Fecha y hora de análisis**: {datos["fecha"]}
- **Motor de ingesta**: Python + SQLite (`datos/logs.db`)
- **Orquestador**: `scripts/pipeline_completo.sh`

---

## 2. Métricas del Servidor Web (`logs_acceso`)
- **Total de solicitudes procesadas**: {datos["total_web"]} peticiones
- **Distribución HTTP**: {datos["http_200"]} exitosas (HTTP 200), {datos["http_errores"]} incidencias (4xx / 5xx)
- **Rutas con mayor tasa de fallo**: {rutas_str}

| Métrica | Visualización |
| :--- | :--- |
| **Distribución de Respuestas** | ![Distribución HTTP](datos/graficos/web_distribucion_http.png) |
| **Rutas más Solicitadas** | ![Rutas](datos/graficos/web_rutas_solicitadas.png) |
| **Direcciones IP Críticas** | ![Top IPs](datos/graficos/web_top_ips.png) |

---

## 3. Diagnóstico del Sistema Operativo (`logs_sistema`)
- **Total de eventos analizados**: {datos["total_sistema"]} eventos
- **Servicios predominantes**: {servicios_str}
- **Alertas e incidentes detectados**: {datos["total_alertas"]} eventos sospechosos/fallos

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
"""

    with open(RUTA_REPORTE, "w", encoding="utf-8") as f:
        f.write(plantilla)

    print(f"[OK] Reporte Markdown generado dinámicamente en: {RUTA_REPORTE}")


if __name__ == "__main__":
    metricas = obtener_metricas()
    generar_markdown(metricas)