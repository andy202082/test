# -*- coding: utf-8 -*-
"""
건물관리 달인명인 정적 사이트 생성기 (외부 라이브러리 없음)

    python3 src/build.py

src/content.py 의 내용을 읽어 site/ 폴더에 HTML 페이지를 만듭니다.
CSS / JS / 이미지(site/assets)는 직접 편집합니다.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import SITE, EXPERTS, SECTION_EXPERTS, CASE_EXPERTS, CATEGORIES, STORY, FAQ  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "site")
e = html.escape

ICONS = {
    "shield": '<path d="M12 3l7 3v6c0 4.2-2.9 7.7-7 9-4.1-1.3-7-4.8-7-9V6l7-3z"/><path d="M12 8c.6 1.7 2.4 2.8 2.4 5a2.4 2.4 0 0 1-4.8 0c0-1 .5-1.8 1.1-2.4.1.8.5 1.3 1 1.5-.3-1.6 0-3 .3-4.1z"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.1L3.5 17.2a1.8 1.8 0 0 0 2.6 2.6l5.8-5.8a4 4 0 0 0 5.1-5.4l-2.4 2.4-2.3-.4-.4-2.3 2.8-2z"/>',
    "building": '<path d="M4 21V5l8-2v18M12 21h8V9l-8-2"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12l2 2 4-4M9 17h6"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z"/><path d="M4 19a2 2 0 0 1 2-2h13M9 7h6"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


ROOF = ('<svg class="roof" viewBox="0 0 60 18" aria-hidden="true"><path d="M4 16 30 3l26 13" fill="none" '
        'stroke="#E3000F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# C형 로고 (배지) — 사이트 대표 로고
BADGE = f'<span class="badge-c" aria-hidden="true">{ROOF}<b>소방</b></span>'
# 헤더/푸터 로고: [소방 배지] + 두 줄 "건물관리 / 달인명인" (두 줄 폭을 같게 맞춤)
LOGO = (BADGE + '<span class="logo-word"><span class="lw1">건물관리</span><span class="lw2" aria-label="달인명인"><i>달</i><i>인</i><i>명</i><i>인</i></span></span>')


def badge_big(sub=True):
    """C형 큰 배지: 지붕 + 소방 + 건물관리 / 달인명인"""
    s = '<span class="bc-sub">건물관리 <i>/</i> 달인명인</span>' if sub else ""
    return f'<span class="badge-c big" role="img" aria-label="소방 · 건물관리 달인명인 로고">{ROOF}<b>소방</b>{s}</span>'


# A형 엠블럼 (지붕 + 건물 + 점검 완료 체크)
EMBLEM_A = (
    '<svg class="emblem-a" viewBox="0 0 120 110" aria-hidden="true">'
    '<path d="M8 50 60 10l52 40" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M26 46h56v58H26z" fill="currentColor"/>'
    '<g fill="#fff"><rect x="34" y="56" width="12" height="12" rx="1.5"/><rect x="50" y="56" width="12" height="12" rx="1.5"/>'
    '<rect x="34" y="72" width="12" height="12" rx="1.5"/><rect x="50" y="72" width="12" height="12" rx="1.5"/></g>'
    '<circle cx="88" cy="84" r="21" fill="#E3000F" stroke="#fff" stroke-width="5"/>'
    '<path d="m78 84 7 7 13-14" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

LOCKUP_A = ('<div class="lockup-a" role="img" aria-label="건물관리 달인명인 BUILDING CARE MASTERS">' + EMBLEM_A +
            '<div><span class="la-k">건물관리</span><strong>달인명인</strong><span class="la-en">BUILDING CARE MASTERS</span></div></div>')

# B형 낙관(도장)
SEAL_B = ('<div class="seal-b" role="img" aria-label="달인명인 낙관 · 건물관리 전문">'
          '<span class="seal"><i>달</i><i>인</i><i>명</i><i>인</i></span>'
          '<div><strong>달인명인</strong><span class="sb-sub">건물관리 전문</span></div></div>')


def kcls(s, extra=""):
    """핵심 항목(key)·HOT 표시용 class 속성"""
    c = " ".join(x for x in [extra, "is-key" if s.get("key") else "", "is-hot" if s.get("hot") else ""] if x)
    return f' class="{c}"' if c else ""


def hot(s):
    return '<em class="hot">HOT</em>' if s.get("hot") else ""


# ---------------------------------------------------------------- layout
def head(title, desc, path=""):
    url = SITE["domain"].rstrip("/") + "/" + path
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="건물관리 달인명인">
<meta property="og:image" content="{e(SITE['domain'].rstrip('/'))}/assets/img/og.png">
<link rel="apple-touch-icon" href="assets/img/icon-180.png">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<link rel="canonical" href="{e(url)}">
<link rel="icon" href="assets/img/favicon-32.png" type="image/png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#E3000F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
"""


def header(active=""):
    items = []
    for c in CATEGORIES:
        subs = "".join(
            f'<li{kcls(s)}><a href="{link(c, s)}"><b>{e(s["name"])}{hot(s)}</b>'
            f'<small>{e(s["summary"])}</small></a></li>' for s in c["sections"])
        cur = ' aria-current="page"' if c["slug"] == active else ""
        story = " is-story" if c["slug"] == "story" else ""
        items.append(f"""
      <li class="nav-i{story}">
        <a class="nav-top" href="{c['slug']}.html"{cur}>{e(c['name'])}</a>
        <div class="mega" role="group" aria-label="{e(c['name'])} 하위 메뉴">
          <span class="m-leaf l" aria-hidden="true"></span><span class="m-leaf r" aria-hidden="true"></span>
          <div class="mega-in">
            <a class="m-intro" href="{c['slug']}.html">
              {icon(c['icon'], 'm-ic')}
              <span class="m-no">{c['no']} · {c['en']}</span>
              <strong>{e(c.get('title', c['name']))}</strong>
              <span class="m-q">{e(c['question'])}</span>
              {cat_avatars(c)}
              <span class="m-go">문 열고 들어가기 →</span>
            </a>
            <ul class="m-list">{subs}</ul>
          </div>
        </div>
      </li>""")
    return f"""
<header class="hd">
  <div class="wrap hd-in">
    <a href="index.html" class="logo" aria-label="건물관리 달인명인 홈">{LOGO}</a>
    <nav class="gnb" id="gnb" aria-label="주 메뉴">
      <ul class="nav">{''.join(items)}
      </ul>
      <div class="gnb-foot"><a href="tel:{SITE['tel']}">📞 {SITE['tel']}</a><a href="index.html#quote">무료 견적</a></div>
    </nav>
    <div class="hd-cta">
      <a class="tel" href="tel:{SITE['tel']}">{SITE['tel']}</a>
      <a class="btn btn-red" href="index.html#quote">무료 견적</a>
    </div>
    <button class="menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="gnb"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="main">
"""


