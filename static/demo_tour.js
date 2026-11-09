/* Demo slides (templates/demo_slides.html), shown in a modal on the evaluation
 * page and the patient dashboard. Desktop/laptop only (the study runs on
 * intranet PCs). Scene attributes are documented in templates/demo/_macros.html. */
(function () {
  'use strict';

  var root = document.querySelector('.dt');
  if (!root) return;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FRAME_WIDTH = 1000;
  var CURSOR_TRAVEL_MS = 720;

  /* ── helpers ─────────────────────────────────────────────────────────── */

  function parseRanges(spec) {
    return String(spec).split(',').map(function (part) {
      var m = part.trim().match(/^(\d+)(-(\d*))?$/);
      if (!m) return null;
      var from = parseInt(m[1], 10);
      var to = m[2] ? (m[3] === '' ? Infinity : parseInt(m[3], 10)) : from;
      return [from, to];
    }).filter(Boolean);
  }

  function inRange(spec, scene) {
    return parseRanges(spec).some(function (r) { return scene >= r[0] && scene <= r[1]; });
  }

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  /* "2:42;5:" → value of the last key <= scene ('' if none) */
  function valueAt(spec, scene) {
    var value = '';
    var best = -1;
    String(spec).split(';').forEach(function (rule) {
      var parts = rule.split(':');
      var at = parseInt(parts[0], 10);
      if (!isNaN(at) && at <= scene && at > best) { best = at; value = (parts[1] || '').trim(); }
    });
    return value;
  }

  function all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* lets the evaluation page stop highlighting the demo button for this step */
  try {
    var seenKey = root.getAttribute('data-seen-key');
    if (seenKey) localStorage.setItem(seenKey, '1');
  } catch (e) {}

  /* ── stage engine ────────────────────────────────────────────────────── */

  var stage = root.querySelector('.dt-stage');
  if (!stage) return;
  var viewport = stage.querySelector('.dt-viewport');
  var frame = stage.querySelector('.dt-frame');
  var cursor = stage.querySelector('.dt-cursor');
  var chapters = all('.dt-chapter', root);
  var dots = all('.dt-scene-dot', root);
  var current = -1;
  var token = 0;
  var scale = 1;

  function applyScene(scene) {
    stage.setAttribute('data-scene', String(scene));

    all('[data-in]', stage).forEach(function (el) {
      var on = inRange(el.getAttribute('data-in'), scene);
      if (el.getAttribute('data-mode') === 'fade') {
        el.classList.toggle('dt-faded', !on);
      } else {
        el.classList.toggle('dt-off', !on);
      }
    });

    all('[data-cls]', stage).forEach(function (el) {
      el.getAttribute('data-cls').split(';').forEach(function (rule) {
        var idx = rule.indexOf(':');
        if (idx < 0) return;
        var range = rule.slice(0, idx).trim();
        var cls = rule.slice(idx + 1).trim();
        var invert = cls.charAt(0) === '!';
        if (invert) cls = cls.slice(1);
        var on = inRange(range, scene);
        el.classList.toggle(cls, invert ? !on : on);
      });
    });

    all('[data-check]', stage).forEach(function (el) {
      el.checked = inRange(el.getAttribute('data-check'), scene);
    });

    all('[data-vas]', stage).forEach(function (bar) {
      var value = valueAt(bar.getAttribute('data-vas'), scene);
      var fill = bar.querySelector('.vas8-fill');
      var thumb = bar.querySelector('.vas8-thumb');
      if (value === '') {
        if (fill) fill.style.width = '0%';
        if (thumb) thumb.style.display = 'none';
      } else {
        if (fill) fill.style.width = value + '%';
        if (thumb) { thumb.style.left = value + '%'; thumb.style.display = 'block'; }
      }
    });

    all('[data-width]', stage).forEach(function (el) {
      el.style.width = (valueAt(el.getAttribute('data-width'), scene) || '0') + '%';
    });

    chapters.forEach(function (ch, i) { ch.classList.toggle('is-active', i === scene); });
    dots.forEach(function (d, i) {
      d.classList.toggle('is-active', i === scene);
      d.setAttribute('aria-selected', i === scene ? 'true' : 'false');
    });
  }

  function cursorTarget(scene) {
    var click = all('[data-cursor]', stage).filter(function (el) {
      return inRange(el.getAttribute('data-cursor'), scene);
    })[0];
    if (click) return { el: click, click: true };
    var hover = all('[data-cursor-hover]', stage).filter(function (el) {
      return inRange(el.getAttribute('data-cursor-hover'), scene);
    })[0];
    return hover ? { el: hover, click: false } : null;
  }

  function isRendered(el) {
    var r = el.getBoundingClientRect();
    return r.width > 0 || r.height > 0;
  }

  function moveCursor(target, animate) {
    if (!cursor) return;
    if (!target || reduceMotion) { cursor.classList.remove('is-on'); return; }
    var sr = stage.getBoundingClientRect();
    var tr = target.el.getBoundingClientRect();
    var x = tr.left - sr.left + tr.width / 2;
    var y = tr.top - sr.top + tr.height / 2;
    cursor.classList.toggle('dt-cursor--instant', !animate);
    cursor.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
    cursor.classList.add('is-on');
  }

  function clickCursor() {
    if (!cursor) return;
    cursor.classList.remove('is-click');
    void cursor.offsetWidth;
    cursor.classList.add('is-click');
  }

  function goTo(scene) {
    if (scene === current) return;
    var prev = current;
    current = scene;
    var myToken = ++token;
    var target = cursorTarget(scene);
    var stepForward = prev >= 0 && scene === prev + 1 && !reduceMotion;

    if (!target || !stepForward) {
      applyScene(scene);
      moveCursor(cursorTarget(scene), prev >= 0);
      return;
    }

    // Element might only become visible in this scene; lay it out first if so.
    if (!isRendered(target.el)) applyScene(scene);
    moveCursor(target, true);
    window.setTimeout(function () {
      if (myToken !== token) return;
      if (target.click) clickCursor();
      applyScene(scene);
      moveCursor(target, true);
    }, CURSOR_TRAVEL_MS);
  }

  /* fit the fixed-width frame into the stage (limited by width and screen height) */
  function availableHeight() {
    var box = root.querySelector('.dts-stagebox');
    return box ? box.clientHeight - 8 : 500;
  }

  function fit() {
    var w = viewport.clientWidth;
    var h = frame.offsetHeight || 1;
    scale = Math.min(1, w / FRAME_WIDTH, Math.max(0.3, availableHeight() / h));
    frame.style.width = FRAME_WIDTH + 'px';
    frame.style.left = Math.max(0, (w - FRAME_WIDTH * scale) / 2) + 'px';
    frame.style.transform = 'scale(' + scale + ')';
    viewport.style.height = Math.ceil(h * scale) + 'px';
    if (current >= 0) moveCursor(cursorTarget(current), false);
  }

  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(fit);
    ro.observe(viewport);
    ro.observe(frame);
    if (root.querySelector('.dts-stagebox')) ro.observe(root.querySelector('.dts-stagebox'));
  } else {
    window.addEventListener('resize', fit);
  }
  fit();

  initSlides();

  /* ── slide navigation: Weiter/Zurück, dots, arrow keys ── */
  function initSlides() {
    var chapterCount = chapters.length;
    var hasSummary = !!root.querySelector('.dts-summary');
    var count = chapterCount + (hasSummary ? 1 : 0);
    var prevBtn = root.querySelector('[data-slide="prev"]');
    var nextBtn = root.querySelector('[data-slide="next"]');
    var counter = root.querySelector('.dts-counter');
    var idx = -1;

    function close() {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'tbeval-demo-close' }, window.location.origin);
      } else {
        window.location.href = root.getAttribute('data-back-url') || '/evaluate';
      }
    }

    function show(i) {
      i = clamp(i, 0, count - 1);
      if (i === idx) return;
      idx = i;
      var onSummary = hasSummary && idx === chapterCount;
      root.classList.toggle('dts-on-summary', onSummary);
      goTo(Math.min(idx, chapterCount - 1));
      dots.forEach(function (d, k) {
        d.classList.toggle('is-active', k === idx);
        d.setAttribute('aria-selected', k === idx ? 'true' : 'false');
      });
      if (counter) counter.textContent = (idx + 1) + ' / ' + count;
      if (prevBtn) prevBtn.disabled = idx === 0;
      if (nextBtn) {
        var last = idx === count - 1;
        nextBtn.innerHTML = last ? 'Demo schließen &#10003;' : 'Weiter &rarr;';
        nextBtn.classList.toggle('dts-btn--done', last);
      }
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { show(idx - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () {
      if (idx === count - 1) close(); else show(idx + 1);
    });
    dots.forEach(function (d) {
      d.addEventListener('click', function () { show(parseInt(d.getAttribute('data-goto'), 10)); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); if (idx < count - 1) show(idx + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(idx - 1); }
      else if (e.key === 'Escape') { close(); }
    });
    show(0);
  }

})();
