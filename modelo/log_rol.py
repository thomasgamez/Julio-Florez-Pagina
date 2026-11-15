# =========================================================
# modelo/log_rol.py — Roles y permisos del panel
# =========================================================
import sqlite3
from modelo.conexion import obtener_conexion, SECCIONES

# El rol "admin" no se puede borrar y siempre conserva estos permisos,
# para que nadie pueda dejar el panel sin un administrador.
ROL_PROTEGIDO = "admin"
PERMISOS_OBLIGATORIOS_ADMIN = ("usuarios", "roles")

def listar():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM roles ORDER BY etiqueta").fetchall()
    con.close()
    return filas


def obtener(id_rol):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM roles WHERE id = ?", (id_rol,)).fetchone()
    con.close()
    return fila


def permisos_de(nombre_rol):
    """Devuelve un conjunto con las secciones que puede ver ese rol, ej. {'noticias','eventos'}."""
    con = obtener_conexion()
    filas = con.execute(
        "SELECT p.seccion FROM permisos_rol p JOIN roles r ON r.id = p.rol_id WHERE r.nombre = ?",
        (nombre_rol,),
    ).fetchall()
    con.close()
    return {f["seccion"] for f in filas}


def permisos_de_todos():
    """Devuelve {id_rol: [secciones]} para mostrar todos los roles en una sola tabla."""
    con = obtener_conexion()
    filas = con.execute("SELECT rol_id, seccion FROM permisos_rol").fetchall()
    con.close()
    resultado = {}
    for f in filas:
        resultado.setdefault(f["rol_id"], []).append(f["seccion"])
    return resultado


def contar_usuarios(nombre_rol):
    con = obtener_conexion()
    n = con.execute("SELECT COUNT(*) FROM usuarios_admin WHERE rol = ?", (nombre_rol,)).fetchone()[0]
    con.close()
    return n

def _validas(secciones):
    """Se queda solo con secciones que existen en SECCIONES (evita datos inventados)."""
    return [s for s in secciones if s in SECCIONES]


def crear(nombre, etiqueta, secciones):
    """Crea un rol con sus permisos. Devuelve el id nuevo, o None si el nombre ya existe."""
    nombre = nombre.strip().lower().replace(" ", "_")
    con = obtener_conexion()
    try:
        cur = con.execute("INSERT INTO roles (nombre, etiqueta) VALUES (?,?)", (nombre, etiqueta.strip()))
        con.executemany(
            "INSERT INTO permisos_rol (rol_id, seccion) VALUES (?,?)",
            [(cur.lastrowid, s) for s in _validas(secciones)],
        )
        con.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None  # ya existe un rol con ese nombre (columna UNIQUE)
    finally:
        con.close()

def actualizar(id_rol, etiqueta, secciones):
    rol = obtener(id_rol)
    if not rol:
        return False
    secciones = set(_validas(secciones))
    if rol["nombre"] == ROL_PROTEGIDO:
        secciones |= set(PERMISOS_OBLIGATORIOS_ADMIN)  # el admin nunca pierde estos permisos
    con = obtener_conexion()
    con.execute("UPDATE roles SET etiqueta = ? WHERE id = ?", (etiqueta.strip(), id_rol))
    con.execute("DELETE FROM permisos_rol WHERE rol_id = ?", (id_rol,))
    con.executemany(
        "INSERT INTO permisos_rol (rol_id, seccion) VALUES (?,?)",
        [(id_rol, s) for s in secciones],
    )
    con.commit()
    con.close()
    return True


def eliminar(id_rol):
    """Devuelve (ok, mensaje). No deja borrar el admin ni roles que aún tengan usuarios."""
    rol = obtener(id_rol)
    if not rol:
        return False, "Rol no encontrado."
    if rol["nombre"] == ROL_PROTEGIDO:
        return False, "El rol admin no se puede eliminar."
    n = contar_usuarios(rol["nombre"])
    if n:
        return False, f"No se puede eliminar: hay {n} usuario(s) con este rol. Cámbialos de rol primero."
    con = obtener_conexion()
    con.execute("DELETE FROM roles WHERE id = ?", (id_rol,))
    con.commit()
    con.close()
    return True, "Rol eliminado."        

def obtener_por_nombre(nombre):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM roles WHERE nombre = ?", (nombre,)).fetchone()
    con.close()
    return fila