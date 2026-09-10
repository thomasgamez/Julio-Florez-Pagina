from modelo.log_usuario import crear_usuario, obtener_por_usuario

nuevos = [
    ("rector", "rector2026", "Rector", "rector"),
    ("secretaria", "secretaria2026", "Secretaría Académica", "secretaria"),
    ("pagaduria", "pagaduria2026", "Pagaduría", "pagaduria"),
]

for usuario, clave, nombre, rol in nuevos:
    if not obtener_por_usuario(usuario):
        crear_usuario(usuario, clave, nombre, rol)
        print(f"{usuario} creado")
    else:
        print(f"{usuario} ya existía")