# =========================================================
# modelo/log_noticia.py — CRUD de Noticias
# =========================================================
from modelo.conexion import obtener_conexion


def listar_publicadas():
    con = obtener_conexion()
    filas = con.execute(
        "SELECT * FROM noticias WHERE publicado = 1 ORDER BY id DESC"
    ).fetchall()
    con.close()
    return filas


def listar_todas():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM noticias ORDER BY id DESC").fetchall()
    con.close()
    return filas


def obtener(id_noticia):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM noticias WHERE id = ?", (id_noticia,)).fetchone()
    con.close()
    return fila


def crear(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO noticias (titulo, categoria, resumen, contenido, autor, imagen, fecha, publicado)
           VALUES (?,?,?,?,?,?,?,?)""",
        (datos["titulo"], datos["categoria"], datos["resumen"], datos["contenido"],
         datos["autor"], datos["imagen"], datos["fecha"], datos.get("publicado", 1)),
    )
    con.commit()
    con.close()


def actualizar(id_noticia, datos):
    con = obtener_conexion()
    con.execute(
        """UPDATE noticias SET titulo=?, categoria=?, resumen=?, contenido=?, autor=?,
           imagen=?, fecha=?, publicado=? WHERE id=?""",
        (datos["titulo"], datos["categoria"], datos["resumen"], datos["contenido"],
         datos["autor"], datos["imagen"], datos["fecha"], datos.get("publicado", 1), id_noticia),
    )
    con.commit()
    con.close()


def eliminar(id_noticia):
    con = obtener_conexion()
    con.execute("DELETE FROM noticias WHERE id = ?", (id_noticia,))
    con.commit()
    con.close()
