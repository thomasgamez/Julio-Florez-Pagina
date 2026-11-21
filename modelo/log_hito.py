# =========================================================
# modelo/log_hito.py — Hitos de la línea de tiempo
# =========================================================
import re
from modelo.conexion import obtener_conexion


def preparar(hitos_base):
    """Crea la tabla. Solo la primera vez (cuando no existía) la llena con los hitos que están en el código."""
    con = obtener_conexion()
    existia = con.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'hitos'").fetchone()
    con.execute(
        "CREATE TABLE IF NOT EXISTS hitos ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, anio TEXT NOT NULL, titulo TEXT NOT NULL, descripcion TEXT NOT NULL)"
    )
    if not existia:
        con.executemany(
            "INSERT INTO hitos (anio, titulo, descripcion) VALUES (?,?,?)",
            [(h["anio"], h["titulo"], h["descripcion"]) for h in hitos_base],
        )
    con.commit()
    con.close()


def listar():
    con = obtener_conexion()
    filas = con.execute("SELECT id, anio, titulo, descripcion FROM hitos ORDER BY anio, id").fetchall()
    con.close()
    return [dict(f) for f in filas]


def _validar(anio, titulo, descripcion):
    """Devuelve ((anio, titulo, descripcion), '') o (None, mensaje de error)."""
    anio = (anio or "").strip()
    titulo = (titulo or "").strip()[:150]
    descripcion = (descripcion or "").strip()[:600]
    if not re.fullmatch(r"\d{4}", anio):
        return None, "El año debe tener 4 cifras (por ejemplo 2015)."
    if not titulo or not descripcion:
        return None, "El título y la descripción son obligatorios."
    return (anio, titulo, descripcion), ""


def crear(anio, titulo, descripcion):
    datos, error = _validar(anio, titulo, descripcion)
    if not datos:
        return False, error
    con = obtener_conexion()
    con.execute("INSERT INTO hitos (anio, titulo, descripcion) VALUES (?,?,?)", datos)
    con.commit()
    con.close()
    return True, "Hito agregado."


def actualizar(id_hito, anio, titulo, descripcion):
    datos, error = _validar(anio, titulo, descripcion)
    if not datos:
        return False, error
    con = obtener_conexion()
    cur = con.execute("UPDATE hitos SET anio = ?, titulo = ?, descripcion = ? WHERE id = ?", datos + (id_hito,))
    con.commit()
    con.close()
    return (True, "Hito actualizado.") if cur.rowcount else (False, "Hito no encontrado.")


def eliminar(id_hito):
    con = obtener_conexion()
    con.execute("DELETE FROM hitos WHERE id = ?", (id_hito,))
    con.commit()
    con.close()


def restaurar_base(hitos_base):
    """Borra todo y vuelve a cargar los hitos originales del código."""
    con = obtener_conexion()
    con.execute("DELETE FROM hitos")
    con.executemany(
        "INSERT INTO hitos (anio, titulo, descripcion) VALUES (?,?,?)",
        [(h["anio"], h["titulo"], h["descripcion"]) for h in hitos_base],
    )
    con.commit()
    con.close()