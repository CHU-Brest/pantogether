<h2>Agenda</h2>

<div class="calendar">
  <div class="calendar-grid"></div>
</div>

<div class="timeline-modern"></div>

<style>
.calendar {
  margin-bottom: 40px;
}

.calendar-grid {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.day {
  background: #f1f1f1;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  min-width: 70px;
  transition: 0.3s;
}

.day:hover {
  background: #007BFF;
  color: white;
}

.day span {
  font-size: 0.8em;
  display: block;
}

.day.active {
  background: #007BFF;
  color: white;
}


/* TIMELINE */
.timeline-modern {
  display: grid;
  gap: 30px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.08);
  transition: 0.3s;
}

.card.highlight {
  border: 2px solid #007BFF;
}

.card:hover {
  transform: translateY(-5px);
}

.card img {
  margin-top: 10px;
  max-width: 100%;
  border-radius: 8px;
  transition: 0.3s;
}

.card img:hover {
  transform: scale(1.05);
}


/* ANIMATION */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: 0.6s;
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
</style>
<script>
async function loadEvents() {
  const response = await fetch('https://CHU-Brest.github.io/pantogether/data/events.csv');
  const text = await response.text();

  const rows = text.split('\n').slice(1);

  console.log(rows); // DEBUG

  const calendar = document.querySelector('.calendar-grid');
  const timeline = document.querySelector('.timeline-modern');

  rows.forEach(row => {
    if (!row.trim()) return;

    const [date, ville, titre, desc, image, lien, statut] = row.split('\t').map(e => e.trim());
    console.log(row.split('\t'));

    const [j, m, a] = date.split('/');
const id = "event-" + a + "-" + m + "-" + j;
    
    const day = document.createElement('div');
    day.className = 'day';
    day.dataset.date = date;
    const [jour, mois, annee] = date.split('/');

day.innerHTML = jour + "<br><span>" + ville + "</span>";
    calendar.appendChild(day);

    const card = document.createElement('div');
    card.className = 'card';
    card.id = id;

    card.innerHTML = `
      <div class="card-date">${date} · ${ville}</div>
      <h3>${titre}</h3>
      ${desc ? `<p>${desc}</p>` : ''}
      <a href="${lien}" target="_blank">
        <img src="${image}">
      </a>
    `;

    timeline.appendChild(card);
  });
}

loadEvents();
</script>
