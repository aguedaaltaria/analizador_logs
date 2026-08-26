#!/usr/bin/env bash

if [ "$1" == "real" ]; then
    ARCHIVO_LOG="../datos/servidor_acceso_real.log"
else
    ARCHIVO_LOG="../datos/servidor_acceso.log"
fi

if [ ! -f "$ARCHIVO_LOG" ]; then
    echo "Error: No se encontró el archivo de log en $ARCHIVO_LOG"
    exit 1
fi

echo "======================================================"
echo "         REPORTE DE ESTADO DEL SERVIDOR              "
echo " Archivo: $ARCHIVO_LOG"
echo "======================================================"

TOTAL_PETICIONES=$(wc -l < "$ARCHIVO_LOG")
echo "1. Total de peticiones procesadas: $TOTAL_PETICIONES"
echo "------------------------------------------------------"

echo "2. Distribución de respuestas HTTP:"
awk '{print $9}' "$ARCHIVO_LOG" | sort | uniq -c | sort -nr
echo "------------------------------------------------------"

echo "3. Top 3 de direcciones IP con más tráfico:"
awk '{print $1}' "$ARCHIVO_LOG" | sort | uniq -c | sort -nr | head -n 3
echo "------------------------------------------------------"

echo "4. Endpoints más solicitados:"
awk '{print $7}' "$ARCHIVO_LOG" | sort | uniq -c | sort -nr
echo "------------------------------------------------------"

echo "5. Alerta de fallos internos (Errores 500):"
CONTEO_500=$(grep -c " 500 " "$ARCHIVO_LOG")

if [ "$CONTEO_500" -gt 0 ]; then
    echo "¡Atención! Se detectaron $CONTEO_500 errores 500 en las siguientes rutas:"
    grep " 500 " "$ARCHIVO_LOG" | awk '{print "   - IP:", $1, "falló en la ruta:", $7}'
    echo "------------------------------------------------------"
else
    echo "No se registraron errores críticos 500."
    echo "------------------------------------------------------"
fi

echo "6. Desglose global de incidentes (4xx y 5xx):"
TOTAL_ERRORES=$(grep -c -E " (400|403|404|500) " "$ARCHIVO_LOG")

if [ "$TOTAL_ERRORES" -gt 0 ]; then
    echo "Total de incidencias detectadas: $TOTAL_ERRORES"
    grep -E " (400|403|404|500) " "$ARCHIVO_LOG" | awk '{print "   - IP:", $1, "| Código:", $9, "| Ruta:", $7}'
else
    echo "No se detectaron errores 4xx ni 5xx en el archivo."
fi

echo "======================================================"
echo "Fin del reporte."