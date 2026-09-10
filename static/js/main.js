// Instituto Técnico Distrital Julio Flórez — script principal

document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.navbar-institucional');

  // Sombra en el navbar al hacer scroll
  window.addEventListener('scroll', () => {
    if (!nav) return;
    if (window.scrollY > 10) {
      nav.style.boxShadow = '0 4px 14px rgba(0,0,0,.15)';
    } else {
      nav.style.boxShadow = 'none';
    }
  });

  // Resaltar el enlace del menú correspondiente a la página actual
  const rutaActual = window.location.pathname;
  document.querySelectorAll('.navbar-institucional .nav-link').forEach(link => {
    if (link.getAttribute('href') === rutaActual) {
      link.classList.add('active');
    }
  });
});
