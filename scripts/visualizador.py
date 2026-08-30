#!/usr/bin/env python3
"""
MÓDULO DE VISUALIZACIÓN COMPLETA DE LOGS (DÍA 4)
Genera gráficos para Logs de Servidor Web (HTTP / Combined Access Log)
y Logs del Sistema Operativo (Linux Syslog / Systemd Journal).
"""

import os
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(DIRECTORIO_BASE, "..", "datos", "logs.db")
CARPETA_GRAFICOS = os.path.join(DIRECTORIO_BASE, "..", "datos", "graficos")

sns.set_theme(style="whitegrid")


# ==============================================================================
# LOGS DE SERVIDOR WEB (HTTP / Combined Access Log) -> Tabla: logs_acceso
# ==============================================================================

def generar_graficos_web(conexion: sqlite3.Connection) -> None:
    cursor = conexion.cursor()

    # Verificación de existencia de datos web
    cursor.execute("SELECT COUNT(*) FROM logs_acceso")
    total_web = cursor.fetchone()[0]

    if total_web == 0:
        print("No se encontraron registros de Logs de Servidor Web (HTTP / Combined Access Log).")
        print("Omitiendo la generación de gráficos web.")
        return

    print(f"Generando gráficos para Logs de Servidor Web ({total_web} registros encontrados)...")

    # 1. Distribución HTTP
    cursor.execute("SELECT CAST(codigo AS TEXT), COUNT(*) FROM logs_acceso GROUP BY codigo ORDER BY 2 DESC")
    datos_http = cursor.fetchall()
    if datos_http:
        codigos, totales = [f"HTTP {f[0]}" for f in datos_http], [f[1] for f in datos_http]
        plt.figure(figsize=(8, 5))
        barras = sns.barplot(x=codigos, y=totales, palette="viridis", hue=codigos, legend=False)
        plt.title("1. Distribución de Respuestas HTTP (Logs de Servidor Web)", fontsize=13, pad=15)
        plt.xlabel("Código de Estado", fontsize=11)
        plt.ylabel("Peticiones", fontsize=11)
        for b in barras.patches:
            barras.annotate(f"{int(b.get_height())}", (b.get_x() + b.get_width() / 2., b.get_height()),
                            ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "web_distribucion_http.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: web_distribucion_http.png")

    # 2. Rutas Solicitadas
    cursor.execute("SELECT ruta, COUNT(*) FROM logs_acceso GROUP BY ruta ORDER BY 2 ASC")
    datos_rutas = cursor.fetchall()
    if datos_rutas:
        rutas, totales = [f[0] for f in datos_rutas], [f[1] for f in datos_rutas]
        plt.figure(figsize=(9, 5))
        barras = sns.barplot(x=totales, y=rutas, palette="magma", hue=rutas, legend=False)
        plt.title("2. Endpoints Más Solicitados (Logs de Servidor Web)", fontsize=13, pad=15)
        plt.xlabel("Total Peticiones", fontsize=11)
        plt.ylabel("Ruta", fontsize=11)
        for b in barras.patches:
            barras.annotate(f"{int(b.get_width())}", (b.get_width(), b.get_y() + b.get_height() / 2.),
                            ha='left', va='center', fontsize=10, xytext=(5, 0), textcoords='offset points')
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "web_rutas_solicitadas.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: web_rutas_solicitadas.png")

    # 3. Top Direcciones IP
    cursor.execute("SELECT ip, COUNT(*) FROM logs_acceso GROUP BY ip ORDER BY 2 DESC LIMIT 5")
    datos_ips = cursor.fetchall()
    if datos_ips:
        ips, totales = [f[0] for f in datos_ips], [f[1] for f in datos_ips]
        plt.figure(figsize=(8, 5))
        barras = sns.barplot(x=ips, y=totales, palette="crest", hue=ips, legend=False)
        plt.title("3. Top 5 Direcciones IP con Más Tráfico (Logs de Servidor Web)", fontsize=13, pad=15)
        plt.xlabel("Dirección IP", fontsize=11)
        plt.ylabel("Peticiones", fontsize=11)
        for b in barras.patches:
            barras.annotate(f"{int(b.get_height())}", (b.get_x() + b.get_width() / 2., b.get_height()),
                            ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "web_top_ips.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: web_top_ips.png")


# ==============================================================================
# LOGS DEL SISTEMA OPERATIVO (Linux Syslog / Systemd Journal) -> Tabla: logs_sistema
# ==============================================================================

