(function () {
  var datos = document.getElementById('editor-datos');
  if (!datos) return;

  // ---------- Estilos (van aquí dentro para que nunca queden desactualizados) ----------
  var estilo = document.createElement('style');
  estilo.textContent = `
    .ed-texto { cursor: pointer; }
    .ed-marco { position: absolute; z-index: 99998; pointer-events: none; border: 2px solid #3b82f6; background: rgba(59,130,246,.08); border-radius: 4px; }
    .ed-barra { position: absolute; z-index: 99999; display: flex; align-items: center; gap: 2px; background: #1b1b1b; color: #fff; padding: 4px 6px; border-radius: 8px; font: 500 13px system-ui, sans-serif; box-shadow: 0 6px 18px rgba(0,0,0,.35); white-space: nowrap; }
    .ed-etiqueta { padding: 0 8px; color: #9ca3af; }
    .ed-insignia { background: #d4af37; color: #151515; border-radius: 6px; padding: 1px 7px; font-size: 11px; font-weight: 700; margin-right: 4px; }
    .ed-barra button { background: transparent; color: #fff; border: 0; border-radius: 6px; padding: 5px 10px; font: inherit; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
    .ed-barra button:hover { background: #3a3a3a; }
    .ed-panel { position: absolute; z-index: 100000; background: #fff; color: #222; border: 2px solid #3b82f6; border-radius: 10px; padding: 10px; box-shadow: 0 16px 48px rgba(0,0,0,.3); font-family: system-ui, sans-serif; text-align: left; box-sizing: border-box; }
    .ed-rotulo { height: 16px; line-height: 16px; margin-bottom: 4px; font-size: 12px; color: #6b746f; font-weight: 600; }
    .ed-campo { display: block; width: 100%; box-sizing: border-box; padding: 8px 10px; border: 1px solid #cfd6d2; border-radius: 8px; font: 400 15px/1.5 system-ui, sans-serif; color: #222; background: #fff; resize: vertical; }
    .ed-campo:focus { outline: 2px solid #3b82f6; border-color: #3b82f6; }
    .ed-ayuda { font-size: 12px; color: #6b746f; margin-top: 6px; }
    .ed-original { margin-top: 8px; font-size: 13px; color: #6b746f; }
    .ed-original div { white-space: pre-line; margin-top: 4px; }
    .ed-botones { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
    .ed-botones button { border: 0; border-radius: 8px; padding: 7px 16px; font: 600 14px system-ui, sans-serif; cursor: pointer; }
    .ed-guardar { background: #0f2e22; color: #fff; }
    .ed-restaurar { background: #fff; color: #444; border: 1px solid #bbb !important; }
    .ed-cancelar { background: transparent; color: #666; }
    .ed-aviso { position: fixed; top: 16px; right: 16px; z-index: 100001; background: #0f2e22; color: #fff; padding: 10px 16px; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,.3); font: 500 14px system-ui, sans-serif; }
    .ed-aviso.error { background: #c0392b; }
  `;
  document.head.appendChild(estilo);

  var csrf = datos.dataset.csrf;
  var urls = { valor: datos.dataset.valor, guardar: datos.dataset.guardar, restaurar: datos.dataset.restaurar };
  var actual = null, temporizador = null, panel = null;

  function el(tag, clase, texto) {
    var e = document.createElement(tag);
    if (clase) e.className = clase;
    if (texto) e.textContent = texto;   // textContent: nunca interpreta HTML
    return e;
  }

  function aviso(texto, esError) {
    var a = el('div', 'ed-aviso' + (esError ? ' error' : ''), texto);
    document.body.appendChild(a);
    setTimeout(function () { a.remove(); }, 2800);
  }

  function enviar(url, campos) {
    var f = new FormData();
    f.append('csrf_token', csrf);
    Object.keys(campos).forEach(function (k) { f.append(k, campos[k]); });
    return fetch(url, { method: 'POST', body: f, credentials: 'same-origin' }).then(function (r) { return r.json(); });
  }

  function actualizarPagina(clave, r) {
    // El mismo texto puede estar en varios sitios (por ejemplo la resolución en la portada y en el pie)
    document.querySelectorAll('.ed-texto[data-clave="' + CSS.escape(clave) + '"]').forEach(function (n) {
      n.innerHTML = r.html;                         // el servidor ya lo entrega escapado
      n.dataset.editado = r.editado ? '1' : '0';
    });
  }

  // ---------- Recuadro y barra al pasar el cursor ----------
  var marco = el('div', 'ed-marco');
  var barra = el('div', 'ed-barra');
  marco.style.display = barra.style.display = 'none';
  document.body.appendChild(marco);
  document.body.appendChild(barra);

  function boton(icono, texto, accion) {
    var b = el('button');
    b.type = 'button';
    b.appendChild(el('i', 'bi ' + icono));
    b.appendChild(document.createTextNode(texto));
    b.addEventListener('click', accion);
    return b;
  }

  function ocultar() {
    marco.style.display = barra.style.display = 'none';
    actual = null;
  }

  function mostrarBarra(t) {
    actual = t;
    var r = t.getBoundingClientRect();
    var x = r.left + window.scrollX, y = r.top + window.scrollY;
    marco.style.display = 'block';
    marco.style.left = (x - 3) + 'px';
    marco.style.top = (y - 3) + 'px';
    marco.style.width = (r.width + 6) + 'px';
    marco.style.height = (r.height + 6) + 'px';

    barra.textContent = '';
    barra.appendChild(el('span', 'ed-etiqueta', t.dataset.tipo === 'parrafo' ? 'Párrafo' : 'Texto'));
    if (t.dataset.editado === '1') barra.appendChild(el('span', 'ed-insignia', 'Editado'));
    barra.appendChild(boton('bi-pencil', 'Editar', function () { abrir(t); }));
    if (t.dataset.editado === '1') {
      barra.appendChild(boton('bi-arrow-counterclockwise', 'Restaurar', function () { restaurar(t); }));
    }
    barra.style.display = 'flex';

    var alto = barra.offsetHeight;
    var cabeArriba = r.top - alto - 3 >= 0;
    barra.style.left = Math.max(4, x - 3) + 'px';
    barra.style.top = (cabeArriba ? y - alto - 3 : y + r.height + 3) + 'px';
  }

  document.addEventListener('mouseover', function (e) {
    if (panel) return;
    clearTimeout(temporizador);
    var t = e.target.closest('.ed-texto');
    if (t) { if (t !== actual) mostrarBarra(t); return; }
    if (e.target.closest('.ed-barra')) return;
    temporizador = setTimeout(ocultar, 120);
  });
  window.addEventListener('resize', ocultar);

  // ---------- Restaurar desde la barra ----------
  function restaurar(t) {
    if (!confirm('¿Volver al texto original?')) return;
    enviar(urls.restaurar, { clave: t.dataset.clave }).then(function (r) {
      if (r.ok) actualizarPagina(t.dataset.clave, r);
      ocultar();
      aviso(r.mensaje, !r.ok);
    }).catch(function () { aviso('No se pudo restaurar.', true); });
  }

  // ---------- Cuadro de edición: se abre encima del propio texto ----------
  function cerrarPanel() {
    if (panel) { panel.remove(); panel = null; }
  }

  function abrir(t) {
    var clave = t.dataset.clave;
    fetch(urls.valor + '?clave=' + encodeURIComponent(clave), { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok) mostrarPanel(t, clave, d);
        else aviso('Ese texto no se puede editar aquí.', true);
      })
      .catch(function () { aviso('No se pudo cargar el texto.', true); });
  }

  function mostrarPanel(t, clave, d) {
    cerrarPanel();
    ocultar();
    var r = t.getBoundingClientRect();

    panel = el('div', 'ed-panel');
    panel.appendChild(el('div', 'ed-rotulo', d.etiqueta));

    var campo;
    if (d.tipo === 'parrafo') {
      campo = el('textarea', 'ed-campo');
      campo.maxLength = 5000;
      campo.style.height = Math.min(Math.max(r.height + 24, 110), 340) + 'px';
    } else {
      campo = el('input', 'ed-campo');
      campo.type = 'text';
      campo.maxLength = 500;
    }
    campo.value = d.valor;
    panel.appendChild(campo);

    if (d.tipo === 'parrafo') {
      panel.appendChild(el('div', 'ed-ayuda', 'Para negrita escribe el texto entre dos asteriscos: **así**.'));
    }
    if (d.editado) {
      var det = el('details', 'ed-original');
      det.appendChild(el('summary', '', 'Ver texto original'));
      det.appendChild(el('div', '', d.base));
      panel.appendChild(det);
    }

    var botones = el('div', 'ed-botones');
    var guardar = el('button', 'ed-guardar', 'Guardar');
    guardar.type = 'button';
    guardar.onclick = function () {
      enviar(urls.guardar, { clave: clave, valor: campo.value }).then(function (res) {
        if (res.ok) { actualizarPagina(clave, res); cerrarPanel(); }
        aviso(res.mensaje, !res.ok);
      }).catch(function () { aviso('No se pudo guardar. Recarga e intenta de nuevo.', true); });
    };
    botones.appendChild(guardar);

    if (d.editado) {
      var rest = el('button', 'ed-restaurar', 'Restaurar original');
      rest.type = 'button';
      rest.onclick = function () {
        if (!confirm('¿Volver al texto original?')) return;
        enviar(urls.restaurar, { clave: clave }).then(function (res) {
          if (res.ok) { actualizarPagina(clave, res); cerrarPanel(); }
          aviso(res.mensaje, !res.ok);
        });
      };
      botones.appendChild(rest);
    }
    var cancelar = el('button', 'ed-cancelar', 'Cancelar');
    cancelar.type = 'button';
    cancelar.onclick = cerrarPanel;
    botones.appendChild(cancelar);
    panel.appendChild(botones);

    // Posición: el campo queda justo sobre el texto que tocaste
    var ancho = Math.min(Math.max(r.width + 22, 300), window.innerWidth - 16);
    var izq = Math.min(Math.max(8, r.left - 11), window.innerWidth - ancho - 8);
    panel.style.width = ancho + 'px';
    panel.style.left = (window.scrollX + izq) + 'px';
    panel.style.top = Math.max(window.scrollY + 4, window.scrollY + r.top - 32) + 'px';
    document.body.appendChild(panel);
    panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    campo.focus();
  }

  document.addEventListener('mousedown', function (e) {
    if (panel && !panel.contains(e.target)) cerrarPanel();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cerrarPanel();
  });

  // ---------- Clics: texto editable, enlaces y formularios ----------
  document.addEventListener('click', function (e) {
    var t = e.target.closest('.ed-texto');
    if (t) { e.preventDefault(); e.stopPropagation(); abrir(t); return; }

    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#' || /^javascript:/i.test(href)) return;   // menús desplegables y similares

    e.preventDefault();
    if (/^(mailto|tel):/i.test(href)) return;
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin) { aviso('Los enlaces externos están desactivados en el modo edición.'); return; }
    u.searchParams.set('editor', '1');   // sigue navegando dentro del modo edición
    location.href = u.href;
  }, true);

  document.addEventListener('submit', function (e) {
    e.preventDefault();
    aviso('Los formularios están desactivados en el modo edición.', true);
  }, true);
})();