# Herramienta de mantenimiento: devuelve a admin y rector todas las secciones del panel.
from modelo.conexion import obtener_conexion, SECCIONES


def resumen(con):
    filas = con.execute(
        "SELECT r.nombre, group_concat(p.seccion) FROM roles r "
        "LEFT JOIN permisos_rol p ON p.rol_id = r.id GROUP BY r.id"
    ).fetchall()
    for nombre, secciones in filas:
        print(f"  {nombre}: {secciones or '(sin secciones)'}")


con = obtener_conexion()
print("ANTES:")
resumen(con)

for nombre in ("admin", "rector"):
    fila = con.execute("SELECT id FROM roles WHERE nombre = ?", (nombre,)).fetchone()
    if fila:
        for seccion in SECCIONES:
            con.execute("INSERT OR IGNORE INTO permisos_rol (rol_id, seccion) VALUES (?,?)", (fila[0], seccion))
con.commit()

print("DESPUÉS:")
resumen(con)
con.close()