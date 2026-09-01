#!/bin/bash
# ==============================================================================
# PIPELINE AUTOMATIZADO DE ANÁLISIS DE LOGS 
# Orquesta la generación, ingesta, análisis y visualización de logs.
# ==============================================================================

set -e  # Detiene la ejecución si ocurre algún error en cualquier paso

DIR_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR_PROYECTO="$(dirname "$DIR_SCRIPTS")"

cd "$DIR_SCRIPTS"

echo "======================================================"
echo "    INICIANDO PIPELINE DE ANÁLISIS DE LOGS            "
echo "======================================================"

# [FASE 1: ORIGEN] Generación y captura de eventos en archivos de texto plano (.log)
echo "[1/4] Generando logs de prueba y capturando logs reales..."
./generar_logs.sh
./generar_logs_reales.sh

# [FASE 2: INGESTA] Parseo con expresiones regulares y almacenamiento estructurado en SQLite
echo "[2/4] Ingestando datos en la base de datos SQLite..."
uv run python3 procesar_logs.py
uv run python3 procesar_logs_reales.py

# [FASE 3: TRANSFORMACIÓN] Consultas analíticas SQL para calcular métricas, errores y agregaciones
echo "[3/4] Generando reportes analíticos consolidados..."
uv run python3 reportes.py

# [FASE 4: PRESENTACIÓN] Renderizado de dashboards gráficos y reporte Markdown dinámico
echo "[4/4] Renderizando dashboard de visualizaciones y reporte Markdown..."
uv run python3 visualizador.py
uv run python3 generar_reporte_md.py

echo "======================================================"
echo "    PIPELINE COMPLETADO CON ÉXITO                     "
echo "======================================================"