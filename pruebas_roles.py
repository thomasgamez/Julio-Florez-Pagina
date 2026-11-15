from modelo import log_rol

print("Permisos de secretaria:", log_rol.permisos_de("secretaria"))

nuevo = log_rol.crear("Coordinador Académico", "Coordinación", ["noticias", "eventos"])
print("Rol creado con id:", nuevo)

print("Intentar borrar admin:", log_rol.eliminar(1))

if nuevo:
    print("Borrar el rol de prueba:", log_rol.eliminar(nuevo))