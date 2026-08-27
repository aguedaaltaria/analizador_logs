#!/usr/bin/env bash

# ==============================================================================
# SCRIPT CLASIFICADOR Y ENRUTADOR AUTOMÁTICO DE LOGS
# ==============================================================================

ARCHIVO_ENTRADA="$1"

if [ -z "$ARCHIVO_ENTRADA" ]; then
    echo "Uso correcto: $0 <ruta_al_archivo_de_log>"
    echo "Ejemplo: $0 ../datos/servidor_acceso.log"
    exit 1
fi

if [ ! -f "$ARCHIVO_ENTRADA" ]; then
    echo "Error: El archivo '$ARCHIVO_ENTRADA' no existe."
    exit 1
fi

echo "======================================================"
echo "         DETECTOR Y CLASIFICADOR DE LOGS              "
echo " Analizando archivo: $ARCHIVO_ENTRADA"
echo "======================================================"

PRIMERA_LINEA=$(head -n 1 "$ARCHIVO_ENTRADA")

echo "Muestra del registro detectado:"
echo "> $PRIMERA_LINEA"
echo "------------------------------------------------------"

# Huellas de servidor web (GET, POST, HTTP)
if echo "$PRIMERA_LINEA" | grep -q -E '("GET |"POST |"PUT |"DELETE |HTTP/[0-9])'; then
    echo "[CLASIFICACIÓN]: Log de Servidor Web (Nginx / Apache / Flask)"
    echo "[ACCIÓN]: Redirigiendo a analizador.sh..."
    echo "======================================================"
    echo ""
    ./analizador.sh "$ARCHIVO_ENTRADA"

# Comienza con un mes de Syslog (Aug, Sep, Oct, etc.)
elif echo "$PRIMERA_LINEA" | grep -q -E '^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]+[0-9]+'; then
    echo "[CLASIFICACIÓN]: Log del Sistema Operativo Linux (Syslog / Journal)"
    echo "[ACCIÓN]: Redirigiendo a analizador_real.sh..."
    echo "======================================================"
    echo ""
    ./analizador_real.sh "$ARCHIVO_ENTRADA"

else
    echo "[ERROR]: Formato desconocido o no soportado."
    echo "No coincide con el estándar de Servidor Web ni con Syslog de Linux."
    exit 1
fi