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

// 회원가입: claude.ai 계정으로 본인을 확인하고, 닉네임을 정해 회원 명단(members)에 등록.
// 비밀번호는 받지 않아요. claude.ai 밖(내 컴퓨터에서 연 파일 등)에서는 이 부분이 숨겨져요.
const account = document.getElementById('account');
const welcome = document.getElementById('welcome');
const signupBtn = document.getElementById('signup-btn');
const editBtn = document.getElementById('edit-btn');
const membersSection = document.getElementById('members');
const memberCount = document.getElementById('member-count');
const memberList = document.getElementById('member-list');
const membersEmpty = document.getElementById('members-empty');
const signup = document.getElementById('signup');
const signupForm = document.getElementById('signup-form');
const signupTitle = document.getElementById('signup-title');
const nicknameInput = document.getElementById('nickname');
const introInput = document.getElementById('intro');
const agreeInput = document.getElementById('agree');
const signupError = document.getElementById('signup-error');
const signupSubmit = document.getElementById('signup-submit');
const withdrawBtn = document.getElementById('withdraw-btn');
const formActions = document.getElementById('form-actions');
const withdrawConfirm = document.getElementById('withdraw-confirm');

let membersRef = null;
let myId = null;
let members = [];

function myProfile() {
  return members.find((m) => m.id === myId) || null;
}

function renderMembers() {
  const me = myProfile();
  welcome.textContent = me ? `${me.nickname}님` : '';
  signupBtn.hidden = !!me;
  editBtn.hidden = !me;

  memberCount.textContent = members.length;
  membersEmpty.hidden = members.length > 0;
  memberList.innerHTML = '';
  for (const m of members) {
    const li = document.createElement('li');
    li.className = m.id === myId ? 'me' : '';
    li.innerHTML = '<span class="nick"></span><span class="intro"></span><span class="badge"></span>';
    li.querySelector('.nick').textContent = m.nickname;
    li.querySelector('.intro').textContent = m.intro || '';
    li.querySelector('.badge').textContent = m.id === myId ? '나' : '';
    memberList.appendChild(li);
  }
}

function showWithdrawConfirm(show) {
  formActions.hidden = show;
  withdrawConfirm.hidden = !show;
}

function openSignup() {
  const me = myProfile();
  signupTitle.textContent = me ? '내 정보' : '회원가입';
  signupSubmit.textContent = me ? '저장' : '가입하기';
  nicknameInput.value = me ? me.nickname : '';
  introInput.value = me ? me.intro || '' : '';
  agreeInput.checked = !!me;
  withdrawBtn.hidden = !me;
  signupError.textContent = '';
  showWithdrawConfirm(false);
  signup.showModal();
  nicknameInput.focus();
}

function errorMessage(e) {
  if (e && e.code === 'invalid_argument') {
    return '이 페이지에 글을 남길 권한이 없어서 가입할 수 없어요. 페이지 주인에게 참여(Contributor) 권한을 요청하세요.';
  }
  if (e && e.code === 'quota_exceeded') return '회원 명단이 가득 찼어요. 페이지 주인에게 알려 주세요.';
  return '저장하지 못했어요. 잠시 후 다시 시도해 주세요.';
}

signupBtn.addEventListener('click', openSignup);
editBtn.addEventListener('click', openSignup);
document.getElementById('signup-cancel').addEventListener('click', () => signup.close());

signupForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const nickname = nicknameInput.value.trim();
  const intro = introInput.value.trim();
  const me = myProfile();

  if (nickname.length < 2) {
    signupError.textContent = '닉네임을 2자 이상 적어 주세요.';
    return nicknameInput.focus();
  }
  const taken = members.some(
    (m) => m.id !== myId && m.nickname.toLowerCase() === nickname.toLowerCase()
  );
  if (taken) {
    signupError.textContent = '이미 쓰고 있는 닉네임이에요. 다른 닉네임을 골라 주세요.';
    return nicknameInput.focus();
  }
  if (!agreeInput.checked) {
    signupError.textContent = '공개에 동의해야 가입할 수 있어요.';
    return agreeInput.focus();
  }

  signupSubmit.disabled = true;
  try {
    await membersRef.doc(myId).set({
      nickname,
      intro,
      joinedAt: me ? me.joinedAt : Date.now(),
    });
    signup.close();
    statusText.textContent = me ? '내 정보를 저장했어요.' : `${nickname}님, 가입을 환영해요!`;
  } catch (err) {
    signupError.textContent = errorMessage(err);
  } finally {
    signupSubmit.disabled = false;
  }
});

withdrawBtn.addEventListener('click', () => showWithdrawConfirm(true));
document.getElementById('withdraw-cancel').addEventListener('click', () => showWithdrawConfirm(false));
document.getElementById('withdraw-ok').addEventListener('click', async () => {
  try {
    await membersRef.doc(myId).delete();
    signup.close();
    statusText.textContent = '탈퇴했어요. 언제든 다시 가입할 수 있어요.';
  } catch (err) {
    showWithdrawConfirm(false);
    signupError.textContent = errorMessage(err);
  }
});

(async () => {
  if (!window.claude || !window.claude.use) return;
  const [db, user] = await Promise.all([window.claude.use('db'), window.claude.use('user')]);
  if (!db || !user) return;
  myId = await user.id();
  if (!myId) return; // 로그인하지 않은 방문자

  membersRef = db.collection('members');
  account.hidden = false;
  membersSection.hidden = false;
  membersRef.orderBy('joinedAt').onSnapshot(
    (snap) => {
      members = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
      renderMembers();
    },
    () => {
      // 명단을 더 이상 받을 수 없으면 회원 기능을 숨김
      account.hidden = true;
      membersSection.hidden = true;
    }
  );
})();
