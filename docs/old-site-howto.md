# old.master1.kr 서버 작업 방법 (Rocky Linux · Apache · PHP)

대상 서버: **172.233.82.191** (master1.kr 기존 PHP 사이트 + emotion.master1.kr 사이트가 함께 있음)

> ⚠️ 같은 서버에 **emotion.master1.kr(이진숙 감정연구소)** 사이트가 있습니다.
> 아래 작업은 **master1.kr 설정 파일만** 고치고, 매번 `apachectl configtest` 로 확인한 뒤 반영하세요.

---

## 0. 서버 접속 · 백업 (5분)

```bash
# 내 PC 터미널(윈도우는 PowerShell)에서
ssh root@172.233.82.191          # 또는 ssh 계정명@172.233.82.191 (호스팅 업체가 준 계정)

# 접속 후: Apache 설정 전체 백업
sudo cp -a /etc/httpd /root/httpd-backup-$(date +%Y%m%d)
```

> SSH 계정을 모르면: 서버를 빌려준 곳(Linode/Akamai 계정 또는 호스팅 업체·개발사)에 접속 정보를 요청하세요.

---

## 1. 가상호스트에 `ServerAlias old.master1.kr` 추가

### 1-1. master1.kr 설정 파일 찾기

```bash
grep -Rln "master1.kr" /etc/httpd/conf.d/ /etc/httpd/conf/
```

보통 이런 파일이 나옵니다 (이름은 서버마다 다름):

| 파일 예시 | 내용 |
|---|---|
| `/etc/httpd/conf.d/master1.kr.conf` | `<VirtualHost *:80>` (http) |
| `/etc/httpd/conf.d/master1.kr-le-ssl.conf` | `<VirtualHost *:443>` (https, certbot 이 만든 파일) |
| `/etc/httpd/conf.d/emotion.master1.kr*.conf` | ❌ **건드리지 않음** |

### 1-2. 두 파일 모두 열어서 수정

```bash
sudo nano /etc/httpd/conf.d/master1.kr.conf          # 실제 이름으로
```

찾을 부분 → 아래처럼 `ServerAlias` 줄에 `old.master1.kr` 추가

```apache
<VirtualHost *:80>
    ServerName master1.kr
    ServerAlias www.master1.kr old.master1.kr      # ← old.master1.kr 추가
    DocumentRoot /var/www/...                       # (이 경로를 메모: 3·4단계에서 사용)
    ...
</VirtualHost>
```

`*-le-ssl.conf`(443) 파일도 똑같이 `ServerAlias` 에 `old.master1.kr` 추가.
(`ServerAlias` 줄이 없으면 `ServerName` 바로 아래에 `ServerAlias old.master1.kr` 한 줄 추가)

nano 저장: `Ctrl+O` → Enter → `Ctrl+X`

### 1-3. 확인 후 반영

```bash
sudo apachectl configtest        # "Syntax OK" 확인
sudo systemctl reload httpd
```

---

## 2. old.master1.kr SSL 인증서 발급 (Let's Encrypt)

```bash
# certbot 이 없으면 설치
sudo dnf install -y certbot python3-certbot-apache

# old.master1.kr 전용 인증서 발급 + Apache 443 설정 자동 연결
sudo certbot --apache -d old.master1.kr --cert-name old.master1.kr
```

- 질문이 나오면: 이메일 입력 → 약관 동의(Y) → "Redirect HTTP to HTTPS" 는 **2(Redirect)** 선택
- 만약 "어느 가상호스트에 설치할지" 물으면 **master1.kr** 쪽 파일을 고르세요 (emotion 아님)

### 기존 master1.kr·www 인증서 정리 (갱신 실패 방지)

```bash
sudo certbot certificates            # 인증서 목록: 이름(Certificate Name)과 도메인 확인
```

- `master1.kr`, `www.master1.kr` 이 들어 있는 인증서는 이제 이 서버를 가리키지 않아 **갱신 때 실패**합니다.
- 443 설정 파일(`*-le-ssl.conf`)의 아래 두 줄이 **old.master1.kr 인증서**를 가리키게 바꾼 뒤:

```apache
SSLCertificateFile    /etc/letsencrypt/live/old.master1.kr/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/old.master1.kr/privkey.pem
```

```bash
sudo apachectl configtest && sudo systemctl reload httpd
sudo certbot delete --cert-name master1.kr      # 목록에서 본 실제 이름으로 (emotion 인증서는 삭제 금지)
sudo certbot renew --dry-run                     # 갱신 테스트: 오류 없으면 완료
```

---

## 3. `https://master1.kr` 강제 이동 규칙 고치기

old.master1.kr 로 들어와도 새 홈페이지(master1.kr)로 튕기는 원인입니다.

### 3-1. 찾기

```bash
# Apache 설정 안의 이동 규칙
grep -Rn "Redirect\|RewriteRule\|RewriteCond" /etc/httpd/conf.d/master1*.conf

# 사이트 폴더(.htaccess) — DocumentRoot 경로로 바꿔서
grep -Rn "master1.kr\|HTTP_HOST" /var/www/사이트폴더/.htaccess
```

