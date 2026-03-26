# Contact 
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Logo interactif</title>

<style>
/* RESET */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f5f7fa;
}

/* LAYOUT */
.container {
  display: flex;
  gap: 30px;
  padding: 30px;
  align-items: flex-start;
  justify-content: center;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    align-items: center;
    padding: 15px;
  }

  .info {
    width: 100%;
  }

  .image-container {
    width: 100%;
    max-width: 400px;
  }
}

/* IMAGE */
.image-container {
  position: relative;
  width: 420px;
}

.image-container img {
  width: 100%;
  display: block;
  border-radius: 12px;
}

/* ZONES INTERACTIVES */
.zone {
  position: absolute;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.25s ease;
}

/* HOVER */
.zone:hover {
  transform: scale(1.08);
  background-color: rgba(0, 150, 255, 0.15);
}

/* ACTIF */
.zone.active {
  border: 3px solid #333;
  background-color: rgba(0, 150, 255, 0.2);
}

/* POSITIONS (TES VALEURS CONSERVÉES) */
.estomac {
  top: 30px;
  left: 140px;
  width: 100px;
  height: 100px;
}

.foie {
  top: 120px;
  left: 90px;
  width: 150px;
  height: 70px;
}

.pancreas {
  top: 170px;
  left: 120px;
  width: 120px;
  height: 50px;
}

/* FICHE INFO */
.info {
  width: 520px;
  min-height: 280px;
  padding: 20px;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 6px 25px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

/* HEADER AVEC LOGO */
.header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.logo {
  width: 50px;
}

/* TITRE */
.card h2 {
  margin: 0;
  font-size: 20px;
}

/* SECTIONS */
.section {
  margin-bottom: 15px;
  padding: 12px;
  border-left: 4px solid #ccc;
  background: #f9fbfc;
  border-radius: 8px;
  transition: 0.3s;
}

.section h3 {
  margin: 0 0 5px;
  font-size: 15px;
}

.section p {
  margin: 0;
  line-height: 1.5;
}

/* LIENS */
.section a {
  color: #0077aa;
  text-decoration: none;
  font-weight: 500;
}

.section a:hover {
  text-decoration: underline;
}
</style>
</head>

<body>

<div class="container">

  <div class="image-container">
    <img src="/assets/pantogether.png" alt="Logo">

    <div class="zone estomac" onclick="showInfo('estomac', this)"></div>
    <div class="zone foie" onclick="showInfo('foie', this)"></div>
    <div class="zone pancreas" onclick="showInfo('pancreas', this)"></div>
  </div>

  <div class="info" id="infoBox">
    Cliquez sur un organe 👈
  </div>

</div>

</body>
</html>

<script>
const data = {
  estomac: {
    text: `
      <div class="card">

        <div class="header">
          <img src="/assets/chubrest.png" class="logo">
          <h2 style="color:#0077aa;">
            Oesophage, Jonction Oeso-gastrique, Estomac
          </h2>
        </div>

        <div class="section" style="border-left-color:#0077aa;">
          <h3>👨‍⚕️ Référents</h3>
          <p>
            <strong>Pr METGES Jean-Philippe</strong><br>
            <strong>Dr BOURBONNE Vincent</strong>
          </p>
        </div>

        <div class="section" style="border-left-color:#0077aa;">
          <h3>🏥 Établissement</h3>
          <p>
            CHU Brest - Hôpital de La Cavale Blanche<br>
            Institut de Cancérologie et d’Imagerie<br>
            Pôle 7 - 1er étage<br>
            Boulevard Tanguy Prigent<br>
            29200 Brest
          </p>
        </div>

        <div class="section" style="border-left-color:#0077aa;">
          <h3>📧 Contact</h3>
          <p>
            <a href="mailto:jean-philippe.metges@chu-brest.fr">
              📩 jean-philippe.metges@chu-brest.fr
            </a><br>
            <a href="mailto:BOURBONV@tcd.ie">
              📩 BOURBONV@tcd.ie
            </a>
          </p>
        </div>

      </div>
    `
  },

  foie: {
    text: `<h3 style="color:#d62828;">Foie</h3><p>Foie et voies biliaires</p>`
  },

  pancreas: {
    text: `<h3 style="color:#f77f00;">Pancréas</h3><p>Informations pancréas</p>`
  }
};

function showInfo(organe, element) {
  const infoBox = document.getElementById("infoBox");

  // reset zones
  document.querySelectorAll('.zone').forEach(z => z.classList.remove('active'));
  element.classList.add('active');

  // couleurs
  const colors = {
    estomac: "#0077aa",
    foie: "#d62828",
    pancreas: "#f77f00"
  };

  const color = colors[organe];

  // affichage contenu
  infoBox.innerHTML = data[organe].text;

  // bordure dynamique
  infoBox.style.borderTop = `6px solid ${color}`;
}
</script>
