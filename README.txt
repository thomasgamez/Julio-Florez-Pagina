INSTITUTO TÉCNICO DISTRITAL JULIO FLÓREZ — Sitio web (Flask)
=============================================================

ESTRUCTURA (igual a tu proyecto en VS Code)
--------------------------------------------
citd_julio_florez/
├── app.py                     -> Rutas Flask + datos de ejemplo
├── requirements.txt
├── modelo/                    -> (vacío) aquí van tus modelos cuando conectes BD
├── static/
│   ├── Styles/main.css        -> Todo el CSS institucional (colores, tipografías)
│   ├── js/main.js             -> JS del sitio (navbar, etc.)
│   ├── images/                -> AQUÍ debes subir tus fotos reales
│   │                              (ver lista de nombres esperados abajo)
│   ├── bootstrap/              -> (vacío, se usa Bootstrap por CDN;
│   │                              si prefieres offline, descarga aquí
│   │                              bootstrap.min.css y bootstrap.bundle.min.js
│   │                              y cambia las etiquetas <link>/<script> en layout.html)
│   └── doc/                    -> aquí puedes poner PDF institucionales (PEI, manual, etc.)
└── templates/
    ├── layout.html             -> Plantilla base: navbar + footer (todas las páginas heredan de aquí)
    ├── inicio_sesion/          -> (vacío, listo para cuando agregues login)
    └── pagina/
        ├── index.html                     -> Inicio
        ├── nuestra_institucion.html       -> Nuestra Institución (misión, visión, reseña, símbolos, ubicación)
        ├── especialidades.html            -> Especialidades técnicas
        ├── bachillerato_internacional.html-> Bachillerato IB
        ├── campos_formacion.html          -> Campos de Formación
        ├── noticias.html
        ├── eventos.html
        ├── galeria.html
        ├── vida_escolar.html              -> Plantilla ÚNICA reutilizable para las 6 subsecciones
        │                                     (rutas, alimentación, horarios, coordinación, padres, información)
        ├── pagaduria.html
        ├── archivo.html
        ├── biblioteca.html
        ├── matriculas.html
        ├── pqr.html
        └── contacto.html

CÓMO EJECUTARLO
----------------
1. Crea un entorno virtual (opcional pero recomendado):
   python -m venv venv
   venv\Scripts\activate      (Windows)
   source venv/bin/activate   (Mac/Linux)

2. Instala dependencias:
   pip install -r requirements.txt

3. Corre el servidor:
   python app.py

4. Abre en el navegador:
   http://127.0.0.1:5000

IMÁGENES QUE DEBES SUBIR A static/images/
-------------------------------------------
escudo.png, hero-portada.jpg, institucion-1.jpg, institucion-2.jpg, institucion-3.jpg,
ib-1.jpg, ib-2.jpg, ib-3.jpg, ib-diplomas-1.jpg, ib-diplomas-2.jpg, ib-grupo.jpg,
esp-administracion.jpg, esp-programacion.jpg, esp-ambiental.jpg, esp-multimedia.jpg,
especialidades-hero.jpg,
campo-inicial.jpg, campo-sociales.jpg, campo-matematico.jpg, campo-comunicacion.jpg,
campo-cientifico.jpg, campo-proyecto-vida.jpg,
noticia-pop.jpg, noticia-donaton.jpg, noticia-acreditacion.jpg,
galeria-1.jpg ... galeria-16.jpg,
biblioteca-1.jpg, biblioteca-2.jpg, biblioteca-3.jpg,
vida-transporte.jpg, vida-alimentacion.jpg, vida-horarios.jpg,
vida-coordinacion.jpg, vida-padres.jpg, vida-informacion.jpg

(Si un nombre de imagen no existe, la página no se rompe: solo se ve el espacio vacío.
 El escudo específicamente se oculta automáticamente si falta el archivo.)

CÓMO CONECTAR DATOS REALES (BASE DE DATOS)
--------------------------------------------
Ahora mismo TODO el contenido (noticias, eventos, especialidades, FAQ, etc.)
vive como diccionarios de Python dentro de app.py, arriba de las rutas.
Cuando tengas tus modelos en /modelo (como en tu proyecto de Pagaduría),
solo reemplaza esas listas por consultas a tu base de datos, por ejemplo:

    from modelo.log_noticia import Noticia
    @app.route("/noticias")
    def noticias():
        lista = Noticia.query.all()
        return render_template("pagina/noticias.html", noticias=lista)

