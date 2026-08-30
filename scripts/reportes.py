#!/usr/bin/env python3
"""
MÓDULO DE REPORTES ANALÍTICOS (DÍA 3)
Ejecuta consultas SQL sobre SQLite (logs.db) para generar resúmenes
ejecutivos de tráfico web e incidentes del sistema operativo.
"""

import os
import sqlite3

# 1. Definición de rutas relativas seguras
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(DIRECTORIO_BASE, "..", "datos", "logs.db")


def obtener_conexion(ruta_db: str) -> sqlite3.Connection:
    """Abre conexión con la base de datos verificando su existencia."""
    if not os.path.exists(ruta_db):
        raise FileNotFoundError(f"No se encontró la base de datos en {ruta_db}")
    return sqlite3.connect(ruta_db)


def reporte_servidor_web(conexion: sqlite3.Connection) -> None:
    """Genera métricas analíticas sobre la tabla logs_acceso."""
    cursor = conexion.cursor()

    print("======================================================")
    print("        REPORTE SQL: SERVIDOR WEB (logs_acceso)       ")
    print("======================================================")

    # Métrica 1: Total de peticiones y volumen transferido
    cursor.execute("SELECT COUNT(*), SUM(tamano), AVG(tamano) FROM logs_acceso")
    total_peticiones, total_bytes, promedio_bytes = cursor.fetchone()
    print(f"Total de peticiones procesadas : {total_peticiones}")
    print(f"Tráfico total transferido      : {total_bytes or 0} bytes")
    print(f"Tamaño promedio por respuesta  : {promedio_bytes or 0:.2f} bytes")
    print("------------------------------------------------------")

    # Métrica 2: Distribución por código de estado HTTP
    print("Distribución de códigos de estado HTTP:")
    cursor.execute(
        """
        SELECT codigo, COUNT(*) AS cantidad
        FROM logs_acceso
        GROUP BY codigo
        ORDER BY cantidad DESC
        """
    )
    for codigo, cantidad in cursor.fetchall():
        print(f"   - HTTP {codigo}: {cantidad} peticiones")
    print("------------------------------------------------------")

    # Métrica 3: Top 3 de IPs con más tráfico
    print("Top 3 direcciones IP más activas:")
    cursor.execute(
        """
        SELECT ip, COUNT(*) AS cantidad
        FROM logs_acceso
        GROUP BY ip
        ORDER BY cantidad DESC
        LIMIT 3
        """
    )
    for ip, cantidad in cursor.fetchall():
        print(f"   - IP {ip}: {cantidad} peticiones")
    print("------------------------------------------------------")

    # Métrica 4: Endpoints con errores (4xx y 5xx)
    print("Rutas afectadas por errores 4xx / 5xx:")
    cursor.execute(
        """
        SELECT ruta, codigo, COUNT(*) AS total
        FROM logs_acceso
        WHERE codigo >= 400
        GROUP BY ruta, codigo
        ORDER BY total DESC
        """
    )
    filas_errores = cursor.fetchall()
    if filas_errores:
        for ruta, codigo, total in filas_errores:
            print(f"   - [{codigo}] {ruta}: {total} incidencia(s)")
    else:
        print("   - No se registraron respuestas 4xx ni 5xx.")
    print("======================================================\n")


def reporte_sistema_operativo(conexion: sqlite3.Connection) -> None:
    """Genera métricas analíticas sobre la tabla logs_sistema."""
    cursor = conexion.cursor()

    print("======================================================")
    print("       REPORTE SQL: SISTEMA OPERATIVO (logs_sistema)  ")
    print("======================================================")

    # Métrica 1: Total de eventos registrados
    cursor.execute("SELECT COUNT(*) FROM logs_sistema")
    total_eventos = cursor.fetchone()[0]
    print(f"Total de eventos de sistema    : {total_eventos}")
    print("------------------------------------------------------")

    # Métrica 2: Top 3 programas con mayor actividad
    print("Top 3 programas/servicios con más eventos:")
    cursor.execute(
        """
        SELECT proceso, COUNT(*) AS total
        FROM logs_sistema
        GROUP BY proceso
        ORDER BY total DESC
        LIMIT 3
        """
    )
    for proceso, total in cursor.fetchall():
        print(f"   - {proceso}: {total} eventos")
    print("------------------------------------------------------")

    # Métrica 3: Detección de fallos y errores del sistema
    print("Alertas e incidentes detectados en Linux:")
    cursor.execute(
        """
        SELECT fecha, proceso, pid, mensaje
        FROM logs_sistema
        WHERE mensaje LIKE '%failed%'
           OR mensaje LIKE '%error%'
           OR mensaje LIKE '%critical%'
           OR mensaje LIKE '%died%'
        ORDER BY id ASC
        """
    )
    fallos = cursor.fetchall()
    if fallos:
        print(f"Total de incidencias encontradas: {len(fallos)}")
        for fecha, proceso, pid, mensaje in fallos:
            pid_str = f"PID {pid}" if pid else "Sin PID"
            # Truncamos mensajes largos a 60 caracteres para visualización limpia
            msg_corto = mensaje[:60] + "..." if len(mensaje) > 60 else mensaje
            print(f"   - [{fecha}] [{proceso} ({pid_str})]: {msg_corto}")
    else:
        print("   - No se detectaron fallos críticos.")
    print("======================================================")


def ejecutar_reportes() -> None:
    """Orquesta la ejecución de ambos reportes."""
    try:
        conexion = obtener_conexion(RUTA_DB)
        reporte_servidor_web(conexion)
        reporte_sistema_operativo(conexion)
        conexion.close()
    except FileNotFoundError as err:
        print(f"Error: {err}")
    except sqlite3.Error as err:
        print(f"Error de base de datos SQLite: {err}")


if __name__ == "__main__":
    ejecutar_reportes()