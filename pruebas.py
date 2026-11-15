from modelo import log_usuario

print(log_usuario.crear("prueba1", "corta", "Usuario Prueba", "secretaria"))         # contraseña corta
print(log_usuario.crear("prueba1", "clave12345", "Usuario Prueba", "inventado"))     # rol inexistente
print(log_usuario.crear("prueba1", "clave12345", "Usuario Prueba", "secretaria"))    # OK
print(log_usuario.crear("prueba1", "clave12345", "Otro", "secretaria"))              # duplicado

u = log_usuario.obtener_por_usuario("prueba1")
print(log_usuario.cambiar_password(u["id"], "nuevaclave99"))
print(log_usuario.eliminar(1, 1))                  # se intenta borrar a sí mismo (admin id 1)
print(log_usuario.eliminar(u["id"], 1))            # borra el de prueba