### 3-2. 흔한 형태와 고치는 법

**A. 주소를 고정해서 이동** (가장 흔함)

```apache
# 고치기 전
RewriteCond %{HTTP_HOST} !^master1\.kr$ [NC]
RewriteRule ^(.*)$ https://master1.kr/$1 [R=301,L]
```
```apache
# 고친 후: old.master1.kr 은 그대로 둠
RewriteCond %{HTTP_HOST} !^old\.master1\.kr$ [NC]
RewriteRule ^(.*)$ https://old.master1.kr/$1 [R=301,L]
```

**B. http → https 이동** (certbot 이 만든 80번 설정)

```apache
RewriteCond %{SERVER_NAME} =master1.kr [OR]
RewriteCond %{SERVER_NAME} =www.master1.kr
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
```
→ 앞 두 줄을 아래처럼 바꾸면 old 도 https 로만 이동 (도메인은 유지)
```apache
RewriteCond %{SERVER_NAME} =old.master1.kr
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
```

**C. `Redirect` 한 줄**
```apache
Redirect permanent / https://master1.kr/      # ← 이런 줄이 있으면 삭제하거나 old 로 변경
```

수정 후:
```bash
sudo apachectl configtest && sudo systemctl reload httpd
```

---

## 4. PHP 안에 고정된 사이트 주소 바꾸기

### 4-1. 찾기 (DocumentRoot 경로로 바꿔서)

```bash
cd /var/www/사이트폴더
grep -Rn "master1\.kr" --include=*.php . | grep -v "old.master1" | head -100
grep -Rn "cookie_domain\|session_set_cookie_params\|setcookie" --include=*.php . | head -30
```

### 4-2. 흔히 나오는 위치와 바꾸는 법

| 찾는 내용 | 흔한 파일 | 바꾸는 법 |
|---|---|---|
| 사이트 주소 상수 | `config.php`, `common.php`, `inc/config.php`, `_common.php` | `define('SITE_URL','https://master1.kr')` → `'https://old.master1.kr'` |
| 로그인 후 이동 | `login.php`, `login_ok.php` | `header('Location: https://master1.kr/...')` → `/...` (앞 주소 빼고 경로만) |
| 관리자 링크 | `admin/` 폴더 | `https://master1.kr/admin` → `/admin` |
| 업로드 이미지 주소 | 게시판·전문가 등록 코드 | `https://master1.kr/uploads/` → `/uploads/` |
| 쿠키 도메인 | `config.php`, `/etc/php.ini` | `cookie_domain = .master1.kr` 또는 `master1.kr` → **빈 값**(그 주소에서만) 또는 `old.master1.kr` |

> 팁: 주소를 `https://old.master1.kr/...` 로 바꾸기보다 **`/uploads/...` 처럼 앞을 빼고 경로만** 쓰면 나중에 주소가 또 바뀌어도 고칠 필요가 없습니다.

php.ini 에 쿠키 도메인이 있는지:
```bash
grep -n "session.cookie_domain" /etc/php.ini /etc/php.d/*.ini
# 값이 master1.kr 이면 비우기:  session.cookie_domain =
sudo systemctl restart php-fpm      # php-fpm 을 쓰는 경우
sudo systemctl reload httpd
```

### 4-3. DB 안에 저장된 주소 (게시글·이미지)

공지·전문가 소개 글에 이미지가 `https://master1.kr/uploads/...` 로 저장돼 있으면 새 홈페이지로 가서 깨집니다.

```bash
# 먼저 DB 백업 (DB 이름·계정은 config.php 의 DB 설정 참고)
mysqldump -u 계정 -p DB이름 > /root/db-backup-$(date +%Y%m%d).sql
```
```sql
-- 어느 표에 있는지 확인 (예: 게시판 내용 칸)
SELECT COUNT(*) FROM 표이름 WHERE 칸이름 LIKE '%https://master1.kr/uploads/%';
-- 바꾸기 (경로만 남기기)
UPDATE 표이름 SET 칸이름 = REPLACE(칸이름, 'https://master1.kr/uploads/', '/uploads/');
```
> 표·칸 이름은 사이트마다 다릅니다. 확실하지 않으면 개발사에 이 단계만 맡기세요.

---

## 5. 확인

```bash
curl -I https://old.master1.kr/              # HTTP/2 200 (인증서 오류 없음)
curl -I https://old.master1.kr/login.php     # 200 — master1.kr 로 301 이면 3단계 다시 확인
curl -I https://emotion.master1.kr/          # 200 — 감정연구소 사이트 영향 없음 확인
```

브라우저에서:
- [ ] https://old.master1.kr → 기존 달인명인 사이트 (자물쇠 정상)
- [ ] 로그인 → 로그인 후에도 주소가 old.master1.kr 유지
- [ ] 관리자 화면 · 파트너 등록 · 견적 접수 · 공지 · 이미지 정상
- [ ] https://emotion.master1.kr 정상

## 문제가 생기면 되돌리기

```bash
sudo rm -rf /etc/httpd && sudo cp -a /root/httpd-backup-날짜 /etc/httpd
sudo systemctl reload httpd
```
