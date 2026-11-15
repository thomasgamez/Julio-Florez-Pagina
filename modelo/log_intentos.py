# =========================================================
# modelo/log_intentos.py — Límite de intentos fallidos de login
# =========================================================
import time
from modelo.conexion import obtener_conexion

MAX_INTENTOS = 5
VENTANA_SEGUNDOS = 10 * 60  # 10 minutos


def bloqueado(clave):
    desde = time.time() - VENTANA_SEGUNDOS
    con = obtener_conexion()
    n = con.execute(
        "SELECT COUNT(*) FROM intentos_login WHERE clave = ? AND momento > ?", (clave, desde)
    ).fetchone()[0]
    con.close()
    return n >= MAX_INTENTOS


def registrar_fallo(clave):
    con = obtener_conexion()
    con.execute("INSERT INTO intentos_login (clave, momento) VALUES (?,?)", (clave, time.time()))
    con.execute("DELETE FROM intentos_login WHERE momento < ?", (time.time() - VENTANA_SEGUNDOS,))
    con.commit()
    con.close()


def limpiar(clave):
    con = obtener_conexion()
    con.execute("DELETE FROM intentos_login WHERE clave = ?", (clave,))
    con.commit()
    con.close()