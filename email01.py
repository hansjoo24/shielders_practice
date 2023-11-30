# 보낸 사람, 제목, 날짜 출력 

import imaplib
import email
from email.header import decode_header


def decode_email_header(header_value):
    decoded_parts = []
    for part, encoding in decode_header(header_value):
        if isinstance(part, bytes):
            try:
                decoded_part = part.decode(encoding or 'utf-8')
            except UnicodeDecodeError:
                # If decoding fails, use ASCII characters
                decoded_part = part.decode('ascii', errors='ignore')
        else:
            decoded_part = part


        decoded_parts.append(decoded_part)

    # Join the decoded parts to get the final decoded header
    return ' '.join(decoded_parts)


def fetch_emails(email_username, email_password):
    try:
        # IMAP 서버에 연결
        mail = imaplib.IMAP4_SSL("imap.naver.com")


        # IMAP 서버에 연결
        mail.login(email_username, email_password)
        mail.select("inbox")


        # 모든 이메일 검색
        status, messages = mail.search(None, "ALL")
       
        for mail_id in messages[0].split():
            _, msg_data = mail.fetch(mail_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])


            # 이메일 헤더 정보 가져오기
            sender = decode_email_header(msg.get("From"))
            subject = decode_email_header(msg.get("Subject"))
            date = msg.get("Date")


            # 출력
            print(f"보낸 사람: {sender}")
            print(f"제목: {subject}")
            print(f"날짜: {date}")
            print("--------")


        # 연결 종료
        mail.logout()


    except Exception as e:
        print(f"오류 발생: {e}")


email_username = "-"
email_password = "-"


# 이메일 목록 가져오기
fetch_emails(email_username, email_password)


