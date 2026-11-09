# 배포 · 도메인 연결 가이드

## ✅ master1.kr 연결 계획 (확정: 기존 사이트는 old.master1.kr 로 유지)

| 주소 | 연결 대상 | 내용 |
|---|---|---|
| `master1.kr`, `www.master1.kr` | GitHub Pages (새 사이트) | 건물관리 달인명인 |
| `old.master1.kr` | 기존 서버 `172.233.82.191` | 기존 PHP 사이트 (로그인·파트너·견적접수·공지·관리자) |

도메인 관리: **가비아** (네임서버 ns.gabia.co.kr) — 이진숙 홈페이지(profiling.kr)와 같은 방식.

### 순서 (이 순서대로 해야 끊김이 없습니다)

**① 기존 서버가 old.master1.kr 도 받도록 설정** (서버 관리자/호스팅 업체에 요청)

> 요청 문구 예시:
> "master1.kr 서버(172.233.82.191, Apache)에서 `old.master1.kr` 도메인도 같은 사이트로 접속되도록
> 가상호스트에 ServerAlias 추가와 SSL 인증서(old.master1.kr) 발급 부탁드립니다.
> 곧 master1.kr / www.master1.kr 은 다른 곳으로 연결을 옮길 예정입니다."

Apache 직접 관리 시: 가상호스트에 `ServerAlias old.master1.kr` 추가 → `sudo certbot --apache -d old.master1.kr` → `sudo systemctl reload httpd`

**② 가비아에 old 레코드 추가** (My가비아 → DNS 관리툴 → master1.kr → 설정)

| 타입 | 호스트 | 값 |
|---|---|---|
| A | old | 172.233.82.191 |

→ `https://old.master1.kr` 로 기존 사이트가 열리는지 확인 (로그인·관리자 화면 포함)

**③ GitHub 에 도메인 등록**: https://github.com/andy202082/test/settings/pages → Custom domain `master1.kr` → Save

**④ 가비아에서 메인 주소 전환** — 기존 `@` A 레코드(172.233.82.191)와 `www` 레코드를 지우고:

| 타입 | 호스트 | 값 |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | andy202082.github.io. |

(반영 10분~최대 24시간)

**⑤ "연결 끝" 알리기** → Claude 가 `src/content.py` 의 `domain` 을 `https://master1.kr` 로 바꿔 배포·확인
→ GitHub Pages 설정에서 **Enforce HTTPS** 체크 (인증서 발급 최대 24시간)

### 옛 주소 자동 이동 (이미 반영됨, `site/404.html`)
- `about.php` → STORY, `experts.php`·`expert_view.php?id=…` → 달인 프로필(해당 달인), `service_view.php?code=…`·`inspection_view.php?code=…` → 해당 서비스 항목, `cases.php` → 해결사례, `faq.php` → FAQ
- `login`·`partners`·`request_quote`·`request_sos`·`notice`·`privacy`·`admin` → **old.master1.kr 같은 주소로**
- 새 사이트 하단에도 공지사항·파트너 등록·개인정보 처리방침 → old.master1.kr 링크

### 주의
- 기존 사이트 안에 `https://master1.kr/...` 처럼 **주소 전체를 적어 둔 링크·이미지**가 있으면 전환 후 새 사이트로 가게 됩니다. 관리자 화면·업로드 이미지 경로를 ②단계에서 확인하세요.
- master1.kr 에는 메일(MX) 설정이 없어 메일에는 영향이 없습니다 (현재 ii21@naver.com 사용).

---

## ⚡ 바로 공개 주소로 보기 (3가지 중 하나 선택)

저장소(`andy202082/test`)가 **비공개**이므로, 무료 계정이면 ② 또는 ③이 가장 쉽습니다.
설정 파일은 이미 저장소에 들어 있어서, 아래 클릭만 하면 됩니다.

### ① GitHub Pages → `https://andy202082.github.io/test/` (이진숙 홈페이지와 같은 방식 · 선택됨)
- 조건: 저장소를 **공개(Public)** 로 바꾸거나, GitHub **Pro/Team** 요금제
- 저장소 **Settings → Pages → Source: GitHub Actions** 선택 (최초 1회)
- 이 브랜치를 **main 에 합치면(merge)** `.github/workflows/deploy-pages.yml` 이 자동으로 빌드·배포
- 이후 main 에 올릴 때마다 자동 갱신 · Actions 탭에서 수동 실행(Run workflow)도 가능

### ② Netlify (비공개 저장소 무료) → `https://사이트이름.netlify.app`
1. netlify.com 가입 (GitHub 계정으로 로그인)
2. **Add new site → Import an existing project → GitHub → andy202082/test**
3. 설정은 `netlify.toml` 이 자동 적용 (빌드 `python3 src/build.py`, 게시 폴더 `site`)
4. Deploy → 공개 주소 발급. 브랜치마다 미리보기 주소도 자동 생성

