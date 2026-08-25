#!/usr/bin/env bash

# ==============================================================================
# SCRIPT DE APRENDIZAJE: EXTRACCIÓN DE LOGS REALES DEL SISTEMA LINUX
#
# NOTA: Este script fue creado exclusivamente con fines educativos para aprender
# cómo extraer registros reales generados por el propio sistema operativo Linux
# (usando journalctl / systemd) hacia un archivo de texto de nuestro proyecto.
# ==============================================================================

# 1. Definir la ruta del archivo de salida
ARCHIVO_SALIDA_REAL="../datos/servidor_acceso_real.log"

# 2. Mensaje inicial en la terminal
echo "Iniciando la extracción de registros reales de la máquina..."

# 3. Limpiar o crear el archivo de destino para empezar desde cero
> "$ARCHIVO_SALIDA_REAL"

# 4. Extraer los últimos 30 registros reales del sistema
#    - journalctl: comando para consultar los logs de systemd en Linux
#    - -n 30: limita la salida a los 30 eventos más recientes
#    - --no-pager: vuelca el texto directo sin abrir el visor interactivo
#    - >: guarda todo el resultado en el archivo especificado
journalctl -n 30 --no-pager > "$ARCHIVO_SALIDA_REAL"

# 5. Confirmar que el proceso terminó con éxito
echo "¡Extracción completada con éxito!"
echo "Archivo creado en: $ARCHIVO_SALIDA_REAL"
echo "Total de líneas guardadas:"
wc -l "$ARCHIVO_SALIDA_REAL"