(function () {
  'use strict';

  function createLightbox() {
    const root = document.createElement('div');
    root.id = 'lightbox';
    root.className = 'lightbox';
    root.hidden = true;
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML =
      '<div class="lightbox-backdrop" data-lightbox-close tabindex="-1"></div>' +
      '<div class="lightbox-panel" role="dialog" aria-modal="true" aria-label="Увеличенный просмотр">' +
        '<button type="button" class="lightbox-close" data-lightbox-close aria-label="Закрыть">&times;</button>' +
        '<p class="lightbox-caption" hidden></p>' +
        '<div class="lightbox-body"></div>' +
      '</div>';
    document.body.appendChild(root);
    return root;
  }

  const lightbox = document.getElementById('lightbox') || createLightbox();
  const body = lightbox.querySelector('.lightbox-body');
  const caption = lightbox.querySelector('.lightbox-caption');
  let lastFocus = null;

  function setCaption(text) {
    if (!text) {
      caption.hidden = true;
      caption.textContent = '';
      return;
    }
    caption.hidden = false;
    caption.textContent = text;
  }

  function open(render, title) {
    lastFocus = document.activeElement;
    body.innerHTML = '';
    setCaption(title || '');
    render(body);
    lightbox.hidden = false;
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lightbox-open');
    lightbox.querySelector('.lightbox-close').focus();
  }

  function close() {
    lightbox.hidden = true;
    lightbox.setAttribute('aria-hidden', 'true');
    body.innerHTML = '';
    setCaption('');
    document.body.classList.remove('lightbox-open');
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  lightbox.addEventListener('click', function (e) {
    if (e.target.closest('[data-lightbox-close]')) close();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !lightbox.hidden) close();
  });

  function bindZoomable(el, onOpen) {
    el.classList.add('zoomable');
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    if (!el.getAttribute('title')) el.setAttribute('title', 'Нажмите для увеличения');

    function activate(e) {
      if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return;
      if (e.type === 'keydown') e.preventDefault();
      if (e.target.closest('a, button')) return;
      onOpen();
    }

    el.addEventListener('click', activate);
    el.addEventListener('keydown', activate);
  }

  document.querySelectorAll('img.chart').forEach(function (img) {
    if (!img.nextElementSibling?.classList.contains('chart-hint')) {
      const hint = document.createElement('span');
      hint.className = 'chart-hint';
      hint.textContent = '🔍  Нажмите на диаграмму для увеличения';
      img.insertAdjacentElement('afterend', hint);
    }
    bindZoomable(img, function () {
      const alt = img.getAttribute('alt') || 'Диаграмма';
      open(function (container) {
        const full = document.createElement('img');
        full.src = img.currentSrc || img.src;
        full.alt = alt;
        full.className = 'lightbox-chart';
        full.decoding = 'async';
        container.appendChild(full);
      }, alt);
    });
  });

  document.querySelectorAll('.table-wrap').forEach(function (wrap) {
    bindZoomable(wrap, function () {
      const heading = wrap.closest('section')?.querySelector('h2, h3');
      const title = heading ? heading.textContent.replace(/\s+/g, ' ').trim() : 'Таблица';
      open(function (container) {
        const clone = wrap.cloneNode(true);
        clone.classList.remove('zoomable');
        clone.removeAttribute('role');
        clone.removeAttribute('tabindex');
        clone.removeAttribute('title');
        clone.classList.add('lightbox-table-wrap');
        container.appendChild(clone);
      }, title);
    });
  });

  document.querySelectorAll('.donut-card').forEach(function (card) {
    bindZoomable(card, function () {
      open(function (container) {
        const clone = card.cloneNode(true);
        clone.classList.remove('zoomable');
        clone.removeAttribute('role');
        clone.removeAttribute('tabindex');
        clone.removeAttribute('title');
        clone.classList.add('lightbox-donut');
        container.appendChild(clone);
      }, 'Диаграмма');
    });
  });
})();
