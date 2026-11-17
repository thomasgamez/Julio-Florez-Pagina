from app import app, contenido
from modelo import log_contenido

CLAVE = "contacto.subtitulo"

with app.test_request_context():
    print("1) Base:      ", contenido(CLAVE))

print(log_contenido.guardar(CLAVE, "Texto editado desde la prueba"))
with app.test_request_context():
    print("2) Editado:   ", contenido(CLAVE))

print(log_contenido.guardar(CLAVE, "Estamos para atenderte"))   # igual a la base
with app.test_request_context():
    print("3) Restaurado:", contenido(CLAVE))

print(log_contenido.guardar("inventada.clave", "hola"))