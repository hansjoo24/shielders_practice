def extend_word_included(msg):
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        # 첨부파일 이름 가져오기
        filename = part.get_filename()
        if filename:
            malicious_extend = ['xlsx']
            for word in malicious_extend:
                if filename.endswith(word):
                    return True
            else:
                return False