# =========================================================
# modelo/log_contenido.py — Cambios de texto hechos desde el panel
# =========================================================
from modelo.conexion import obtener_conexion
from contenido_base import CONTENIDO_BASE

LIMITE_CARACTERES = 5000


def todos():
    """Devuelve {clave: valor} con todo lo que se ha editado."""
    con = obtener_conexion()
    filas = con.execute("SELECT clave, valor FROM contenido").fetchall()
    con.close()
    return {f["clave"]: f["valor"] for f in filas}


def restaurar(clave):
    con = obtener_conexion()
    con.execute("DELETE FROM contenido WHERE clave = ?", (clave,))
    con.commit()
    con.close()


def guardar(clave, valor):
    """Guarda un cambio. Si queda vacío o igual a la base, se descarta. Devuelve (ok, mensaje)."""
    item = CONTENIDO_BASE.get(clave)
    if not item:
        return False, "Ese texto no existe."

    valor = valor.replace("\r\n", "\n").strip()
    if len(valor) > LIMITE_CARACTERES:
        return False, f"El texto es demasiado largo (máximo {LIMITE_CARACTERES} caracteres)."

    if not valor or valor == item["base"].strip():
        restaurar(clave)
        return True, "Sin cambios: se mantiene el texto base."

    if item["tipo"] == "url" and not valor.lower().startswith(("http://", "https://")):
        return False, "El enlace debe empezar por http:// o https://"

    con = obtener_conexion()
    con.execute(
        "INSERT INTO contenido (clave, valor, actualizado) VALUES (?,?,CURRENT_TIMESTAMP) "
        "ON CONFLICT(clave) DO UPDATE SET valor = excluded.valor, actualizado = CURRENT_TIMESTAMP",
        (clave, valor),
    )
    con.commit()
    con.close()
    return True, "Texto guardado."