def band():
    return f"""
<section class="band">
  <div class="wrap band-in">
    {SEAL_B}
    <h2>점검 · 공사 · 보험 · 건물관리,<br><mark>한번에 달인명인</mark>으로 끝내세요</h2>
    <div class="acts">
      <a class="btn btn-w" href="tel:{SITE['tel']}">📞 {SITE['tel']}</a>
      <a class="btn btn-y" href="index.html#quote">무료 견적 비교</a>
    </div>
  </div>
</section>"""


def footer():
    br = "".join(f"<li><b>{e(b['name'])}</b> {e(b['addr'])}</li>" for b in SITE["branches"])
    menu = "".join(f'<a href="{c["slug"]}.html">{e(c["name"])}</a>' for c in CATEGORIES)
    return f"""
</main>
<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <a href="index.html" class="logo" aria-label="건물관리 달인명인 홈">{LOGO}</a>
      <nav class="ft-menu" aria-label="하단 메뉴">{menu}</nav>
    </div>
    <div class="ft-grid">
      <div>
        <p class="ft-tel"><a href="tel:{SITE['tel']}">{SITE['tel']}</a> <span>({SITE['tel_note']})</span></p>
        <p>{e(SITE['company'])} · {e(SITE['company_desc'])}</p>
        <p>사업자등록번호 {SITE['biz_no']} · 개인정보보호 책임자 {e(SITE['privacy_officer'])} · E-mail <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      </div>
      <ul class="ft-br">{br}</ul>
    </div>
    <div class="ft-bottom">
      <span>© 2026 건물관리 달인명인 · {e(SITE['company'])}. All rights reserved.</span>
      <span class="ft-links"><a href="{SITE['old_site']}/notice.php" rel="noopener">공지사항</a><a href="{SITE['old_site']}/partners.php" rel="noopener">파트너 등록</a><a href="{SITE['old_site']}/privacy.php" rel="noopener">개인정보 처리방침</a><a href="{SITE['blog']}" rel="noopener">블로그</a></span>
    </div>
  </div>
</footer>
<nav class="mcta" aria-label="빠른 상담">
  <a class="m1" href="tel:{SITE['tel']}">전화</a>
  <a class="m2" href="{SITE['kakao']}">카톡상담</a>
  <a class="m3" href="index.html#quote">무료 견적</a>
</nav>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- components
DOOR_SLUGS = ("fire-safety", "fire-construction", "inspection", "building")  # 문으로 보여줄 4개 (STORY 제외)


def door(c, i):
    """방화문 카드 — 닫힌 채로 시작, 누르면 열리고(안쪽 메뉴판), 닫기로 다시 닫힘. 한 번에 한 문만 열림."""
    subs = "".join(f'<li{kcls(s)}><a href="{link(c, s)}">{e(s["name"])}</a></li>' for s in c["sections"])
    return f"""
    <li class="door" style="--d:0s">
      <div class="frame">
        <div class="fx">
          <div class="room" id="room-{c['slug']}">
            <button class="door-close" type="button" aria-label="{e(c['name'])} 문 닫기">닫기 ✕</button>
            <span class="r-no">No. {c['no']}</span>
            <strong class="r-ttl">{e(c.get('title', c['name']))}</strong>
            <span class="r-en">{c['en']}</span>
            <ul>{subs}</ul>
            <a class="r-enter" href="{c['slug']}.html">들어가기 →</a>
          </div>
          <span class="spill" aria-hidden="true"></span>
          <span class="leaf l" aria-hidden="true"><i class="win"></i><b class="bar"></b></span>
          <span class="leaf r" aria-hidden="true"><i class="win"></i><b class="bar"></b></span>
        </div>
        <button class="door-btn" type="button" aria-expanded="false" aria-controls="room-{c['slug']}" aria-label="{e(c['name'])} 문 열기">
          <span class="knock">똑똑 · 눌러서 열기</span>
        </button>
        <span class="plate" aria-hidden="true">{c['no']}</span>
      </div>
      <a class="d-info" href="{c['slug']}.html">
        <p class="d-no">No. {c['no']} <span>{c['en']}</span></p>
        <h3>{e(c.get('title', c['name']))}</h3>
        <p class="d-q">{e(c['question'])}</p>
        <p class="d-t">{e(c['desc'])}</p>
        {cat_avatars(c, 'd-av')}
        <span class="d-go">ENTER</span>
      </a>
    </li>"""


# ---------------------------------------------------------------- 달인 (전문가) 컴포넌트
GROUPS = {"fire": "소방", "building": "건물관리·보험", "legal": "법정점검·위생"}


def link(c, s):
    return s.get("href") or f'{c["slug"]}.html#{s["id"]}'


def expert_services(key):
    """이 달인이 맡은 콘텐츠 [(카테고리, 섹션)]"""
    out = []
    for c in CATEGORIES:
        for s in c["sections"]:
            if key in SECTION_EXPERTS.get(s["id"], []):
                out.append((c, s))
    return out


def cat_experts(c):
    keys = []
    for s in c["sections"]:
        for k in SECTION_EXPERTS.get(s["id"], []):
            if k not in keys:
                keys.append(k)
    return keys


def photo(x, cls="xph"):
    if cls.startswith("av"):  # 작은 동그라미: 미리 잘라 둔 얼굴 썸네일
        return (f'<span class="{cls}"><img src="assets/img/experts/thumb-{x["photo"]}" alt="{e(x["name"])} {e(x["honor"])}" '
                f'loading="lazy" decoding="async" width="80" height="80"></span>')
    if "fit" in cls:  # 자르지 않고 전체 표시 + 같은 사진을 흐리게 깔아 빈 곳 채움
        src = f'assets/img/experts/{x["photo"]}'
        return (f'<span class="{cls}"><span class="xph-bg" style="background-image:url({src})" aria-hidden="true"></span>'
                f'<img src="{src}" alt="{e(x["name"])} {e(x["honor"])} ({e(x["field"])})" loading="lazy" decoding="async"></span>')
    return (f'<span class="{cls}" style="--fx:{x["focus"]}%;--fy:{x.get("fy", 30)}%"><img src="assets/img/experts/{x["photo"]}" '
            f'alt="{e(x["name"])} {e(x["honor"])} ({e(x["field"])})" loading="lazy" decoding="async"></span>')


def cat_avatars(c, cls="m-av"):
    keys = cat_experts(c)
    if not keys:
        return ""
    faces = "".join(photo(EXPERTS[k], "av") for k in keys[:5])
    names = " · ".join(EXPERTS[k]["name"] for k in keys[:3]) + (f" 외 {len(keys) - 3}인" if len(keys) > 3 else "")
    return f'<span class="{cls}"><span class="av-stack">{faces}</span><span class="av-t">담당 달인 {e(names)}</span></span>'


def chip_expert(key):
    x = EXPERTS[key]
    return (f'<a class="xchip" href="experts.html#{key}">{photo(x, "av")}<span>담당 <b>{e(x["name"])} {e(x["honor"])}</b></span></a>')


def master_card(key):
    """메인 '달인 라운지' 카드"""
    x = EXPERTS[key]
    tags = "".join(f'<li>{e(s["name"])}</li>' for _, s in expert_services(key)[:3])
    return f"""
      <article class="mcard" data-g="{x['group']}"><a href="experts.html#{key}">
        <div class="mc-ph">{photo(x, "xph fit")}<span class="mc-honor">{e(x['honor'])}</span><span class="mc-yrs">{e(x['years'])}</span></div>
        <div class="mc-bd">
          <p class="mc-f">{e(x['field'])}</p>
          <h3>{e(x['name'])} <small>{e(x['honor'])}</small></h3>
          <p class="mc-q">“{e(x['quote'])}”</p>
          <ul class="mc-tags">{tags}</ul>
        </div></a></article>"""


def expert_lead(key, svc_name=None):
    """하위 콘텐츠의 대표 담당 달인 (크게)"""
    x = EXPERTS[key]
    creds = "".join(f"<li>{e(v)}</li>" for v in x["creds"])
    strengths = "".join(f"<li>{e(v)}</li>" for v in x["strengths"])
    ct, cx = x["case"]
    return f"""
  <div class="xp-lead">
    <div class="xp-ph">{photo(x, "xph fit")}<span class="xp-honor">{e(x['honor'])}</span></div>
    <div class="xp-bd">
      <p class="xp-k">이 서비스의 담당 달인 · {e(x['field'])}</p>
      <h3>{e(x['name'])} <small>{e(x['honor'])}</small><span class="xp-yrs">{e(x['years'])}</span></h3>
      <p class="xp-q">“{e(x['quote'])}”</p>
      <ul class="xp-creds">{creds}</ul>
      <ul class="xp-str">{strengths}</ul>
      <div class="xp-case"><b>대표 해결 사례 · {e(ct)}</b><p>{e(cx)}</p></div>
      <div class="xp-acts"><a class="btn btn-red sm" href="index.html#quote">{e(x['name'])} {e(x['honor'])}에게 견적</a><a class="btn btn-ghost sm" href="experts.html#{key}">프로필 전체 보기</a></div>
    </div>
  </div>"""


def expert_mini(key):
    x = EXPERTS[key]
    return (f'<a class="xp-mini" href="experts.html#{key}">{photo(x, "av lg")}<span><small>{e(x["field"])}</small>'
            f'<b>{e(x["name"])} {e(x["honor"])}</b><i>“{e(x["quote"])}”</i></span></a>')


def svc_card(C):
    facts = "".join(f"<li><small>{e(k)}</small><b>{e(v)}</b></li>" for k, v in C["facts"])
    tg = "".join(f"<li>{e(x)}</li>" for x in C["targets"])
    st = "".join(f"<li><span>{i + 1:02d}</span><b>{e(t)}</b><small>{e(d)}</small></li>" for i, (t, d) in enumerate(C["steps"]))
    return f"""
  <div class="xp-lead svc">
    <div class="xp-ph"><span class="xph"><img src="assets/img/{C['img']}" alt="{e(C['alt'])}" loading="lazy" decoding="async"></span><span class="xp-honor">{e(C['kicker'])}</span></div>
    <div class="xp-bd">
      <p class="xp-k">{e(C['kicker'])}</p>
      <h3>{e(C['title'])}</h3>
      <p class="sv-desc">{e(C['desc'])}</p>
      <ul class="sv-facts">{facts}</ul>
      <p class="sv-h">주요 점검 대상 설비</p>
      <ul class="xp-creds">{tg}</ul>
      <p class="sv-h">진행 절차</p>
      <ol class="sv-steps">{st}</ol>
      <div class="xp-case"><b>새 제도, 놓치기 전에 확인하세요</b><p>{e(C['note'])}</p></div>
      <div class="xp-acts"><a class="btn btn-red sm" href="index.html#quote">적용 대상 무료 확인</a><a class="btn btn-ghost sm" href="tel:{SITE['tel']}">전화 {SITE['tel']}</a></div>
    </div>
  </div>"""


def section_experts(s):
    if s.get("svc_card"):
        return svc_card(s["svc_card"])
    keys = SECTION_EXPERTS.get(s["id"], [])
    if not keys:
        return ""
    out = expert_lead(keys[0])
    if len(keys) > 1:
        out += '<div class="xp-more"><p>함께하는 달인</p>' + "".join(expert_mini(k) for k in keys[1:]) + "</div>"
    return out


EXT_ICONS = {
    "calendar": '<rect x="4" y="6" width="24" height="22" rx="3"/><path d="M4 12h24M10 3v6M22 3v6"/><text x="16" y="24.5" text-anchor="middle" font-size="9" font-weight="900" fill="currentColor" stroke="none">10년</text>',
    "trash": '<path d="M6 9h20M12 9V5h8v4M8 9l1.5 19h13L24 9M13 14v10M16 14v10M19 14v10"/>',
    "truck": '<path d="M3 9h16v14H3zM19 14h6l4 5v4H19z"/><circle cx="9" cy="25" r="3"/><circle cx="24" cy="25" r="3"/>',
    "globe": '<circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c4 4 4 20 0 24M16 4c-4 4-4 20 0 24"/>',
    "recycle": '<path d="M12 6l4-3 4 3M16 3v9M6 22l-2-5 5-1M4 17l8 4M26 22l2-5-5-1M28 17l-8 4"/><path d="M10 9l-4 7M22 9l4 7M10 27h12"/>',
    "flag": '<circle cx="16" cy="16" r="12"/><path d="M10 16a3 3 0 0 1 6 0 3 3 0 0 0 6 0"/><path d="M7 8l2 2M23 22l2 2M25 8l-2 2M7 24l2-2"/>',
    "coins": '<ellipse cx="13" cy="9" rx="8" ry="3"/><path d="M5 9v5c0 1.7 3.6 3 8 3s8-1.3 8-3V9M5 14v5c0 1.7 3.6 3 8 3"/><path d="M24 15v12M20 23l4 4 4-4"/>',
}


def ext_icon(name):
    return (f'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{EXT_ICONS[name]}</svg>')


def extinguisher_landing(L):
    """소화기 납품 랜딩: 히어로 → 제품 4종 → 구매 전 확인 → 대량구매 혜택 → 견적"""
    prods = "".join(
        f'<article class="xl-prod{" main" if main else ""}"><h4>{e(n)}</h4>'
        f'<img src="assets/img/ext/{img}" alt="{e(n)}" loading="lazy" decoding="async">'
        f'<span class="xl-tag">{e(tag)}</span></article>' for n, img, tag, main in L["products"])
    checks = "".join(
        f'<article class="xl-chk"><span class="xl-ic">{ext_icon(ic)}</span><h4>{e(t)}</h4><p>{e(d)}</p><small>{e(s)}</small></article>'
        for ic, t, d, s in L["checks"])
    bens = "".join(
        f'<li><span class="xl-bic">{ext_icon(ic)}</span><small>{e(a)}</small><b>{e(b)}</b></li>' for ic, a, b in L["benefits"])
    return f"""
  <div class="xl">
    <div class="xl-hero">
      <img class="xl-hero-ph" src="assets/img/ext/hero.jpg" alt="벽에 비치된 분말소화기와 소화기 표지" loading="lazy" decoding="async">
      <div class="xl-hero-t">
        <p class="xl-k">{e(L['kicker'])}</p>
        <p class="xl-tt">{e(L['title'])}</p>
        <p class="xl-sub">{e(L['sub'])}</p>
      </div>
    </div>
    <div class="xl-prods">{prods}</div>
    <h3 class="xl-bar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m7 12 3.5 3.5L17 9"/></svg><span>소화기 구매 전 <em>꼭 확인</em>하세요!</span></h3>
    <div class="xl-chks">{checks}</div>
    <div class="xl-ben">
      <h3><span>대량구매</span> 특별혜택</h3>
      <ul>{bens}</ul>
      <p>※ {e(L['benefit_note'])}</p>
      <a class="xl-cta" href="index.html#quote">대량구매 견적 문의 <span aria-hidden="true">›</span></a>
    </div>
  </div>"""


def section(c, s, idx):
    out = [f'<section class="sub-sec{" alt" if idx % 2 else ""}" id="{s["id"]}"><div class="wrap">']
    out.append(f'<p class="s-no">{c["no"]}-{idx + 1:02d}</p><h2 class="s-tt">{e(s.get("page_title", s["name"]))}{hot(s)}</h2>')
    if s.get("badge"):
        out.append(f'<p class="s-badge">🎁 {e(s["badge"])}</p>')
    if s.get("lead"):
        if s.get("intro"):  # 문서형: 제목 띠 + 소개
            out.append(f'<p class="s-band">{e(s["lead"])}</p>')
        else:
            out.append(f'<blockquote class="s-lead">“{e(s["lead"])}”</blockquote>')
    if s.get("landing"):
        out.append(extinguisher_landing(s["landing"]))
    if s.get("poster"):
        P = s["poster"]; x0, y0, x1, y1 = P["cta"]["box"]; W, H = P["w"], P["h"]
        cta = (f'<a class="poster-cta" href="{P["cta"]["href"]}" style="left:{x0/W*100:.2f}%;top:{y0/H*100:.2f}%;'
               f'width:{(x1-x0)/W*100:.2f}%;height:{(y1-y0)/H*100:.2f}%" aria-label="{e(P["cta"]["label"])}"></a>')
        txt = "".join(f"<p>{e(x)}</p>" for x in P["text"])
        out.append(f'<figure class="poster"><picture><source srcset="assets/img/{"ext/" + P["img"]}.webp" type="image/webp">'
                   f'<img src="assets/img/ext/{P["img"]}.jpg" width="{W}" height="{H}" alt="{e(P["text"][0])}" loading="lazy" decoding="async"></picture>'
                   f'{cta}<figcaption class="sr-only">{txt}</figcaption></figure>')
    if s.get("intro"):
        out.append(f'<p class="s-intro">{e(s["intro"])}</p>')
    if s.get("photos"):
        out.append('<div class="s-photos">' + "".join(
            f'<figure><img src="assets/img/{p}" alt="{e(cap)}" loading="lazy" decoding="async" width="540" height="540"><figcaption>{e(cap)}</figcaption></figure>'
            for p, cap in s["photos"]) + "</div>")
    if s.get("about"):
        (t0, d0), rest = s["about"][0], s["about"][1:]
        out.append(f'<div class="s-about"><div class="sa-def"><h3>{e(t0)}</h3><p>{e(d0)}</p></div>'
                   '<ul class="sa-eff">' + "".join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in rest) + '</ul></div>')
    if s.get("points"):
        out.append('<div class="pts">' + "".join(
            f'<div class="pt"><span>{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
            for i, (t, d) in enumerate(s["points"])) + "</div>")
    if s.get("table"):
        t = s["table"]
        th = "".join(f"<th>{e(h)}</th>" for h in t["head"])
        rows = "".join("<tr>" + "".join(f"<td>{e(v)}</td>" for v in r) + "</tr>" for r in t["rows"])
        out.append(f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')
    for tb in s.get("tables", []):  # 제목 있는 표 여러 개
        th = "".join(f"<th>{e(h)}</th>" for h in tb["head"])
        rows = "".join("<tr>" + "".join(f"<td>{e(v)}</td>" for v in r) + "</tr>" for r in tb["rows"])
        foot = f'<p class="tbl-foot">{e(tb["foot"])}</p>' if tb.get("foot") else ""
        out.append(f'<h3 class="tbl-tt">{e(tb["title"])}</h3><div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead>'
                   f'<tbody>{rows}</tbody></table></div>{foot}')
        if tb.get("bullets"):
            out.append('<ul class="s-bul">' + "".join(f"<li>{e(x)}</li>" for x in tb["bullets"]) + "</ul>")
        if tb.get("callout"):
            out.append(f'<p class="s-call">{e(tb["callout"])}</p>')
    if s.get("cases"):
        out.append('<div class="cases">' + "".join(
            f'<article class="case"><div class="ba"><div class="b"><span>BEFORE</span></div><div class="a"><span>AFTER</span></div></div>'
            f'<div class="bd"><p class="cat">{e(k)}</p><h3>{e(t)}</h3><div class="meta"><span>{e(d)}</span><span>{e(w)}</span></div>'
            f'{chip_expert(CASE_EXPERTS[i]) if i < len(CASE_EXPERTS) else ""}</div></article>'
            for i, (k, t, d, w) in enumerate(s["cases"])) + "</div>")
    if s.get("steps"):
        many = " many" if len(s["steps"]) > 6 else ""
        out.append(f'<h3 class="tbl-tt">진행 절차 {len(s["steps"])}단계</h3><ol class="steps{many}">' + "".join(
            f'<li><b>{e(t)}</b><p>{e(d)}</p></li>' for t, d in s["steps"]) + "</ol>")
    if s.get("note"):
        out.append(f'<p class="s-note">⚠️ {e(s["note"])}</p>')
    out.append(section_experts(s))
    cta = s.get("cta", f'{s["name"]} 견적 받기')
    out.append(f'<div class="s-cta"><a class="btn btn-red" href="index.html#quote">{e(cta)}</a>'
               f'<a class="btn btn-ghost" href="tel:{SITE["tel"]}">전화 상담 {SITE["tel"]}</a></div>')
    out.append("</div></section>")
    return "\n".join(out)


def page_hero(c):
    chips = "".join(f'<a href="{s.get("href", "#" + s["id"])}"{kcls(s)}>{e(s["name"])}</a>' for s in c["sections"])
    return f"""
