# =========================================================
# modelo/log_usuario.py — Usuarios del panel administrativo
# =========================================================
from modelo.conexion import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash


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
