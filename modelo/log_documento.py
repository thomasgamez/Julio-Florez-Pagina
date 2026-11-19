# =========================================================
# modelo/log_documento.py — Documentos de Pagaduría
# =========================================================
from modelo.conexion import obtener_conexion


def listar():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM documentos ORDER BY creado DESC, id DESC").fetchall()
    con.close()
    return filas


def obtener(id_documento):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM documentos WHERE id = ?", (id_documento,)).fetchone()
    con.close()
    return fila


def crear(titulo, descripcion, categoria, archivo, nombre_original, extension, tamano):
    con = obtener_conexion()
    con.execute(
        "INSERT INTO documentos (titulo, descripcion, categoria, archivo, nombre_original, extension, tamano) "
        "VALUES (?,?,?,?,?,?,?)",
        (titulo, descripcion, categoria, archivo, nombre_original, extension, tamano),
    )
    con.commit()
    con.close()


def actualizar(id_documento, titulo, descripcion, categoria):
    con = obtener_conexion()
    con.execute(
        "UPDATE documentos SET titulo = ?, descripcion = ?, categoria = ? WHERE id = ?",
        (titulo, descripcion, categoria, id_documento),
    )
    con.commit()
    con.close()


def eliminar(id_documento):
    """Borra el registro y devuelve el nombre del archivo guardado (para borrarlo del disco), o None."""
    doc = obtener(id_documento)
    if not doc:
        return None
    con = obtener_conexion()
    con.execute("DELETE FROM documentos WHERE id = ?", (id_documento,))
    con.commit()
    con.close()
    return doc["archivo"]