<section class="ph">
  <div class="ph-room">
    <div class="wrap">
      <p class="crumb"><a href="index.html">홈</a> / {e(c['name'])}</p>
      <p class="ph-no">{c['no']} · {c['en']}</p>
      <h1>{e(c.get('title', c['name']))}</h1>
      <p class="ph-q">{e(c['question'])}</p>
      <p class="ph-d">{e(c['desc'])}</p>
      <div class="ph-chips">{chips}</div>
    </div>
  </div>
  <span class="ph-leaf l" aria-hidden="true"><i class="win"></i><b class="bar"></b></span>
  <span class="ph-leaf r" aria-hidden="true"><i class="win"></i><b class="bar"></b></span>
  <span class="ph-sign" aria-hidden="true">{icon(c['icon'], 'ph-ic')}<b>{e(c['name'])}</b></span>
</section>
<nav class="subtabs" aria-label="{e(c['name'])} 하위 메뉴"><div class="wrap">{''.join(
        f'<a href="{s.get("href", "#" + s["id"])}"{kcls(s)}>{e(s["name"])}</a>' for s in c["sections"])}</div></nav>"""


def other_doors(cur):
    others = [c for c in CATEGORIES if c["slug"] in DOOR_SLUGS and c["slug"] != cur]
    return '<section class="sec more-doors"><div class="wrap"><p class="eyebrow">OTHER DOORS</p><h2 class="tt">다른 문도 열어보세요</h2><ul class="d-list small">' + \
        "".join(door(c, i) for i, c in enumerate(others)) + "</ul></div></section>"


# ---------------------------------------------------------------- pages
def page_category(c):
    title = f"{c['name']} | 건물관리 달인명인 — " + ", ".join(s["name"] for s in c["sections"][:4])
    body = head(title, c["desc"], c["slug"] + ".html") + header(c["slug"]) + page_hero(c)
    body += "\n".join(section(c, s, i) for i, s in enumerate(c["sections"]))
    body += other_doors(c["slug"]) + band() + footer()
    return body


def page_story():
    c = next(x for x in CATEGORIES if x["slug"] == "story")
    origin = "".join(f"<p{' class=q' if p.startswith('“') else ''}>{e(p)}</p>" for p in STORY["origin"])
    values = "".join(f'<div class="val"><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in STORY["values"])
    prom = "".join(f"<li><span>{i + 1:02d}</span>{e(p)}</li>" for i, p in enumerate(STORY["promises"]))
    hist = "".join(f'<li><time>{e(y)}</time><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for y, t, d in STORY["history"])
    br = "".join(
        f'<article class="br"><p class="br-a">{e(b["area"])}</p><h3>{e(b["name"])}</h3><p>{e(b["addr"])}</p>'
        f'<a href="https://map.naver.com/p/search/{e(b["addr"])}" rel="noopener">지도 보기 →</a></article>'
        for b in SITE["branches"])
    body = head("STORY | 건물관리 달인명인 — 스토리와 걸어온 길", "관리소장님의 낡은 수첩에서 시작된 달인명인 이야기, 걸어온 길과 지사 안내.", "story.html")
    body += header("story") + page_hero(c)
    body += f"""
