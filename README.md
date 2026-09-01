# 📊 Data Pipeline Automatizado de Análisis de Logs y Salud del Sistema

Un pipeline ETL (*Extract, Transform, Load*) y analítico completo implementado en **Linux**, **Bash**, **Python** y **SQLite**. El sistema captura registros sin procesar (logs sintéticos y del sistema operativo real), valida y estructura los datos con expresiones regulares, persiste la información en una base relacional, genera métricas analíticas mediante SQL, renderiza un dashboard de visualizaciones gráficas y compila un reporte ejecutivo dinámico en Markdown.

---

## 🏗️ Arquitectura del Pipeline

El flujo de datos sigue 4 fases secuenciales estrictas, coordinadas por un orquestador unificado con manejo de errores (`set -e`):

- **Fase 1 (Origen)**: Generación de logs de acceso web sintéticos y extracción segura de logs de sistema mediante `journalctl`.
- **Fase 2 (Ingesta y Persistencia)**: Validación defensiva mediante expresiones regulares (`Regex`), descarte de registros no válidos e inserción transaccional en `datos/logs.db`.
- **Fase 3 (Transformación y Métricas)**: Consultas SQL consolidadas para calcular tasas de fallos (códigos 4xx/5xx), volumen de tráfico en bytes, endpoints críticos y anomalías del kernel/servicios.
- **Fase 4 (Presentación y Reporte)**: Renderizado automatizado de 6 gráficos estadísticos en alta resolución (`.png`) y compilación dinámica del documento ejecutivo `reporte_final.md`.

---

## 📂 Estructura del Repositorio

```text
analizador_logs/
├── datos/
│   ├── logs.db                    # Base de datos relacional SQLite (ignorado en git)
│   ├── servidor_acceso.log        # Registro de peticiones web (ignorado en git)
│   ├── servidor_acceso_real.log   # Registro del sistema operativo (ignorado en git)
│   └── graficos/                  # Dashboard de imágenes exportadas (ignorado en git)
│       ├── web_distribucion_http.png
│       ├── web_rutas_solicitadas.png
│       ├── web_top_ips.png
│       ├── sistema_eventos_servicios.png
│       ├── sistema_incidentes_servicio.png
│       └── sistema_pids_actividad.png
├── scripts/
│   ├── generar_logs.sh            # Simulación de tráfico HTTP
│   ├── generar_logs_reales.sh     # Extracción de eventos de journalctl
│   ├── procesar_logs.py           # Ingesta y validación de logs web
│   ├── procesar_logs_reales.py    # Ingesta y validación de logs de sistema
│   ├── reportes.py                # Consultas analíticas SQL en consola
│   ├── visualizador.py            # Generación del dashboard de gráficos
│   ├── generar_reporte_md.py      # Generador dinámico de reporte ejecutivo
│   └── pipeline_completo.sh       # Orquestador del pipeline completo
├── reporte_final.md               # Reporte ejecutivo autogenerado
├── pyproject.toml                 # Gestión de dependencias con uv
└── README.md                      # Documentación del proyecto
