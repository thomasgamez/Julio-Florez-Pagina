# =========================================================
# modelo/log_evento.py — CRUD de Eventos
# =========================================================
from modelo.conexion import obtener_conexion


def listar_publicados():
    con = obtener_conexion()
    filas = con.execute(
        "SELECT * FROM eventos WHERE publicado = 1 ORDER BY id DESC"
    ).fetchall()
    con.close()
    return filas


def listar_todos():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM eventos ORDER BY id DESC").fetchall()
    con.close()
    return filas


def obtener(id_evento):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM eventos WHERE id = ?", (id_evento,)).fetchone()
    con.close()
    return fila


def crear(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO eventos (titulo, categoria, estado, descripcion, fecha_completa, mes, dia, sede, publicado)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (datos["titulo"], datos["categoria"], datos["estado"], datos["descripcion"],
         datos["fecha_completa"], datos["mes"], datos["dia"], datos["sede"], datos.get("publicado", 1)),
    )
    con.commit()
    con.close()


def actualizar(id_evento, datos):
    con = obtener_conexion()
    con.execute(
        """UPDATE eventos SET titulo=?, categoria=?, estado=?, descripcion=?, fecha_completa=?,
           mes=?, dia=?, sede=?, publicado=? WHERE id=?""",
        (datos["titulo"], datos["categoria"], datos["estado"], datos["descripcion"],
         datos["fecha_completa"], datos["mes"], datos["dia"], datos["sede"],
         datos.get("publicado", 1), id_evento),
    )
    con.commit()
    con.close()


def eliminar(id_evento):
    con = obtener_conexion()
    con.execute("DELETE FROM eventos WHERE id = ?", (id_evento,))
    con.commit()
    con.close()
