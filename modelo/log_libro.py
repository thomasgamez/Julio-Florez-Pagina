# =========================================================
# modelo/log_libro.py — CRUD de Biblioteca (libros y préstamos)
# =========================================================
from modelo.conexion import obtener_conexion


def listar():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM libros ORDER BY titulo ASC").fetchall()
    con.close()
    return filas


def obtener(id_libro):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM libros WHERE id = ?", (id_libro,)).fetchone()
    con.close()
    return fila


def crear(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO libros (titulo, autor, categoria, grado, cantidad_total, cantidad_disponible)
           VALUES (?,?,?,?,?,?)""",
        (datos["titulo"], datos["autor"], datos["categoria"], datos["grado"],
         datos["cantidad_total"], datos["cantidad_total"]),
    )
    con.commit()
    con.close()


def actualizar(id_libro, datos):
    con = obtener_conexion()
    con.execute(
        """UPDATE libros SET titulo=?, autor=?, categoria=?, grado=?,
           cantidad_total=?, cantidad_disponible=? WHERE id=?""",
        (datos["titulo"], datos["autor"], datos["categoria"], datos["grado"],
         datos["cantidad_total"], datos["cantidad_disponible"], id_libro),
    )
    con.commit()
    con.close()


def eliminar(id_libro):
    con = obtener_conexion()
    con.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    con.commit()
    con.close()


# ---------- Préstamos ----------

def listar_prestamos_activos():
    con = obtener_conexion()
    filas = con.execute(
        """SELECT prestamos.*, libros.titulo AS libro_titulo
           FROM prestamos JOIN libros ON prestamos.libro_id = libros.id
           WHERE prestamos.devuelto = 0 ORDER BY prestamos.fecha_limite ASC"""
    ).fetchall()
    con.close()
    return filas


def registrar_prestamo(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO prestamos (libro_id, estudiante, grado, fecha_prestamo, fecha_limite, devuelto)
           VALUES (?,?,?,?,?,0)""",
        (datos["libro_id"], datos["estudiante"], datos["grado"],
         datos["fecha_prestamo"], datos["fecha_limite"]),
    )
    con.execute(
        "UPDATE libros SET cantidad_disponible = cantidad_disponible - 1 WHERE id = ? AND cantidad_disponible > 0",
        (datos["libro_id"],),
    )
    con.commit()
    con.close()


def marcar_devuelto(id_prestamo):
    con = obtener_conexion()
    prestamo = con.execute("SELECT * FROM prestamos WHERE id = ?", (id_prestamo,)).fetchone()
    if prestamo and not prestamo["devuelto"]:
        con.execute("UPDATE prestamos SET devuelto = 1 WHERE id = ?", (id_prestamo,))
        con.execute(
            "UPDATE libros SET cantidad_disponible = cantidad_disponible + 1 WHERE id = ?",
            (prestamo["libro_id"],),
        )
        con.commit()
    con.close()
