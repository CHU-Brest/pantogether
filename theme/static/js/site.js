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

  /* ---------- Affiches d'agenda : agrandissement ----------
     Les affiches de congrès sont illisibles en vignette. Le clic les ouvre
     dans un <dialog> natif : on hérite gratuitement du piège de focus, de
     l'inertie de l'arrière-plan et de la fermeture par Échap.
     Le href pointe sur le fichier image : si <dialog> manque, le navigateur
     suit le lien et affiche quand même l'affiche en grand. */
  function bindPosters() {
    var links = document.querySelectorAll('a.poster');
    if (!links.length) return;
    var dlg = null, dlgImg = null;

    function build() {
      dlg = document.createElement('dialog');
      dlg.className = 'poster-zoom';
      var close = document.createElement('button');
      close.type = 'button';
      close.className = 'poster-zoom-close';
      close.setAttribute('aria-label', 'Fermer l\u2019affiche');
      close.innerHTML = '&times;';
      dlgImg = document.createElement('img');
      dlg.appendChild(close);
      dlg.appendChild(dlgImg);
      document.body.appendChild(dlg);
      close.addEventListener('click', function () { dlg.close(); });
      /* Clic sur le fond : la cible n'est le <dialog> que hors de son contenu. */
      dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
    }

    function open(ev) {
      var img = this.querySelector('img');
      if (!img) return;
      if (!dlg) build();
      if (!dlg.showModal) return;   /* pas de <dialog> : on laisse suivre le lien */
      ev.preventDefault();
      dlgImg.src = this.getAttribute('href');
      dlgImg.alt = img.getAttribute('alt') || '';
      dlg.showModal();
    }

    for (var i = 0; i < links.length; i++) links[i].addEventListener('click', open);
  }

  /* ---------- Coordonnées protégées ---------- */
  // Adresses et numéros arrivent brouillés dans data-coord (plugin « coordonnees »)
  // — rot13/rot5 puis base64 : rien d'exploitable dans le HTML tant que le visiteur
  // n'a pas cliqué. Même principe que les fiches RCP, révélées au clic elles aussi.
  function derot(s) {
    // rot13 sur les lettres, rot5 sur les chiffres : sa propre inverse.
    return s.replace(/[a-z0-9]/gi, function (c) {
      var o = c.charCodeAt(0);
      if (o >= 65 && o <= 90) return String.fromCharCode((o - 65 + 13) % 26 + 65);
      if (o >= 97 && o <= 122) return String.fromCharCode((o - 97 + 13) % 26 + 97);
      return String.fromCharCode((o - 48 + 5) % 10 + 48);
    });
  }

  function bindCoordonnees() {
    var btns = document.querySelectorAll('.reveal-btn[data-coord]');
    if (!btns.length) return;

    function reveal() {
      var valeur;
      try { valeur = derot(decodeURIComponent(escape(atob(this.dataset.coord)))); }
      catch (err) { return; }
      var mail = this.getAttribute('data-kind') === 'mail';
      var a = document.createElement('a');
      // tel: n'accepte ni espace ni séparateur, contrairement à l'affichage.
      a.href = mail ? 'mailto:' + valeur : 'tel:' + valeur.replace(/[^+0-9]/g, '');
      a.textContent = valeur;
      this.replaceWith(a);
    }

    for (var i = 0; i < btns.length; i++) btns[i].addEventListener('click', reveal);
  }

  function init() { bindThemeToggle(); bindBurger(); initDocs(); bindPosters(); bindCoordonnees(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
