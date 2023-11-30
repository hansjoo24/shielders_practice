#이해인 (이메일 마스킹 프로그램)

import re


#이메일 마스킹 프로그램
def mask_email(email):
    # 이메일 입력(아이디와 비밀번호를 나누는 기준)
    username, domain = email.split('@')


    # 아이디 마스킹
    masked_username = re.sub(r'[a-zA-Z0-9]', '*', username[:-3]) + username[-3:]


    # 이메일 주소 마스킹
    masked_domain = re.sub(r'[a-zA-Z0-9]', '*', domain[:-3]) + domain[-3:]


    # 마스킹한 주소 합치기
    masked_email = masked_username + '@' + masked_domain


    return masked_email #주소값 리턴


# 예시
original_email = 'john.doe@example.com'
masked_email = mask_email(original_email)


#비교 출력
print(f'기존 Email: {original_email}')
print(f'마스킹한 Email: {masked_email}')

def decode_email_header(header_value):
    decoded_parts = []
    for part, encoding in decode_header(header_value):
        if isinstance(part, bytes):
            try:
                decoded_part = part.decode(encoding or 'utf-8')
            except (UnicodeDecodeError, LookupError):
                # If decoding fails or encoding is unknown, use ASCII characters
                decoded_part = part.decode('ascii', errors='ignore')
        else:
            decoded_part = part


        decoded_parts.append(decoded_part)


    # Join the decoded parts to get the final decoded header
    return ' '.join(decoded_parts)