Los templates (.html) no necesitan cambiar: ya están escritos para recorrer
listas de diccionarios/objetos con esos mismos nombres de campos.

SIGUIENTE PASOS SUGERIDOS
----------------------------
- Formulario de PQR y Contacto: hoy solo muestran un mensaje de confirmación
  (flash). Debes conectar el guardado real en base de datos y el envío de correo.
- Plataforma Académica / Edupage: son enlaces externos, reemplaza el "#" por
  la URL real cuando la tengas.
- Sistema de Archivo: la página /servicios/archivo redirige automáticamente;
  cambia la URL de destino en templates/pagina/archivo.html.


=============================================================
NUEVO: BASE DE DATOS + PANEL ADMINISTRATIVO
=============================================================

Ahora el proyecto tiene una base de datos real en SQLite:
    database/julio_florez.db   (se crea sola la primera vez que corres app.py)

MODELOS (carpeta modelo/, misma convención log_*.py que ya usabas):
    conexion.py     -> conexión + creación de tablas + datos de ejemplo
    log_noticia.py  -> CRUD de noticias
    log_evento.py   -> CRUD de eventos
    log_libro.py    -> CRUD de libros + préstamos (biblioteca)
    log_pago.py     -> CRUD de conceptos de pago + registro de pagos (pagaduría)
    log_usuario.py  -> usuarios del panel admin (login)

PANEL ADMINISTRATIVO
----------------------
URL:      http://127.0.0.1:5000/admin/login
Usuario:  admin
Clave:    julioflorez2026

⚠ CAMBIA esta clave apenas puedas: entra a modelo/conexion.py, función
  inicializar_bd(), y modifica la contraseña sembrada, o crea un usuario
  nuevo con modelo.log_usuario.crear_usuario() y borra el archivo
  database/julio_florez.db para que se vuelva a crear.

Desde el panel puedes:
  - Noticias:   crear, editar, eliminar y publicar/despublicar en vivo.
                Se reflejan de inmediato en /noticias y en la portada.
  - Eventos:    lo mismo, se reflejan en /eventos y en el calendario del inicio.
  - Biblioteca: administrar el catálogo de libros (cantidad total/disponible)
                y ver/gestionar préstamos activos (marcar como devuelto).
  - Pagaduría:  administrar los conceptos de pago autorizados (los que se ven
                en /servicios/pagaduria) y consultar los pagos registrados.

Todas las rutas /admin/* están protegidas: si no has iniciado sesión, te
redirige automáticamente a /admin/login (decorador @login_requerido en app.py).

NUEVAS PÁGINAS PÚBLICAS
--------------------------
  /organigrama   -> Pirámide de cargos: Rector > Coordinaciones > Docentes de
                     especialidad y de campos de formación > Orientación.
                     Los datos están en app.py (listas COORDINACIONES,
                     DOCENTES_ESPECIALIDAD, DOCENTES_CAMPOS) — edítalas con
                     los nombres reales cuando los tengas.
  /secretaria    -> Trámites de Secretaría Académica (certificados, traslados, etc).
  /orientacion   -> Página de Orientación Escolar (apoyo psicosocial y vocacional).

SUBIR IMÁGENES DESDE EL PANEL
--------------------------------
El formulario de noticias ya permite subir una imagen directamente (se guarda
en static/images/ automáticamente). Los demás formularios (eventos, libros,
conceptos) por ahora son solo texto — si quieres que también permitan subir
imagen, dímelo y lo agrego siguiendo el mismo patrón.

PENDIENTE PARA PRODUCCIÓN
----------------------------
- Cambiar app.secret_key por una clave segura y guardarla en variable de entorno.
- Cambiar la contraseña del usuario admin sembrado.
- Agregar más usuarios/roles si varias personas van a administrar el sitio
  (ya existe el campo "rol" en usuarios_admin para eso).
