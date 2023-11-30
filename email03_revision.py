#김승현님 + 이지원님 코드 합한 결과
#3초에 1번씩 실행되도록 수정 

import imaplib
import email
from email.header import decode_header
import pandas as pd
from datetime import datetime
import schedule
import time

previous_messages = []

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

    #return ' '.join(decoded_parts).strip('\"')
    return ' '.join(decoded_parts)


def get_email_body(msg):
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

    return body


def is_email_allowed(email_address, allowed_domains):
    # Extract the domain part of the email address
    _, domain = email_address.lower().split('@', 1) if '@' in email_address else (None, None)


    # Remove '>' symbol at the end if present
    domain = domain.rstrip('>')
   
    # Debugging
    print(f"추출한 도메인 : {domain}")


    # Check if the extracted domain is in the allowed domains list
    allowed = domain in allowed_domains
    print(f"Domain: {domain}, Allowed: {allowed}") # Debugging output
    return allowed


 
def fetch_all_unread_emails(email_username, email_password):
    global previous_messages

    try:
        # IMAP 서버에 연결
        mail = imaplib.IMAP4_SSL("imap.naver.com")

        # IMAP 서버에 연결
        mail.login(email_username, email_password)
        mail.select("inbox")
       
        # Excel 파일에서 허용된 도메인을 읽어옴
        allowed_domains_df = pd.read_excel(r'resorces\allowedEmail.xlsx', engine='openpyxl')
        allowed_domains = allowed_domains_df['Domain'].str.lower().tolist()
       
        # 디버깅
        print(f"허용 가능한 메일의 도메인 목록 : {allowed_domains}")


        # 모든 안 읽은 이메일 체크
        status, messages = mail.search(None, "UNSEEN")
        mail_cnt=0

        
        if status == "OK":
            all_emails_data = {'Sender': [], 'Subject': [], 'Date': [], 'Body': []}
           
            for num in messages[0].split():

                if num in previous_messages:
                    #print("이미 읽은 이메일 입니다")
                    continue

                _, msg_data = mail.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])


                # 이메일 정보 가져오기
                sender = decode_email_header(msg.get("From"))
                subject = decode_email_header(msg.get("Subject"))
                date = msg.get("Date")
                body = get_email_body(msg)
               
                # 도메인이 허용된지 확인
                if is_email_allowed(sender, allowed_domains):
                    # 도메인이 허용되면 출력
                    print(f"보낸 사람 : {sender}")
                    print(f"제목 : {subject}")
                    print(f"날짜 : {date}")
                    print("\n\n")
                else:
                    # 비허용 도메인에 대한 경고 출력
                    print(f"경고: 허용되지 않은 이메일 도메인입니다.")
                    print(f"발신자 : {sender}")
                    print("\n\n")


                # '광고' 단어 체크
                if '광고' in body:
                    print(f"보낸 사람 : {sender}")
                    print(f"제목 : {subject}")
                    print(f"날짜 : {date}")
                    print(f"본문 :\n{body}")


                    all_emails_data['Sender'].append(sender)
                    all_emails_data['Subject'].append(subject)
                    all_emails_data['Date'].append(date)
                    all_emails_data['Body'].append(body)


                    print("이메일 내용에 '광고'가 포함되어 있어 스팸일 수 있습니다.")
                    print("--------")

                mail_cnt+=1


            previous_messages = list(messages[0].split())
            df = pd.DataFrame(all_emails_data)
            

        if mail_cnt==0:
            print("안 읽은 이메일이 없습니다.")
        
        else:
            # 엑셀파일 저장
            current_time = datetime.now().strftime("%Y%m%d")
            file_name = f"spam_{current_time}.xlsx"
            df.to_excel("result\\"+file_name, index=False)
            print(f"광고 이메일 정보가 '{file_name}'로 저장되었습니다.")

        # 연결 종료
        mail.logout()

    except Exception as e:
        print(f"오류 발생: {e}")
       
       

# 이메일 계정 정보 입력
email_username = "id"
email_password = "password"


# 이메일 목록 가져오기

schedule.every(3).seconds.do(lambda: fetch_all_unread_emails(email_username, email_password))
while True:
    schedule.run_pending()
    time.sleep(1)

