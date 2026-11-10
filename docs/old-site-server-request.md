# 서버 관리자 요청: old.master1.kr 연결

## 보낼 메시지 (복사해서 전달)

---

안녕하세요. master1.kr 사이트 서버(IP **172.233.82.191**, Rocky Linux · Apache) 관련 요청드립니다.

**배경**
- master1.kr / www.master1.kr 도메인은 새 홈페이지(GitHub Pages)로 연결을 옮겼습니다.
- 기존 PHP 사이트(로그인 · 파트너 등록 · 견적 접수 · 공지 · 관리자)는 **old.master1.kr** 주소로 계속 사용하려고 합니다.
- 가비아 DNS에 `old.master1.kr → 172.233.82.191` A 레코드는 이미 추가해 두었습니다.

**현재 증상**
- https://old.master1.kr 접속 시 기존 master1.kr 사이트가 아니라 **emotion.master1.kr(이진숙 감정연구소) 사이트가 열리고**,
  인증서도 `emotion.master1.kr` 용이라 브라우저에 보안 경고가 뜹니다.
- 즉, 서버에 `old.master1.kr` 이름이 등록되어 있지 않아 기본(첫 번째) 가상호스트가 응답하는 상태입니다.

**요청 사항**
1. 기존 master1.kr 사이트의 Apache 가상호스트(80, 443 둘 다)에 `ServerAlias old.master1.kr` 추가
2. `old.master1.kr` 용 SSL 인증서 발급 (Let's Encrypt)
3. 사이트 설정·.htaccess 에 `https://master1.kr` 로 **강제 이동(리다이렉트)** 하는 규칙이 있으면 old.master1.kr 에서는 이동하지 않도록 수정
   (그대로 두면 old.master1.kr 로 들어와도 새 홈페이지로 넘어가 버립니다)
4. PHP 설정에 사이트 주소가 `https://master1.kr` 로 고정돼 있으면 `https://old.master1.kr` 로 변경
   (로그인 후 이동 주소, 관리자 화면 링크, 업로드 이미지 주소, 세션·쿠키 도메인 등)

**참고 (인증서 갱신 오류 예방)**
- master1.kr / www.master1.kr 은 이제 이 서버를 가리키지 않으므로, 이 서버에 있는 master1.kr·www 인증서는 **자동 갱신 시 실패**합니다.
  old.master1.kr 인증서는 **별도로** 발급하고, master1.kr·www 인증서는 갱신 목록에서 정리 부탁드립니다.
- 같은 서버의 emotion.master1.kr 사이트는 변경 대상이 아닙니다 (DNS 그대로).

완료 후 https://old.master1.kr 에서 로그인·관리자 화면 접속이 되는지 함께 확인 부탁드립니다. 감사합니다.

---

## 서버 작업 참고 (관리자용)

```bash
# 1) master1.kr 가상호스트 설정 파일 찾기
grep -Rl "master1.kr" /etc/httpd/conf.d/ /etc/httpd/conf/

# 2) 해당 <VirtualHost *:80> 과 <VirtualHost *:443> 에 추가
#    ServerAlias old.master1.kr

# 3) 설정 확인 후 반영
sudo apachectl configtest && sudo systemctl reload httpd

# 4) old.master1.kr 인증서 발급 (별도 인증서로)
sudo certbot --apache -d old.master1.kr --cert-name old.master1.kr

# 5) 더 이상 이 서버를 가리키지 않는 master1.kr·www 인증서 정리 (갱신 실패 방지)
sudo certbot certificates
#    → master1.kr / www.master1.kr 인증서 이름 확인 후, 443 가상호스트가 old 인증서를 쓰도록 바꾼 다음
# sudo certbot delete --cert-name <master1.kr 인증서 이름>

# 6) 강제 이동 규칙 확인
grep -Rn "master1.kr" /var/www/ --include=.htaccess
grep -Rn "https://master1.kr\|http://master1.kr" /var/www/ --include=*.php | head -50
```

확인 방법:

```bash
curl -I https://old.master1.kr/            # 200, 인증서 오류 없음
curl -I https://old.master1.kr/login.php   # 200 (master1.kr 로 301 되면 3번 항목 미처리)
```