<section class="sub-sec" id="story"><div class="wrap">
  <p class="s-no">05-01</p><h2 class="s-tt">{e(STORY['origin_title'])}</h2>
  <div class="story-brand">{SEAL_B}{LOCKUP_A}</div>
  <div class="story">
    <div class="note-book" aria-hidden="true"><span>점검 일정</span><span>업체 연락처</span><span>고칠 것</span><span>보고서 제출</span><span>…</span></div>
    <div class="story-t">{origin}</div>
  </div>
  <div class="vals">{values}</div>
  <blockquote class="s-lead">“건물관리는 노하우(Know-How)가 아니라, 최적의 해결책을 가진 달인을 정확히 아는 노웨어(Know-Where) 비즈니스입니다.”</blockquote>
  <h3 class="sub-h">모두가 윈윈하는 6가지 약속</h3>
  <ol class="promises">{prom}</ol>
</div></section>
<section class="sub-sec alt" id="history"><div class="wrap">
  <p class="s-no">05-02</p><h2 class="s-tt">걸어온 길</h2>
  <ol class="timeline">{hist}</ol>
  <p class="s-note">{e(STORY['history_note'])}</p>
  <h3 class="sub-h">지사 안내</h3>
  <div class="brs">{br}</div>
  <div class="company">
    <p><b>{e(SITE['company'])}</b> · {e(SITE['company_desc'])}</p>
    <p>사업자등록번호 {SITE['biz_no']} · 대표전화 {SITE['tel']} · {SITE['email']}</p>
  </div>
