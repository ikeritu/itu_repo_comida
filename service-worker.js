const CACHE_NAME = 'recetario-video-lab-v3-2';
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './data/recetas_video_lab_v3.json',
  './assets/thumbs/01_contact_sheet.jpg', './assets/thumbs/02_contact_sheet.jpg', './assets/thumbs/03_contact_sheet.jpg', './assets/thumbs/04_contact_sheet.jpg', './assets/thumbs/05_tartitas_infantiles_yogur_frambuesas.jpg',
  './assets/videos/01_cremoso_chocolate_proteico.mp4', './assets/videos/02_patatas_fritas_airfryer.mp4', './assets/videos/03_trenza_pan_ajo_queso.mp4', './assets/videos/04_guacamole_no_oxida.mp4', './assets/videos/05_tartitas_infantiles_yogur_frambuesas.mp4'
];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).catch(() => undefined));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))));
});
self.addEventListener('fetch', event => {
  event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));
});
