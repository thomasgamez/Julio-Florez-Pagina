// Agrega el código de seguridad (CSRF) a todos los formularios POST de la página.
document.addEventListener('DOMContentLoaded', () => {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (!meta) return;
  document.querySelectorAll('form').forEach(form => {
    if ((form.getAttribute('method') || '').toUpperCase() !== 'POST') return;
    const campo = document.createElement('input');
    campo.type = 'hidden';
    campo.name = 'csrf_token';
    campo.value = meta.content;
    form.appendChild(campo);
  });
});