#강산
# 제목,본문 내용으로 스팸 탐지

def is_spam(email_subject, email_body):
    spam_keywords = ["돈 벌기", "빨리 부자 되기", "사은품", "기간 한정", "기간한정", "여기를 클릭하세요", "광고"]


    for keyword in spam_keywords:
        if keyword in email_subject.lower() or keyword in email_body.lower():
            return True


    return False


def main():
    email_subject = input("이메일 제목: ")
    email_body = input("본문 내용: ")


    if is_spam(email_subject, email_body):
        print("이 메일은 스팸일 수 있습니다. ")
    else:
        print("이 메일은 정상적인 메일일 수 있습니다. ")


if __name__ == "__main__":
    main()

