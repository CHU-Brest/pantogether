# Contact 
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Logo interactif</title>

<style>
body {
  font-family: Arial, sans-serif;
}

.container {
  display: flex;
  gap: 40px;
  align-items: center;
  padding: 20px;
}

.image-container {
  position: relative;
  width: 420px;
}

/* Image */
.image-container img {
  width: 100%;
  display: block;
}

/* Zones interactives */
.zone {
  position: absolute;
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
}

/* Hover (survol) */
.zone:hover {
  background-color: rgba(0, 150, 255, 0.25);
  transform: scale(1.05);
}

/* Actif (organe sélectionné) */
.zone.active {
  border: 3px solid #00aaff;
  background-color: rgba(0, 150, 255, 0.2);
}

/* Positions (AJUSTÉES POUR TON IMAGE) */
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

/* Zone texte */
.info {
  width: 320px;
  min-height: 200px;
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  background: #fafafa;
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

<script>
function showInfo(organe, element) {
  const infoBox = document.getElementById("infoBox");

  document.querySelectorAll('.zone').forEach(z => z.classList.remove('active'));
  element.classList.add('active');

  const colors = {
    estomac: "#0077aa",
    foie: "#d62828",
    pancreas: "#f77f00"
  };

  const color = colors[organe];

  infoBox.innerHTML = data[organe].text;

  // applique la couleur dynamique
  infoBox.style.borderTop = `6px solid ${color}`;
}
  // contenu dynamique
  const data = {
  estomac: {
  text: `
    <div class="card">

      <div class="header">
        <img src="chubrest.png" class="logo">
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
      title: "Foie",
      text: "Foie et Voies Biliaires"
    },
    pancreas: {
      title: "Pancréas",
      text: "Pancréas"
    }
  };

  infoBox.innerHTML = `
    <h3>${data[organe].title}</h3>
    <p>${data[organe].text}</p>
  `;
}
</script>

</body>
</html>
