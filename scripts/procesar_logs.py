#!/usr/bin/env python3
"""
MÓDULO DE INGESTIÓN Y ESTRUCTURACIÓN DE LOGS 
Lee el archivo de logs del servidor web, extrae los campos mediante
expresiones regulares y persiste los datos limpios en una base SQLite.
"""

import os
import re
import sqlite3
from typing import List, Tuple, Optional

# 1. Definición de rutas relativas basadas en la ubicación del script
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_LOG = os.path.join(DIRECTORIO_BASE, "..", "datos", "servidor_acceso.log")
RUTA_DB = os.path.join(DIRECTORIO_BASE, "..", "datos", "logs.db")

# 2. Expresión regular con grupos nombrados para formato Combined Web Log
PATRON_LOG = re.compile(
    r'^(?P<ip>\S+)\s-\s-\s\['
    r'(?P<fecha>[\w:/]+\s[+\-]\d{4})\]\s"'
    r'(?P<metodo>[A-Z]+)\s'
    r'(?P<ruta>\S+)\s'
    r'HTTP/[0-9.]+"\s'
    r'(?P<codigo>\d{3})\s'
    r'(?P<tamano>\d+)'
)


def inicializar_base_datos(ruta_db: str) -> None:
    """Crea la tabla logs_acceso si aún no existe."""
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs_acceso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            fecha TEXT NOT NULL,
            metodo TEXT NOT NULL,
            ruta TEXT NOT NULL,
            codigo INTEGER NOT NULL,
            tamano INTEGER NOT NULL
        )
        """
    )
    conexion.commit()
    conexion.close()


def parsear_linea(linea: str) -> Optional[Tuple[str, str, str, str, int, int]]:
    """Parsea una línea de texto y retorna los datos con su tipo adecuado."""
    coincidencia = PATRON_LOG.match(linea.strip())
    if coincidencia:
        datos = coincidencia.groupdict()
        return (
            datos["ip"],
            datos["fecha"],
            datos["metodo"],
            datos["ruta"],
            int(datos["codigo"]),
            int(datos["tamano"]),
        )
    return None


def procesar_archivo_logs() -> None:
    """Lee el archivo .log, procesa cada línea y realiza la inserción por lotes."""
    if not os.path.exists(RUTA_LOG):
        print(f"Error: No se encontró el archivo de log en {RUTA_LOG}")
        return

    inicializar_base_datos(RUTA_DB)

    registros: List[Tuple[str, str, str, str, int, int]] = []
    lineas_invalidas = 0

    with open(RUTA_LOG, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            fila = parsear_linea(linea)
            if fila:
                registros.append(fila)
            else:
                lineas_invalidas += 1
                print(f"Advertencia: Línea {numero_linea} no coincide con el patrón: {linea.strip()}")

    # Inserción por lotes para optimizar rendimiento I/O
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    
    # Limpiar tabla previa para pruebas repetibles
    cursor.execute("DELETE FROM logs_acceso")
    
    cursor.executemany(
        """
        INSERT INTO logs_acceso (ip, fecha, metodo, ruta, codigo, tamano)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        registros,
    )
    conexion.commit()
    total_insertados = cursor.rowcount
    conexion.close()

    print("======================================================")
    print("        REPORTE DE INGESTIÓN A BASE DE DATOS          ")
    print("======================================================")
    print(f"Base de datos destino: {RUTA_DB}")
    print(f"Registros insertados : {len(registros)}")
    print(f"Líneas descartadas   : {lineas_invalidas}")
    print("======================================================")


if __name__ == "__main__":
    procesar_archivo_logs()