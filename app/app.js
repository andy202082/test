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
const folderInput = document.getElementById('folder-input');
const statusText = document.getElementById('status');
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
  statusText.textContent = images.length
    ? `사진 ${images.length}장을 불러왔어요.`
    : '불러올 사진이 없어요.';
  await render();
}

// 끌어다 놓은 폴더 안의 파일을 하위 폴더까지 모두 꺼냄
async function filesFromEntry(entry) {
  if (entry.isFile) {
    return [await new Promise((resolve, reject) => entry.file(resolve, reject))];
  }
  const reader = entry.createReader();
  const files = [];
  // readEntries는 한 번에 일부만 돌려주므로 빈 배열이 나올 때까지 반복
  while (true) {
    const entries = await new Promise((resolve, reject) => reader.readEntries(resolve, reject));
    if (!entries.length) break;
    for (const child of entries) files.push(...(await filesFromEntry(child)));
  }
  return files;
}

async function filesFromDrop(dataTransfer) {
  const entries = [...dataTransfer.items]
    .map((item) => item.webkitGetAsEntry && item.webkitGetAsEntry())
    .filter(Boolean);
  if (!entries.length) return [...dataTransfer.files];
  const files = [];
  for (const entry of entries) files.push(...(await filesFromEntry(entry)));
  return files;
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

folderInput.addEventListener('change', () => {
  addFiles(folderInput.files);
  folderInput.value = '';
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('over');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('over'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('over');
  // 이벤트가 끝나면 dataTransfer를 못 읽으므로 먼저 꺼내 둠
  filesFromDrop(e.dataTransfer).then(addFiles);
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
