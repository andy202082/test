# 배포 · 도메인 연결 가이드

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
4. `example.com` → 실제 도메인으로 교체: `site/index.html`, `site/robots.txt`, `site/sitemap.xml`
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

## 3. GitHub Pages 를 쓸 경우 (선택 C)

저장소 Settings → Pages → Source 를 "GitHub Actions" 로 바꾼 뒤 아래 파일을 `.github/workflows/pages.yml` 로 추가합니다.

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
- 기존 master1.kr PHP 견적 처리에 연결하거나
- Netlify Forms / Formspree 같은 폼 서비스, 또는 카카오 알림톡 연동 백엔드를 새로 만듭니다.
