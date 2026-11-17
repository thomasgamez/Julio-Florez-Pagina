# =========================================================
# contenido_base.py — Textos base del sitio
# Aquí vive la "base" de la información. Lo que se edite
# desde el panel se guarda aparte y tiene prioridad; si se
# restaura, vuelve a mostrarse lo que está escrito aquí.
# =========================================================

# tipo: "texto" = una línea, "parrafo" = varias líneas
def _t(grupo, etiqueta, base, tipo="texto"):
    """Atajo para registrar un texto."""
    return {"grupo": grupo, "etiqueta": etiqueta, "tipo": tipo, "base": base}

CONTENIDO_BASE = {
        # ---------- Inicio: portada ----------
    "inicio.hero_institucion": _t("Inicio", "Portada: nombre de la institución", "INSTITUTO TECNICO DISTRITAL JULIO FLOREZ"),
    "inicio.hero_titulo_1": _t("Inicio", "Portada: Lema", ("Jóvenes Líderes Transformadores de la Realidad"), "parrafo"),
    "inicio.hero_texto": _t("Inicio", "Portada: párrafo", (
        "Institución educativa oficial de carácter técnico, comprometida con una educación innovadora y de calidad. "
        "Formamos ciudadanos del mundo..."), "parrafo"),

    # ---------- Inicio: Nuestra Institución ----------
    "inicio.inst_titulo": _t("Inicio", "Nuestra institución: título", "Nuestra Institución"),
    "inicio.inst_lema": _t("Inicio", "Nuestra institución: lema", "Formando ciudadanos del mundo desde el corazón de Bogotá"),
    "inicio.inst_parrafo_1": _t("Inicio", "Nuestra institución: primer párrafo", (
        "El colegio es una institución educativa oficial de carácter técnico (Programación de Software, "
        "Administración de Empresas, Diseño e integración multimedia y Manejo Ambiental), ubicada en la localidad "
        "de Suba, Bogotá D.C. Siendo los pioneros en la implementación de la **jornada única** en el Distrito "
        "Capital desde el año 2015."), "parrafo"),
    "inicio.inst_parrafo_2": _t("Inicio", "Nuestra institución: segundo párrafo", (
        "Hacemos parte de los 5 primeros colegios públicos de Bogotá en graduar y certificar estudiantes del "
        "**Programa de Orientación Profesional del Bachillerato Internacional (IB).**"), "parrafo"),
    "inicio.inst_boton": _t("Inicio", "Nuestra institución: texto del botón", "Conocer más →"),

    # ---------- Inicio: Especialidades ----------
    "inicio.esp_titulo": _t("Inicio", "Especialidades: título", "Estudios de Formación Profesional o Especialidades Técnicas"),
    "inicio.esp_texto": _t("Inicio", "Especialidades: texto", (
        "Cuatro programas articulados que preparan a nuestros estudiantes para el mundo laboral y universitario"), "parrafo"),
    "inicio.esp_boton": _t("Inicio", "Especialidades: texto del botón", "Ver más"),

    # ---------- Inicio: Bachillerato Internacional ----------
    "inicio.ib_titulo": _t("Inicio", "Bachillerato Internacional: título", "Bachillerato Internacional"),
    "inicio.ib_parrafo_1": _t("Inicio", "Bachillerato Internacional: primer párrafo", (
        "El Bachillerato Internacional (IB) es una organización educativa global que ofrece programas académicos "
        "para estudiantes en más de 160 países. Permite que los alumnos agencien su propio aprendizaje y desarrollen "
        "habilidades de pensamiento, comunicación, autogestión, sociales e indagación que les da la confianza en sí "
        "mismos para progresar y hacer la diferencia."), "parrafo"),
    "inicio.ib_parrafo_2": _t("Inicio", "Bachillerato Internacional: segundo párrafo", (
        "Desde diciembre de 2023, somos la única institución educativa de Suba que implementa uno de los Programas "
        "del Bachillerato Internacional, estrategia orientada al cierre de brechas educativas dentro del sistema "
        "educativo oficial del Distrito Capital."), "parrafo"),
    "inicio.ib_boton_1": _t("Inicio", "Bachillerato Internacional: primer botón", "Conocer el POP →"),
    "inicio.ib_boton_2": _t("Inicio", "Bachillerato Internacional: segundo botón", "Inscribirse"),

    # ---------- Inicio: Campos de formación ----------
    "inicio.campos_titulo": _t("Inicio", "Campos de formación: título", "Campos de Formación"),
    "inicio.campos_texto": _t("Inicio", "Campos de formación: texto", (
        "Una propuesta pedagógica integral que articula el saber, el ser y el hacer en seis campos del conocimiento"), "parrafo"),
    "inicio.campos_boton": _t("Inicio", "Campos de formación: texto del botón", "Explorar campos →"),

    # ---------- Inicio: Accesos rápidos ----------
    "inicio.accesos_etiqueta": _t("Inicio", "Accesos rápidos: título", "Accesos Rápidos"),
    "inicio.accesos_texto": _t("Inicio", "Accesos rápidos: texto", "Servicios y trámites al alcance de un clic"),
    "inicio.acc_pagaduria": _t("Inicio", "Accesos rápidos: nombre de Pagaduría", "Pagaduría"),
    "inicio.acc_biblioteca": _t("Inicio", "Accesos rápidos: nombre de Biblioteca", "Biblioteca"),
    "inicio.acc_archivo": _t("Inicio", "Accesos rápidos: nombre de Archivo", "Sistema de Archivo"),
    "inicio.acc_edupage": _t("Inicio", "Accesos rápidos: nombre de Edupage", "Edupage"),
    "inicio.acc_zoe": _t("Inicio", "Accesos rápidos: nombre de ZOE", "ZOE"),
    "inicio.acc_contacto": _t("Inicio", "Accesos rápidos: nombre de Contacto", "Contacto"),

    # ---------- Inicio: Calendario y noticias ----------
    "inicio.calendario_titulo": _t("Inicio", "Calendario: título", "Calendario"),
    "inicio.calendario_boton": _t("Inicio", "Calendario: texto del botón", "Ver todos los eventos →"),
    "inicio.noticias_titulo": _t("Inicio", "Noticias: título", "Últimas Noticias"),
    "inicio.noticias_leer": _t("Inicio", "Noticias: texto de cada «Leer más»", "Leer más →"),
    "inicio.noticias_boton": _t("Inicio", "Noticias: texto del botón", "Ver todas las noticias →"),

        # ---------- IB: ¿Qué es el IB? ----------
    "bi.ib.hero_etiqueta": _t("IB: ¿Qué es el IB?", "Portada: etiqueta superior", "Programa del Diploma · IB"),
    "bi.ib.hero_titulo": _t("IB: ¿Qué es el IB?", "Portada: título", "Bachillerato Internacional"),
    "bi.ib.hero_subtitulo": _t("IB: ¿Qué es el IB?", "Portada: subtítulo", "Colegio Distrital de Bogotá con el Programa del Diploma IB"),
    "bi.ib.parrafo_1": _t("IB: ¿Qué es el IB?", "Primer párrafo", (
        "El Bachillerato Internacional (IB) es una organización educativa global que ofrece programas académicos "
        "para estudiantes en más de 160 países. Permite que los alumnos agencien su propio aprendizaje y desarrollen "
        "habilidades de pensamiento, comunicación, autogestión, sociales e indagación que les da la confianza en sí "
        "mismos para progresar y hacer la diferencia."), "parrafo"),
    "bi.ib.parrafo_2": _t("IB: ¿Qué es el IB?", "Segundo párrafo", (
        "Para los colegios públicos del Distrito, es una propuesta educativa orientada a transformar la educación y "
        "fortalecer la formación integral de los estudiantes, formando personas con mentalidad internacional, "
        "conscientes de los vínculos que comparten como seres humanos y su responsabilidad en el cuidado del planeta."), "parrafo"),
    "bi.ib.parrafo_3": _t("IB: ¿Qué es el IB?", "Tercer párrafo", (
        "**Desde diciembre de 2023**, somos la única institución educativa de Suba que implementa uno de los Programas "
        "del Bachillerato Internacional, estrategia orientada al cierre de brechas educativas dentro del sistema "
        "educativo oficial del Distrito Capital."), "parrafo"),

    # ---------- IB: POP ----------
    "bi.pop.parrafo_1": _t("IB: POP", "Primer párrafo", (
        "El Programa de Orientación Profesional (POP) integra los valores del Bachillerato Internacional (IB) con una "
        "formación profesional adaptada a las necesidades de aquellos estudiantes que desean seguir una carrera específica."), "parrafo"),
    "bi.pop.parrafo_2": _t("IB: POP", "Segundo párrafo", (
        "Para desarrollar este programa en el CITD Julio Flórez, los estudiantes vivencian los atributos del Perfil de "
        "la Comunidad de Aprendizaje, estudian tres cursos del Programa de Diploma (PD), junto con los componentes "
        "troncales del POP y un programa de Estudios de Formación Profesional correspondiente a los programas técnicos "
        "especializados que ofrece la institución."), "parrafo"),
    "bi.pop.parrafo_3": _t("IB: POP", "Tercer párrafo", (
        "Este programa está diseñado para preparar a los estudiantes tanto en el ámbito profesional como académico, "
        "promoviendo actitudes y hábitos mentales que estimulan un aprendizaje continuo a lo largo de la vida."), "parrafo"),

    # ---------- IB: Media Técnica ----------
    "bi.media.parrafo_1": _t("IB: Media Técnica", "Primer párrafo", (
        "La Media Técnica Internacional del CITD Julio Flórez está dirigida a estudiantes de **décimo y undécimo grado**. "
        "Su propósito es fortalecer una formación integral que les permita convertirse en ciudadanos seguros, "
        "competentes y preparados para continuar estudios posteriores, ingresar a la educación superior o asumir los "
        "retos del mundo laboral."), "parrafo"),
    "bi.media.parrafo_2": _t("IB: Media Técnica", "Segundo párrafo", (
        "Esta propuesta formativa incorpora al horizonte institucional los valores y principios del Bachillerato "
        "Internacional, y responde a las necesidades de los estudiantes promoviendo el desarrollo de competencias "
        "personales, académicas y laborales. En este proceso, se busca que los estudiantes:"), "parrafo"),
    "bi.media.tarjeta_1": _t("IB: Media Técnica", "Tarjeta 1 (maletín)",
        "Desarrollen competencias laborales generales y fortalezcan sus habilidades en áreas específicas de formación.", "parrafo"),
    "bi.media.tarjeta_2": _t("IB: Media Técnica", "Tarjeta 2 (bombillo)",
        "Cultiven aptitudes y hábitos mentales que favorezcan el aprendizaje continuo.", "parrafo"),
    "bi.media.tarjeta_3": _t("IB: Media Técnica", "Tarjeta 3 (escudo)",
        "Se preparen para actuar con seguridad y responsabilidad en contextos académicos, profesionales y laborales.", "parrafo"),
    "bi.media.nota": _t("IB: Media Técnica", "Nota final", (
        "La Media Técnica Internacional se desarrolla en concordancia con la propuesta educativa institucional y tiene "
        "en cuenta los parámetros de planeación, seguimiento y valoración propuestos por el Bachillerato Internacional "
        "para las asignaturas PD, los componentes troncales y la formación técnica en cada uno de los Estudios de "
        "Formación Profesional."), "parrafo"),

    # ---------- IB: Asignaturas PD ----------
    "bi.pd.intro": _t("IB: Asignaturas PD", "Texto introductorio", (
        "Las asignaturas del plan de estudios institucional concuerdan con tres asignaturas ofertadas por el Programa "
        "de Diploma, lo que facilita la implementación del programa en el ciclo V (décimo y undécimo)"), "parrafo"),

    # ---------- IB: Componentes troncales ----------
    "bi.troncales.intro": _t("IB: Componentes troncales", "Texto introductorio", (
        "Articulan todas las partes del programa y aseguran que la formación no se limite a un conjunto de asignaturas "
        "aisladas, sino que constituya una experiencia integrada, significativa y con un propósito claro. Actúan como "
        "ejes que permiten a los estudiantes conectar los principios trabajados en el aula con situaciones y prácticas "
        "del mundo real."), "parrafo",
    ),

        # ---------- IB: Perfil de la comunidad ----------
    "bi.perfil.intro": _t("IB: Perfil de la comunidad", "Texto introductorio", (
        "Diez atributos valorados por los Colegios del Mundo del IB, que ayudan a las personas a ser miembros "
        "responsables de las comunidades locales, nacionales y mundiales"), "parrafo"),
    "bi.perfil.fuente": _t("IB: Perfil de la comunidad", "Fuente (debajo de los atributos)",
        "Fuente: Organización del Bachillerato Internacional, 2015"),
    "bi.perfil.habilidades_titulo": _t("IB: Perfil de la comunidad", "Título de la sección de habilidades",
        "Habilidades que Desarrollarán"),

    # ---------- IB: Equipo IB ----------
    "bi.equipo.subtitulo": _t("IB: Equipo IB", "Subtítulo de la página",
        "Profesionales que lideran y acompañan el Programa del Diploma"),
    "bi.equipo.coord_rol": _t("IB: Equipo IB", "Persona 1: cargo", "Coordinador IB"),
    "bi.equipo.coord_area": _t("IB: Equipo IB", "Persona 1: área", "Bachillerato Internacional"),
    "bi.equipo.coord_nombre": _t("IB: Equipo IB", "Persona 1: nombre", "Carlos Alberto Gil Vargas"),
    "bi.equipo.coord_desc": _t("IB: Equipo IB", "Persona 1: descripción", (
        "Lidera la implementación del Programa de Orientación Profesional (POP), articula el currículo institucional "
        "con los estándares IB y acompaña a los estudiantes en su trayectoria hacia el diploma."), "parrafo"),
    "bi.equipo.coord_correo": _t("IB: Equipo IB", "Persona 1: correo", "ib.dp@ejulioflorez.edu.co"),
    "bi.equipo.doc_rol": _t("IB: Equipo IB", "Persona 2: cargo", "Docente de articulación"),
    "bi.equipo.doc_area": _t("IB: Equipo IB", "Persona 2: área", "Componentes troncales"),
    "bi.equipo.doc_nombre": _t("IB: Equipo IB", "Persona 2: nombre", "Stella Rincón Velandia"),
    "bi.equipo.doc_desc": _t("IB: Equipo IB", "Persona 2: descripción", (
        "Acompaña el proceso pedagógico del programa IB, gestiona la formación docente y articula las prácticas IB "
        "con los proyectos institucionales."), "parrafo"),
    "bi.equipo.doc_correo": _t("IB: Equipo IB", "Persona 2: correo", "srinconv@educacionbogota.edu.co"),
    "bi.equipo.cta_titulo": _t("IB: Equipo IB", "Invitación final: título", "¿Interesado en el Programa IB?"),
    "bi.equipo.cta_texto": _t("IB: Equipo IB", "Invitación final: texto", (
        "Inscríbete al proceso de matrículas y haz parte de la comunidad de líderes globales del Julio Flórez"), "parrafo"),
    "bi.equipo.cta_boton": _t("IB: Equipo IB", "Invitación final: texto del botón", "Iniciar proceso de inscripción →"),

    # ---------- IB: Estudios de formación ----------
    "bi.estudios.intro": _t("IB: Estudios de formación", "Texto del encabezado", (
        "Nuestra institución implementa el Programa de Orientación Profesional del IB por su enfoque técnico. Las "
        "especialidades existentes, ahora Estudios de Formación Profesional, avaladas por la Universidad Católica de "
        "Colombia y la Universidad Minuto de Dios, validan la implementación de la propuesta educativa del "
        "Bachillerato Internacional."), "parrafo"),
    "bi.estudios.ver_competencias": _t("IB: Estudios de formación", "Texto del desplegable de cada especialidad",
        "Ver competencias y perfil"),
    "bi.estudios.docente_label": _t("IB: Estudios de formación", "Etiqueta «Docente a cargo»", "Docente a cargo"),
    "bi.estudios.coord_iniciales": _t("IB: Estudios de formación", "Coordinación: iniciales del recuadro", "CE"),
    "bi.estudios.coord_cargo": _t("IB: Estudios de formación", "Coordinación: cargo",
        "COORDINADORA DE ESTUDIOS DE FORMACIÓN PROFESIONAL"),
    "bi.estudios.coord_nombre": _t("IB: Estudios de formación", "Coordinación: nombre", "Luz Dary Rosas Crespo"),
    "bi.estudios.coord_desc": _t("IB: Estudios de formación", "Coordinación: descripción", (
        "Gestiona la formación docente y asegura la calidad de los procesos de aprendizaje de cada Estudio de "
        "Formación Profesional."), "parrafo"),
    "bi.estudios.coord_correo": _t("IB: Estudios de formación", "Coordinación: correo",
        "especialidades@ejulioflorez.edu.co"),
    
    "contacto.titulo": {
        "grupo": "Contacto", "etiqueta": "Título de la página",
        "tipo": "texto", "base": "Contacto",
    },
    "contacto.subtitulo": {
        "grupo": "Contacto", "etiqueta": "Subtítulo de la página",
        "tipo": "texto", "base": "Estamos para atenderte",
    },
        # ---------- Datos de contacto ----------
    "sedes.principal_nombre": {
        "grupo": "Datos de contacto", "etiqueta": "Sede principal: nombre completo",
        "tipo": "texto", "base": "Sede Principal — Bachillerato Julio Flórez",
    },
    "sedes.principal_corto": {
        "grupo": "Datos de contacto", "etiqueta": "Sede principal: nombre corto (pie de página)",
        "tipo": "texto", "base": "Sede Principal",
    },
    "sedes.principal_direccion": {
        "grupo": "Datos de contacto", "etiqueta": "Sede principal: dirección",
        "tipo": "texto", "base": "Carrera 68B N° 94-12, Bogotá D.C.",
    },
    "sedes.principal_telefonos": {
        "grupo": "Datos de contacto", "etiqueta": "Sede principal: teléfonos",
        "tipo": "texto", "base": "305 792 3922 · 253 6376",
    },
    "sedes.a_nombre": {
        "grupo": "Datos de contacto", "etiqueta": "Sede A: nombre completo",
        "tipo": "texto", "base": "Sede A — Primaria Santa Rosa",
    },
    "sedes.a_corto": {
        "grupo": "Datos de contacto", "etiqueta": "Sede A: nombre corto (pie de página)",
        "tipo": "texto", "base": "Sede A",
    },
    "sedes.a_direccion": {
        "grupo": "Datos de contacto", "etiqueta": "Sede A: dirección",
        "tipo": "texto", "base": "Calle 102A N° 70-40, Bogotá D.C.",
    },
    "sedes.a_telefonos": {
        "grupo": "Datos de contacto", "etiqueta": "Sede A: teléfonos",
        "tipo": "texto", "base": "300 207 2701",
    },
    "contacto.correo_institucional": {
        "grupo": "Datos de contacto", "etiqueta": "Correo institucional (rectoría)",
        "tipo": "texto", "base": "rectoria@ejulioflorez.edu.co",
    },
    "contacto.correo_general": {
        "grupo": "Datos de contacto", "etiqueta": "Correo general (barra superior)",
        "tipo": "texto", "base": "info@ejulioflorez.edu.co",
    },
    "contacto.correo_sed": {
        "grupo": "Datos de contacto", "etiqueta": "Correo de la Secretaría de Educación",
        "tipo": "texto", "base": "cedjulioflorez11@educacionbogota.edu.co",
    },
    "contacto.linea_gratuita": {
        "grupo": "Datos de contacto", "etiqueta": "Línea gratuita (barra superior)",
        "tipo": "texto", "base": "1800 671-0800",
    },
    "contacto.horario": {
        "grupo": "Datos de contacto", "etiqueta": "Horario de atención",
        "tipo": "texto", "base": "Lunes a Viernes: 6:30 a.m. – 4:00 p.m.",
    },

    # ---------- Redes sociales ----------
    "redes.facebook": {
        "grupo": "Redes sociales", "etiqueta": "Facebook (enlace completo)",
        "tipo": "url", "base": "",
    },
    "redes.instagram": {
        "grupo": "Redes sociales", "etiqueta": "Instagram (enlace completo)",
        "tipo": "url", "base": "",
    },
    "redes.tiktok": {
        "grupo": "Redes sociales", "etiqueta": "TikTok (enlace completo)",
        "tipo": "url", "base": "",
    },
        # ---------- Datos generales ----------
    "sitio.resolucion": _t("Datos generales", "Resolución de aprobación (portada y pie de página)",
        "Resolución de Aprobación N° 002348 de 2023 — Secretaría de Educación del Distrito"),

    # ---------- Enlaces del sitio ----------
    "enlaces.biblioteca": _t("Enlaces del sitio", "Biblioteca (enlace completo)", "https://biblioteca-final-1.onrender.com", "url"),
    "enlaces.edupage": _t("Enlaces del sitio", "Edupage (enlace completo)", "https://citdjulioflorez.edupage.org/login/index.php?out=1", "url"),
    "enlaces.zoe": _t("Enlaces del sitio", "ZOE (enlace completo)", "https://zoe-app-mimm.onrender.com", "url"),
}

# Títulos y botones del submenú del Bachillerato Internacional: (título de la página, nombre corto del botón)
BI_SECCIONES = {
    "que-es-ib": ("¿Qué es el Bachillerato Internacional?", "¿Qué es el BI?"),
    "media-tecnica": ("Media Técnica Internacional", "Media Técnica"),
    "pop": ("Programa de Orientación Profesional (POP)", "POP"),
    "asignaturas-pd": ("Asignaturas PD", "Asignaturas PD"),
    "estudios-formacion": ("Estudios de Formación Profesional", "Estudios de Formación"),
    "componentes-troncales": ("Componentes Troncales del POP", "Componentes Troncales"),
    "perfil-comunidad": ("Perfil de la Comunidad de Aprendizaje", "Perfil Comunidad"),
    "equipo-ib": ("Equipo de Coordinación IB", "Equipo IB"),
}

for _clave, (_titulo, _corto) in BI_SECCIONES.items():
    CONTENIDO_BASE[f"bi.{_clave}.titulo"] = _t("BI: títulos y menú", f"Título de la página «{_corto}»", _titulo)
    CONTENIDO_BASE[f"bi.{_clave}.corto"] = _t("BI: títulos y menú", f"Botón del submenú «{_corto}»", _corto)