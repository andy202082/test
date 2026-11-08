// 소방원 공통 스크립트

// 모바일 메뉴 열기/닫기
(function () {
  const btn = document.querySelector('.menu-btn');
  const gnb = document.getElementById('gnb');
  if (!btn || !gnb) return;
  btn.addEventListener('click', () => {
    const open = gnb.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
  gnb.addEventListener('click', (e) => {
    if (e.target.closest('a')) { gnb.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  });
})();

// 견적 폼 — TODO: 실제 접수 API(기존 PHP 또는 신규 백엔드) 연결
(function () {
  const form = document.getElementById('quote');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('견적 신청이 접수되었습니다. (시안: 아직 서버에 연결되지 않음)');
  });
})();
