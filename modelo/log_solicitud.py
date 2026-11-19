# =========================================================
# modelo/log_solicitud.py — PQR y mensajes de contacto
# =========================================================
from datetime import date
from modelo.conexion import obtener_conexion

TIPOS_PQR = ("Petición", "Queja", "Reclamo", "Sugerencia")
ESTADOS = ("Nuevo", "En trámite", "Respondido", "Cerrado")
PREFIJOS = {"pqr": "PQR", "contacto": "MSJ"}


def crear(origen, nombre, correo, asunto, descripcion, tipo="", telefono="", tipo_usuario="", sede=""):
    """Guarda una solicitud y devuelve su radicado (ej. PQR-2026-000012)."""
    con = obtener_conexion()
    cur = con.execute(
        "INSERT INTO solicitudes (origen, tipo, nombre, correo, telefono, tipo_usuario, sede, asunto, descripcion) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (origen, tipo, nombre, correo, telefono, tipo_usuario, sede, asunto, descripcion),
    )
    radicado = f"{PREFIJOS[origen]}-{date.today().year}-{cur.lastrowid:06d}"
    con.execute("UPDATE solicitudes SET radicado = ? WHERE id = ?", (radicado, cur.lastrowid))
    con.commit()
    con.close()
    return radicado


def listar(origen=None, estado=None):
    consulta = "SELECT * FROM solicitudes WHERE 1 = 1"
    parametros = []
    if origen:
        consulta += " AND origen = ?"
        parametros.append(origen)
    if estado:
        consulta += " AND estado = ?"
        parametros.append(estado)
    consulta += " ORDER BY creado DESC, id DESC"
    con = obtener_conexion()
    filas = con.execute(consulta, parametros).fetchall()
    con.close()
    return filas


def obtener(id_solicitud):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM solicitudes WHERE id = ?", (id_solicitud,)).fetchone()
    con.close()
    return fila


def contar_nuevas():
    con = obtener_conexion()
    n = con.execute("SELECT COUNT(*) FROM solicitudes WHERE estado = 'Nuevo'").fetchone()[0]
    con.close()
    return n


def buscar_por_radicado(radicado, correo):
    """Para la consulta pública: solo devuelve algo si coinciden radicado Y correo."""
    con = obtener_conexion()
    fila = con.execute(
        "SELECT radicado, tipo, estado FROM solicitudes WHERE radicado = ? AND lower(correo) = lower(?)",
        (radicado, correo),
    ).fetchone()
    con.close()
    return fila


def actualizar(id_solicitud, estado, nota):
    """Devuelve (ok, mensaje)."""
    if estado not in ESTADOS:
        return False, "Estado no válido."
    if not obtener(id_solicitud):
        return False, "Solicitud no encontrada."
    con = obtener_conexion()
    con.execute(
        "UPDATE solicitudes SET estado = ?, nota = ?, actualizado = datetime('now', '-5 hours') WHERE id = ?",
        (estado, nota, id_solicitud),
    )
    con.commit()
    con.close()
    return True, "Solicitud actualizada."


def eliminar(id_solicitud):
    con = obtener_conexion()
    con.execute("DELETE FROM solicitudes WHERE id = ?", (id_solicitud,))
    con.commit()
    con.close()