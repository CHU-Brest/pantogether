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
  top: 25px;
  left: 90px;
  width: 100px;
  height: 90px;
}

.foie {
  top: 90px;
  left: 60px;
  width: 140px;
  height: 60px;
}

.pancreas {
  top: 125px;
  left: 85px;
  width: 110px;
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
  width: 90px;
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
  
.left-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.admin-link {
  margin-top: 15px;
  font-size: 16px;
  color: #0077aa;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.admin-link:hover {
  text-decoration: underline;
  transform: scale(1.05);
}
  
</style>
</head>

<body>

<div class="container">

 <div class="left-block">
  <div class="image-container">
    <img src="/assets/pantogether.png" alt="Logo">

    <div class="zone estomac" onclick="showInfo('estomac', this)"></div>
    <div class="zone foie" onclick="showInfo('foie', this)"></div>
    <div class="zone pancreas" onclick="showInfo('pancreas', this)"></div>
  </div>

  <!-- 👇 NOUVEAU LIEN -->
  <div class="admin-link" onclick="showInfo('admin', this)">
    📋 Coordination administrative
  </div>
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
          <h3>📧 Contacts</h3>
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
    text: `
      <div class="card">

        <div class="header">
          <img src="/assets/chuavicenne.png" class="logo">
          <h2 style="color:#d62828;">
            Foie et voies biliaires
          </h2>
        </div>

        <div class="section" style="border-left-color:#d62828;">
          <h3>👨‍⚕️ Référents</h3>
          <p>
            <strong>Pr GANNE-CARRIE Nathalie</strong><br>
            <strong>Pr NAHON Pierre</strong>
          </p>
        </div>

        <div class="section" style="border-left-color:#d62828;">
          <h3>🏥 Établissement</h3>
          <p>
            Hôpital Avicenne, AP-HP <br>
            Service d'Hépatologie et d'oncologie Hépatique <br>
            Bâtiment Larrey A <br>
            125 rue de Stalingrad <br>
            93000 Bobigny 
          </p>
        </div>

        <div class="section" style="border-left-color:#d62828;">
          <h3>📧 Contacts</h3>
          <p>
            <a href="mailto:nathalie.ganne@aphp.fr">
              📩 nathalie.ganne@aphp.fr 
            </a><br>
            <a href="mailto:pierre.nahon@aphp.fr">
              📩 pierre.nahon@aphp.fr
            </a>
          </p>
        </div>

      </div>
    `
  },

  pancreas: {
    text: `
      <div class="card">

        <div class="header">
          <img src="/assets/chupitie.png" class="logo">
          <h2 style="color:#f77f00;">
            Pancréas
          </h2>
        </div>

        <div class="section" style="border-left-color:#f77f00;">
          <h3>👨‍⚕️ Référent</h3>
          <p>
            <strong>Pr BACHET Jean-Baptiste</strong><br>
          </p>
        </div>

        <div class="section" style="border-left-color:#f77f00;">
          <h3>🏥 Établissement</h3>
          <p>
            Hôpital Pitié-Salpêtrière, AP-HP <br>
            Service d'hépato-gastro-entérologie <br>
            47-83 boulevard de l'Hôpital <br>
            75013 Paris  
          </p>
        </div>

        <div class="section" style="border-left-color:#f77f00;">
          <h3>📧 Contact</h3>
          <p>
            <a href="mailto:jean-baptiste.bachet@aphp.fr">
              📩 jean-baptiste.bachet@aphp.fr 
            </a><br>
          </p>
        </div>

      </div>
    `
  }
    
  admin: {
  text: `
    <div class="card">

      <div class="header">
        <img src="chubrest.png" class="logo">
        <h2 style="color:#6c757d;">
          Coordination administrative
        </h2>
      </div>

      <div class="section" style="border-left-color:#6c757d;">
        <h3>📋 Service</h3>
        <p>
          Coordination du réseau PAN-TOGETHER <br>
        </p>
      </div>

      <div class="section" style="border-left-color:#6c757d;">
        <h3>📧 Contact</h3>
        <p>
          <a href="mailto:kristell.oizel@chu-brest.fr">
            📩 kristell.oizel@chu-brest.fr
            Tel : 02 98 22 39 80
          </a>
        </p>
      </div>

    </div>
  `
}
};

function showInfo(organe, element) {
  const infoBox = document.getElementById("infoBox");

  // reset zones
  document.querySelectorAll('.zone, .admin-link')
  .forEach(el => el.classList.remove('active'));

element.classList.add('active');

  // couleurs
  const colors = {
    estomac: "#0077aa",
    foie: "#d62828",
    pancreas: "#f77f00"
    admin: "#6c757d"
  };

  const color = colors[organe];

  // affichage contenu
  infoBox.innerHTML = data[organe].text;

  // bordure dynamique
  infoBox.style.borderTop = `6px solid ${color}`;
}
</script>