def generar_graficos_sistema(conexion: sqlite3.Connection) -> None:
    cursor = conexion.cursor()

    # Verificación de existencia de datos de sistema
    cursor.execute("SELECT COUNT(*) FROM logs_sistema")
    total_sistema = cursor.fetchone()[0]

    if total_sistema == 0:
        print("No se encontraron registros de Logs del Sistema Operativo (Linux Syslog / Systemd Journal).")
        print("Omitiendo la generación de gráficos de sistema.")
        return

    print(f"Generando gráficos para Logs del Sistema Operativo ({total_sistema} registros encontrados)...")

    # 4. Proporción de Servicios (Donut Chart)
    cursor.execute("SELECT proceso, COUNT(*) FROM logs_sistema GROUP BY proceso ORDER BY 2 DESC LIMIT 5")
    datos_servicios = cursor.fetchall()
    if datos_servicios:
        procesos, totales = [f[0] for f in datos_servicios], [f[1] for f in datos_servicios]
        plt.figure(figsize=(7, 7))
        colores = sns.color_palette("pastel")[0:len(procesos)]
        plt.pie(totales, labels=procesos, autopct="%1.1f%%", startangle=140, colors=colores,
                wedgeprops=dict(width=0.4, edgecolor='w'))
        plt.title("4. Actividad General por Servicio (Logs de Sistema)", fontsize=13, pad=15)
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "sistema_eventos_servicios.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: sistema_eventos_servicios.png")

    # 5. Incidentes y Errores por Servicio
    cursor.execute(
        """
        SELECT proceso, COUNT(*) 
        FROM logs_sistema 
        WHERE mensaje LIKE '%failed%' OR mensaje LIKE '%error%' OR mensaje LIKE '%critical%'
        GROUP BY proceso 
        ORDER BY 2 ASC
        """
    )
    datos_fallos = cursor.fetchall()
    if datos_fallos:
        procesos, totales = [f[0] for f in datos_fallos], [f[1] for f in datos_fallos]
        plt.figure(figsize=(9, 5))
        barras = sns.barplot(x=totales, y=procesos, palette="flare", hue=procesos, legend=False)
        plt.title("5. Fallos y Errores Detectados por Servicio (Logs de Sistema)", fontsize=13, pad=15)
        plt.xlabel("Total Incidentes", fontsize=11)
        plt.ylabel("Servicio", fontsize=11)
        for b in barras.patches:
            barras.annotate(f"{int(b.get_width())}", (b.get_width(), b.get_y() + b.get_height() / 2.),
                            ha='left', va='center', fontsize=10, xytext=(5, 0), textcoords='offset points')
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "sistema_incidentes_servicio.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: sistema_incidentes_servicio.png")

    # 6. Actividad por PID (Identificador de Proceso)
    cursor.execute("SELECT 'PID ' || CAST(pid AS TEXT), COUNT(*) FROM logs_sistema WHERE pid IS NOT NULL GROUP BY pid ORDER BY 2 DESC LIMIT 5")
    datos_pids = cursor.fetchall()
    if datos_pids:
        pids, totales = [f[0] for f in datos_pids], [f[1] for f in datos_pids]
        plt.figure(figsize=(8, 5))
        barras = sns.barplot(x=pids, y=totales, palette="Blues_r", hue=pids, legend=False)
        plt.title("6. Carga de Eventos por PID (Logs de Sistema)", fontsize=13, pad=15)
        plt.xlabel("Identificador (PID)", fontsize=11)
        plt.ylabel("Eventos Registrados", fontsize=11)
        for b in barras.patches:
            barras.annotate(f"{int(b.get_height())}", (b.get_x() + b.get_width() / 2., b.get_height()),
                            ha='center', va='bottom', fontsize=10, xytext=(0, 3), textcoords='offset points')
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_GRAFICOS, "sistema_pids_actividad.png"), dpi=300)
        plt.close()
        print("   - [OK] Generado: sistema_pids_actividad.png")


def main() -> None:
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    if not os.path.exists(RUTA_DB):
        print(f"Error: Base de datos no encontrada en {RUTA_DB}")
        return

    conexion = sqlite3.connect(RUTA_DB)
    print("======================================================")
    print("      GENERACIÓN COMPLETA: DASHBOARDS GRÁFICOS        ")
    print("======================================================")
    generar_graficos_web(conexion)
    print("------------------------------------------------------")
    generar_graficos_sistema(conexion)
    conexion.close()
    print("======================================================")
    print("Proceso de visualización finalizado.")


if __name__ == "__main__":
    main()