</div></section>"""
    body += other_doors("story") + band() + footer()
    return body


def page_experts():
    pseudo = {"slug": "story", "no": "05", "en": "MASTERS", "name": "검증된 달인", "icon": "shield",
              "question": "우리 건물은 누가 맡게 되나요?",
              "desc": f"현장에서 검증된 달인 {len(EXPERTS)}인. 모든 서비스에 담당 달인의 이름을 겁니다.",
              "sections": [{"id": k, "name": f"{x['name']} {x['honor']}"} for k, x in EXPERTS.items()]}
    profiles = []
    for i, (k, x) in enumerate(EXPERTS.items()):
        svcs = "".join(f'<a href="{link(c, s)}">{e(c["name"])} · {e(s["name"])}</a>' for c, s in expert_services(k))
        creds = "".join(f"<li>{e(v)}</li>" for v in x["creds"])
        strengths = "".join(f"<li>{e(v)}</li>" for v in x["strengths"])
        ct, cx = x["case"]
        profiles.append(f"""
<article class="profile{' alt' if i % 2 else ''}" id="{k}"><div class="wrap pf-in">
  <div class="pf-ph">{photo(x, "xph fit")}<span class="xp-honor">{e(x['honor'])}</span></div>
  <div class="pf-bd">
    <p class="xp-k">{e(GROUPS[x['group']])} · {e(x['field'])}</p>
    <h2>{e(x['name'])} <small>{e(x['honor'])}</small><span class="xp-yrs">{e(x['years'])}</span></h2>
    <p class="pf-tag">{e(x['tagline'])}</p>
    <p class="xp-q">“{e(x['quote'])}”</p>
    <div class="pf-cols">
      <div><h3>경력 · 자격</h3><ul class="xp-creds">{creds}</ul></div>
      <div><h3>핵심 강점</h3><ul class="xp-str">{strengths}</ul></div>
    </div>
    <div class="xp-case"><b>대표 해결 사례 · {e(ct)}</b><p>{e(cx)}</p></div>
    <p class="pf-promise">{e(x['promise'])}</p>
    <div class="pf-svc"><h3>담당 서비스</h3>{svcs}</div>
    <div class="xp-acts"><a class="btn btn-red sm" href="index.html#quote">{e(x['name'])} {e(x['honor'])}에게 견적</a><a class="btn btn-ghost sm" href="tel:{SITE['tel']}">전화 {SITE['tel']}</a></div>
  </div>
