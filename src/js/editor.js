'use strict';

import { loadData } from './data-loader.js';

const POSITIONS = ['adopt', 'trial', 'assess', 'hold'];
const POSITION_COLORS = { adopt: '#1D9E75', trial: '#185FA5', assess: '#BA7517', hold: '#A32D2D' };

let techs = [];
let edits = {};

function renderCard(tech) {
  const current = edits[tech.id]?.position ?? tech.position;
  const currentNotes = edits[tech.id]?.notes ?? tech.notes ?? '';

  return `
  <div class="tech-card" id="card-${tech.id}">
    <div class="card-header">
      <span class="card-name">${tech.name}</span>
      <span class="card-category">${tech.category}</span>
    </div>
    <div class="position-buttons">
      ${POSITIONS.map(p => `
        <button class="pos-btn ${current === p ? 'active' : ''}"
          data-id="${tech.id}" data-pos="${p}"
          style="${current === p ? `--btn-color:${POSITION_COLORS[p]}` : ''}">
          ${p.toUpperCase()}
        </button>
      `).join('')}
    </div>
    <textarea class="notes-input" data-id="${tech.id}" placeholder="Notes..."
      rows="2">${currentNotes}</textarea>
  </div>`;
}

function renderAll() {
  const container = document.getElementById('cards');
  container.innerHTML = techs.map(renderCard).join('');

  container.querySelectorAll('.pos-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const pos = btn.dataset.pos;
      if (!edits[id]) edits[id] = {};
      edits[id].position = pos;
      edits[id].since = new Date().toISOString().slice(0, 7);
      const card = document.getElementById(`card-${id}`);
      card.querySelectorAll('.pos-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.pos === pos);
        b.style.setProperty('--btn-color', b.dataset.pos === pos ? POSITION_COLORS[pos] : '');
      });
      updateChangedCount();
    });
  });

  container.querySelectorAll('.notes-input').forEach(ta => {
    ta.addEventListener('input', () => {
      const id = ta.dataset.id;
      if (!edits[id]) edits[id] = {};
      edits[id].notes = ta.value;
      updateChangedCount();
    });
  });
}

function updateChangedCount() {
  const count = Object.keys(edits).filter(id => {
    const orig = techs.find(t => t.id === id);
    return (edits[id].position && edits[id].position !== orig?.position)
      || (edits[id].notes !== undefined && edits[id].notes !== (orig?.notes ?? ''));
  }).length;
  document.getElementById('changed-count').textContent =
    count > 0 ? `${count} modification${count > 1 ? 's' : ''}` : '';
}

function exportYaml() {
  const lines = ['technologies:'];
  techs.forEach(tech => {
    const pos = edits[tech.id]?.position ?? tech.position;
    const notes = edits[tech.id]?.notes ?? tech.notes ?? '';
    const since = edits[tech.id]?.since ?? tech.since ?? '';
    const sources = tech.sources || {};

    lines.push(`  - id: ${tech.id}`);
    lines.push(`    name: ${tech.name}`);
    lines.push(`    category: ${tech.category}`);
    lines.push(`    position: ${pos}`);
    if (since) lines.push(`    since: "${since}"`);
    if (tech.switching_cost) lines.push(`    switching_cost: ${tech.switching_cost}`);
    if (notes) lines.push(`    notes: "${notes.replace(/"/g, '\\"')}"`);

    const srcEntries = Object.entries(sources);
    if (srcEntries.length > 0) {
      lines.push('    sources:');
      srcEntries.forEach(([k, v]) => lines.push(`      ${k}: ${v}`));
    } else {
      lines.push('    sources: {}');
    }
    lines.push('');
  });

  document.getElementById('yaml-output').value = lines.join('\n');
  document.getElementById('export-section').style.display = 'block';
  document.getElementById('yaml-output').select();
}

function copyYaml() {
  const ta = document.getElementById('yaml-output');
  ta.select();
  document.execCommand('copy');
  const btn = document.getElementById('copy-btn');
  btn.textContent = 'Copié !';
  setTimeout(() => { btn.textContent = 'Copier'; }, 2000);
}

async function init() {
  try {
    const data = await loadData();
    techs = data.technologies;
    document.getElementById('last-update').textContent =
      new Date(data.generated_at).toLocaleString('fr-FR');

    renderAll();

    document.getElementById('export-btn').addEventListener('click', exportYaml);
    document.getElementById('copy-btn').addEventListener('click', copyYaml);
    document.getElementById('reset-btn').addEventListener('click', () => {
      edits = {};
      renderAll();
      updateChangedCount();
      document.getElementById('export-section').style.display = 'none';
    });
  } catch (err) {
    document.getElementById('cards').innerHTML =
      `<div class="error">Erreur : ${err.message}</div>`;
  }
}

init();
