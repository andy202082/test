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

function dbStore(db) {
  return {
    getAll: () => run(db, 'readonly', (s) => s.getAll()),
    add: (photo) => run(db, 'readwrite', (s) => s.add(photo)),
    remove: (id) => run(db, 'readwrite', (s) => s.delete(id)),
  };
}

// IndexedDB를 쓸 수 없는 브라우저(사생활 보호 모드 등)에서는 메모리에만 보관
function memoryStore() {
  const photos = [];
  let nextId = 1;
  return {
    getAll: async () => photos.slice(),
    add: async (photo) => { photos.push({ ...photo, id: nextId++ }); },
    remove: async (id) => {
      const i = photos.findIndex((p) => p.id === id);
      if (i >= 0) photos.splice(i, 1);
    },
  };
}

const gallery = document.getElementById('gallery');
const empty = document.getElementById('empty');
const count = document.getElementById('count');
const notice = document.getElementById('notice');
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const folderInput = document.getElementById('folder-input');
const statusText = document.getElementById('status');
const viewer = document.getElementById('viewer');
const viewerImg = document.getElementById('viewer-img');
const viewerName = document.getElementById('viewer-name');
const viewerActions = document.getElementById('viewer-actions');
const confirmActions = document.getElementById('confirm-actions');

let store;
let urls = [];
let current = null;

async function render() {
  const photos = await store.getAll();
  urls.forEach(URL.revokeObjectURL);
  urls = [];
  gallery.innerHTML = '';

  // 최근에 넣은 사진이 앞에 오도록. 번호는 넣은 순서
  photos.forEach((photo, i) => { photo.no = i + 1; });
  for (const photo of photos.reverse()) {
    const url = URL.createObjectURL(photo.blob);
    urls.push(url);
    const li = document.createElement('li');
    li.tabIndex = 0;
    li.innerHTML = '<img alt=""><div class="caption"><span class="no"></span><span class="name"></span></div>';
    li.querySelector('img').src = url;
    li.querySelector('img').alt = photo.name;
    li.querySelector('.no').textContent = '#' + String(photo.no).padStart(2, '0');
    li.querySelector('.name').textContent = photo.name;
    li.addEventListener('click', () => openViewer(photo, url));
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') openViewer(photo, url);
    });
    gallery.appendChild(li);
  }

  count.textContent = `사진 ${photos.length}장`;
  empty.hidden = photos.length > 0;
}

async function addFiles(files) {
  const images = [...files].filter((f) => f.type.startsWith('image/'));
  for (const file of images) {
    await store.add({ name: file.name, blob: file, addedAt: Date.now() });
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

function showConfirm(show) {
  viewerActions.hidden = show;
  confirmActions.hidden = !show;
}

function openViewer(photo, url) {
  current = photo;
  viewerImg.src = url;
  viewerImg.alt = photo.name;
  viewerName.textContent = photo.name;
  showConfirm(false);
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
document.getElementById('delete-btn').addEventListener('click', () => showConfirm(true));
document.getElementById('cancel-delete-btn').addEventListener('click', () => showConfirm(false));
document.getElementById('confirm-delete-btn').addEventListener('click', async () => {
  if (!current) return;
  const name = current.name;
  await store.remove(current.id);
  viewer.close();
  statusText.textContent = `"${name}" 사진을 삭제했어요.`;
  await render();
});

(async () => {
  try {
    store = dbStore(await openDB());
    await store.getAll();
  } catch {
    store = memoryStore();
    notice.hidden = false;
  }
  render();
})();
