'use strict';

const DATA_URL = './data.json';

let _cache = null;

export async function loadData() {
  if (_cache) return _cache;
  const response = await fetch(DATA_URL);
  if (!response.ok) throw new Error(`Failed to load data.json: ${response.status}`);
  _cache = await response.json();
  return _cache;
}

export function formatNumber(n) {
  if (n == null) return '—';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
  return String(n);
}

export function trajectoryLabel(t) {
  if (t === 'rising') return '↑ rising';
  if (t === 'declining') return '↓ declining';
  return '→ stable';
}

export function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
}

export function getPositionColor(position) {
  const colors = { adopt: '#1D9E75', trial: '#185FA5', assess: '#BA7517', hold: '#A32D2D' };
  return colors[position] || '#6b7280';
}

export function getCategoryColor(category) {
  const colors = {
    languages: '#7c3aed',
    frameworks_front: '#0ea5e9',
    frameworks_back: '#06b6d4',
    mobile: '#f59e0b',
    databases: '#10b981',
    devops: '#6366f1',
    observability: '#f97316',
    security: '#ef4444',
    messaging: '#ec4899',
    ai: '#a855f7',
  };
  return colors[category] || '#6b7280';
}
