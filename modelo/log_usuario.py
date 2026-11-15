# =========================================================
# modelo/log_usuario.py — Usuarios del panel administrativo
# =========================================================
import sqlite3
from modelo.conexion import obtener_conexion
from modelo import log_rol
from werkzeug.security import check_password_hash, generate_password_hash

LONGITUD_MINIMA_PASSWORD = 8
ROL_ADMIN = "admin"

def obtener_por_usuario(usuario):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM usuarios_admin WHERE usuario = ?", (usuario,)).fetchone()
    con.close()
    return fila


def obtener_por_id(id_usuario):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM usuarios_admin WHERE id = ?", (id_usuario,)).fetchone()
    con.close()
    return fila


def verificar_credenciales(usuario, password):
    fila = obtener_por_usuario(usuario)
    if fila and check_password_hash(fila["password_hash"], password):
        return fila
    return None


def crear_usuario(usuario, password, nombre, rol="editor"):
    con = obtener_conexion()
    con.execute(
        "INSERT INTO usuarios_admin (usuario, password_hash, nombre, rol) VALUES (?,?,?,?)",
        (usuario, generate_password_hash(password), nombre, rol),
    )
    con.commit()
    con.close()

def listar():
    """Todos los usuarios, con el nombre bonito de su rol."""
    con = obtener_conexion()
    filas = con.execute(
        "SELECT u.id, u.usuario, u.nombre, u.rol, COALESCE(r.etiqueta, u.rol) AS rol_etiqueta "
        "FROM usuarios_admin u LEFT JOIN roles r ON r.nombre = u.rol "
        "ORDER BY u.nombre"
    ).fetchall()
    con.close()
    return filas


def contar_admins():
    con = obtener_conexion()
    n = con.execute("SELECT COUNT(*) FROM usuarios_admin WHERE rol = ?", (ROL_ADMIN,)).fetchone()[0]
    con.close()
    return n


def _rol_existe(nombre_rol):
    return any(r["nombre"] == nombre_rol for r in log_rol.listar())

def crear(usuario, password, nombre, rol):
    usuario = usuario.strip().lower()
    nombre = nombre.strip()
    if not usuario or not nombre:
        return False, "El usuario y el nombre son obligatorios."
    if len(password) < LONGITUD_MINIMA_PASSWORD:
        return False, f"La contraseña debe tener al menos {LONGITUD_MINIMA_PASSWORD} caracteres."
    if not _rol_existe(rol):
        return False, "El rol seleccionado no existe."

    con = obtener_conexion()
    try:
        con.execute(
            "INSERT INTO usuarios_admin (usuario, password_hash, nombre, rol) VALUES (?,?,?,?)",
            (usuario, generate_password_hash(password), nombre, rol),
        )
        con.commit()
        return True, "Usuario creado correctamente."
    except sqlite3.IntegrityError:
        return False, "Ya existe un usuario con ese nombre de usuario."
    finally:
        con.close()

def actualizar(id_usuario, nombre, rol):
    u = obtener_por_id(id_usuario)
    if not u:
        return False, "Usuario no encontrado."
    if not nombre.strip():
        return False, "El nombre es obligatorio."
    if not _rol_existe(rol):
        return False, "El rol seleccionado no existe."
    if u["rol"] == ROL_ADMIN and rol != ROL_ADMIN and contar_admins() <= 1:
        return False, "Debe quedar al menos un administrador. Asigna el rol admin a otra persona primero."

    con = obtener_conexion()
    con.execute("UPDATE usuarios_admin SET nombre = ?, rol = ? WHERE id = ?", (nombre.strip(), rol, id_usuario))
    con.commit()
    con.close()
    return True, "Usuario actualizado."


def cambiar_password(id_usuario, nueva):
    if not obtener_por_id(id_usuario):
        return False, "Usuario no encontrado."
    if len(nueva) < LONGITUD_MINIMA_PASSWORD:
        return False, f"La contraseña debe tener al menos {LONGITUD_MINIMA_PASSWORD} caracteres."
    con = obtener_conexion()
    con.execute("UPDATE usuarios_admin SET password_hash = ? WHERE id = ?", (generate_password_hash(nueva), id_usuario))
    con.commit()
    con.close()
    return True, "Contraseña actualizada."

def eliminar(id_usuario, id_actual):
    """id_actual es el usuario que está con sesión iniciada (para que no se borre a sí mismo)."""
    u = obtener_por_id(id_usuario)
    if not u:
        return False, "Usuario no encontrado."
    if id_usuario == id_actual:
        return False, "No puedes eliminar tu propio usuario."
    if u["rol"] == ROL_ADMIN and contar_admins() <= 1:
        return False, "No se puede eliminar al único administrador."

    con = obtener_conexion()
    con.execute("DELETE FROM usuarios_admin WHERE id = ?", (id_usuario,))
    con.commit()
    con.close()
    return True, "Usuario eliminado."