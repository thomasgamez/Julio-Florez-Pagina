# =========================================================
# modelo/log_galeria.py — CRUD de la Galería de fotos
# =========================================================
from modelo.conexion import obtener_conexion


def listar_publicadas():
    con = obtener_conexion()
    filas = con.execute(
        "SELECT * FROM galeria WHERE publicado = 1 ORDER BY id DESC"
    ).fetchall()
    con.close()
    return filas


def listar_todas():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM galeria ORDER BY id DESC").fetchall()
    con.close()
    return filas


def obtener(id_foto):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM galeria WHERE id = ?", (id_foto,)).fetchone()
    con.close()
    return fila


def crear(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO galeria (titulo, categoria, imagen, publicado)
           VALUES (?,?,?,?)""",
        (datos.get("titulo", ""), datos["categoria"], datos["imagen"], datos.get("publicado", 1)),
    )
    con.commit()
    con.close()


def actualizar(id_foto, datos):
    con = obtener_conexion()
    con.execute(
        """UPDATE galeria SET titulo=?, categoria=?, imagen=?, publicado=? WHERE id=?""",
        (datos.get("titulo", ""), datos["categoria"], datos["imagen"], datos.get("publicado", 1), id_foto),
    )
    con.commit()
    con.close()


def eliminar(id_foto):
    con = obtener_conexion()
    con.execute("DELETE FROM galeria WHERE id = ?", (id_foto,))
    con.commit()
    con.close()