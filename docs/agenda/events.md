<h2>Évènements à venir</h2>
<div class="calendar">
  <div class="calendar-grid"></div>
</div>
<div class="timeline-modern" id="future-events"></div>

<h2>Évènements passés</h2>
<div class="timeline-modern past" id="past-events"></div>

<style>
.past .card {
  opacity: 0.6;
}

.past .card:hover {
  opacity: 1;
}
</style>
<script>
const events = [
  {
    date: "2026-05-22",
    displayDate: "22 Mai 2026",
    ville: "Rennes",
    titre: "Journées scientifiques Hépato-Bilio-Pancréatique",
    description: "",
    image: "/assets/onco220526.png",
    lien: "https://www.oncobretagne.fr/...",
  },
  {
    date: "2025-11-28",
    displayDate: "28 Novembre 2025",
    ville: "Saint-Malo",
    titre: "Journées scientifiques d'Oncologie Digestive",
    description: "",
    image: "/assets/oncobretagne2025.png",
    lien: "https://www.oncobretagne.fr/...",
  }
];
</script>

<script>
function renderEvents() {
  const calendar = document.querySelector('.calendar-grid');
  const futureContainer = document.getElementById('future-events');
  const pastContainer = document.getElementById('past-events');

  const today = new Date();

  // 🔥 TRI AUTOMATIQUE
  events.sort((a, b) => new Date(a.date) - new Date(b.date));

  events.forEach((event, index) => {

    const eventDate = new Date(event.date);
    const isPast = eventDate < today;

    const id = "event-" + index;

    // 📅 CALENDRIER (uniquement futur)
    if (!isPast) {
      const day = document.createElement('div');
      day.className = 'day';
      day.dataset.target = id;

      const dayNumber = event.displayDate.split(' ')[0];

      day.innerHTML = `${dayNumber}<br><span>${event.ville}</span>`;
      calendar.appendChild(day);
    }

    // 📜 CARD
    const card = document.createElement('div');
    card.className = 'card';
    card.id = id;

    card.innerHTML = `
      <div class="card-date">${event.displayDate} · ${event.ville}</div>
      <h3>${event.titre}</h3>
      ${event.description ? `<p>${event.description}</p>` : ''}
      <a href="${event.lien}" target="_blank">
        <img src="${event.image}">
      </a>
    `;

    // 🔀 FUTUR / PASSÉ
    if (isPast) {
      pastContainer.appendChild(card);
    } else {
      futureContainer.appendChild(card);
    }
  });

  initInteractions();
}

function initInteractions() {
  document.querySelectorAll('.day').forEach(day => {
    day.addEventListener('click', () => {
      const target = document.getElementById(day.dataset.target);

      target.scrollIntoView({ behavior: 'smooth', block: 'center' });

      document.querySelectorAll('.card').forEach(c => c.classList.remove('highlight'));
      target.classList.add('highlight');

      document.querySelectorAll('.day').forEach(d => d.classList.remove('active'));
      day.classList.add('active');
    });
  });
}

renderEvents();
</script>
