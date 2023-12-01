#김승현님 + 이지원님 코드 합한 결과
#3초에 1번씩 실행되도록 수정 

import imaplib
import email
from email.header import decode_header
import pandas as pd
from datetime import datetime
import schedule
import time
import openpyxl
from openpyxl.styles import Alignment
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv, find_dotenv
import os

from domain_check import domain_check
from word_check import ad_word_included

# .env 파일에서 환경 변수 로드
dotenv_path = find_dotenv(filename=".env", raise_error_if_not_found=True)
load_dotenv(dotenv_path)


# 환경 변수 설정
SECRET_ID = os.getenv("SECRET_ID")
SECRET_PASS = os.getenv("SECRET_PASS")
MY_EMAIL = os.getenv("MY_EMAIL")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")


# 이메일 헤더 디코딩 함수
def decode_email_header(header_value):
    decoded_parts = []
    for part, encoding in decode_header(header_value):
        if isinstance(part, bytes):
            try:
                decoded_part = part.decode(encoding or 'utf-8')
            except UnicodeDecodeError:
                # 디코딩에 실패하면 ASCII 문자 사용
                decoded_part = part.decode('ascii', errors='ignore')
        else:
            decoded_part = part


        decoded_parts.append(decoded_part)


    return ' '.join(decoded_parts)


# 이메일 본문 가져오는 함수
def get_email_body(msg):
    body = ""


    # 멀티파트인 경우
    if msg.is_multipart():
        for part in msg.walk():
            # 텍스트 형식인 경우
            if part.get_content_type() == "text/plain":
                # 본문 추가
                body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        # 멀티파트가 아닌 경우 본문 직접 가져오기
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")


    return body


#스팸 정보 메일 전송 함수
def mail_sender(SECRET_ID, SECRET_PASS, YOUR_EMAIL, file_name):
    try:
        # SMTP 서버 설정
        smtp = smtplib.SMTP('smtp.naver.com', 587)
        smtp.ehlo()
        smtp.starttls()


        # 로그인
        smtp.login(SECRET_ID, SECRET_PASS)


        # 메일 구성
        msg = MIMEMultipart()


        msg['Subject'] = f"{now}_스팸 메일 보고서"
        msg['From'] = MY_EMAIL
        msg['To'] = YOUR_EMAIL


        text = f"""
        <html>
        <body>
        <p>관리자님,</p>
        <p>{now} 기준으로 수집된 스팸 메일 보고서를 안내드립니다.</p>
        <p>첨부된 엑셀 파일을 확인하여 더 자세한 정보를 파악하실 수 있습니다.</p>
        <p>보고서를 확인 후 적절한 조치를 부탁드립니다.</p>
        <p>감사합니다.</p>
        </body>
        </html>
        """


        contentPart = MIMEText(text, "html")
        msg.attach(contentPart)


        # 엑셀 파일 열기
        workbook = openpyxl.load_workbook(file_name)


        # 엑셀 셀 크기 조정
        for sheet in workbook:
            for row in sheet.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
               
        for column, width in zip(['A', 'B', 'C', 'D'], [30, 20, 30, 10]):
            sheet.column_dimensions[column].width = width


        # 엑셀 파일 다시 저장
        workbook.save(file_name)
       
        # 엑셀 파일 다시 첨부
        with open(file_name, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=file_name)
            part['Content-Disposition'] = f'attachment; filename="{file_name}"'
            msg.attach(part)


        # 메일 전송
        smtp.sendmail(MY_EMAIL, YOUR_EMAIL, msg.as_string())
        smtp.quit()
        print(f"'{file_name}' 성공적으로 전송.")


    except Exception as e:
        print(f"메일 전송 실패 : {e}")



# 안 읽은 모든 메일 가져오는 함수
def fetch_all_unread_emails(SECRET_ID, SECRET_PASS):
    file_name = None
    try:
        # IMAP 서버에 연결
        mail = imaplib.IMAP4_SSL("imap.naver.com")


        # IMAP 서버에 연결
        mail.login(SECRET_ID, SECRET_PASS)
        mail.select("inbox")
       
        # Excel 파일에서 허용된 도메인을 읽어옴
        allowed_domains_df = pd.read_excel(os.path.join("resorces", 'allowedEmail.xlsx'), engine='openpyxl')
        allowed_domains = allowed_domains_df['Domain'].str.lower().tolist()
       
        # 디버깅
        print(f"엑셀 파일 내의 allowed_domains 목록 : {allowed_domains}")
        print("--------")


        # 모든 안 읽은 이메일 체크
        status, messages = mail.search(None, "UNSEEN")
        if status == "OK" and any(messages):
            all_emails_data = {'Sender': [], 'Subject': [], 'Date': [], 'Body': []}
           
            for num in messages[0].split():
                _, msg_data = mail.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])


                # 이메일 정보 가져오기
                sender = decode_email_header(msg.get("From"))
                subject = decode_email_header(msg.get("Subject"))
                date = msg.get("Date")
                body = get_email_body(msg)
               
                # 도메인이 허용되는지 확인
                if domain_check(sender, allowed_domains):

                    # 허용 도메인이면 '광고' 단어 체크
                    if(ad_word_included(body)):
                        all_emails_data['Sender'].append(sender)
                        all_emails_data['Subject'].append(subject)
                        all_emails_data['Date'].append(date)
                        all_emails_data['Body'].append(body)


                        print("메일 내용에 '광고' 단어가 포함되어 있어 스팸일 수 있습니다.")
                        print("--------")
                    else:
                        # 정상 메일인 경우
                        print("정상적인 메일입니다.")
                        print("--------")
                else:
                    # 비허용 도메인에 대한 경고 출력
                    print(f"경고: 허용되지 않은 이메일 도메인입니다. - {sender}")
                    print("--------")


            # 수집된 메일 정보 저장
            df = pd.DataFrame(all_emails_data)


            # 엑셀파일 저장
            file_name = f"{now}_spam_mail_report.xlsx"
            df.to_excel(file_name, index=False)
            print(f"스팸 메일 정보가 '{file_name}'로 저장되었습니다.")


        else:
            # 안 읽은 메일이 없는 경우
            print("안 읽은 메일이 없습니다.")


        # 연결 종료
        mail.logout()


    except Exception as e:
        print(f"오류 발생: {e}")


    # Excel 파일이 생성된 경우 스팸 정보 메일 전송
    if file_name is not None:
        mail_sender(SECRET_ID, SECRET_PASS, YOUR_EMAIL, file_name)


# 현재 날짜 및 시간 얻기
now = datetime.now().strftime("%Y-%m-%d")


# 메일 목록 가져오기
schedule.every(3).seconds.do(lambda: fetch_all_unread_emails(SECRET_ID, SECRET_PASS))
while True:
    schedule.run_pending()
    time.sleep(1)