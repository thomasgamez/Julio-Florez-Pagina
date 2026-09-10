# =========================================================
# modelo/log_logro.py — CRUD de Logros y Reconocimientos
# =========================================================
from modelo.conexion import obtener_conexion


def listar_publicados():
    con = obtener_conexion()
    filas = con.execute(
        "SELECT * FROM logros WHERE publicado = 1 ORDER BY id DESC"
    ).fetchall()
    con.close()
    return filas


def listar_todos():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM logros ORDER BY id DESC").fetchall()
    con.close()
    return filas


def obtener(id_logro):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM logros WHERE id = ?", (id_logro,)).fetchone()
    con.close()
    return fila


def crear(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO logros (nombre, categoria, titulo_logro, descripcion, grado, imagen, fecha, publicado)
           VALUES (?,?,?,?,?,?,?,?)""",
        (datos["nombre"], datos["categoria"], datos["titulo_logro"], datos["descripcion"],
         datos["grado"], datos["imagen"], datos["fecha"], datos.get("publicado", 1)),
    )
    con.commit()
    con.close()


def actualizar(id_logro, datos):
    con = obtener_conexion()
    con.execute(
        """UPDATE logros SET nombre=?, categoria=?, titulo_logro=?, descripcion=?,
           grado=?, imagen=?, fecha=?, publicado=? WHERE id=?""",
        (datos["nombre"], datos["categoria"], datos["titulo_logro"], datos["descripcion"],
         datos["grado"], datos["imagen"], datos["fecha"], datos.get("publicado", 1), id_logro),
    )
    con.commit()
    con.close()


def eliminar(id_logro):
    con = obtener_conexion()
    con.execute("DELETE FROM logros WHERE id = ?", (id_logro,))
    con.commit()
    con.close()