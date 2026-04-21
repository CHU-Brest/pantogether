<script>
async function loadEvents() {
  const response = await fetch('/data/events.csv');
  const text = await response.text();

  const rows = text.split('\n').slice(1);

  const calendar = document.querySelector('.calendar-grid');
  const timeline = document.querySelector('.timeline-modern');

  rows.forEach(row => {
    if (!row.trim()) return;

    const [date, ville, titre, desc, image, lien, statut] = row.split(',');

    const id = "event-" + date;

    // CALENDRIER
    const day = document.createElement('div');
    day.className = 'day';
    day.dataset.date = date;
    day.innerHTML = date.split('-')[2] + "<br><span>" + ville + "</span>";
    calendar.appendChild(day);

    // TIMELINE
    const card = document.createElement('div');
    card.className = 'card reveal';
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

  initInteractions();
}

function initInteractions() {
  document.querySelectorAll('.day').forEach(day => {
    day.addEventListener('click', () => {
      const target = document.getElementById('event-' + day.dataset.date);

      target.scrollIntoView({ behavior: 'smooth', block: 'center' });

      document.querySelectorAll('.card').forEach(c => c.classList.remove('highlight'));
      target.classList.add('highlight');

      document.querySelectorAll('.day').forEach(d => d.classList.remove('active'));
      day.classList.add('active');
    });
  });
}

loadEvents();
</script>
