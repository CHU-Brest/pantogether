/* ============================================================
   PAN-TOGETHER — Comportements partagés
   Thème clair/sombre · navigation docs · scroll-spy ancres
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Thème clair / sombre ---------- */
  var saved = null;
  try { saved = localStorage.getItem('pt-theme'); } catch (e) {}
  if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');

  function bindThemeToggle() {
    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (dark) { document.documentElement.removeAttribute('data-theme'); }
      else { document.documentElement.setAttribute('data-theme', 'dark'); }
      try { localStorage.setItem('pt-theme', dark ? 'light' : 'dark'); } catch (e) {}
    });
  }

  /* ---------- Nav mobile ---------- */
  function bindBurger() {
    var b = document.querySelector('.burger');
    var nav = document.querySelector('.main-nav');
    if (!b || !nav) return;
    b.addEventListener('click', function () { nav.classList.toggle('open'); });
  }

  /* ---------- Documentation : sous-sections + ancres ---------- */
  function initDocs() {
    var root = document.querySelector('[data-docs]');
    if (!root) return;

    var navLinks = Array.prototype.slice.call(root.querySelectorAll('.docs-nav a[data-target]'));
    var panels = Array.prototype.slice.call(root.querySelectorAll('.doc-panel'));
    var tocList = root.querySelector('.doc-toc ul');
    var crumbCur = root.querySelector('.breadcrumb .cur');
    var headerH = 102;

    function buildToc(panel) {
      if (!tocList) return;
      tocList.innerHTML = '';
      var heads = panel.querySelectorAll('h2[id], h3[id]');
      heads.forEach(function (h) {
        var li = document.createElement('li');
        li.className = h.tagName === 'H3' ? 'lvl-3' : 'lvl-2';
        var a = document.createElement('a');
        a.href = '#' + h.id;
        a.textContent = h.textContent;
        a.dataset.anchor = h.id;
        a.addEventListener('click', function (ev) {
          ev.preventDefault();
          var t = document.getElementById(h.id);
          var y = t.getBoundingClientRect().top + window.pageYOffset - headerH;
          window.scrollTo({ top: y, behavior: 'smooth' });
          history.replaceState(null, '', '#' + h.id);
        });
        li.appendChild(a);
        tocList.appendChild(li);
      });
    }

    function activate(target, push) {
      panels.forEach(function (p) { p.classList.toggle('active', p.id === target); });
      navLinks.forEach(function (a) { a.classList.toggle('active', a.dataset.target === target); });
      var panel = document.getElementById(target);
      if (!panel) return;
      buildToc(panel);
      var link = navLinks.filter(function (a) { return a.dataset.target === target; })[0];
      if (link && crumbCur) crumbCur.textContent = link.dataset.label || link.textContent.trim();
      if (push) history.replaceState(null, '', '#' + target);
      window.scrollTo({ top: 0, behavior: 'auto' });
      spy();
    }

    navLinks.forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        activate(a.dataset.target, true);
      });
    });

    /* scroll-spy sur les ancres du panneau actif */
    function spy() {
      var panel = root.querySelector('.doc-panel.active');
      if (!panel || !tocList) return;
      var heads = Array.prototype.slice.call(panel.querySelectorAll('h2[id], h3[id]'));
      var pos = window.pageYOffset + headerH + 40;
      var current = heads[0];
      heads.forEach(function (h) { if (h.offsetTop <= pos) current = h; });
      var links = tocList.querySelectorAll('a');
      links.forEach(function (l) {
        l.classList.toggle('active', current && l.dataset.anchor === current.id);
      });
    }
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(function () { spy(); ticking = false; }); ticking = true; }
    }, { passive: true });

    /* sélection initiale (hash de panneau, sinon premier) */
    var hash = (location.hash || '').replace('#', '');
    var initial = navLinks[0] && navLinks[0].dataset.target;
    var anchorHash = null;
    if (hash) {
      if (navLinks.some(function (a) { return a.dataset.target === hash; })) {
        initial = hash;
      } else {
        // hash pointant vers une ancre : trouver le panneau qui la contient
        var el = document.getElementById(hash);
        var owner = el && el.closest('.doc-panel');
        if (owner) { initial = owner.id; anchorHash = hash; }
      }
    }
    if (initial) activate(initial, false);
    if (anchorHash) {
      requestAnimationFrame(function () {
        var t = document.getElementById(anchorHash);
        if (t) window.scrollTo({ top: t.getBoundingClientRect().top + window.pageYOffset - headerH, behavior: 'auto' });
      });
    }
  }

  function init() { bindThemeToggle(); bindBurger(); initDocs(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