</div></article>""")
    body = head("검증된 달인 | 건물관리 달인명인 — 분야별 달인 프로필",
                f"비상방송, 소방밸브, 방화셔터, 소방공사, 보험, 기계설비, 저수조까지 현장에서 검증된 달인 {len(EXPERTS)}인의 경력과 해결 사례.",
                "experts.html")
    body += header("story") + page_hero(pseudo) + "".join(profiles) + other_doors("story") + band() + footer()
    return body


def page_index():
    doors = "".join(door(c, i) for i, c in enumerate(x for x in CATEGORIES if x["slug"] in DOOR_SLUGS))
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{e(q)}</summary><div class="ans">{e(a)}</div></details>'
                  for i, (q, a) in enumerate(FAQ))
    svc = ["소방점검", "셀프점검", "비상방송/음향", "방화셔터", "지적사항공사", "스프링클러·밸브",
           "화재·누수보험", "종합건물관리", "법정점검", "관리비 절감"]
    chips = "".join(f'<label class="chip"><input type="checkbox" name="svc" value="{e(v)}"{" checked" if i == 0 else ""}><span>{e(v)}</span></label>'
                    for i, v in enumerate(svc))
    bt = ["공동주택", "빌딩·상가", "고시원·숙박", "학교·공공", "공장·창고"]
    bchips = "".join(f'<label class="chip"><input type="radio" name="bt" value="{e(v)}"{" checked" if i == 0 else ""}><span>{e(v)}</span></label>'
                     for i, v in enumerate(bt))
    cards = "".join(master_card(k) for k in EXPERTS)
    tabs = '<button type="button" class="on" data-f="all">전체 {}</button>'.format(len(EXPERTS)) + "".join(
        f'<button type="button" data-f="{g}">{e(n)} {sum(1 for x in EXPERTS.values() if x["group"] == g)}</button>' for g, n in GROUPS.items())
    br = "".join(f'<li><b>{e(b["area"])}</b><span>{e(b["addr"])}</span></li>' for b in SITE["branches"])

    body = head("건물관리 달인명인 | 소방점검 + 소방공사 + 화재·누수보험 한번에",
                "비상방송, 소방점검, 종합건물관리부터 보험까지. 전문가 배치로 가격 비교와 견적 신청을 한 곳에서 투명하고 편리하게 해결하는 건물관리 달인명인.")
    body += header()
    body += f"""
