#!/usr/bin/env python3
"""
MÓDULO DE INGESTIÓN DE LOGS DEL SISTEMA
Lee servidor_acceso_real.log, extrae procesos, PIDs y mensajes,
y los persiste en la tabla logs_sistema dentro de logs.db.
"""

import os
import re
import sqlite3
from typing import List, Tuple, Optional

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_LOG_REAL = os.path.join(DIRECTORIO_BASE, "..", "datos", "servidor_acceso_real.log")
RUTA_DB = os.path.join(DIRECTORIO_BASE, "..", "datos", "logs.db")

PATRON_SYSLOG = re.compile(
    r'^(?P<fecha>[A-Z][a-z]{2}\s+\d+\s\d{2}:\d{2}:\d{2})\s+'
    r'(?P<hostname>\S+)\s+'
    r'(?P<proceso>[^:\[]+)'
    r'(?:\[(?P<pid>\d+)\])?:\s*'
    r'(?P<mensaje>.*)$'
)


def inicializar_tabla_sistema(ruta_db: str) -> None:
    """Crea la tabla logs_sistema en la base de datos común."""
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            hostname TEXT NOT NULL,
            proceso TEXT NOT NULL,
            pid INTEGER,
            mensaje TEXT NOT NULL
        )
        """
    )
    conexion.commit()
    conexion.close()


def parsear_linea_sistema(linea: str) -> Optional[Tuple[str, str, str, Optional[int], str]]:
    """Parsea una línea de syslog y devuelve la tupla tipada."""
    coincidencia = PATRON_SYSLOG.match(linea.strip())
    if coincidencia:
        datos = coincidencia.groupdict()
        pid_valor = int(datos["pid"]) if datos["pid"] else None
        return (
            datos["fecha"],
            datos["hostname"],
            datos["proceso"].strip(),
            pid_valor,
            datos["mensaje"].strip(),
        )
    return None


def procesar_archivo_sistema() -> None:
    """Lee servidor_acceso_real.log e inserta por lotes en SQLite."""
    if not os.path.exists(RUTA_LOG_REAL):
        print(f"Error: No se encontró {RUTA_LOG_REAL}")
        return

    inicializar_tabla_sistema(RUTA_DB)

    registros: List[Tuple[str, str, str, Optional[int], str]] = []
    lineas_descartadas = 0

    with open(RUTA_LOG_REAL, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue
            fila = parsear_linea_sistema(linea)
            if fila:
                registros.append(fila)
            else:
                lineas_descartadas += 1

    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM logs_sistema")
    cursor.executemany(
        """
        INSERT INTO logs_sistema (fecha, hostname, proceso, pid, mensaje)
        VALUES (?, ?, ?, ?, ?)
        """,
        registros,
    )
    conexion.commit()
    conexion.close()

    print("======================================================")
    print("      INGESTIÓN DE LOGS DE SISTEMA (SQLITE)           ")
    print("======================================================")
    print(f"Base de datos destino : {RUTA_DB}")
    print(f"Eventos insertados    : {len(registros)}")
    print(f"Líneas descartadas    : {lineas_descartadas}")
    print("======================================================")


if __name__ == "__main__":
    procesar_archivo_sistema()