### ③ Cloudflare Pages (비공개 저장소 무료, 국내 속도 좋음) → `https://siseoltong.pages.dev`
1. dash.cloudflare.com 가입 → **Workers & Pages → Create → Pages → Connect to Git**
2. `andy202082/test` 선택
3. Build command: `python3 src/build.py` · Build output directory: `site`
4. Save and Deploy → 공개 주소 발급 (브랜치별 미리보기 주소 자동 생성)

> **자체 도메인 (profiling.kr 처럼)**: 도메인을 산 뒤 `site/CNAME` 파일에 도메인 한 줄(예: `www.siseoltong.kr`)을 넣고, `src/content.py` 의 `domain` 을 바꿔 다시 빌드 → DNS 설정(아래 2번).
> 어떤 방법이든 자체 도메인은 나중에 같은 화면의 **Custom domain** 에서 연결합니다 (아래 2번).
> 자체 도메인을 연결하면 `src/content.py` 의 `domain` 값을 바꾸고 다시 빌드하세요.

---

`site/` 폴더는 빌드 과정이 필요 없는 정적 웹사이트입니다. 아래 중 하나를 고르면 됩니다.

## 선택지 비교

| 방법 | 비용 | 장점 | 비고 |
|---|---|---|---|
| **A. Cloudflare Pages** (권장) | 무료 | 빠름(국내 포함), HTTPS 자동, GitHub 푸시 시 자동 배포 | 빌드 명령 없음, 출력 폴더 `site` |
| B. Netlify | 무료 | 설정 쉬움, 폼 접수 기능 내장 | 게시 폴더 `site` |
| C. GitHub Pages | 무료 | 저장소와 바로 연동 | 아래 워크플로 추가 필요 |
| D. 기존 호스팅(master1.kr 서버) | 기존 | PHP 견적 처리와 같이 운영 | `site/` 내용을 FTP로 업로드 |

## 1. 배포 공통 순서

1. 이 저장소를 호스팅 서비스에 연결 (A·B·C) 또는 `site/` 폴더 업로드 (D)
2. 배포된 임시 주소에서 화면 확인
3. 도메인 연결 (아래 2번)
4. `src/content.py` 의 `domain` 을 실제 도메인으로 바꾸고 `python3 src/build.py` 실행 후 커밋
5. 네이버 서치어드바이저 · 구글 서치콘솔에 사이트 등록, `sitemap.xml` 제출

## 2. 도메인 연결 (DNS 설정)

도메인을 산 곳(가비아, 후이즈, 카페24 등)의 **DNS 관리** 메뉴에서 설정합니다.
정확한 값은 선택한 호스팅의 "Custom domain" 화면에 나오는 값을 우선으로 따르세요.

| 연결할 주소 | 레코드 | 값 (예시) |
|---|---|---|
| `www.도메인` | CNAME | Cloudflare: `프로젝트명.pages.dev` / Netlify: `사이트명.netlify.app` / GitHub: `계정명.github.io` |
| `도메인` (www 없이) | A 또는 ALIAS | 호스팅이 안내하는 IP. GitHub Pages는 `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |

- 반영까지 수 분 ~ 최대 48시간 걸릴 수 있습니다.
- HTTPS(자물쇠)는 연결 후 호스팅에서 자동 발급됩니다.
- 기존 master1.kr 을 그대로 쓸 경우, 기존 페이지 주소(`/about.php` 등)에서 새 주소로 **301 리다이렉트**를 걸어야 검색 순위가 유지됩니다.

## 3. GitHub Pages 워크플로 (이미 추가됨)

`.github/workflows/deploy-pages.yml` 에 아래와 같은 워크플로가 들어 있습니다 (빌드 단계 포함).

```yaml
name: Deploy site
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: github-pages
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - uses: actions/deploy-pages@v4
```

도메인을 연결하면 `site/CNAME` 파일에 도메인 한 줄(예: `www.example.com`)을 넣습니다.

## 4. 앱으로 확장

- 지금도 `manifest.webmanifest` 가 있어 휴대폰에서 **"홈 화면에 추가"** 하면 앱처럼 열립니다 (PWA).
- 오프라인 동작·푸시 알림(점검 기한 알림 등)이 필요해지면 서비스워커를 추가합니다.
- 앱스토어 등록이 필요하면 같은 웹사이트를 감싸는 방식(TWA / Capacitor)으로 진행할 수 있습니다.

## 5. 견적 폼 연결 (배포 전 필수)

현재 견적 폼은 화면만 있고 접수 서버가 없습니다 (`site/assets/js/main.js` 의 TODO).
- 페이지 HTML 은 `src/build.py` 가 만들므로, 배포 전에 항상 `python3 src/build.py` 를 실행해 최신 상태로 커밋하세요.
- 기존 master1.kr PHP 견적 처리에 연결하거나
- Netlify Forms / Formspree 같은 폼 서비스, 또는 카카오 알림톡 연동 백엔드를 새로 만듭니다.
