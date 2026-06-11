'use strict';

import { loadData, formatNumber, trajectoryLabel, formatDate } from './data-loader.js';

const CATEGORIES = {
  languages: 'Langages',
  frameworks_front: 'Front-end',
  frameworks_back: 'Back-end',
  mobile: 'Mobile',
  databases: 'Bases de données',
  devops: 'DevOps',
  observability: 'Observabilité',
  security: 'Sécurité',
  messaging: 'Messaging',
  ai: 'IA',
};

let allTechs = [];
let sortKey = 'name';
let sortAsc = true;

function positionOrder(p) {
  return { adopt: 0, trial: 1, assess: 2, hold: 3 }[p] ?? 99;
}

function renderBadge(value, type) {
  return `<span class="badge badge-${value}">${value}</span>`;
}

function renderRow(tech) {
  const gh = tech.metrics?.github;
  const npm = tech.metrics?.npm;
  const traj = trajectoryLabel(tech.trajectory);
  const trajClass = tech.trajectory || 'stable';

  return `<tr data-id="${tech.id}">
    <td><strong>${tech.name}</strong></td>
    <td>${CATEGORIES[tech.category] || tech.category}</td>
    <td>${renderBadge(tech.position)}</td>
    <td><span class="badge badge-${trajClass}">${traj}</span></td>
    <td>${gh ? formatNumber(gh.stars) : '—'}</td>
    <td>${npm ? formatNumber(npm.downloads_weekly) : '—'}</td>
    <td>${tech.switching_cost || '—'}</td>
    <td>${formatDate(tech.metrics?.github?.fetched_at || tech.metrics?.npm?.fetched_at)}</td>
  </tr>`;
}

function getFilteredSorted() {
  const query = document.getElementById('search').value.toLowerCase();
  const posFilter = document.getElementById('filter-position').value;
  const catFilter = document.getElementById('filter-category').value;

  let result = allTechs.filter(t => {
    const matchText = !query || t.name.toLowerCase().includes(query) || (t.notes || '').toLowerCase().includes(query);
    const matchPos = !posFilter || t.position === posFilter;
    const matchCat = !catFilter || t.category === catFilter;
    return matchText && matchPos && matchCat;
  });

  result.sort((a, b) => {
    let va, vb;
    if (sortKey === 'position') { va = positionOrder(a.position); vb = positionOrder(b.position); }
    else if (sortKey === 'stars') { va = a.metrics?.github?.stars ?? -1; vb = b.metrics?.github?.stars ?? -1; }
    else if (sortKey === 'npm') { va = a.metrics?.npm?.downloads_weekly ?? -1; vb = b.metrics?.npm?.downloads_weekly ?? -1; }
    else if (sortKey === 'trajectory') { va = a.trajectory || ''; vb = b.trajectory || ''; }
    else { va = (a[sortKey] || '').toString().toLowerCase(); vb = (b[sortKey] || '').toString().toLowerCase(); }

    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  });

  return result;
}

function render() {
  const tbody = document.getElementById('tbody');
  const filtered = getFilteredSorted();
  tbody.innerHTML = filtered.length
    ? filtered.map(renderRow).join('')
    : '<tr><td colspan="8" class="loading">Aucune technologie trouvée</td></tr>';
  document.getElementById('count').textContent = `${filtered.length} technologie${filtered.length > 1 ? 's' : ''}`;
}

function setupSortHeaders() {
  document.querySelectorAll('th[data-sort]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      if (sortKey === key) {
        sortAsc = !sortAsc;
      } else {
        sortKey = key;
        sortAsc = true;
      }
      document.querySelectorAll('th[data-sort]').forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
      th.classList.add(sortAsc ? 'sort-asc' : 'sort-desc');
      render();
    });
  });
}

async function init() {
  try {
    const data = await loadData();
    allTechs = data.technologies;

    document.getElementById('last-update').textContent =
      new Date(data.generated_at).toLocaleString('fr-FR');

    const catSelect = document.getElementById('filter-category');
    const cats = [...new Set(allTechs.map(t => t.category))].sort();
    cats.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = CATEGORIES[c] || c;
      catSelect.appendChild(opt);
    });

    setupSortHeaders();

    ['search', 'filter-position', 'filter-category'].forEach(id => {
      document.getElementById(id).addEventListener('input', render);
      document.getElementById(id).addEventListener('change', render);
    });

    render();
  } catch (err) {
    document.getElementById('tbody').innerHTML =
      `<tr><td colspan="8" class="error">Erreur de chargement : ${err.message}</td></tr>`;
  }
}

init();
