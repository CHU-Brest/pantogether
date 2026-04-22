<h2>Agenda</h2>

<div class="timeline" id="timeline"></div>

<style>
.timeline {
  position: relative;
  max-width: 900px;
  margin: 50px auto;
}

.timeline::after {
  content: '';
  position: absolute;
  width: 4px;
  background: #ddd;
  top: 0;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  width: 50%;
  padding: 20px 40px;
  opacity: 0;
  transform: translateY(40px);
  transition: 0.6s;
}

.timeline-item.show {
  opacity: 1;
  transform: translateY(0);
}

.timeline-item.left { left: 0; }
.timeline-item.right { left: 50%; }

.timeline-item::before {
  content: '';
  position: absolute;
  top: 30px;
  width: 16px;
  height: 16px;
  background: #007BFF;
  border-radius: 50%;
  z-index: 1;
}

.timeline-item.left::before { right: -8px; }
.timeline-item.right::before { left: -8px; }

.content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.08);
  transition: 0.3s;
}

.content:hover {
  transform: translateY(-5px);
}

.content img {
  margin-top: 10px;
  max-width: 100%;
  border-radius: 6px;
}

.date {
  font-size: 0.9em;
  color: #007BFF;
  font-weight: bold;
}

/* MOBILE */
@media screen and (max-width: 768px) {
  .timeline::after { left: 20px; }

  .timeline-item {
    width: 100%;
    padding-left: 60px;
    padding-right: 20px;
  }

  .timeline-item.right { left: 0; }

  .timeline-item.left::before,
  .timeline-item.right::before {
    left: 12px;
  }
  .timeline-month {
  text-align: center;
  font-weight: bold;
  font-size: 1.2em;
  margin: 40px 0 20px;
  color: #333;
  letter-spacing: 1px;
}
}
</style>

<script>
const events = [
  {
    date : "2026-05-22"
    displayDate: "22 Mai 2026",
    ville: "Rennes",
    titre: "Journées scientifiques Hépato-Bilio-Pancréatique",
    image: "/assets/onco220526.png",
    lien: "https://www.oncobretagne.fr/wp-content/uploads/2026/01/pre-programme-hepato2026.pdf"
  },
  {
    displayDate: "12 Juin 2026",
    ville: "Dijon",
    titre: "Journées de Printemps de Cancérologie Digestive",
    image: "/assets/FFCDprintemps2026.png",
    lien: "https://www.ffcd.fr/index.php/formation/journees/614-journee-de-printemps-2026"
  },
  {
    displayDate: "17 Juin 2026",
    ville: "Nantes",
    titre: "15ème Journée Annuelle du GIRCI Grand Ouest",
    image: "/assets/GIRCIGO170626.png",
    lien: "https://my.weezevent.com/journee-du-girci"
  },
  {
    displayDate: "19-20 Juin 2026",
    ville: "Vittel",
    titre: "9ème séminaire interrégional de cancérologie digestive",
    image: "/assets/oncobfc26.png",
    lien: "https://www.onco-grandest.fr/evenements/9eme-seminaire-interregional-de-cancerologie-digestive/"
  },
  {
    displayDate: "07-09 Octobre 2026",
    ville: "Strasbourg",
    titre: "99ème Journées Scientifiques de l'AFEF",
    image: "/assets/AFEF2026.png",
    lien: "https://www.congres-afef.com/"
  }
];

// 🔥 TRI PAR DATE
events.sort((a, b) => new Date(a.date) - new Date(b.date));

// 🔥 GROUPEMENT PAR MOIS
const months = {};

events.forEach(event => {
  const d = new Date(event.date);
  const key = d.toLocaleString('fr-FR', { month: 'long', year: 'numeric' });

  if (!months[key]) months[key] = [];
  months[key].push(event);
});

const timeline = document.getElementById('timeline');

let index = 0;

// 🔥 AFFICHAGE
for (const month in months) {

  // TITRE DU MOIS
  const monthBlock = document.createElement('div');
  monthBlock.className = 'timeline-month';
  monthBlock.innerHTML = month.toUpperCase();

  timeline.appendChild(monthBlock);

  // EVENTS DU MOIS
  months[month].forEach(event => {

    const side = index % 2 === 0 ? 'left' : 'right';

    const item = document.createElement('div');
    item.className = 'timeline-item ' + side;

    item.innerHTML = `
      <div class="content">
        <span class="date">${event.displayDate} · ${event.ville}</span>
        <h3>${event.titre}</h3>
        <a href="${event.lien}" target="_blank">
          <img src="${event.image}">
        </a>
      </div>
    `;

    timeline.appendChild(item);
    index++;
  });
}

// ANIMATION
function reveal() {
  const items = document.querySelectorAll('.timeline-item');
  const trigger = window.innerHeight * 0.85;

  items.forEach(item => {
    const top = item.getBoundingClientRect().top;
    if (top < trigger) item.classList.add('show');
  });
}

window.addEventListener('scroll', reveal);
window.addEventListener('load', reveal);
</script>
