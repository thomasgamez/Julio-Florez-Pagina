from app import app
from modelo import log_intentos

cliente = app.test_client()

# 1) Un POST sin código de seguridad debe ser rechazado
r = cliente.post("/admin/login", data={"usuario": "admin", "password": "x"})
print("Sin token:", r.status_code)  # 400

# 2) Con token válido, 6 intentos con clave mala: el sexto debe quedar bloqueado
with cliente.session_transaction() as s:
    s["csrf_token"] = "abc"
for i in range(1, 7):
    r = cliente.post("/admin/login", data={"usuario": "admin", "password": "mala", "csrf_token": "abc"})
    print(i, r.status_code, "BLOQUEADO" if "Demasiados" in r.get_data(as_text=True) else "")

# 3) Limpiar para no dejarte bloqueado
log_intentos.limpiar("127.0.0.1|admin")