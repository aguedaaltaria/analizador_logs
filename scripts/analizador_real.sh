#!/usr/bin/env bash

# ==============================================================================
# ANALIZADOR DEDICADO PARA LOGS DEL SISTEMA OPERATIVO (SYSLOG / SYSTEMD)
# ==============================================================================

# ARCHIVO_LOG="../datos/servidor_acceso_real.log"

ARCHIVO_LOG="${1:-../datos/servidor_acceso_real.log}"

if [ ! -f "$ARCHIVO_LOG" ]; then
    echo "Error: No se encontró el archivo de log en $ARCHIVO_LOG"
    exit 1
fi

echo "======================================================"
echo "       REPORTE DE SALUD DEL SISTEMA OPERATIVO         "
echo " Archivo: $ARCHIVO_LOG"
echo "======================================================"

TOTAL_EVENTOS=$(wc -l < "$ARCHIVO_LOG")
echo "1. Total de eventos del sistema procesados: $TOTAL_EVENTOS"
echo "------------------------------------------------------"

echo "2. Top 3 de programas/servicios con mayor actividad:"
awk '{print $5}' "$ARCHIVO_LOG" | sed -E 's/\[[0-9]+\]:?|://g' | sort | uniq -c | sort -nr | head -n 3
echo "------------------------------------------------------"

echo "3. Detección de incidentes del sistema (Failed, Error, CRITICAL, Died):"
TOTAL_FALLOS=$(grep -c -E -i "(failed|error|critical|died)" "$ARCHIVO_LOG")

if [ "$TOTAL_FALLOS" -gt 0 ]; then
    echo "¡Atención! Se detectaron $TOTAL_FALLOS incidencias en el sistema:"
    echo ""
    grep -E -i "(failed|error|critical|died)" "$ARCHIVO_LOG" | awk '{
        proceso = $5;
        gsub(/\[[0-9]+\]:?|:/, "", proceso);
        hora = $3;
        $1=$2=$3=$4=$5="";
        print "   - [" hora "] [" proceso "]:" $0
    }'
else
    echo "No se registraron fallos ni advertencias críticas."
fi

echo "======================================================"
echo "Fin del reporte del sistema."