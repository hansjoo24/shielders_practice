# 스팸 단어 체크
def ad_word_included(body):
    malicious_words = ["광고"]

    for word in malicious_words:
        if word in body:
            return True,f"- {word} 단어 포함"
        
    else:
        return False
