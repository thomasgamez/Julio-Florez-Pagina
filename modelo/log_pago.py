# =========================================================
# modelo/log_pago.py — CRUD de Pagaduría (conceptos y pagos)
# =========================================================
from modelo.conexion import obtener_conexion


# ---------- Conceptos autorizados ----------

def listar_conceptos_activos():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM conceptos_pago WHERE activo = 1 ORDER BY nombre ASC").fetchall()
    con.close()
    return filas


def listar_conceptos():
    con = obtener_conexion()
    filas = con.execute("SELECT * FROM conceptos_pago ORDER BY nombre ASC").fetchall()
    con.close()
    return filas


def obtener_concepto(id_concepto):
    con = obtener_conexion()
    fila = con.execute("SELECT * FROM conceptos_pago WHERE id = ?", (id_concepto,)).fetchone()
    con.close()
    return fila


def crear_concepto(datos):
    con = obtener_conexion()
    con.execute(
        "INSERT INTO conceptos_pago (nombre, valor, obligatorio, descripcion, activo) VALUES (?,?,?,?,?)",
        (datos["nombre"], datos["valor"], datos.get("obligatorio", 0),
         datos["descripcion"], datos.get("activo", 1)),
    )
    con.commit()
    con.close()


def actualizar_concepto(id_concepto, datos):
    con = obtener_conexion()
    con.execute(
        "UPDATE conceptos_pago SET nombre=?, valor=?, obligatorio=?, descripcion=?, activo=? WHERE id=?",
        (datos["nombre"], datos["valor"], datos.get("obligatorio", 0),
         datos["descripcion"], datos.get("activo", 1), id_concepto),
    )
    con.commit()
    con.close()


def eliminar_concepto(id_concepto):
    con = obtener_conexion()
    con.execute("DELETE FROM conceptos_pago WHERE id = ?", (id_concepto,))
    con.commit()
    con.close()


# ---------- Pagos registrados ----------

def listar_pagos():
    con = obtener_conexion()
    filas = con.execute(
        """SELECT pagos_registrados.*, conceptos_pago.nombre AS concepto_nombre
           FROM pagos_registrados LEFT JOIN conceptos_pago ON pagos_registrados.concepto_id = conceptos_pago.id
           ORDER BY pagos_registrados.id DESC"""
    ).fetchall()
    con.close()
    return filas


def registrar_pago(datos):
    con = obtener_conexion()
    con.execute(
        """INSERT INTO pagos_registrados (estudiante, grado, concepto_id, valor_pagado, medio_pago, fecha_pago, estado)
           VALUES (?,?,?,?,?,?,?)""",
        (datos["estudiante"], datos["grado"], datos["concepto_id"], datos["valor_pagado"],
         datos["medio_pago"], datos["fecha_pago"], datos.get("estado", "Pagado")),
    )
    con.commit()
    con.close()
