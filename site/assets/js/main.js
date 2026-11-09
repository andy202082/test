// 건물관리 달인명인 공통 스크립트
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mobile = () => window.matchMedia('(max-width: 900px)').matches;

  // ---------------------------------------------- 모바일 메뉴 (드로어 + 아코디언)
  const btn = document.querySelector('.menu-btn');
  const gnb = document.getElementById('gnb');
  if (btn && gnb) {
    btn.addEventListener('click', () => {
      const open = gnb.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    gnb.querySelectorAll('.nav-top').forEach((a) => {
      a.addEventListener('click', (e) => {
        if (!mobile()) return;
        const li = a.parentElement;
        if (!li.classList.contains('open')) { e.preventDefault(); }
        gnb.querySelectorAll('.nav-i.open').forEach((x) => x !== li && x.classList.remove('open'));
        li.classList.toggle('open');
      });
    });
    gnb.addEventListener('click', (e) => {
      const a = e.target.closest('.m-list a, .m-intro, .gnb-foot a');
      if (a && mobile()) { gnb.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
    });
  }
  // 데스크톱: ESC 로 메가메뉴 닫기
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.activeElement && document.activeElement.closest('.nav-i')) document.activeElement.blur();
  });

  // ---------------------------------------------- 인트로: 스크롤에 따라 방화문이 열림
  const intro = document.querySelector('.intro');
  if (intro && !reduce) {
    const stage = intro.querySelector('.stage');
    const hero = intro.querySelector('.hero-in');
    let ticking = false;
    const update = () => {
      ticking = false;
      const r = intro.getBoundingClientRect();
      const span = intro.offsetHeight - stage.offsetHeight;
      const p = Math.min(1, Math.max(0, -r.top / (span * 0.75)));
      const ease = 1 - Math.pow(1 - p, 2);
      stage.style.setProperty('--p', ease.toFixed(4));
      hero.style.setProperty('--hs', (0.92 + 0.08 * ease).toFixed(4));
      hero.style.setProperty('--ho', (0.35 + 0.65 * ease).toFixed(4));
      intro.classList.toggle('done', p >= 0.98);
    };
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
    const skip = intro.querySelector('.skip-door');
    if (skip) skip.addEventListener('click', () => {
      const y = intro.offsetTop + (intro.offsetHeight - stage.offsetHeight) * 0.85;
      window.scrollTo({ top: y, behavior: 'smooth' });
    });
  }

  // ---------------------------------------------- 5개의 문: 화면에 들어오면 차례로 열림
  const doors = document.querySelectorAll('.door');
  if (doors.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      doors.forEach((d) => d.classList.add('open'));
    } else {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('open'); io.unobserve(en.target); } });
      }, { threshold: 0.45 });
      doors.forEach((d) => io.observe(d));
    }
  }

  // ---------------------------------------------- 하위 페이지 히어로 문 열기
  const ph = document.querySelector('.ph');
  if (ph) setTimeout(() => ph.classList.add('open'), reduce ? 0 : 350);

  // ---------------------------------------------- 하위 탭 현재 위치 표시
  const tabs = document.querySelectorAll('.subtabs a');
  if (tabs.length && 'IntersectionObserver' in window) {
    const map = new Map([...tabs].map((a) => [a.getAttribute('href').slice(1), a]));
    const io2 = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          tabs.forEach((t) => t.classList.remove('on'));
          const t = map.get(en.target.id);
          if (t) { t.classList.add('on'); t.scrollIntoView({ block: 'nearest', inline: 'center' }); }
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io2.observe(s); });
  }

  // ---------------------------------------------- 견적 폼 — TODO: 실제 접수 서버 연결
  const form = document.getElementById('quote-form');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    let msg = form.querySelector('.q-done');
    if (!msg) { msg = document.createElement('p'); msg.className = 'q-done'; msg.setAttribute('role', 'status'); form.appendChild(msg); }
    msg.textContent = '견적 신청 내용이 준비되었습니다. (시안: 아직 접수 서버에 연결되지 않아 실제로 전송되지는 않습니다)';
  });
})();
