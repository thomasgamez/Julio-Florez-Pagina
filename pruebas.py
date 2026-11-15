from modelo import log_rol

secretaria = next(r for r in log_rol.listar() if r["nombre"] == "secretaria")
log_rol.actualizar(secretaria["id"], secretaria["etiqueta"], ["noticias", "eventos"])  # le quitamos logros y galería
print(log_rol.permisos_de("secretaria"))