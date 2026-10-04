// 사진통: 사진을 브라우저(IndexedDB)에 저장하고 보여주는 앱

const DB_NAME = 'photo-box';
const STORE = 'photos';

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(STORE, { keyPath: 'id', autoIncrement: true });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function run(db, mode, action) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, mode);
    const req = action(tx.objectStore(STORE));
    tx.oncomplete = () => resolve(req.result);
    tx.onerror = () => reject(tx.error);
  });
}

const gallery = document.getElementById('gallery');
const empty = document.getElementById('empty');
const count = document.getElementById('count');
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const viewer = document.getElementById('viewer');
const viewerImg = document.getElementById('viewer-img');
const viewerName = document.getElementById('viewer-name');

let db;
let urls = [];
let current = null;

async function render() {
  const photos = await run(db, 'readonly', (s) => s.getAll());
  urls.forEach(URL.revokeObjectURL);
  urls = [];
  gallery.innerHTML = '';

  // 최근에 넣은 사진이 앞에 오도록
  for (const photo of photos.reverse()) {
    const url = URL.createObjectURL(photo.blob);
    urls.push(url);
    const li = document.createElement('li');
    const img = document.createElement('img');
    img.src = url;
    img.alt = photo.name;
    img.addEventListener('click', () => openViewer(photo, url));
    li.appendChild(img);
    gallery.appendChild(li);
  }

  count.textContent = `사진 ${photos.length}장`;
  empty.hidden = photos.length > 0;
}

async function addFiles(files) {
  const images = [...files].filter((f) => f.type.startsWith('image/'));
  for (const file of images) {
    await run(db, 'readwrite', (s) =>
      s.add({ name: file.name, blob: file, addedAt: Date.now() })
    );
  }
  await render();
}

function openViewer(photo, url) {
  current = photo;
  viewerImg.src = url;
  viewerImg.alt = photo.name;
  viewerName.textContent = photo.name;
  viewer.showModal();
}

fileInput.addEventListener('change', () => {
  addFiles(fileInput.files);
  fileInput.value = '';
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('over');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('over'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('over');
  addFiles(e.dataTransfer.files);
});

document.getElementById('close-btn').addEventListener('click', () => viewer.close());
document.getElementById('delete-btn').addEventListener('click', async () => {
  if (!current || !confirm(`"${current.name}" 사진을 삭제할까요?`)) return;
  await run(db, 'readwrite', (s) => s.delete(current.id));
  viewer.close();
  await render();
});

openDB().then((d) => {
  db = d;
  render();
});
