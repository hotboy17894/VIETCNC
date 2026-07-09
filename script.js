const DOWNLOAD_LINK = 'https://raw.githubusercontent.com/hotboy17894/VIETCNC/main/webvietcnc/vietcnc.rbz';
const UPDATE_JSON_URL = 'https://raw.githubusercontent.com/hotboy17894/VIETCNC/main/webvietcnc/update.json';

function formatDate(dateString) {
  if (!dateString || !dateString.includes('-')) return 'Đang cập nhật';
  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function setDate(id, value) {
  const element = document.getElementById(id);
  if (!element) return;
  element.textContent = formatDate(value);
  element.setAttribute('datetime', value || '');
}

function applyReleaseInfo(data) {
  const version = data.version || '2026';
  const releaseDate = data.release_date || '';
  const minSketchUp = data.min_sketchup_version || '2021';
  const maxSketchUp = data.max_sketchup_version || '2025';
  const downloadUrl = data.download_url || DOWNLOAD_LINK;

  setText('current-version', version);
  setText('panel-version', version);
  setDate('release-date', releaseDate);
  setText('panel-date', formatDate(releaseDate));
  setText('sketchup-range', `${minSketchUp} - ${maxSketchUp}`);

  document.querySelectorAll('a[href*="vietcnc.rbz"]').forEach((link) => {
    link.href = downloadUrl;
    link.setAttribute('aria-label', `Tải VietNT phiên bản ${version}`);
  });
}

async function loadVersionInfo() {
  const fallback = {
    version: '3.2.6',
    release_date: '2026-02-14',
    min_sketchup_version: '2021',
    max_sketchup_version: '2025',
    download_url: DOWNLOAD_LINK
  };

  try {
    const response = await fetch(`${UPDATE_JSON_URL}?t=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    applyReleaseInfo({ ...fallback, ...data });
  } catch (error) {
    const localData = await loadLocalReleaseInfo();
    applyReleaseInfo(localData ? { ...fallback, ...localData } : fallback);
  }
}

async function loadLocalReleaseInfo() {
  const candidates = ['webvietcnc/update.json', 'update.json'];
  for (const path of candidates) {
    try {
      const response = await fetch(path, { cache: 'no-store' });
      if (!response.ok) continue;
      return await response.json();
    } catch (_error) {
      continue;
    }
  }
  return null;
}

function setupNavigation() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  links.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

function setupSmoothAnchors() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

function setupReveal() {
  const elements = document.querySelectorAll('.timeline article, .feature-card, .preview-copy, .preview-figure, .spec-list div, .download-panel');
  elements.forEach((element) => element.classList.add('reveal'));

  if (!('IntersectionObserver' in window)) {
    elements.forEach((element) => element.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.14 });

  elements.forEach((element) => observer.observe(element));
}

document.addEventListener('DOMContentLoaded', () => {
  loadVersionInfo();
  setupNavigation();
  setupSmoothAnchors();
  setupReveal();
});