<!-- 1. 방화문 인트로: 스크롤하면 문이 열립니다 -->
<section class="intro" id="intro" aria-label="건물관리 달인명인 소개">
  <div class="stage">
    <div class="hero-in">
      <div class="wrap">
        <span class="badge">⏱ 건물 소방법 개정 및 안전관리 강화 안심 솔루션</span>
        <p class="formula"><b>소</b>방점검<span class="plus">+</span>소<b>방</b>공사<span class="plus">+</span><b>화</b>재·누수보험</p>
        <h1 class="headline">한번에 <span class="r">달인명인</span></h1>
        <p class="sub">비상방송, 소방점검, 종합건물관리부터 보험까지 전문가 배치로 가격 비교와 견적 신청을 한 곳에서 투명하고 편리하게 해결하세요.</p>
        <div class="choice">
          <a href="fire-construction.html" class="c-cost"><span class="t">돈 드는 <span class="r">소방공사</span></span><span class="d">신설·교체 공사, 여러 업체 견적 비교</span><span class="go" aria-hidden="true">→</span></a>
          <a href="#quote" class="c-fix"><span class="reco">먼저 확인하세요 · 비용 절감</span><span class="t"><span class="r">소방시설</span> 보수 수리</span><span class="d">교체 대신 고쳐 쓰는 지적사항 해결</span><span class="go" aria-hidden="true">→</span></a>
        </div>
        <a class="to-doors" href="#doors">4개의 문 둘러보기 ↓</a>
      </div>
    </div>
    <span class="beam" aria-hidden="true"></span>
    <span class="dl l" aria-hidden="true"><i class="win"><b class="sign s-red">소화전</b></i><b class="bar"></b></span>
    <span class="dl r" aria-hidden="true"><i class="win"><b class="sign s-white">방재실</b></i><b class="bar"></b></span>
    <div class="door-copy" aria-hidden="true">
      <span class="badge-glow" role="img" aria-label="소방 · 정보통신 · 기계설비 로고">{ROOF}<b>소방</b><span class="bg-sub">정보통신<i></i>기계설비</span></span>
      <p class="dc-k">BUILDING CARE MASTERS</p>
      <p class="dc-knock">똑똑!</p>
      <p class="dc-h">문을 열면,<br><span>시설물 관리실 <i>&amp;</i> 안전점검</span></p>
    </div>
    <button class="skip-door" type="button">바로 들어가기 ↘</button>
    <p class="hint" aria-hidden="true">내려서 문 열기</p>
  </div>
</section>

<!-- 2. 다섯 개의 문 (메뉴 큰 항목) -->
<section class="sec doors" id="doors" aria-labelledby="doors-title">
  <div class="wrap">
    <p class="eyebrow">FOUR DOORS</p>
    <h2 class="tt" id="doors-title">어느 문으로<br>들어가시겠어요?</h2>
    <p class="lead">문을 누르면 열립니다. 안을 둘러보고 닫은 뒤, 다음 문을 열어보세요.</p>
    <ul class="d-list">{doors}</ul>
  </div>
</section>

<!-- 2-1. 달인 라운지: 문 뒤의 사람들 -->
<section class="sec lounge" id="masters" aria-labelledby="masters-title">
  <div class="wrap">
    <div class="lg-head">
      <div>
        <p class="eyebrow">BEHIND THE DOORS</p>
        <h2 class="tt" id="masters-title">문 뒤에는,<br>검증된 달인 {len(EXPERTS)}인이 있습니다</h2>
        <p class="lead">자격증보다 해결 경험을 먼저 봅니다. 모든 서비스에 담당 달인의 이름을 걸었습니다.</p>
      </div>
      <div class="lg-tabs" role="group" aria-label="분야별 달인 보기">{tabs}</div>
    </div>
    <div class="mgrid">{cards}</div>
    <a class="more-link" href="experts.html">달인 {len(EXPERTS)}인 프로필 전체 보기 →</a>
  </div>
</section>

<!-- 3. 견적 -->
<section class="sec quote-sec" id="quote">
  <div class="wrap quote-in">
    <div>
      {LOCKUP_A}
      <p class="eyebrow">FREE QUOTE</p>
      <h2 class="tt">30초 무료 견적,<br><span class="r">사진 한 장</span>이면 충분합니다</h2>
      <p class="lead">소방서 지적 통보서나 고장 부위 사진을 올려주시면 담당 달인이 보수·교체 견적을 함께 비교해 드립니다.</p>
      <ul class="q-points"><li>평균 30분 내 담당 전문가 연락</li><li>교체보다 수리 가능 여부부터 진단</li><li>서울 · 인천 4개 지사 출동</li></ul>
    </div>
    <form class="qq" id="quote-form">
      <p class="lb">필요한 서비스 (복수 선택)</p>
      <div class="chips">{chips}</div>
      <p class="lb">건물 유형</p>
      <div class="chips">{bchips}</div>
      <label class="lb" for="q-ph">연락처</label>
      <div class="row2">
        <input class="field" id="q-nm" name="name" placeholder="이름 / 담당자" aria-label="이름">
        <input class="field" id="q-ph" name="phone" type="tel" placeholder="010-0000-0000" required>
      </div>
      <label class="upload"><input type="file" name="photo" accept="image/*">📷 지적 통보서·현장 사진 첨부 (선택)</label>
      <button class="btn btn-red" type="submit">견적 비교 받기</button>
      <p class="note">개인정보는 견적 상담 목적으로만 사용됩니다</p>
    </form>
  </div>
</section>

