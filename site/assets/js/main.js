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
  // 스크롤 위치(target)를 그대로 쓰지 않고 부드럽게 따라가게(lerp) 해서
  // 휴대폰 터치 스크롤에서도 문이 툭툭 끊기지 않고 묵직하게 열립니다.
  const intro = document.querySelector('.intro');
  if (intro && !reduce) {
    const stage = intro.querySelector('.stage');
    const hero = intro.querySelector('.hero-in');
    let target = 0, cur = 0, running = false;
    const measure = () => {
      const r = intro.getBoundingClientRect();
      const span = intro.offsetHeight - stage.offsetHeight;
      if (span > 40) {
        target = Math.min(1, Math.max(0, -r.top / (span * 0.92)));  // 스크롤 끝 직전에 다 열리도록 (헛스크롤 최소화)
      } else {
        // 세로로 긴 화면: 고정 없이, 문이 위로 올라가는 동안 열림
        const hd = stage.getBoundingClientRect().top - r.top + (document.querySelector('.hd')?.offsetHeight || 0);
        target = Math.min(1, Math.max(0, (hd - r.top) / (stage.offsetHeight * 0.5)));
      }
      if (!running) { running = true; requestAnimationFrame(tick); }
    };
    const paint = (p) => {
      const ease = 1 - Math.pow(1 - p, 2.2);
      stage.style.setProperty('--p', ease.toFixed(4));
      // 문틈 빛: 막 열릴 때 가장 밝고, 다 열리면 사라짐
      stage.style.setProperty('--beam', (Math.sin(Math.min(1, p * 2.4) * Math.PI) * 0.9).toFixed(3));
      hero.style.setProperty('--hs', (0.93 + 0.07 * ease).toFixed(4));
      hero.style.setProperty('--ho', (0.3 + 0.7 * ease).toFixed(4));
      intro.classList.toggle('done', p >= 0.985);
    };
    function tick() {
      cur += (target - cur) * 0.14;
      if (Math.abs(target - cur) < 0.001) cur = target;
      paint(cur);
      if (cur !== target) requestAnimationFrame(tick); else running = false;
    }
    window.addEventListener('scroll', measure, { passive: true });
    window.addEventListener('resize', measure);
    measure();
    const skip = intro.querySelector('.skip-door');
    if (skip) skip.addEventListener('click', () => {
      const y = intro.offsetTop + (intro.offsetHeight - stage.offsetHeight) * 0.85;
      window.scrollTo({ top: y, behavior: 'smooth' });
    });
  }

  // ---------------------------------------------- 4개의 문
  // PC: 문 목록이 화면에 들어오면 왼쪽부터 차례로 열림
  // 휴대폰(가로 넘김): 넘겨서 가운데 온 문이 그때 열림 → 복도를 걸으며 문을 여는 느낌
  const lists = document.querySelectorAll('.d-list');
  if (lists.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      document.querySelectorAll('.door').forEach((d) => d.classList.add('open'));
    } else {
      lists.forEach((list) => {
        const doors = [...list.querySelectorAll('.door')];
        let visible = false;
        const centered = new Set();
        const sync = () => {
          if (!visible) return;
          const carousel = getComputedStyle(list).display === 'flex';
          doors.forEach((d, i) => {
            if (d.classList.contains('open')) return;
            if (!carousel) { d.style.setProperty('--d', (i * 0.18).toFixed(2) + 's'); d.classList.add('open'); }
            else if (centered.has(d)) { d.style.setProperty('--d', '0s'); d.classList.add('open'); }
          });
        };
        new IntersectionObserver((en) => { visible = en[0].isIntersecting; sync(); }, { threshold: 0.35 }).observe(list);
        const io = new IntersectionObserver((entries) => {
          entries.forEach((x) => (x.isIntersecting ? centered.add(x.target) : centered.delete(x.target)));
          sync();
        }, { root: list, threshold: 0.7 });
        doors.forEach((d) => io.observe(d));
      });
    }
  }

  // ---------------------------------------------- 달인 라운지 분야 필터
  const tabsBox = document.querySelector('.lg-tabs');
  if (tabsBox) tabsBox.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    tabsBox.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    const f = b.dataset.f;
    document.querySelectorAll('.mcard').forEach((c) => c.classList.toggle('hide', f !== 'all' && c.dataset.g !== f));
  });

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
