# Contact 
<ul>
<li><strong>Oesophage, Jonction Oeso-gastrique, Estomac :</strong></li> <br>
<strong>Pr METGES Jean-Philippe</strong> & <strong>Dr BOURBONNE Vincent</strong> <br>
CHU Brest - Hôpital de La Cavale Blanche <br>
Institut de Cancérologie et d’Imagerie - Pôle 7 - 1er étage <br>
Boulevard Tanguy Prigent, 29200 Brest <br>
jean-philippe.metges@chu-brest.fr <br>
BOURBONV@tcd.ie <br>
<br>
<li><strong>Foie et Voies Biliaires :</strong></li> <br>
<strong>Pr GANNE-CARRIE Nathalie</strong> & <strong>Pr NAHON Pierre</strong> <br>
Hôpital Avicenne, AP-HP <br>
Service d'Hépatologie et d'oncologie Hépatique, Batiment Larrey A <br>
125 rue de Stalingrad, 93000 Bobigny <br>
nathalie.ganne@aphp.fr <br>
pierre.nahon@aphp.fr <br>
Tel secrétariat : 01 48 02 68 03 <br>
<br>
<li><strong>Pancréas :</strong></li> <br>
<strong>Pr BACHET Jean-Baptiste</strong> <br> 
Hôpital Pitié-Salpêtrière, AP-HP <br>
Service d'hépato-gastro-entérologie <br>
47-83 boulevard de l'Hôpital, 75013 Paris <br>
jean-baptiste.bachet@aphp.fr <br>
<br>
<li><strong>Coordinatrice administrative du réseau</strong></li> <br>
<strong>OIZEL Kristell</strong> <br>
Institut de Cancérologie et d’Imagerie - Pôle 7 - 1er étage <br>
CHU Brest - Hôpital de La Cavale Blanche <br>
Boulevard Tanguy Prigent - 29200 BREST <br>
kristell.oizel@chu-brest.fr <br>
Tel : 02 98 22 39 80 <br> 
</ul>

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Logo interactif</title>
  <style>
    .container {
      display: flex;
      gap: 40px;
      align-items: center;
    }

    .image-container {
      position: relative;
      width: 400px;
    }

    .image-container img {
      width: 100%;
    }

    .zone {
      position: absolute;
      cursor: pointer;
    }

    /* Exemple positions (à ajuster !) */
    .estomac {
      top: 60px;
      left: 120px;
      width: 100px;
      height: 120px;
    }

    .foie {
      top: 120px;
      left: 90px;
      width: 140px;
      height: 80px;
    }

    .info {
      width: 300px;
      font-size: 16px;
    }
  </style>
</head>
<body>

<div class="container">
  
  <div class="image-container">
    <img src="logo.png" alt="Logo">

    <div class="zone estomac" onclick="showInfo('estomac')"></div>
    <div class="zone foie" onclick="showInfo('foie')"></div>

  </div>

  <div class="info" id="infoBox">
    Clique sur un organe 👈
  </div>

</div>

<script>
function showInfo(organe) {
  const infoBox = document.getElementById("infoBox");

  if (organe === "estomac") {
    infoBox.innerHTML = "<h3>Estomac</h3><p>L'estomac digère les aliments.</p>";
  }

  if (organe === "foie") {
    infoBox.innerHTML = "<h3>Foie</h3><p>Le foie filtre les toxines et produit la bile.</p>";
  }
}
</script>

</body>
</html>
