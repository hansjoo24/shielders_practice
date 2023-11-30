## 파일 메일로 받기

from datetime import datetime
import imaplib
import email
from email.header import decode_header
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication




def mail_sender(email_username, email_password, to_email, file_name):
    try:
        smtp = smtplib.SMTP('smtp.naver.com', 587)
        smtp.ehlo()
        smtp.starttls()


        smtp.login(email_username, email_password)


        msg = MIMEMultipart()


        msg['Subject'] = 'Spam mail Report'
        msg['From'] = email_username
        msg['To'] = to_email


        text = """
        <html>
        <body>
        스팸 메일 리스트입니다.<br>
        첨부파일을 확인해주세요.
        </body>
        </html>
        """


        contentPart = MIMEText(text, "html")
        msg.attach(contentPart)
       
        # 엑셀 파일 첨부
        with open(file_name, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=file_name)
            part['Content-Disposition'] = f'attachment; filename="{file_name}"'
            msg.attach(part)


        smtp.sendmail(MY_EMAIL,to_email, msg.as_string())
        smtp.quit()
        print(f"'{file_name}' 성공적으로 전송.")


    except Exception as e:
        print(f"메일 전송 실패 : {e}")

    mail_sender(email_username, email_password, '@.com', file_name)


