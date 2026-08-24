#!/usr/bin/env bash

# ==========================================
# CONFIGURACIÓN
# ==========================================
ARCHIVO_SALIDA="../datos/servidor_acceso.log"

# Limpiamos el archivo para que empiece desde cero
> "$ARCHIVO_SALIDA"

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

# 1. Función para elegir una IP
obtener_ip() {
    local opciones=("192.168.1.10" "192.168.1.25" "10.0.0.15" "172.16.0.4" "203.0.113.195")
    # shuf elige 1 elemento al azar de la lista
    echo "${opciones[@]}" | tr ' ' '\n' | shuf -n 1
}

# 2. Función para elegir un método HTTP
obtener_metodo() {
    local opciones=("GET" "POST")
    echo "${opciones[@]}" | tr ' ' '\n' | shuf -n 1
}

# 3. Función para elegir una ruta web
obtener_ruta() {
    local opciones=("/inicio" "/login" "/panel" "/api/datos" "/contacto")
    echo "${opciones[@]}" | tr ' ' '\n' | shuf -n 1
}

# 4. Función para elegir un código de estado
obtener_codigo_estado() {
    local opciones=("200" "200" "200" "404" "500" "403")
    echo "${opciones[@]}" | tr ' ' '\n' | shuf -n 1
}

# 5. Función para generar un tamaño en bytes
obtener_tamano() {
    # Genera un número entero aleatorio entre 200 y 4000
    shuf -i 200-4000 -n 1
}

# 6. Función para obtener la fecha y hora formateada
obtener_fecha() {
    date +"%d/%b/%Y:%H:%M:%S +0000"
}

# ==========================================
# BUCLE PRINCIPAL (GENERAR REGISTROS)
# ==========================================

echo "Generando registros de log de forma sencilla..."

for numero_linea in {1..50}; do
    # Paso A: Llamar a cada función y guardar su resultado
    ip=$(obtener_ip)
    metodo=$(obtener_metodo)
    ruta=$(obtener_ruta)
    codigo=$(obtener_codigo_estado)
    tamano=$(obtener_tamano)
    fecha=$(obtener_fecha)

    # Paso B: Unir todos los datos en una sola línea de texto
    linea_log="$ip - - [$fecha] \"$metodo $ruta HTTP/1.1\" $codigo $tamano"

    # Paso C: Guardar la línea en el archivo de texto
    echo "$linea_log" >> "$ARCHIVO_SALIDA"
done

echo "¡Listo! Se guardaron 50 registros en $ARCHIVO_SALIDA"