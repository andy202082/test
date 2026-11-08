# 소방원 웹사이트

소방점검 + 소방공사 + 화재·누수보험을 **한번에** 해결하는 "소방원" 웹사이트 프로젝트입니다.
(기존 master1.kr 사이트를 소방 중심으로 개편)

## 폴더 구조

```
.
├─ site/                    ← 실제 배포되는 웹사이트 (이 폴더만 서버/호스팅에 올리면 됨)
│  ├─ index.html            메인(랜딩) 페이지
│  ├─ 404.html              없는 주소 안내 페이지
│  ├─ pages/                하위 페이지 (소방점검 상세, 보수 견적 등) 추가 위치
│  ├─ assets/
│  │  ├─ css/style.css      공통 디자인 (색상·글꼴은 맨 위 :root 변수에서 변경)
│  │  ├─ js/main.js         공통 동작 (모바일 메뉴, 견적 폼)
│  │  └─ img/               로고·아이콘·이미지
│  ├─ manifest.webmanifest  앱(홈 화면 추가, PWA) 설정
│  ├─ robots.txt            검색엔진 허용 설정
│  └─ sitemap.xml           검색엔진용 페이지 목록
└─ docs/                    기획·운영 문서
   ├─ master1-fire-renewal-plan.md   기존 사이트 분석 + 소방 중심 개편 기획
   ├─ DEPLOY.md             도메인 연결·배포 방법
   ├─ CHANGELOG.md          작업 기록
   └─ previews/             화면 캡처
```

## 개발하면서 화면 보기

```bash
npx live-server@1.2.2 site --port=8080
```

파일을 저장하면 열려 있는 브라우저가 자동으로 새로고침됩니다.

## 브랜드 기본값

| 항목 | 값 |
|---|---|
| 이름 | 소방원 |
| 메인 카피 | 소방점검 + 소방공사 + 화재·누수보험, 한번에 소방원 |
| 메인 색 | 빨강 `#E3000F` · 노랑 `#FFE600` · 진회색 `#16181D` |
| 글꼴 | Noto Sans KR |
| 대표전화 | 1555-5048 |

## 도메인 연결 전 바꿔야 할 것

`example.com` 을 실제 도메인으로 바꿉니다: `site/index.html`(canonical), `site/robots.txt`, `site/sitemap.xml`.
자세한 절차는 [docs/DEPLOY.md](docs/DEPLOY.md) 참고.
