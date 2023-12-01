def ad_word_included(body):
    malicious_words = ["광고"]

    for word in malicious_words:
        if word in body:
            return True
        
    else:
        return False
