# 도메인 허용 확인
def domain_check(email_address, allowed_domains):
    # 이메일 주소의 도메인 부분 추출
    _, domain = email_address.lower().split('@', 1) if '@' in email_address else (None, None)

    # 마지막 '>' 기호 제거
    domain = domain.rstrip('>')
   
    # 디버깅
    print(f"추출한 도메인 : {domain}")

    # 추출한 도메인이 허용 목록에 있는지 확인
    allowed = domain in allowed_domains

    # 허용된 도메인 출력
    print(f"Domain: {domain}, Allowed: {allowed}\n")
    return allowed