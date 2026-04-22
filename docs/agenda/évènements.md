<div class="month-nav" id="month-nav"></div>
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
 .month-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  border-bottom: 1px solid #eee;
}

.month-btn {
  padding: 8px 14px;
  border-radius: 20px;
  background: #f1f1f1;
  cursor: pointer;
  transition: 0.3s;
  font-size: 0.9em;
}

.month-btn:hover {
  background: #007BFF;
  color: white;
}

.month-btn.active {
  background: #007BFF;
  color: white;
} 
  }
</style>

<script>
const events = [
  {
    date : "2026-05-22",
    displayDate: "22 Mai 2026",
    ville: "Rennes",
    titre: "Journées scientifiques Hépato-Bilio-Pancréatique",
    image: "/assets/onco220526.png",
    lien: "https://www.oncobretagne.fr/wp-content/uploads/2026/01/pre-programme-hepato2026.pdf"
  },
  {
    date : "2026-06-12",
    displayDate: "12 Juin 2026",
    ville: "Dijon",
    titre: "Journées de Printemps de Cancérologie Digestive",
    image: "/assets/FFCDprintemps2026.png",
    lien: "https://www.ffcd.fr/index.php/formation/journees/614-journee-de-printemps-2026"
  },
  {
    date : "2026-06-17",
    displayDate: "17 Juin 2026",
    ville: "Nantes",
    titre: "15ème Journée Annuelle du GIRCI Grand Ouest",
    image: "/assets/GIRCIGO170626.png",
    lien: "https://my.weezevent.com/journee-du-girci"
  },
  {
    date : "2026-06-19",
    displayDate: "19-20 Juin 2026",
    ville: "Vittel",
    titre: "9ème séminaire interrégional de cancérologie digestive",
    image: "/assets/oncobfc26.png",
    lien: "https://www.onco-grandest.fr/evenements/9eme-seminaire-interregional-de-cancerologie-digestive/"
  },
  {
    date : "2026-10-07",
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
  const id = month.replace(/\s/g, '-');

monthBlock.className = 'timeline-month';
monthBlock.id = id;
monthBlock.innerHTML = month;

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
// NAVIGATION PAR MOIS
// NAVIGATION PAR MOIS
const nav = document.getElementById('month-nav');
const monthElements = [];

Object.keys(months).forEach(month => {

  const id = month.replace(/\s/g, '-');

  // bouton
  const btn = document.createElement('div');
  btn.className = 'month-btn';
  btn.innerText = month;
  btn.dataset.target = id;

  btn.addEventListener('click', () => {
    document.getElementById(id).scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  });

  nav.appendChild(btn);

  // stocker les sections
  const section = document.getElementById(id);
  if (section) {
    monthElements.push({ id, element: section, btn });
  }
});


// 🔥 SURBRILLANCE AU SCROLL
window.addEventListener('scroll', () => {

  let current = null;

  monthElements.forEach(m => {
    const rect = m.element.getBoundingClientRect();

    if (rect.top <= 120) {
      current = m;
    }
  });

  if (current) {
    document.querySelectorAll('.month-btn').forEach(b => b.classList.remove('active'));
    current.btn.classList.add('active');
  }
});

window.addEventListener('scroll', reveal);
window.addEventListener('load', reveal);
</script>
