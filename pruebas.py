from modelo import log_rol, log_usuario

secretaria = next(r for r in log_rol.listar() if r["nombre"] == "secretaria")
log_rol.actualizar(secretaria["id"], secretaria["etiqueta"], ["noticias", "usuarios"])
print(log_rol.permisos_de("secretaria"))  # debe salir solo {'noticias'}, sin 'usuarios'

print(log_usuario.crear("intruso", "clave12345", "Intruso", "admin", "secretaria"))  # (False, 'Solo el administrador...')

# devolver los permisos originales
log_rol.actualizar(secretaria["id"], secretaria["etiqueta"], ["noticias", "eventos", "logros", "galeria"])