/* ============================================================
   PAN-TOGETHER — Moteur de recherche des RCP
   Données : /data/rcp.json (généré par build_dataset.py)
   Recherche : Fuse.js sur les colonnes brutes
   Carte : Leaflet + fond IGN Géoplateforme
   ============================================================ */
(function () {
  'use strict';

  var AXES = {
    foie: 'Foie & voies biliaires',
    pancreas: 'Pancréas',
    oesogastrique: 'Œsophage & jonction'
  };
  var AXCOLOR = {
    foie: 'var(--axis-foie)',
    pancreas: 'var(--axis-pancreas)',
    oesogastrique: 'var(--axis-gastric)'
  };
  var AXCLASS = { foie: 'mk-foie', pancreas: 'mk-pancreas', oesogastrique: 'mk-gastric' };

  // Fond volontairement plat — ni routes secondaires ni hydrographie : les
  // marqueurs colorés par axe doivent rester l'information dominante.
  // Esri publie une variante sombre native, d'où l'absence de filtre CSS.
  // Attention : l'ordre des gabarits est {z}/{y}/{x} chez Esri, pas {z}/{x}/{y}.
  var ESRI = 'https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/';
  var BASEMAP = {
    light: ESRI + 'World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    dark: ESRI + 'World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}'
  };
  var BASEMAP_ATTR = 'Fond de carte &copy; <a href="https://www.esri.com/" target="_blank" rel="noopener">Esri</a>' +
    ' — sources : Esri, HERE, Garmin, &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>';

  var ALL = [], VOCAB = {}, fuse = null, current = [];
  var state = { q: '', axe: [], region: [], jour: [], plateaux: [], sos: [], visio: false, sel: null };
  var map = null, markerLayer = null, tileLayer = null, tab = 'map', restoring = false;

  var els = {};
  ['q', 'go', 'filters', 'results', 'count', 'info-body', 'om-strip', 'om-title', 'reset', 'map']
    .forEach(function (id) { els[id] = document.getElementById(id); });

  /* ---------------- utilitaires ---------------- */
  function esc(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function arr(v) { return Array.isArray(v) ? v : (v ? [v] : []); }
  function axLabel(d) { return AXES[d.AXE] || d.AXE || 'Axe non renseigné'; }
  function axColor(d) { return AXCOLOR[d.AXE] || 'var(--brand)'; }

  /* ---------------- filtres ---------------- */
  var SHOW_MAX = 4;

  function countSingle(key, value) {
    return ALL.filter(function (d) { return d[key] === value; }).length;
  }
  function countMulti(key, value) {
    return ALL.filter(function (d) { return arr(d[key]).indexOf(value) >= 0; }).length;
  }
  function chk(group, value, label, n) {
    return '<label class="chk"><input type="checkbox" data-g="' + group + '" value="' + esc(value) + '" />' +
      '<span>' + esc(label) + '</span><span class="cnt">' + n + '</span></label>';
  }
  function grp(title, items) {
    var html;
    if (items.length > SHOW_MAX + 1) {
      html = items.slice(0, SHOW_MAX).join('') +
        '<div class="extra" hidden>' + items.slice(SHOW_MAX).join('') + '</div>' +
        '<button type="button" class="more-btn">Voir plus (' + (items.length - SHOW_MAX) + ')</button>';
    } else {
      html = items.join('');
    }
    return '<div class="grp"><h4>' + esc(title) + '</h4>' + html + '</div>';
  }

  function renderFilters() {
    var h = '';
    h += grp('Axe', (VOCAB.axes || []).map(function (a) {
      return chk('axe', a, AXES[a] || a, countSingle('AXE', a));
    }));
    h += grp('Région', (VOCAB.regions || []).map(function (r) {
      return chk('region', r, r, countSingle('CENTRE_REGION', r));
    }));
    h += grp('Jour de la réunion', (VOCAB.jours || []).map(function (j) {
      return chk('jour', j, j, countSingle('RCP_JOUR', j));
    }));
    h += grp('Plateaux techniques', (VOCAB.plateaux || []).map(function (p) {
      return chk('plateaux', p, p, countMulti('PLATEAUX', p));
    }));
    h += grp('Soins oncologiques de support', (VOCAB.sos || []).map(function (s) {
      return chk('sos', s, s, countMulti('SOS', s));
    }));
    h += '<div class="grp"><h4>Visioconférence</h4>' +
      '<label class="chk"><input type="checkbox" data-g="visio" value="1" />' +
      '<span>RCP accessible en visio</span><span class="cnt">' +
      ALL.filter(function (d) { return d.RCP_VISIO; }).length + '</span></label></div>';
    els.filters.innerHTML = h;
  }

  els.filters.addEventListener('click', function (e) {
    var b = e.target.closest('.more-btn');
    if (!b) return;
    var extra = b.parentElement.querySelector('.extra');
    var open = !extra.hidden;
    extra.hidden = open;
    b.textContent = open ? 'Voir plus (' + extra.querySelectorAll('label').length + ')' : 'Voir moins';
  });

  els.filters.addEventListener('change', function (e) {
    var t = e.target;
    if (!t.dataset || !t.dataset.g) return;
    if (t.dataset.g === 'visio') {
      state.visio = t.checked;
    } else {
      var a = state[t.dataset.g];
      if (t.checked) { if (a.indexOf(t.value) < 0) a.push(t.value); }
      else { a.splice(a.indexOf(t.value), 1); }
    }
    runSearch();
  });

  /* ---------------- recherche ---------------- */
  function passesFacets(d) {
    // OR à l'intérieur d'un groupe d'attributs exclusifs…
    if (state.axe.length && state.axe.indexOf(d.AXE) < 0) return false;
    if (state.region.length && state.region.indexOf(d.CENTRE_REGION) < 0) return false;
    if (state.jour.length && state.jour.indexOf(d.RCP_JOUR) < 0) return false;
    // …ET à l'intérieur des groupes de capacités : on cherche un centre qui
    // dispose de TOUT ce qui est coché, pas de l'un ou l'autre.
    var plx = arr(d.PLATEAUX);
    if (!state.plateaux.every(function (p) { return plx.indexOf(p) >= 0; })) return false;
    var sos = arr(d.SOS).concat(arr(d.SOS_AUTRES));
    if (!state.sos.every(function (s) { return sos.indexOf(s) >= 0; })) return false;
    if (state.visio && !d.RCP_VISIO) return false;
    return true;
  }

  function runSearch() {
    state.q = els.q.value.trim();
    var base;
    if (state.q && fuse) {
      base = fuse.search(state.q).map(function (r) { return r.item; });
    } else {
      base = ALL;
    }
    current = base.filter(passesFacets);
    if (state.sel && !current.some(function (d) { return d.id === state.sel; })) state.sel = null;
    renderResults();
    renderMarkers();
    renderInfo();
    syncHash();
  }

  /* ---------------- résultats ---------------- */
  function renderResults() {
    els.count.textContent = current.length + ' RCP trouvée' + (current.length > 1 ? 's' : '');
    if (!current.length) {
      els.results.innerHTML = '<div class="res-empty">Aucune RCP ne correspond à votre recherche.<br/>Essayez d\'élargir les filtres.</div>';
      return;
    }
    els.results.innerHTML = current.map(function (d) {
      var meta = [d.RCP_JOUR, d.RCP_HORAIRE, d.RCP_FREQUENCE].filter(Boolean).join(' · ');
      if (d.RCP_VISIO) meta += (meta ? ' · ' : '') + 'Visio';
      return '<button class="res-item' + (d.id === state.sel ? ' sel' : '') + '" type="button"' +
        ' data-id="' + esc(d.id) + '" style="--ac:' + axColor(d) + '">' +
        '<span class="ax">' + esc(axLabel(d)) + '</span>' +
        '<h4>' + esc(d.RCP_NOM || 'RCP sans intitulé') + '</h4>' +
        '<div class="ctr">' + esc(d.CENTRE_NOM) + (d.CENTRE_VILLE ? ' · ' + esc(d.CENTRE_VILLE) : '') + '</div>' +
        '<div class="meta">' + esc(meta) + '</div></button>';
    }).join('');
  }

  els.results.addEventListener('click', function (e) {
    var b = e.target.closest('.res-item');
    if (b) select(b.dataset.id);
  });

  function select(id, keepTab) {
    state.sel = (state.sel === id) ? null : id;
    renderResults();
    renderMarkers();
    renderInfo();
    if (state.sel && !keepTab) showTab('info');
    syncHash();
  }

  /* ---------------- onglets ---------------- */
  var tabBtns = Array.prototype.slice.call(document.querySelectorAll('.tab-btn'));
  function showTab(name) {
    tab = name;
    tabBtns.forEach(function (b) { b.classList.toggle('on', b.dataset.tab === name); });
    document.getElementById('tab-map').classList.toggle('on', name === 'map');
    document.getElementById('tab-info').classList.toggle('on', name === 'info');
    // Leaflet ne connaît pas la taille d'un conteneur masqué : sans cet appel
    // au retour sur l'onglet, les tuiles ne couvrent qu'une partie de la carte.
    if (name === 'map' && map) { map.invalidateSize(); fitToResults(); }
  }
  tabBtns.forEach(function (b) {
    b.addEventListener('click', function () { showTab(b.dataset.tab); });
  });

  /* ---------------- fiche ---------------- */
  // Adresses et numéros arrivent en base64 : le bouton ne les reconstitue qu'au
  // clic (cf. le gestionnaire plus bas), pour ne rien livrer aux collecteurs.
  function revealBtn(b64, kind) {
    if (!b64) return '';
    return '<button class="reveal-btn" type="button" data-kind="' + kind + '"' +
      ' data-b64="' + esc(b64) + '">' +
      (kind === 'mail' ? 'Afficher l\'e-mail' : 'Afficher le numéro') + '</button>';
  }
  function mailBtn(b64) { return revealBtn(b64, 'mail'); }
  function telBtn(b64) { return revealBtn(b64, 'tel'); }
  function kv(pairs) {
    var rows = pairs.filter(function (p) { return p[1]; }).map(function (p) {
      return '<dt>' + esc(p[0]) + '</dt><dd>' + p[1] + '</dd>';
    }).join('');
    return rows ? '<dl class="kv">' + rows + '</dl>' : '<p class="kv none">Non renseigné.</p>';
  }
  function liste(values) {
    if (!values.length) return '<p class="kv none">Non renseigné.</p>';
    return '<ul class="plx">' + values.map(function (v) { return '<li>' + esc(v) + '</li>'; }).join('') + '</ul>';
  }

  function renderInfo() {
    var d = ALL.filter(function (x) { return x.id === state.sel; })[0];
    if (!d) {
      els['info-body'].innerHTML = '<div class="info-empty">Sélectionnez une RCP dans la liste pour afficher ses informations détaillées.</div>';
      return;
    }
    var tags = '';
    if (d.est_coordonnateur) tags += '<span class="tag">Centre coordonnateur</span>';
    if (d.est_referent) tags += '<span class="tag">Centre expert référent</span>';

    var lieu = [esc(d.CENTRE_NOM), esc(d.CENTRE_VILLE)].filter(Boolean).join(' — ');
    if (d.CENTRE_REGION) lieu += ' (' + esc(d.CENTRE_REGION) + ')';

    els['info-body'].innerHTML = '<div class="info" style="--ac:' + axColor(d) + '">' +
      '<span class="ax">' + esc(axLabel(d)) + '</span>' +
      '<h2>' + esc(d.RCP_NOM || 'RCP sans intitulé') + '</h2>' +
      '<p class="sub">' + lieu + '</p>' + tags +

      '<h3>Réunion</h3>' + kv([
        ['Jour', esc(d.RCP_JOUR)],
        ['Horaire', esc(d.RCP_HORAIRE)],
        ['Fréquence', esc(d.RCP_FREQUENCE)],
        ['Lieu', esc(d.RCP_LIEU)],
        ['Visioconférence', d.RCP_VISIO ? 'Oui' : 'Non'],
        ['Réseau', esc(d.RCP_RESEAU)]
      ]) +

      '<h3>Soumettre un dossier</h3>' + kv([
        ['Modalités', esc(d.RCP_SOUMISSION)],
        ['Assistante médico-administrative', esc(d.RCP_AMA_NOM)],
        ['E-mail', mailBtn(d.RCP_AMA_EMAIL)],
        ['Téléphone', telBtn(d.RCP_AMA_TEL)]
      ]) +

      '<h3>Centre</h3>' + kv([
        ['Service', esc(d.CENTRE_SERVICE)],
        ['Adresse', esc(d.CENTRE_ADRESSE)],
        ['Médecin référent', esc(d.MEDECIN_NOM)],
        ['Contact médecin', mailBtn(d.MEDECIN_EMAIL)],
        ['Secrétariat', esc(d.SECRETARIAT_NOM)],
        ['E-mail secrétariat', mailBtn(d.SECRETARIAT_EMAIL)],
        ['Téléphone secrétariat', telBtn(d.SECRETARIAT_TEL)],
        ['Site web', d.SITEWEB ? '<a href="' + esc(d.SITEWEB) + '" target="_blank" rel="noopener">' + esc(d.SITEWEB) + '</a>' : '']
      ]) +

      '<h3>Équipe de coordination</h3>' + kv([
        ['Infirmier(e) de coordination', esc(d.IDEC_NOM)],
        ['Contact IDEC', mailBtn(d.IDEC_EMAIL) || telBtn(d.IDEC_TEL)],
        ['Infirmier(e) en pratique avancée', esc(d.IPA_NOM)],
        ['Contact IPA', mailBtn(d.IPA_EMAIL) || telBtn(d.IPA_TEL)],
        ['Attaché(e) de recherche clinique', esc(d.ARC_NOM)],
        ['Contact ARC', mailBtn(d.ARC_EMAIL) || telBtn(d.ARC_TEL)]
      ]) +

      '<h3>Plateaux techniques</h3>' + liste(arr(d.PLATEAUX)) +
      '<h3>Soins oncologiques de support</h3>' + liste(arr(d.SOS).concat(arr(d.SOS_AUTRES))) +
      (d.CONVENTIONS ? '<h3>Conventions</h3><p class="kv">' + esc(d.CONVENTIONS) + '</p>' : '') +
      '</div>';
  }

  els['info-body'].addEventListener('click', function (e) {
    var b = e.target.closest('.reveal-btn');
    if (!b) return;
    var texte;
    try { texte = decodeURIComponent(escape(atob(b.dataset.b64))); }
    catch (err) { return; }
    var mail = b.dataset.kind === 'mail';
    // Une cellule du classeur peut porter deux numéros séparés par « ; » : on
    // rend chacun cliquable plutôt qu'un seul lien portant les deux.
    var valeurs = texte.split(';').map(function (v) { return v.trim(); }).filter(Boolean);
    if (!valeurs.length) return;
    var frag = document.createDocumentFragment();
    valeurs.forEach(function (v, i) {
      if (i) frag.appendChild(document.createTextNode(' · '));
      var a = document.createElement('a');
      // tel: n'accepte ni espace ni séparateur, contrairement à l'affichage.
      a.href = mail ? 'mailto:' + v : 'tel:' + v.replace(/[^+0-9]/g, '');
      a.textContent = v;
      frag.appendChild(a);
    });
    b.replaceWith(frag);
  });

  /* ---------------- carte ---------------- */
  function isDark() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  function setBasemap() {
    if (!map) return;
    if (tileLayer) map.removeLayer(tileLayer);
    tileLayer = L.tileLayer(BASEMAP[isDark() ? 'dark' : 'light'], {
      attribution: BASEMAP_ATTR, maxZoom: 16, minZoom: 2
    });
    tileLayer.addTo(map);
    tileLayer.bringToBack();
  }

  function initMap() {
    map = L.map(els.map, { scrollWheelZoom: false, zoomControl: true, zoomSnap: 0.25, zoomDelta: 0.5 })
      .setView([46.6, 2.4], 5);
    setBasemap();
    markerLayer = L.layerGroup().addTo(map);
    // Molette activée seulement après un clic : sinon la carte capture le
    // défilement de la page dès qu'on la survole.
    map.on('click', function () { map.scrollWheelZoom.enable(); });
    // site.js bascule `data-theme` sur <html> ; on suit l'attribut plutôt que
    // le bouton, ce qui couvre aussi le thème restauré depuis localStorage.
    new MutationObserver(setBasemap).observe(document.documentElement, {
      attributes: true, attributeFilter: ['data-theme']
    });
  }

  function groupByPoint(list) {
    var groups = {};
    list.forEach(function (d) {
      if (typeof d.CENTRE_LATITUDE !== 'number' || typeof d.CENTRE_LONGITUDE !== 'number') return;
      var key = d.CENTRE_LATITUDE.toFixed(4) + ',' + d.CENTRE_LONGITUDE.toFixed(4);
      (groups[key] = groups[key] || { lat: d.CENTRE_LATITUDE, lon: d.CENTRE_LONGITUDE, items: [] }).items.push(d);
    });
    return Object.keys(groups).map(function (k) { return groups[k]; });
  }

  function renderMarkers() {
    if (!map) return;
    markerLayer.clearLayers();

    groupByPoint(current).forEach(function (g) {
      var axes = g.items.map(function (d) { return d.AXE; });
      var uniform = axes.every(function (a) { return a === axes[0]; });
      var cls = uniform ? (AXCLASS[axes[0]] || 'mk-mixte') : 'mk-mixte';
      var selected = g.items.some(function (d) { return d.id === state.sel; });

      var m = L.circleMarker([g.lat, g.lon], {
        radius: Math.min(6 + 2 * (g.items.length - 1), 14),
        className: 'mk ' + cls + (selected ? ' sel' : ''),
        weight: 2
      });
      m.bindTooltip(g.items[0].CENTRE_NOM + (g.items.length > 1 ? ' — ' + g.items.length + ' RCP' : ''));
      m.bindPopup(
        '<div class="pop-h">' + esc(g.items[0].CENTRE_VILLE || '') + '</div>' +
        g.items.map(function (d) {
          return '<button class="pop-item" type="button" data-id="' + esc(d.id) + '" style="--ac:' + axColor(d) + '">' +
            '<span class="ax">' + esc(axLabel(d)) + '</span>' + esc(d.RCP_NOM || 'RCP') + '</button>';
        }).join('')
      );
      markerLayer.addLayer(m);
    });

    renderOM();
  }

  // Délégation sur la popup Leaflet, recréée à chaque ouverture.
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.pop-item');
    if (!b) return;
    select(b.dataset.id);
  });

  function fitToResults() {
    if (!map) return;
    var metropole = current.filter(function (d) {
      return !d.outremer && typeof d.CENTRE_LATITUDE === 'number';
    });
    var source = metropole.length ? metropole : current;
    var pts = source
      .filter(function (d) { return typeof d.CENTRE_LATITUDE === 'number'; })
      .map(function (d) { return [d.CENTRE_LATITUDE, d.CENTRE_LONGITUDE]; });
    if (!pts.length) { map.setView([46.6, 2.4], 5); return; }
    // Le conteneur peut avoir changé de taille (onglet, redimensionnement) :
    // sans cette remise à niveau, fitBounds calcule sur des dimensions périmées.
    map.invalidateSize();
    map.fitBounds(L.latLngBounds(pts), { padding: [24, 24], maxZoom: 11 });
  }

  function renderOM() {
    var om = current.filter(function (d) { return d.outremer; });
    els['om-title'].hidden = !om.length;
    els['om-strip'].innerHTML = om.map(function (d) {
      return '<button class="om-tile' + (d.id === state.sel ? ' sel' : '') + '" type="button"' +
        ' data-id="' + esc(d.id) + '" style="--ac:' + axColor(d) + '">' +
        '<span class="d"></span><b>' + esc(d.CENTRE_REGION) + '</b> · ' +
        esc(d.RCP_NOM || d.CENTRE_VILLE) + '</button>';
    }).join('');
  }

  els['om-strip'].addEventListener('click', function (e) {
    var b = e.target.closest('.om-tile');
    if (!b) return;
    var d = ALL.filter(function (x) { return x.id === b.dataset.id; })[0];
    select(b.dataset.id, true);
    if (d && map && typeof d.CENTRE_LATITUDE === 'number') {
      map.flyTo([d.CENTRE_LATITUDE, d.CENTRE_LONGITUDE], 10);
    }
  });

  /* ---------------- URL partageable ---------------- */
  var LIST_KEYS = ['axe', 'region', 'jour', 'plateaux', 'sos'];

  function syncHash() {
    if (restoring) return;
    var p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    LIST_KEYS.forEach(function (k) { state[k].forEach(function (v) { p.append(k, v); }); });
    if (state.visio) p.set('visio', '1');
    if (state.sel) p.set('sel', state.sel);
    var h = p.toString();
    history.replaceState(null, '', h ? '#' + h : location.pathname);
  }

  function restoreHash() {
    var h = (location.hash || '').replace(/^#/, '');
    if (!h) return;
    restoring = true;
    var p = new URLSearchParams(h);
    state.q = p.get('q') || '';
    els.q.value = state.q;
    LIST_KEYS.forEach(function (k) { state[k] = p.getAll(k); });
    state.visio = p.get('visio') === '1';
    state.sel = p.get('sel') || null;

    els.filters.querySelectorAll('input[data-g]').forEach(function (i) {
      var g = i.dataset.g;
      i.checked = (g === 'visio') ? state.visio : (state[g] || []).indexOf(i.value) >= 0;
      // Déplier le groupe si la case restaurée y est masquée.
      if (i.checked) {
        var extra = i.closest('.extra');
        if (extra && extra.hidden) {
          extra.hidden = false;
          var btn = extra.parentElement.querySelector('.more-btn');
          if (btn) btn.textContent = 'Voir moins';
        }
      }
    });
    restoring = false;
  }

  /* ---------------- événements ---------------- */
  // `syncHash` passe par replaceState, qui n'émet pas d'événement : un
  // hashchange signale donc toujours une intervention extérieure (lien collé,
  // bouton Précédent). On rejoue l'état plutôt que de l'ignorer.
  window.addEventListener('hashchange', function () {
    restoreHash();
    runSearch();
    if (state.sel) showTab('info');
    else fitToResults();
  });

  els.go.addEventListener('click', runSearch);
  els.q.addEventListener('keydown', function (e) { if (e.key === 'Enter') runSearch(); });
  var typing;
  els.q.addEventListener('input', function () {
    clearTimeout(typing);
    typing = setTimeout(runSearch, 180);
  });
  els.reset.addEventListener('click', function () {
    LIST_KEYS.forEach(function (k) { state[k] = []; });
    state.visio = false;
    state.sel = null;
    els.q.value = '';
    els.filters.querySelectorAll('input').forEach(function (i) { i.checked = false; });
    runSearch();
  });

  /* ---------------- hauteur de l'application ---------------- */
  // rcp.css pose une valeur de repli, mais le bandeau SITE_BANNER est
  // optionnel et sa hauteur dépend du texte : on mesure la chrome réelle
  // plutôt que de la coder en dur.
  function sizeApp() {
    var h = 0;
    ['.site-banner', '.site-header', '.rcp-search'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) h += el.offsetHeight;
    });
    document.documentElement.style.setProperty('--rcp-chrome', h + 'px');
    if (map) map.invalidateSize();
  }
  var resizing;
  window.addEventListener('resize', function () {
    clearTimeout(resizing);
    resizing = setTimeout(function () { sizeApp(); fitToResults(); }, 150);
  });
  sizeApp();

  /* ---------------- démarrage ---------------- */
  els.count.textContent = 'Chargement…';

  fetch(window.RCP_DATA_URL)
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (payload) {
      ALL = payload.rcp || [];
      VOCAB = payload.vocab || {};

      // Les champs d'identité sont pondérés plus haut que les capacités : sans
      // cela un centre dont seul le SOS matche remonterait devant la RCP qui
      // porte le mot dans son intitulé.
      fuse = new Fuse(ALL, {
        keys: [
          { name: 'RCP_NOM', weight: 3 },
          { name: 'CENTRE_NOM', weight: 3 },
          { name: 'CENTRE_VILLE', weight: 2 },
          { name: 'CENTRE_REGION', weight: 2 },
          { name: 'AXE', weight: 2 },
          { name: 'MEDECIN_NOM', weight: 2 },
          { name: 'CENTRE_SERVICE', weight: 1 },
          { name: 'RCP_RESEAU', weight: 1 },
          { name: 'PLATEAUX', weight: 1 },
          { name: 'SOS', weight: 1 },
          { name: 'SOS_AUTRES', weight: 1 }
        ],
        threshold: 0.3,
        // Sans cela Fuse applique `distance: 100` et ignore en pratique toute
        // correspondance située au-delà d'une centaine de caractères, ce qui
        // arrive couramment sur CENTRE_SERVICE.
        ignoreLocation: true
      });

      renderFilters();
      restoreHash();
      initMap();
      sizeApp();
      runSearch();
      fitToResults();
      if (state.sel) showTab('info');
    })
    .catch(function (err) {
      els.count.textContent = 'Données indisponibles';
      els.results.innerHTML = '<div class="res-empty">Impossible de charger l\'annuaire des RCP.<br/>' +
        esc(err.message) + '</div>';
    });
})();
