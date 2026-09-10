# =========================================================
# modelo/conexion.py
# Conexión a la base de datos SQLite + creación de tablas
# =========================================================
import sqlite3
import os
from werkzeug.security import generate_password_hash

RUTA_BD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "julio_florez.db")


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_bd():
    """Crea las tablas si no existen y siembra datos de ejemplo la primera vez."""
    conexion = obtener_conexion()
    cur = conexion.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios_admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'editor'
    );

    CREATE TABLE IF NOT EXISTS noticias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        resumen TEXT,
        contenido TEXT,
        autor TEXT,
        imagen TEXT,
        fecha TEXT NOT NULL,
        publicado INTEGER NOT NULL DEFAULT 1,
        creado_en TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Programado',
        descripcion TEXT,
        fecha_completa TEXT NOT NULL,
        mes TEXT NOT NULL,
        dia TEXT NOT NULL,
        sede TEXT DEFAULT 'Ambas',
        publicado INTEGER NOT NULL DEFAULT 1,
        creado_en TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        categoria TEXT,
        grado TEXT,
        cantidad_total INTEGER NOT NULL DEFAULT 1,
        cantidad_disponible INTEGER NOT NULL DEFAULT 1,
        creado_en TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS prestamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        libro_id INTEGER NOT NULL REFERENCES libros(id) ON DELETE CASCADE,
        estudiante TEXT NOT NULL,
        grado TEXT,
        fecha_prestamo TEXT NOT NULL,
        fecha_limite TEXT NOT NULL,
        devuelto INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS conceptos_pago (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        valor INTEGER NOT NULL DEFAULT 0,
        obligatorio INTEGER NOT NULL DEFAULT 0,
        descripcion TEXT,
        activo INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS pagos_registrados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante TEXT NOT NULL,
        grado TEXT,
        concepto_id INTEGER REFERENCES conceptos_pago(id),
        valor_pagado INTEGER NOT NULL,
        medio_pago TEXT,
        fecha_pago TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Pagado'
    );

    CREATE TABLE IF NOT EXISTS logros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        titulo_logro TEXT NOT NULL,
        descripcion TEXT,
        grado TEXT,
        imagen TEXT,
        fecha TEXT NOT NULL,
        publicado INTEGER NOT NULL DEFAULT 1,
        creado_en TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conexion.commit()

    # --- Sembrar datos de ejemplo solo si las tablas están vacías ---
    if cur.execute("SELECT COUNT(*) FROM usuarios_admin").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO usuarios_admin (usuario, password_hash, nombre, rol) VALUES (?,?,?,?)",
            [
                ("rector", generate_password_hash("rector2026"), "Rector", "rector"),
                ("admin", generate_password_hash("julioflorez2026"), "Administrador General", "admin"),
                ("secretaria", generate_password_hash("secretaria2026"), "Secretaría Académica", "secretaria"),
                ("pagaduria", generate_password_hash("pagaduria2026"), "Pagaduría", "pagaduria"),
            ],
        )

    if cur.execute("SELECT COUNT(*) FROM noticias").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO noticias (titulo, categoria, resumen, contenido, autor, imagen, fecha, publicado) VALUES (?,?,?,?,?,?,?,1)",
            [
                ("Programa de Orientación Profesional (POP)", "Orientación",
                 "El Instituto Técnico Distrital Julio Flórez lanza su Programa de Orientación Profesional para apoyar a los estudiantes en la toma de decisiones sobre su proyecto de vida.",
                 "El Instituto Técnico Distrital Julio Flórez lanza su Programa de Orientación Profesional (POP) para apoyar a los estudiantes de grados 10° y 11° en la toma de decisiones sobre su proyecto de vida, con talleres vocacionales, pruebas de intereses y acompañamiento personalizado.",
                 "Departamento de Orientación", "noticia-pop.jpg", "3 de abril de 2026"),
                ("Donatón: Tu Ayuda Alimenta Sonrisas", "Bienestar",
                 "La comunidad educativa del Colegio Julio Flórez se une en una jornada solidaria de recolección de alimentos para apoyar a las familias más vulnerables de nuestra comunidad.",
                 "La comunidad educativa del Colegio Julio Flórez se unió en una jornada solidaria de recolección de alimentos no perecederos para apoyar a las familias en situación de vulnerabilidad de los barrios aledaños. La actividad hizo parte del componente CAS del Programa del Diploma IB.",
                 "Comité de Bienestar", "noticia-donaton.jpg", "2 de abril de 2026"),
                ("Acreditación de Excelencia en Gestión Educativa", "Institucional",
                 "El Instituto Técnico Distrital Julio Flórez recibe una nueva distinción en el marco del programa Los Mejores de Bogotá por su destacada gestión educativa y resultados académicos.",
                 "El Instituto Técnico Distrital Julio Flórez recibió una nueva distinción en el marco del programa 'Los Mejores de Bogotá' por su destacada gestión educativa, resultados académicos y compromiso con la comunidad del norte de la ciudad.",
                 "Rectoría", "noticia-acreditacion.jpg", "15 de marzo de 2026"),
            ],
        )

    if cur.execute("SELECT COUNT(*) FROM eventos").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO eventos (titulo, categoria, estado, descripcion, fecha_completa, mes, dia, sede, publicado) VALUES (?,?,?,?,?,?,?,?,1)",
            [
                ("Ceremonia de Izada de Bandera", "Institucional", "Programado",
                 "Ceremonia institucional mensual de izada de bandera con reconocimientos académicos y deportivos a estudiantes destacados.",
                 "21 de junio de 2026", "JUN", "21", "Ambas"),
                ("Muestra de Especialidades Técnicas", "Académico", "Programado",
                 "Exposición de proyectos desarrollados por los estudiantes de las cuatro especialidades técnicas.",
                 "10 de mayo de 2026", "MAY", "10", "Sede A"),
                ("Jornada de Donatón", "Bienestar", "Finalizado",
                 "Jornada solidaria de recolección de alimentos para apoyar a familias en situación de vulnerabilidad.",
                 "15 de abril de 2026", "ABR", "15", "Ambas"),
                ("Inicio de Clases — Año Escolar 2026", "Académico", "Finalizado",
                 "Inicio oficial del año escolar 2026 para todos los estudiantes de la institución.",
                 "6 de abril de 2026", "ABR", "6", "Ambas"),
                ("Inscripciones Abiertas — Matrículas 2026", "Académico", "Finalizado",
                 "Se abren las inscripciones para el proceso de matrícula del año escolar 2026.",
                 "5 de marzo de 2026", "MAR", "5", "Ambas"),
            ],
        )

    if cur.execute("SELECT COUNT(*) FROM libros").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO libros (titulo, autor, categoria, grado, cantidad_total, cantidad_disponible) VALUES (?,?,?,?,?,?)",
            [
                ("Cien años de soledad", "Gabriel García Márquez", "Literatura", "10°-11°", 6, 4),
                ("Fundamentos de Programación", "Luis Joyanes Aguilar", "Técnico", "10°-11°", 4, 4),
                ("Química General", "Raymond Chang", "Ciencias", "9°-11°", 5, 3),
            ],
        )

    if cur.execute("SELECT COUNT(*) FROM conceptos_pago").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO conceptos_pago (nombre, valor, obligatorio, descripcion, activo) VALUES (?,?,?,?,1)",
            [
                ("Seguro estudiantil", 25000, 1, "Cobertura de accidentes escolares, autorizado por la Secretaría de Educación."),
                ("Materiales especialidad técnica", 45000, 0, "Insumos para las especialidades de Diseño Multimedial y Manejo Ambiental."),
                ("Certificado de estudio (copia adicional)", 5000, 0, "Costo por copia adicional a la primera, que es gratuita."),
            ],
        )

    if cur.execute("SELECT COUNT(*) FROM logros").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO logros (nombre, categoria, titulo_logro, descripcion, grado, imagen, fecha, publicado) VALUES (?,?,?,?,?,?,?,1)",
            [
                ("María José Rodríguez", "Deportivo", "Medalla de Oro — Juegos Intercolegiados de Atletismo",
                 "Representó a la institución en los 400 metros planos, logrando el primer puesto a nivel distrital.",
                 "10°", "logro-atletismo.jpg", "20 de mayo de 2026"),
                ("Equipo de Robótica Julio Flórez", "Académico", "Segundo Puesto — Feria Distrital de Ciencia y Tecnología",
                 "El equipo de la especialidad de Programación de Software presentó un proyecto de automatización con Arduino que obtuvo reconocimiento distrital.",
                 "11°", "logro-robotica.jpg", "12 de mayo de 2026"),
                ("Santiago Pérez", "Mención Especial", "Mejor Promedio Académico — Promoción 2025",
                 "Reconocido por la Rectoría por mantener el promedio más alto de su generación durante los grados 10° y 11°.",
                 "11°", "logro-mencion.jpg", "28 de noviembre de 2025"),
                ("Grupo de Danzas Folclóricas", "Cultural", "Primer Lugar — Semana de Integración con la Comunidad",
                 "El grupo representó danzas típicas de la región Andina y Pacífica, obteniendo el primer lugar en la muestra cultural interinstitucional.",
                 "Mixto", "logro-danzas.jpg", "3 de octubre de 2025"),
                ("Delegación Programa del Diploma IB", "Grupos y Programas", "Reconocimiento World School — Bachillerato Internacional",
                 "La institución recibió el reconocimiento como Colegio del Mundo IB por el compromiso de sus estudiantes con el perfil de la comunidad de aprendizaje.",
                 "10°-11°", "logro-ib.jpg", "15 de agosto de 2025"),
            ],
        )

    conexion.commit()
    conexion.close()