<!-- 4. 공사 vs 보수 -->
<section class="sec sec-alt" id="vs">
  <div class="wrap">
    <p class="eyebrow">COST SAVING</p>
    <h2 class="tt">교체부터 하지 마세요.<br><span class="r">고쳐 쓸 수 있는지</span> 먼저 봅니다</h2>
    <div class="vs">
      <div class="col cost"><span class="tag">일반 업체</span><h3>돈 드는 소방공사</h3>
        <dl><div><dt>접근 방식</dt><dd>부품·설비 전체 교체 위주</dd></div><div><dt>견적</dt><dd>업체 1곳, 비교 어려움</dd></div><div><dt>사후 관리</dt><dd>공사 후 종료</dd></div></dl>
        <p class="eg">예) 방송 랙 고장 → 시스템 통째 교체 (수백~수천만 원)</p></div>
      <div class="mid" aria-hidden="true">VS</div>
      <div class="col fix"><span class="tag">달인명인</span><h3>소방시설 보수 수리</h3>
        <dl><div><dt>접근 방식</dt><dd>원인 진단 후 필요한 부분만 수리</dd></div><div><dt>견적</dt><dd>검증된 달인 여러 명 가격 비교</dd></div><div><dt>사후 관리</dt><dd>재점검 · 월간 관리로 연결</dd></div></dl>
        <p class="eg">예) 수신기 2개 연동 비상방송 → 핵심 부품·선로 수리 30만원 내외</p></div>
    </div>
  </div>
</section>

<!-- 5. 상황별 -->
<section class="sec" id="sits">
  <div class="wrap">
    <p class="eyebrow">QUICK START</p>
    <h2 class="tt">지금 어떤 상황이신가요?</h2>
    <div class="sits">
      <a href="fire-safety.html#inspection" class="sit"><span class="ic">📅</span><b>점검 시기가<br>다가와요</b><small>작동·종합점검 일정 잡기</small></a>
      <a href="fire-construction.html#deficiency" class="sit"><span class="ic">📄</span><b>소방서 지적을<br>받았어요</b><small>통보서 사진으로 보수 견적</small></a>
      <a href="fire-construction.html#shutter" class="sit"><span class="ic">🚗</span><b>방화셔터가<br>내려왔어요</b><small>긴급 출동 · 수동 개방</small></a>
      <a href="building.html#savings" class="sit"><span class="ic">💰</span><b>관리비를<br>줄이고 싶어요</b><small>무료 관리비 진단</small></a>
      <a href="tel:{SITE['tel']}" class="sit urgent"><span class="ic">🚨</span><b>경보가 계속<br>울려요</b><small>긴급 출동 {SITE['tel']}</small></a>
    </div>
  </div>
</section>

<!-- 6. 프로세스 + 달인 -->
<section class="sec sec-alt">
  <div class="wrap">
    <p class="eyebrow">PROCESS</p>
    <h2 class="tt">점검에서 끝나지 않습니다</h2>
    <ol class="steps big"><li><b>점검</b><p>소방시설관리사가 현장 점검 및 계측</p></li><li><b>보고서 제출</b><p>결과보고서 작성 · 관할 관청 제출 대행</p></li><li><b>지적사항 보수</b><p>달인 네트워크가 견적 비교 후 바로 수리</p></li><li><b>월간 관리</b><p>다음 점검까지 상시 관리</p></li></ol>
  </div>
</section>

<!-- 7. FAQ -->
<section class="sec" id="faq">
  <div class="wrap faq-wrap">
    <div><p class="eyebrow">FAQ</p><h2 class="tt">자주 묻는 질문</h2><p class="lead">더 궁금한 점은 {SITE['tel']} 으로 전화 주세요.</p></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<!-- 8. 지사 -->
<section class="sec sec-alt" id="branches">
  <div class="wrap">
    <p class="eyebrow">BRANCHES</p>
    <h2 class="tt">서울 · 인천 4개 지사가 달려갑니다</h2>
    <ul class="br-list">{br}</ul>
    <a class="more-link" href="story.html#history">걸어온 길 · 지사 안내 →</a>
  </div>
</section>
"""
    body += band() + footer()
    return body


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(text)
    print("built", name)


def sitemap():
    base = SITE["domain"].rstrip("/")
    urls = [""] + [c["slug"] + ".html" for c in CATEGORIES] + ["experts.html"]
    body = "".join(f"  <url><loc>{base}/{u}</loc></url>\n" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")


def snapshot(ver):
    """현재 사이트를 site/<ver>/ 에 통째로 복사 (미리보기 버전, 예: 도메인/v2/).

    이진숙 홈페이지(profiling.kr)의 v1~v12 방식과 같습니다.
    루트(/)는 운영 버전, v폴더는 검토용 미리보기입니다.
    """
    import re
    import shutil
    if not re.fullmatch(r"v\d+(-[a-z0-9-]+)?", ver):
        sys.exit("버전 이름은 v1, v2, v3-test 처럼 지정하세요")
    dst = os.path.join(ROOT, ver)
    if os.path.exists(dst):
        sys.exit(f"{ver} 는 이미 있습니다. 새 번호를 쓰거나 폴더를 지운 뒤 다시 실행하세요")
    skip = re.compile(r"^(v\d+.*|CNAME|sitemap\.xml|robots\.txt|404\.html)$")
    os.makedirs(dst)
    for name in os.listdir(ROOT):
        if skip.match(name):
            continue
        src = os.path.join(ROOT, name)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, os.path.join(dst, name))
    # 미리보기 버전은 검색엔진에 노출하지 않음
    for name in os.listdir(dst):
        if name.endswith(".html"):
            p = os.path.join(dst, name)
            t = open(p, encoding="utf-8").read()
            t = t.replace("<head>\n", '<head>\n<meta name="robots" content="noindex">\n', 1)
            t = re.sub(r"<title>", f"<title>[{ver} 미리보기] ", t, count=1)
            open(p, "w", encoding="utf-8").write(t)
    print(f"snapshot -> site/{ver}/  (배포 후 주소: {SITE['domain'].rstrip('/')}/{ver}/)")


if __name__ == "__main__":
    write("index.html", page_index())
    for c in CATEGORIES:
        write(c["slug"] + ".html", page_story() if c["slug"] == "story" else page_category(c))
    write("experts.html", page_experts())
    sitemap()
    # 사용법: python3 src/build.py --snapshot v1
    if len(sys.argv) == 3 and sys.argv[1] == "--snapshot":
        snapshot(sys.argv[2])
