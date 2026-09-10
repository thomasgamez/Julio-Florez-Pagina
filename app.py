# =========================================================
# Instituto Técnico Distrital Julio Flórez
# Aplicación Flask principal
# =========================================================
import os
from functools import wraps
from datetime import date
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session

from modelo.conexion import inicializar_bd
from modelo import log_noticia, log_evento, log_libro, log_pago, log_usuario, log_logro

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"

CARPETA_IMAGENES = os.path.join(app.root_path, "static", "images")
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

inicializar_bd()


def login_requerido(vista):
    """Decorador: exige sesión de administrador para entrar al panel."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Debes iniciar sesión para acceder al panel administrativo.", "error")
            return redirect(url_for("admin_login"))
        return vista(*args, **kwargs)
    return envoltura


def guardar_imagen_subida(archivo):
    """Guarda un archivo de imagen subido por un formulario y devuelve su nombre, o None."""
    if archivo and archivo.filename:
        nombre = secure_filename(archivo.filename)
        archivo.save(os.path.join(CARPETA_IMAGENES, nombre))
        return nombre
    return None


# ---------------------------------------------------------
# DATOS DE EJEMPLO (luego puedes moverlos a tu carpeta /modelo
# y traerlos desde una base de datos real)
# ---------------------------------------------------------

ESPECIALIDADES = [
    {
        "nombre": "Administración de Empresas",
        "icono": "bi-briefcase",
        "imagen": "especialidad admin.jpeg",
        "posicion": "top",
        "descripcion": "Contribuir a la formación del Tecnica en Administracion de Empresas mediante el desarrilli de competencias cognitivas laborales y sociales que permiten al estudiante dar soluciones a las necesidades de su comunidad destacandose por su vocación de servicio y liderazgo.",
        "competencias": ["Contabilidad básica y financiera", "Gestión de talento humano", "Mercadeo y ventas", "Emprendimiento"],
        "docente": "Monica Bolaños Aguilar",
        "iniciales": "AE",
    },
    {
        "nombre": "Programación de Software",
        "icono": "bi-code-slash",
        "imagen": "PROSOF.jpeg",
        "posicion": "center",
        "descripcion": "Desarrolla habilidades en programación orientada a objetos, desarrollo web, bases de datos y sistemas de información.",
        "competencias": ["Lógica de programación", "Desarrollo web (frontend/backend)", "Bases de datos", "Trabajo en equipo ágil"],
        "docente": "Jose Miguel Santana Cardenas",
        "iniciales": "PS",
    },
    {
        "nombre": "Manejo Ambiental",
        "icono": "bi-tree",
        "imagen": "Especialidad ambiental.jpeg",
        "posicion": "top",
        "descripcion": "Forma líderes ambientales con conocimientos en gestión de recursos naturales, manejo de residuos, monitoreo ambiental y educación ecológica.",
        "competencias": ["Manejo de residuos sólidos", "Monitoreo de recursos naturales", "Educación ambiental", "Normatividad ambiental"],
        "docente": "Eliana Mayerly Bohorquez Perilla",
        "iniciales": "MA",
    },
    {
        "nombre": "Diseño e Integración Multimedial",
        "icono": "bi-palette",
        "imagen": "especialidad diseño.jpeg",
        "posicion": "center",
        "descripcion": "Diseñar soluciones multimediales y sistemas digitales encaminados en la gestion de la información, la comunicación audiovisual y la animación.",
        "competencias": ["Historia de la Comunicacion y el Diseño", "Diseño de Guiones, Dibujo e ilustración Digital", "Fotografía e Imagen, Diseño Editorial", "Diseño Web, Animación Digital", "Video y Efectos Especiales, Diseño Grafico y Proyecto Multimedia."],
        "docente": "Raul Rodriguez Carrillo",
        "iniciales": "DM",
    },
]

ASIGNATURAS_PD = [
    {"nombre": "Inglés Ab Initio", "icono": "bi-translate"},
    {"nombre": "Matemáticas: Aplicaciones e Interpretación", "icono": "bi-calculator"},
    {"nombre": "Lengua y Literatura", "icono": "bi-journal-text"},
]

COMPONENTES_TRONCALES_POP = [
    {"nombre": "Compromiso Comunitario", "icono": "bi-people-fill"},
    {"nombre": "Estudios Lingüísticos y Culturales", "icono": "bi-globe2"},
    {"nombre": "Proyecto de Reflexión", "icono": "bi-journal-check"},
    {"nombre": "Habilidades Personales y Profesionales", "icono": "bi-award"},
]

BACHILLERATO_SECCIONES = {
    "que-es-ib": {"titulo": "¿Qué es el Bachillerato Internacional?", "corto": "¿Qué es el BI?", "icono": "bi-globe-americas"},
    "media-tecnica": {"titulo": "Media Técnica Internacional", "corto": "Media Técnica", "icono": "bi-mortarboard"},
    "pop": {"titulo": "Programa de Orientación Profesional (POP)", "corto": "POP", "icono": "bi-compass"},
    "asignaturas-pd": {"titulo": "Asignaturas PD", "corto": "Asignaturas PD", "icono": "bi-journal-text"},
    "estudios-formacion": {"titulo": "Estudios de Formación Profesional", "corto": "Estudios de Formación", "icono": "bi-briefcase"},
    "componentes-troncales": {"titulo": "Componentes Troncales del POP", "corto": "Componentes Troncales", "icono": "bi-diagram-3"},
    "perfil-comunidad": {"titulo": "Perfil de la Comunidad de Aprendizaje", "corto": "Perfil Comunidad", "icono": "bi-people"},
    "equipo-ib": {"titulo": "Equipo de Coordinación IB", "corto": "Equipo IB", "icono": "bi-person-badge"},
}

BACHILLERATO_TEMPLATES = {
    "que-es-ib": "pagina/Bachillerato/IB.html",
    "media-tecnica": "pagina/Bachillerato/Media_Tecnica.html",
    "pop": "pagina/Bachillerato/POP.html",
    "asignaturas-pd": "pagina/Bachillerato/Asignaturas_PD.html",
    "estudios-formacion": "pagina/Bachillerato/Estudios_formacion.html",
    "componentes-troncales": "pagina/Bachillerato/Componentes_troncales.html",
    "perfil-comunidad": "pagina/Bachillerato/Perfil_comunidad.html",
    "equipo-ib": "pagina/Bachillerato/Equipo_Ib.html",
}

NUESTRA_INSTITUCION_SECCIONES = {
    "historia": {"titulo": "Historia del Colegio", "corto": "Historia", "icono": "bi-journal-bookmark"},
    "simbolos": {"titulo": "Símbolos Institucionales", "corto": "Símbolos", "icono": "bi-shield-shaded"},
    "ubicacion": {"titulo": "Ubicación Geográfica", "corto": "Ubicación", "icono": "bi-geo-alt"},
}

NUESTRA_INSTITUCION_TEMPLATES = {
    "historia": "pagina/institucion/historia.html",
    "resena-historica": "pagina/institucion/resena_historica.html",
    "simbolos": "pagina/institucion/simbolos.html",
    "ubicacion": "pagina/institucion/ubicacion.html",
}

HITOS = [
    {
        "anio": "1958",
        "titulo": "Fundación de la institución",
        "descripcion": "Inicio de la historia del Instituto Técnico Distrital Julio Flórez."
    },
    {
        "anio": "1995",
        "titulo": "Legalización del CED Julio Flórez",
        "descripcion": "Legalización del CED Julio Flórez en jornadas mañana y tarde."
    },
    {
        "anio": "1995",
        "titulo": "Educación Media",
        "descripcion": "Aprobación de la Educación Media en la institución mediante la Resolución 7086."
    },
    {
        "anio": "1997",
        "titulo": "Reconocimiento de la institución",
        "descripcion": "Reconocimiento y fortalecimiento de la institución educativa."
    },
    {
        "anio": "2001",
        "titulo": "Bachillerato",
        "descripcion": "Reconocimiento de bachilleres de 11° mediante la Resolución 8988."
    },
    {
        "anio": "2002",
        "titulo": "Reconocimiento del CED Julio Flórez",
        "descripcion": "Reconocimiento del CED Julio Flórez mediante la Resolución 4261."
    },
    {
        "anio": "2005",
        "titulo": "Creación del CED Julio Flórez",
        "descripcion": "Creación del CED Julio Flórez mediante la Resolución 4440 del 27 de octubre de 2005."
    },
    {
        "anio": "2006",
        "titulo": "Unificación de las sedes",
        "descripcion": "Unificación del CED Santa Rosa y el CED Julio Flórez bajo una misma institución."
    },
    {
        "anio": "2007",
        "titulo": "Articulación con el SENA",
        "descripcion": "Se inicia la articulación y fortalecimiento de la formación técnica con el Servicio Nacional de Aprendizaje (SENA)."
    },
    {
        "anio": "2010",
        "titulo": "Convenios de formación",
        "descripcion": "Fortalecimiento de los procesos de formación mediante alianzas y convenios educativos."
    },
    {
        "anio": "2011",
        "titulo": "Fortalecimiento educativo",
        "descripcion": "Continuidad de los procesos de mejoramiento y formación técnica de la institución."
    },
    {
        "anio": "2012",
        "titulo": "Proyecto de mejoramiento",
        "descripcion": "Implementación de proyectos orientados al mejoramiento educativo y fortalecimiento institucional."
    },
    {
        "anio": "2013",
        "titulo": "Proyecto Hermes",
        "descripcion": "Desarrollo del Proyecto Hermes como parte de las iniciativas institucionales."
    },
    {
        "anio": "2014",
        "titulo": "Educación Media Fortalecida",
        "descripcion": "Fortalecimiento de la Educación Media mediante programas y proyectos de formación para los estudiantes."
    },
    {
        "anio": "2015",
        "titulo": "Media Técnica",
        "descripcion": "Consolidación de la formación técnica y de las especialidades ofrecidas por la institución."
    },
    {
        "anio": "2016",
        "titulo": "Acreditación de excelencia",
        "descripcion": "Reconocimiento mediante procesos de acreditación y fortalecimiento de la excelencia en la gestión educativa."
    },
    {
        "anio": "2017",
        "titulo": "Fortalecimiento institucional",
        "descripcion": "Continuidad de los procesos de formación, innovación y mejoramiento de la institución."
    },
    {
        "anio": "2018",
        "titulo": "Excelencia en la gestión educativa",
        "descripcion": "Reconocimiento a los procesos de excelencia y calidad desarrollados por la institución."
    }
]

CAMPOS_HOME = [
    {"nombre": "Educación Inicial", "icono": "bi-flower1", "resumen": "Desarrollo integral de la primera infancia con enfoque lúdico y pedagógico."},
    {"nombre": "Saberes Sociales", "icono": "bi-globe", "resumen": "Comprensión del entorno histórico, social, cultural y ciudadano."},
    {"nombre": "Campo Matemático", "icono": "bi-calculator", "resumen": "Razonamiento lógico, resolución de problemas y pensamiento abstracto."},
    {"nombre": "Campo de la Comunicación", "icono": "bi-chat-square-text", "resumen": "Lenguaje, expresión oral y escrita, segunda lengua y comunicación digital."},
    {"nombre": "Campo Científico-Tecnológico", "icono": "bi-cpu", "resumen": "Ciencias naturales, tecnología, programación y pensamiento científico."},
    {"nombre": "Formación Especializada y Proyecto de Vida", "icono": "bi-compass", "resumen": "Especialidades técnicas articuladas con SENA y construcción de proyecto de vida."},
]

CAMPOS = [
    {"nombre": "Educación Inicial", "icono": "bi-flower1", "imagen": "campo-inicial.jpg",
     "descripcion": "Estos niveles (pre-jardín, jardín y transición) se caracterizan por trabajar de manera integrar todos sus procesos de aprendizajes, mediante proyectos de aula, a partir de las actividades generadas por los intereses y necesidades de los niños."
     "En el ciclo inicial se evalúan procesos de desarrollo en las dimensiones cognitivas, comunicativa, corporal, artística y personal social con sus respectivos ejes de trabajo, la estrategia pedagógica está fundamentada en los pilares de la educación (Juego, arte, literatura y exploración del medio) y la base es la observación y seguimiento a los procesos de desarrollo infantil.",
     "imagen": "sede a 1.jpeg",
     "puntos": ["Aprendizaje lúdico y experiencial", "Desarrollo de autonomía y autoconfianza", "Educación emocional desde temprana edad", "Integración familia-escuela"]},
    {"nombre": "Saberes Sociales", "icono": "bi-globe", "imagen": "campo-sociales.jpg",
     "descripcion": "El campo de Formación para la Construcción de Saberes Sociales integra las asignaturas de ciencias sociales, Filosofía, Ciencias Políticas y Económicas, y desde el año 2019 por acuerdo institucional religión y ética se fusionaron en la asignatura de Pensamiento y formación para la vida. Para desarrollar los procesos de enseñanza y aprendizaje se apoya en la Constitución Política de Colombia de 1991, en la Ley General de Educación 115, en los documentos del Ministerio de Educación Nacional (Ed. Básica y media), la Secretaria de Educación de Bogotá SED, en los Lineamientos y Estándares Curriculares, aprendizajes básicos, competencias para la vida UNESCO y los Objetivos de Desarrollo Sostenible, con el propósito de conocer, comprender, transformar realidades y tomar conciencia de su ser y de su entorno.De acuerdo con lo anterior, se requiere de la apropiación del conocimiento histórico, social, espacial y cultural que está en permanente dinamismo y cambio. Donde los/las estudiantes desde su contexto interpretan, intervienen y construyen una mejor sociedad como sujetos de derechos, deberes, creativos, transformadores y felices. Es así como la conciencia social le permite al individuo percibirse en sí mismo, en la sociedad y en el mundo, para fortalecer la construcción de trayectorias de vida, desde visiones pluri-paradigmáticas.",
     "imagen": "sede a 3.jpeg",
     "puntos": ["Historia y memoria colectiva", "Democracia participativa", "Diversidad cultural y ética", "Derechos humanos y ciudadanía"]},
    {"nombre": "Campo Matemático", "icono": "bi-calculator", "imagen": "campo-matematico.jpg",
     "descripcion": "Conformado por las asignaturas de matemáticas, desarrollo del pensamiento matemático y geométrico y Geometría. En la actualidad, es indiscutible el papel que desempeñan las matemáticas para la vida. Desde aspectos relacionados con el estudio de la ciencia, la tecnología, la biología, la medicina y la economía entre otras hasta la lectura e interpretación de distintos tipos de información que involucran modelos y representaciones matemáticas, es evidente la necesidad de formar ciudadanos competentes que puedan enfrentarse a una buena cantidad de tareas que requieren de la utilización de habilidades y conceptos matemáticos de diferentes tipos. Por otro lado, el desarrollo del pensamiento lógico le permite asumir retos actuales como son la complejidad de la vida, el trabajo en equipo, el tratamiento de conflictos, el manejo de la incertidumbre y el tratamiento de la cultura, para conseguir una vida sana.",
     "imagen": "sede a 4.jpeg",
     "puntos": ["Pensamiento lógico y abstracto", "Resolución de problemas reales", "Matemáticas para la vida cotidiana", "Estadística y análisis de datos"]},
    {"nombre": "Campo de la Comunicación", "icono": "bi-chat-square-text", "imagen": "campo-comunicacion.jpg",
     "descripcion": "Conformado por las asignaturas de Lengua Castellana, Idioma Extranjero y Lectoescritura. De acuerdo con la Ley General de Educación de 1994 en el artículo 23 de la Ley 115 para el logro de los objetivos de la educación básica se establece que, en el Plan de Estudios de Humanidades, debe incluir de lengua castellana e idioma extranjero como una de las áreas obligatorias y fundamentales del conocimiento y de la formación que necesariamente que se tendrán que ofrecer de acuerdo con el currículo y el Proyecto Educativo Institucional (PEI). El Campo de la Comunicación se fundamenta en la apropiación de los aprendizajes basados en el desarrollo de las habilidades para leer, escribir, escuchar y expresarse correctamente. El desarrollo de estas habilidades, permitirá que los estudiantes lleguen a ser capaces de comprender, analizar y valorar la información contenidas en diferentes tipos de textos y a su vez, facilitará que compartan sus ideas, sus experiencias, sus emociones y que estén en capacidad de defenderlas o debatirlas ante sus compañeros. La lectura, la escritura y la oralidad son aprendizajes fundamentales para el acceso a la cultura y al desarrollo de las demás competencias y saberes. Estos procesos van más allá de la simple decodificación y codificación de textos escritos u orales ya que permiten el surgimiento de hipótesis, interpretaciones, construcciones del mundo, experiencia y de expresiones por parte de los sujetos.",
     "imagen": "sede a 5.jpeg",
     "puntos": ["Lectura crítica y comprensiva", "Escritura creativa y argumentativa", "Segunda lengua — inglés", "Comunicación digital y medios"]},
    {"nombre": "Campo Científico-Tecnológico", "icono": "bi-cpu", "imagen": "campo-cientifico.jpg",
     "descripcion": "Conformado por las asignaturas ciencias naturales y educación ambiental, química, física y tecnología e informática. El área de tecnología e Informática en el colegio Julio Flórez pretende asumir y aplicar los avances tecnológicos y de las comunicaciones para relacionar el quehacer pedagógico con el mundo real del estudiante y con el sector social y productivo, busca potenciar en los estudiantes sus capacidades, garantizar la equidad para tener acceso a la información, proporcionándoles herramientas que les permita interactuar exitosamente en el ambiente tecnológico para alcanzar sus objetivos personales, educativos y de su sitio de trabajo.",
     "imagen": "sede a 2.jpeg",
     "puntos": ["Método científico y experimentación", "Tecnología e informática aplicada", "Ciencias naturales integradas", "Innovación y pensamiento de diseño"]},
    {"nombre": "Formación Especializada y Proyecto de Vida", "icono": "bi-compass", "imagen": "campo-proyecto-vida.jpg",
     "descripcion": "Conformado por las especialidades de Administración de Empresas, Administración Turística y Hotelera, Diseño e Integración de Multimedia, Manejo Ambiental y Programación de Software. La organización del campo de formación especializado permite una estructura curricular flexible de los programas de estudio de las especialidades, al ajustar sus componentes en varias posibilidades de desarrollo, permitiendo a los estudiantes y comunidad educativa, participar en la toma de decisiones sobre rutas de formación que respondan a las necesidades e intereses académicos de los estudiantes, con el propósito de generar una disminución en la deserción escolar. Las especialidades atienden expectativas del mercado de trabajo, al tomar como referente de elaboración los desempeños laborales de una función productiva, registrados en las normas de competencia, por lo que, contenidos, actividades y recursos didácticos se expresan en términos de competencias reconocidas por el sector productivo. Tales condiciones proponen un esquema de formación técnica integral, que permita el desarrollo de competencias en los estudiantes para su desempeño en la vida social en general y en las actividades laborales en particular.",
     "imagen": "bachillerato.jpeg",
     "puntos": ["Especialidad técnica articulada", "Orientación vocacional y profesional", "Emprendimiento e innovación", "Proyecto de vida y metas personales"]},
]

NOTICIAS_HOME = [
    {"categoria": "Orientación", "fecha": "3 de abril de 2026", "imagen": "comunidad 2.jpeg",
     "titulo": "Programa de Orientación Profesional (POP)", "resumen": "El Instituto Técnico Distrital Julio Flórez lanza su Programa de Orientación Prof..."},

    {"categoria": "Bienestar", "fecha": "2 de abril de 2026", "imagen": "noticia-donaton.jpg",
     "titulo": "Donatón: Tu Ayuda Alimenta Sonrisas", "resumen": "La comunidad educativa del Colegio Julio Flórez se une en una jornada solidaria de reco..."},

    {"categoria": "Institucional", "fecha": "15 de marzo de 2026", "imagen": "noticia-acreditacion.jpg",
     "titulo": "Acreditación de Excelencia en Gestión Educativa", "resumen": "El Instituto Técnico Distrital Julio Flórez recibe una nueva distinción en..."},
]

NOTICIAS = [
    dict(NOTICIAS_HOME[0], autor="Departamento de Orientación"),
    dict(NOTICIAS_HOME[1], autor="Comité de Bienestar"),
    dict(NOTICIAS_HOME[2], autor="Rectoría"),
]

EVENTOS_HOME = [
    {"mes": "JUN", "dia": "21", "categoria": "Institucional", "titulo": "Ceremonia de Izada de Bandera", "sede": "Ambas"},
    {"mes": "MAY", "dia": "10", "categoria": "Académico", "titulo": "Muestra de Especialidades Técnicas", "sede": "Sede A"},
    {"mes": "ABR", "dia": "15", "categoria": "Bienestar", "titulo": "Jornada de Donatón", "sede": "Ambas"},
]

EVENTOS = [
    {"mes": "JUN", "dia": "21", "categoria": "Institucional", "estado": "Programado", "titulo": "Ceremonia de Izada de Bandera",
     "descripcion": "Ceremonia institucional mensual de izada de bandera con reconocimientos académicos y deportivos a estudiantes destacados.",
     "fecha_completa": "21 de junio de 2026", "sede": "Ambas"},
    {"mes": "MAY", "dia": "10", "categoria": "Académico", "estado": "Programado", "titulo": "Muestra de Especialidades Técnicas",
     "descripcion": "Exposición de proyectos desarrollados por los estudiantes de las cuatro especialidades técnicas: Administración de Empresas, Programación de Software, Manejo Ambiental y Diseño e Integración Multimedial.",
     "fecha_completa": "10 de mayo de 2026", "sede": "Sede A"},
    {"mes": "ABR", "dia": "15", "categoria": "Bienestar", "estado": "Finalizado", "titulo": "Jornada de Donatón",
     "descripcion": "Jornada solidaria de recolección de alimentos para apoyar a familias en situación de vulnerabilidad de los barrios aledaños al colegio. Actividad del componente CAS del Programa IB.",
     "fecha_completa": "15 de abril de 2026", "sede": "Ambas"},
    {"mes": "ABR", "dia": "6", "categoria": "Académico", "estado": "Finalizado", "titulo": "Inicio de Clases — Año Escolar 2026",
     "descripcion": "Inicio oficial del año escolar 2026 para todos los estudiantes de la institución, desde grado Jardín hasta grado 11°.",
     "fecha_completa": "6 de abril de 2026", "sede": "Ambas"},
    {"mes": "MAR", "dia": "5", "categoria": "Académico", "estado": "Finalizado", "titulo": "Inscripciones Abiertas — Matrículas 2026",
     "descripcion": "Se abren las inscripciones para el proceso de matrícula del año escolar 2026. Los interesados pueden acercarse a las oficinas administrativas de ambas sedes o ingresar al sistema Edupage para diligenciar el formulario en línea.",
     "fecha_completa": "5 de marzo de 2026", "sede": "Ambas"},
]

GALERIA = (
    [f"images/actividades-{i}.jpeg" for i in range(1, 9)] +
    [f"imagenes_nuevas/comunidad n2-{i}.jpeg" for i in range(9, 17)]
)

PERFIL_IB = [
    {"nombre": "Indagación", "icono": "bi-search", "desc": "Cultivamos nuestra curiosidad y desarrollamos habilidades de indagación e investigación. Aprendemos de manera autónoma y junto con otros, con entusiasmo, durante toda la vida."},
    {"nombre": "Conocimiento", "icono": "bi-book", "desc": "Desarrollamos y usamos nuestra comprensión conceptual explorando el conocimiento en diversas disciplinas, comprometiéndonos con ideas y cuestiones de importancia local y mundial."},
    {"nombre": "Razonamiento", "icono": "bi-lightbulb", "desc": "Utilizamos el pensamiento crítico y creativo para analizar y actuar de manera responsable ante problemas complejos, tomando decisiones razonadas y éticas."},
    {"nombre": "Comunicación", "icono": "bi-chat-dots", "desc": "Nos expresamos con confianza y creatividad en diversas lenguas y maneras, colaborando eficazmente y escuchando las perspectivas de otras personas."},
    {"nombre": "Integridad", "icono": "bi-shield-check", "desc": "Actuamos con integridad y honradez, con un profundo sentido de la equidad y respeto por la dignidad de las personas, asumiendo la responsabilidad de nuestros actos."},
    {"nombre": "Mentalidad Abierta", "icono": "bi-globe2", "desc": "Desarrollamos una apreciación crítica de nuestra propia cultura e historia personal, así como de los valores y tradiciones de los demás, considerando distintos puntos de vista."},
    {"nombre": "Solidaridad", "icono": "bi-heart", "desc": "Mostramos empatía, sensibilidad y respeto, comprometiéndonos a ayudar a los demás e influir positivamente en las personas y el mundo que nos rodea."},
    {"nombre": "Audacia", "icono": "bi-lightning-charge", "desc": "Abordamos la incertidumbre con previsión y determinación, trabajando de forma autónoma y colaborativa para explorar nuevas ideas con ingenio y resiliencia."},
    {"nombre": "Equilibrio", "icono": "bi-yin-yang", "desc": "Entendemos la importancia del equilibrio físico, mental y emocional para el bienestar propio y el de los demás, reconociendo nuestra interdependencia con el mundo."},
    {"nombre": "Reflexión", "icono": "bi-arrow-repeat", "desc": "Evaluamos detenidamente el mundo, nuestras ideas y experiencias, esforzándonos por comprender nuestras fortalezas y debilidades para nuestro desarrollo personal."},
]

HABILIDADES_IB = [
    {"nombre": "Liderazgo", "color": "#173a63"},
    {"nombre": "Servicio", "color": "#0f2e22"},
    {"nombre": "Pensamiento crítico", "color": "#173a63"},
    {"nombre": "Empatía y Solidaridad", "color": "#4a90d9"},
    {"nombre": "Mentalidad Internacional", "color": "#4a90d9"},
    {"nombre": "Investigación", "color": "#173a63"},
    {"nombre": "Trabajo colaborativo", "color": "#0f2e22"},
    {"nombre": "Innovación", "color": "#4a90d9"},
]

FAQ_PAGADURIA = [
    {"pregunta": "¿Cuáles son los medios de pago autorizados?",
     "respuesta": "La institución acepta pagos en efectivo en la caja de Pagaduría, transferencia bancaria a la cuenta autorizada y PSE a través del portal institucional. No se aceptan pagos a docentes o personal no autorizado."},
    {"pregunta": "¿Qué conceptos se cobran en Pagaduría?",
     "respuesta": "Derechos de matrícula, seguro estudiantil, materiales especiales de especialidad técnica y certificados con costo. La educación básica y media es gratuita según la política de gratuidad del Distrito."},
    {"pregunta": "¿Cómo obtengo un certificado de matrícula o notas?",
     "respuesta": "Los certificados se solicitan en la secretaría académica o en Pagaduría. El trámite tiene un plazo de 3 días hábiles. Algunos certificados pueden tener un costo según el tipo y número de copias."},
    {"pregunta": "¿Existe la posibilidad de acuerdos de pago?",
     "respuesta": "Sí. En caso de dificultades económicas, las familias pueden solicitar una cita con la coordinación académica para gestionar un plan de pago o acceder a los apoyos de bienestar estudiantil."},
]

PASOS_MATRICULA = [
    {"titulo": "Revisión de requisitos", "descripcion": "Verifica que cumples con los requisitos de edad, nivel académico y documentación necesaria para el grado al que deseas ingresar."},
    {"titulo": "Diligenciamiento del formulario", "descripcion": "Completa el formulario de inscripción disponible en el sistema Edupage o en las oficinas administrativas de cualquiera de las dos sedes."},
    {"titulo": "Entrega de documentos", "descripcion": "Presenta los documentos requeridos en la secretaría académica de la sede correspondiente en los horarios establecidos."},
    {"titulo": "Entrevista y evaluación", "descripcion": "Para grados 10° y 11° con énfasis en IB, se realiza una entrevista de selección para conocer el perfil y expectativas del aspirante."},
    {"titulo": "Comunicación de resultados", "descripcion": "Recibirás notificación por correo electrónico sobre el estado de la solicitud de matrícula en un plazo de 5 días hábiles."},
    {"titulo": "Formalización de matrícula", "descripcion": "Una vez aceptado, realiza el proceso de formalización de matrícula y pago de derechos educativos en la Pagaduría."},
]

NIVELES_MATRICULA = [
    {"nombre": "Educación Inicial (Jardín y Transición)",
     "documentos": ["Registro civil de nacimiento", "Carné de vacunación actualizado", "Fotografías recientes 3x4", "Último informe o boletín de calificaciones (si aplica)"]},
    {"nombre": "Básica Primaria (1° a 5°)",
     "documentos": ["Registro civil de nacimiento", "Boletín final del año anterior", "Constancia de estudio o certificado", "Fotografías recientes 3x4"]},
    {"nombre": "Básica Secundaria (6° a 9°)",
     "documentos": ["Registro civil de nacimiento", "Tarjeta de identidad (si tiene)", "Boletín final del año anterior con notas", "Certificado de estudios con firma y sello"]},
    {"nombre": "Media Técnica (10° y 11°)",
     "documentos": ["Tarjeta de identidad", "Boletín del año anterior", "Certificado de estudios", "Fotografías 3x4", "Carta de motivación (para aspirantes al Programa IB)", "Entrevista de selección"]},
]

# ---- Organigrama institucional ----
COORDINACIONES = [
    {"cargo": "Coordinación Académica", "nombre": "Coordinador(a) Académico", "area": "Gestión pedagógica y curricular", "icono": "bi-journal-check"},
    {"cargo": "Coordinación de Convivencia", "nombre": "Coordinador(a) de Convivencia", "area": "Manual de Convivencia y disciplina", "icono": "bi-people-fill"},
    {"cargo": "Coordinación de Especialidades", "nombre": "Coordinador(a) de Especialidades", "area": "Programas técnicos SENA", "icono": "bi-tools"},
    {"cargo": "Coordinación IB", "nombre": "Coordinador(a) del Programa IB", "area": "Bachillerato Internacional", "icono": "bi-globe-americas"},
]

DOCENTES_ESPECIALIDAD = [
    {"nombre": "Docente — Administración de Empresas", "area": "Especialidad técnica", "icono": "bi-briefcase"},
    {"nombre": "Docente — Programación de Software", "area": "Especialidad técnica", "icono": "bi-code-slash"},
    {"nombre": "Docente — Manejo Ambiental", "area": "Especialidad técnica", "icono": "bi-tree"},
    {"nombre": "Docente — Diseño e Integración Multimedial", "area": "Especialidad técnica", "icono": "bi-palette"},
]

DOCENTES_CAMPOS = [
    {"nombre": "Docentes — Educación Inicial", "area": "Campo de Formación", "icono": "bi-flower1"},
    {"nombre": "Docentes — Saberes Sociales", "area": "Campo de Formación", "icono": "bi-globe"},
    {"nombre": "Docentes — Campo Matemático", "area": "Campo de Formación", "icono": "bi-calculator"},
    {"nombre": "Docentes — Comunicación", "area": "Campo de Formación", "icono": "bi-chat-square-text"},
    {"nombre": "Docentes — Científico-Tecnológico", "area": "Campo de Formación", "icono": "bi-cpu"},
]

# ---- Secciones de "Vida Escolar" (subpáginas dinámicas) ----'
VIDA_ESCOLAR = {
    "rutas": {
        "titulo": "Rutas y Transporte Escolar", "icono": "bi-bus-front", "color": "#0f2e22",
        "imagen": "JULITOS IB.jpg", "resumen": "Recorridos y horarios",
        "contenido": """
        <p>El servicio de transporte escolar está disponible para estudiantes que residen en zonas alejadas de las sedes del colegio. Este servicio es coordinado por la Secretaría de Educación del Distrito en articulación con la institución.</p>
        <p><strong>Rutas disponibles:</strong> Las rutas cubren los barrios de Usaquén, Santa Bárbara, Cedritos y zonas aledañas. El itinerario se actualiza cada semestre según la demanda.</p>
        <p><strong>Inscripción:</strong> Los padres o acudientes interesados deben acercarse a la coordinación en las dos primeras semanas del año escolar para solicitar el servicio. La asignación está sujeta a disponibilidad y priorización por distancia.</p>
        <p><strong>Normas:</strong> Los estudiantes deben estar en el punto de recogida 5 minutos antes de la hora indicada. El incumplimiento reiterado puede resultar en la pérdida del beneficio.</p>
        """
    },
    "alimentacion": {
        "titulo": "Alimentación / Comedor Escolar", "icono": "bi-cup-hot", "color": "#c0392b",
        "imagen": "IMG_4935.JPG", "resumen": "Servicio de restaurante",
        "contenido": """
        <p>El programa de alimentación escolar hace parte de la política de bienestar del Distrito. La institución ofrece refrigerio y almuerzo caliente a los estudiantes que participan en el programa PAE (Programa de Alimentación Escolar).</p>
        <p><strong>Beneficiarios:</strong> Estudiantes matriculados que se encuentren en la jornada completa y que cumplan con los criterios de vulnerabilidad del SIMAT.</p>
        <p><strong>Horario del comedor:</strong> Lunes a viernes — Refrigerio: 9:30 a.m. / Almuerzo: 12:00 m.</p>
        <p><strong>Inscripción al PAE:</strong> El proceso de inscripción se realiza a través de la secretaría académica al inicio del año escolar.</p>
        """
    },
    "horarios": {
        "titulo": "Horarios", "icono": "bi-clock", "color": "#0f2e22",
        "imagen": "IMG_9345.JPG", "resumen": "Jornadas escolares",
        "contenido": """
        <p><strong>Jornada Única:</strong> El Instituto Técnico Distrital Julio Flórez opera en jornada única.</p>
        <p><strong>Horario general:</strong></p>
        <ul>
          <li>Ingreso: 6:15 a.m.</li>
          <li>Primer bloque: 6:30 – 8:10 a.m.</li>
          <li>Segundo bloque: 8:10 – 10:05 a.m.</li>
          <li>Descanso: 10:05 – 10:30 a.m.</li>
          <li>Tercer bloque: 10:30 – 12:15 p.m.</li>
          <li>Almuerzo: 11:30 a.m. – 12:30 p.m.</li>
          <li>Tercer bloque: 12:30 – 2:30 p.m.</li>
          <li>Salida: 2:15 p.m.</li>
        </ul>
        <p><strong>Grados 10° y 11° IB:</strong> Pueden tener horario extendido hasta las 3:30 p.m. para actividades del Programa del Diploma.</p>
        <p><strong>Atención administrativa:</strong> Lunes a viernes de 7:00 a.m. a 4:00 p.m.</p>
        """
    },
    "coordinacion": {
        "titulo": "Coordinación", "icono": "bi-people", "color": "#c0392b",
        "imagen": "Julio Florez Poeta.png", "resumen": "Atención académica",
        "contenido": """
        <p>La coordinación académica y de convivencia acompaña a los estudiantes, familias y docentes en los procesos formativos y disciplinarios.</p>
        <p><strong>Coordinación Académica:</strong> Gestiona el proceso pedagógico, los resultados académicos, los planes de mejoramiento y la articulación con el Programa IB.</p>
        <p><strong>Coordinación de Convivencia:</strong> Atiende situaciones de convivencia, aplica el Manual de Convivencia y acompaña los procesos de resolución de conflictos desde el enfoque restaurativo.</p>
        <p><strong>Contacto:</strong> coordinacion@ejulioflorez.edu.co<br>
        <strong>Horario de atención a padres:</strong> Martes y jueves de 8:00 a.m. a 12:00 m. y de 2:00 p.m. a 4:00 p.m.</p>
        """
    },
    "padres": {
        "titulo": "Atención a Padres de Familia", "icono": "bi-journal-text", "color": "#0f2e22",
        "imagen": "image7.jpg", "resumen": "Canales de comunicación",
        "contenido": """
        <p>El colegio tiene un compromiso con la participación activa de las familias en el proceso educativo. Los canales de comunicación y atención son:</p>
        <p><strong>Docentes por asignatura:</strong> Los padres pueden solicitar cita directamente con el docente a través de la agenda escolar o la plataforma Edupage.</p>
        <p><strong>Reuniones de padres:</strong> Se realizan cuatro reuniones generales por año (bimestrales), más reuniones específicas cuando la situación lo requiera.</p>
        <p><strong>Consejo de Padres:</strong> Órgano representativo de las familias. Las elecciones se realizan en el primer mes del año escolar.</p>
        <p><strong>Orientación escolar:</strong> Atención a familias con estudiantes que requieren apoyo psicosocial o académico especial. Contacto: orientacion@ejulioflorez.edu.co</p>
        """
    },
    "informacion": {
        "titulo": "Información Importante", "icono": "bi-info-circle", "color": "#c0392b",
        "imagen": "actividades.jpeg", "resumen": "Normativas y políticas",
        "contenido": """
        <p><strong>Política de puertas:</strong> Por seguridad, no se permite el ingreso de estudiantes después de las 6:45 a.m. sin justificación. Los padres deben comunicar las ausencias antes de las 7:00 a.m.</p>
        <p><strong>Comunicados:</strong> Los comunicados oficiales se envían por Edupage y se publican en el tablero de avisos de cada sede. No se reconocen comunicados enviados por medios no oficiales.</p>
        <p><strong>Gobierno Escolar:</strong> El Personero Estudiantil y el Consejo de Estudiantes son elegidos anualmente. Toda la comunidad puede postularse y participar.</p>
        <p><strong>Atención médica:</strong> La institución cuenta con servicio de enfermería básica. En caso de urgencia, se contactará a los padres y se activará el protocolo de emergencias médicas.</p>
        <p><strong>Red de apoyo:</strong> En casos de vulnerabilidad económica, psicosocial o familiar, contáctese con Orientación Escolar.</p>
        """
    },
}

# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

@app.route("/")
def inicio():
    return render_template(
        "pagina/index.html",
        especialidades=ESPECIALIDADES,
        campos_home=CAMPOS_HOME,
        noticias_home=log_noticia.listar_publicadas()[:3],
        eventos_home=log_evento.listar_publicados()[:3],
    )


@app.route("/nuestra-institucion")
def nuestra_institucion():
    return redirect(url_for("nuestra_institucion_seccion", seccion="historia"))


@app.route("/nuestra-institucion/<seccion>")
def nuestra_institucion_seccion(seccion):
    info = NUESTRA_INSTITUCION_SECCIONES.get(seccion)
    if not info:
        return redirect(url_for("nuestra_institucion_seccion", seccion="historia"))
    return render_template(
        NUESTRA_INSTITUCION_TEMPLATES[seccion],
        info=info,
        seccion_actual=seccion,
        secciones=NUESTRA_INSTITUCION_SECCIONES,
        hitos=HITOS,
    )


@app.route("/especialidades")
def especialidades():    
    # Especialidades ahora vive dentro de Bachillerato Internacional
    # como "Estudios de Formación Profesional". Mantenemos esta ruta
    # como redirect por si alguien tiene el link viejo guardado.
    return redirect(url_for("bachillerato_seccion", seccion="estudios-formacion"), code=301)


@app.route("/Bachillerato/_subnav")
def bachillerato_internacional():
    # Punto de entrada: redirige siempre a la primera sección
    return redirect(url_for("bachillerato_seccion", seccion="que-es-ib"))


@app.route("/bachillerato-internacional/<seccion>")
def bachillerato_seccion(seccion):
    info = BACHILLERATO_SECCIONES.get(seccion)
    if not info:
        return redirect(url_for("bachillerato_seccion", seccion="que-es-ib"))
    return render_template(
        BACHILLERATO_TEMPLATES[seccion],
        info=info,
        seccion_actual=seccion,
        secciones=BACHILLERATO_SECCIONES,
        perfil_ib=PERFIL_IB,
        habilidades_ib=HABILIDADES_IB,
        especialidades=ESPECIALIDADES,
        asignaturas_pd=ASIGNATURAS_PD,
        componentes_troncales=COMPONENTES_TRONCALES_POP,
    )


@app.route("/campos-de-formacion")
def campos_formacion():
    return render_template("pagina/campos_formacion.html", campos=CAMPOS)


@app.route("/noticias")
def noticias():
    return render_template("pagina/noticias.html", noticias=log_noticia.listar_publicadas())


@app.route("/eventos")
def eventos():
    return render_template("pagina/eventos.html", eventos=log_evento.listar_publicados())


@app.route("/galeria")
def galeria():
    return render_template("pagina/galeria.html", galeria=GALERIA)


@app.route("/logros")
def logros():
    return render_template("pagina/logros.html", logros=log_logro.listar_publicados())


@app.route("/organigrama")
def organigrama():
    return render_template(
        "pagina/organigrama.html",
        coordinaciones=COORDINACIONES,
        docentes_especialidad=DOCENTES_ESPECIALIDAD,
        docentes_campos=DOCENTES_CAMPOS,
    )


@app.route("/secretaria")
def secretaria():
    return render_template("pagina/secretaria.html")


@app.route("/orientacion")
def orientacion():
    return render_template("pagina/orientacion.html")


@app.route("/vida-escolar/<seccion>")
def vida_escolar(seccion):
    info = VIDA_ESCOLAR.get(seccion)
    if not info:
        return redirect(url_for("nuestra_institucion"))
    return render_template(
        "pagina/vida_escolar.html",
        info=info,
        secciones=VIDA_ESCOLAR,
        seccion_actual=seccion,
    )


@app.route("/servicios/pagaduria")
def pagaduria():
    return render_template(
        "pagina/pagaduria.html",
        faq=FAQ_PAGADURIA,
        conceptos=log_pago.listar_conceptos_activos(),
    )


@app.route("/servicios/archivo")
def archivo():
    return render_template("pagina/archivo.html")


@app.route("/servicios/biblioteca")
def biblioteca():
    return render_template("pagina/biblioteca.html", libros=log_libro.listar())


@app.route("/matriculas")
def matriculas():
    return render_template(
        "pagina/matriculas.html",
        pasos_matricula=PASOS_MATRICULA,
        niveles_matricula=NIVELES_MATRICULA,
    )


@app.route("/pqr", methods=["GET", "POST"])
def pqr():
    if request.method == "POST":
        # Aquí guardarías la solicitud en tu base de datos (carpeta /modelo)
        flash("Tu solicitud PQR fue radicada correctamente. Te responderemos en máximo 15 días hábiles.")
        return redirect(url_for("pqr"))
    return render_template("pagina/pqr.html")


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        flash("Tu mensaje fue enviado. Gracias por contactarnos.")
        return redirect(url_for("contacto"))
    return render_template("pagina/contacto.html")


# =========================================================
# PANEL ADMINISTRATIVO
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        fila = log_usuario.verificar_credenciales(usuario, password)
        if fila:
            session["admin_id"] = fila["id"]
            session["admin_nombre"] = fila["nombre"]
            session["admin_rol"] = fila["rol"]
            return redirect(url_for("admin_dashboard"))
        flash("Usuario o contraseña incorrectos.", "error")
    return render_template("inicio_sesion/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_requerido
def admin_dashboard():
    rol = session.get("admin_rol")
    acceso_total = rol in ("admin", "rector")
    return render_template(
        "admin/dashboard.html",
        activo="dashboard",
        rol=rol,
        ver_noticias=acceso_total or rol == "secretaria",
        ver_eventos=acceso_total or rol == "secretaria",
        ver_logros=acceso_total or rol == "secretaria",
        ver_biblioteca=acceso_total,
        ver_pagaduria=acceso_total or rol == "pagaduria",
        total_noticias=len(log_noticia.listar_todas()),
        total_eventos=len(log_evento.listar_todos()),
        total_logros=len(log_logro.listar_todos()),
        total_libros=len(log_libro.listar()),
        total_conceptos=len(log_pago.listar_conceptos()),
    )

# ---- Control de acceso por ROL ----
# admin y rector -> acceso total (todas las secciones)
# secretaria     -> solo noticias y eventos
# pagaduria      -> solo pagaduría
SECCIONES_POR_ROL = {
    "noticias": ["admin", "rector", "secretaria"],
    "eventos": ["admin", "rector", "secretaria"],
    "logros": ["admin", "rector", "secretaria"],
    "biblioteca": ["admin", "rector"],
    "pagaduria": ["admin", "rector", "pagaduria"],
}


@app.before_request
def verificar_permisos_por_rol():
    ruta = request.path
    if not ruta.startswith("/admin/") and ruta != "/admin":
        return  # ruta pública, no aplica control de roles

    if ruta == "/admin/login" or ruta == "/admin/logout":
        return  # login/logout siempre accesibles

    if not session.get("admin_id"):
        flash("Debes iniciar sesión para acceder al panel administrativo.", "error")
        return redirect(url_for("admin_login"))

    rol = session.get("admin_rol")
    if rol in ("admin", "rector"):
        return  # acceso total, sin restricciones

    for seccion, roles_permitidos in SECCIONES_POR_ROL.items():
        if ruta.startswith(f"/admin/{seccion}"):
            if rol not in roles_permitidos:
                flash("No tienes permisos para acceder a esta sección.", "error")
                return redirect(url_for("admin_dashboard"))
            return
    # rutas admin genéricas (ej. /admin dashboard) -> cualquier rol logueado entra
    return

# ---------------- NOTICIAS ----------------

@app.route("/admin/noticias")
@login_requerido
def admin_noticias():
    return render_template("admin/noticias_lista.html", activo="noticias", noticias=log_noticia.listar_todas())


@app.route("/admin/noticias/nueva", methods=["GET", "POST"])
@login_requerido
def admin_noticia_nueva():
    if request.method == "POST":
        imagen = guardar_imagen_subida(request.files.get("imagen_archivo")) or "placeholder.jpg"
        log_noticia.crear({
            "titulo": request.form["titulo"], "categoria": request.form["categoria"],
            "resumen": request.form["resumen"], "contenido": request.form.get("contenido", ""),
            "autor": request.form.get("autor", ""), "imagen": imagen,
            "fecha": request.form["fecha"], "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Noticia creada y publicada correctamente.")
        return redirect(url_for("admin_noticias"))
    return render_template("admin/noticias_form.html", activo="noticias", noticia=None)


@app.route("/admin/noticias/<int:id_noticia>/editar", methods=["GET", "POST"])
@login_requerido
def admin_noticia_editar(id_noticia):
    noticia = log_noticia.obtener(id_noticia)
    if not noticia:
        flash("Noticia no encontrada.", "error")
        return redirect(url_for("admin_noticias"))
    if request.method == "POST":
        imagen_nueva = guardar_imagen_subida(request.files.get("imagen_archivo"))
        log_noticia.actualizar(id_noticia, {
            "titulo": request.form["titulo"], "categoria": request.form["categoria"],
            "resumen": request.form["resumen"], "contenido": request.form.get("contenido", ""),
            "autor": request.form.get("autor", ""), "imagen": imagen_nueva or noticia["imagen"],
            "fecha": request.form["fecha"], "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Noticia actualizada correctamente.")
        return redirect(url_for("admin_noticias"))
    return render_template("admin/noticias_form.html", activo="noticias", noticia=noticia)


@app.route("/admin/noticias/<int:id_noticia>/eliminar", methods=["POST"])
@login_requerido
def admin_noticia_eliminar(id_noticia):
    log_noticia.eliminar(id_noticia)
    flash("Noticia eliminada.")
    return redirect(url_for("admin_noticias"))


# ---------------- EVENTOS ----------------

@app.route("/admin/eventos")
@login_requerido
def admin_eventos():
    return render_template("admin/eventos_lista.html", activo="eventos", eventos=log_evento.listar_todos())


@app.route("/admin/eventos/nuevo", methods=["GET", "POST"])
@login_requerido
def admin_evento_nuevo():
    if request.method == "POST":
        log_evento.crear({
            "titulo": request.form["titulo"], "categoria": request.form["categoria"],
            "estado": request.form["estado"], "descripcion": request.form["descripcion"],
            "fecha_completa": request.form["fecha_completa"], "mes": request.form["mes"].upper(),
            "dia": request.form["dia"], "sede": request.form["sede"],
            "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Evento creado y publicado correctamente.")
        return redirect(url_for("admin_eventos"))
    return render_template("admin/eventos_form.html", activo="eventos", evento=None)


@app.route("/admin/eventos/<int:id_evento>/editar", methods=["GET", "POST"])
@login_requerido
def admin_evento_editar(id_evento):
    evento = log_evento.obtener(id_evento)
    if not evento:
        flash("Evento no encontrado.", "error")
        return redirect(url_for("admin_eventos"))
    if request.method == "POST":
        log_evento.actualizar(id_evento, {
            "titulo": request.form["titulo"], "categoria": request.form["categoria"],
            "estado": request.form["estado"], "descripcion": request.form["descripcion"],
            "fecha_completa": request.form["fecha_completa"], "mes": request.form["mes"].upper(),
            "dia": request.form["dia"], "sede": request.form["sede"],
            "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Evento actualizado correctamente.")
        return redirect(url_for("admin_eventos"))
    return render_template("admin/eventos_form.html", activo="eventos", evento=evento)


@app.route("/admin/eventos/<int:id_evento>/eliminar", methods=["POST"])
@login_requerido
def admin_evento_eliminar(id_evento):
    log_evento.eliminar(id_evento)
    flash("Evento eliminado.")
    return redirect(url_for("admin_eventos"))


# ---------------- LOGROS Y RECONOCIMIENTOS ----------------

@app.route("/admin/logros")
@login_requerido
def admin_logros():
    return render_template("admin/logros_lista.html", activo="logros", logros=log_logro.listar_todos())


@app.route("/admin/logros/nuevo", methods=["GET", "POST"])
@login_requerido
def admin_logro_nuevo():
    if request.method == "POST":
        imagen = guardar_imagen_subida(request.files.get("imagen_archivo")) or "placeholder.jpg"
        log_logro.crear({
            "nombre": request.form["nombre"], "categoria": request.form["categoria"],
            "titulo_logro": request.form["titulo_logro"], "descripcion": request.form["descripcion"],
            "grado": request.form.get("grado", ""), "imagen": imagen,
            "fecha": request.form["fecha"], "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Logro creado y publicado correctamente.")
        return redirect(url_for("admin_logros"))
    return render_template("admin/logros_form.html", activo="logros", logro=None)


@app.route("/admin/logros/<int:id_logro>/editar", methods=["GET", "POST"])
@login_requerido
def admin_logro_editar(id_logro):
    logro = log_logro.obtener(id_logro)
    if not logro:
        flash("Logro no encontrado.", "error")
        return redirect(url_for("admin_logros"))
    if request.method == "POST":
        imagen_nueva = guardar_imagen_subida(request.files.get("imagen_archivo"))
        log_logro.actualizar(id_logro, {
            "nombre": request.form["nombre"], "categoria": request.form["categoria"],
            "titulo_logro": request.form["titulo_logro"], "descripcion": request.form["descripcion"],
            "grado": request.form.get("grado", ""), "imagen": imagen_nueva or logro["imagen"],
            "fecha": request.form["fecha"], "publicado": 1 if request.form.get("publicado") else 0,
        })
        flash("Logro actualizado correctamente.")
        return redirect(url_for("admin_logros"))
    return render_template("admin/logros_form.html", activo="logros", logro=logro)


@app.route("/admin/logros/<int:id_logro>/eliminar", methods=["POST"])
@login_requerido
def admin_logro_eliminar(id_logro):
    log_logro.eliminar(id_logro)
    flash("Logro eliminado.")
    return redirect(url_for("admin_logros"))


# ---------------- BIBLIOTECA ----------------

@app.route("/admin/biblioteca", methods=["GET", "POST"])
@login_requerido
def admin_biblioteca():
    if request.method == "POST":
        log_libro.crear({
            "titulo": request.form["titulo"], "autor": request.form["autor"],
            "categoria": request.form.get("categoria", ""), "grado": request.form.get("grado", ""),
            "cantidad_total": int(request.form["cantidad_total"]),
        })
        flash("Libro agregado al catálogo.")
        return redirect(url_for("admin_biblioteca"))
    return render_template(
        "admin/biblioteca_lista.html", activo="biblioteca",
        libros=log_libro.listar(), prestamos=log_libro.listar_prestamos_activos(),
    )


@app.route("/admin/biblioteca/<int:id_libro>/editar", methods=["POST"])
@login_requerido
def admin_biblioteca_editar(id_libro):
    log_libro.actualizar(id_libro, {
        "titulo": request.form["titulo"], "autor": request.form["autor"],
        "categoria": request.form.get("categoria", ""), "grado": request.form.get("grado", ""),
        "cantidad_total": int(request.form["cantidad_total"]),
        "cantidad_disponible": int(request.form["cantidad_disponible"]),
    })
    flash("Libro actualizado correctamente.")
    return redirect(url_for("admin_biblioteca"))


@app.route("/admin/biblioteca/<int:id_libro>/eliminar", methods=["POST"])
@login_requerido
def admin_biblioteca_eliminar(id_libro):
    log_libro.eliminar(id_libro)
    flash("Libro eliminado del catálogo.")
    return redirect(url_for("admin_biblioteca"))


@app.route("/admin/biblioteca/prestamos/<int:id_prestamo>/devolver", methods=["POST"])
@login_requerido
def admin_biblioteca_devolver(id_prestamo):
    log_libro.marcar_devuelto(id_prestamo)
    flash("Préstamo marcado como devuelto.")
    return redirect(url_for("admin_biblioteca"))


# ---------------- PAGADURÍA ----------------

@app.route("/admin/pagaduria", methods=["GET", "POST"])
@login_requerido
def admin_pagaduria():
    if request.method == "POST":
        log_pago.crear_concepto({
            "nombre": request.form["nombre"], "valor": int(request.form["valor"]),
            "obligatorio": 1 if request.form.get("obligatorio") else 0,
            "descripcion": request.form.get("descripcion", ""), "activo": 1,
        })
        flash("Concepto de pago agregado.")
        return redirect(url_for("admin_pagaduria"))
    return render_template(
        "admin/pagaduria_lista.html", activo="pagaduria",
        conceptos=log_pago.listar_conceptos(), pagos=log_pago.listar_pagos(),
    )


@app.route("/admin/pagaduria/<int:id_concepto>/editar", methods=["POST"])
@login_requerido
def admin_pagaduria_editar(id_concepto):
    log_pago.actualizar_concepto(id_concepto, {
        "nombre": request.form["nombre"], "valor": int(request.form["valor"]),
        "obligatorio": 1 if request.form.get("obligatorio") else 0,
        "descripcion": request.form.get("descripcion", ""),
        "activo": 1 if request.form.get("activo") else 0,
    })
    flash("Concepto actualizado correctamente.")
    return redirect(url_for("admin_pagaduria"))


@app.route("/admin/pagaduria/<int:id_concepto>/eliminar", methods=["POST"])
@login_requerido
def admin_pagaduria_eliminar(id_concepto):
    log_pago.eliminar_concepto(id_concepto)
    flash("Concepto eliminado.")
    return redirect(url_for("admin_pagaduria"))


if __name__ == "__main__":
    app.run(debug=True)

