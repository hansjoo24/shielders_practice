def is_banned_sender(sender):
    banned_senders = ["hansjoo25@naver.com",""]
    
    for banned_sender in banned_senders:
        if banned_sender in sender:
            return True, f"스팸으로 분류된 송신자 : {sender}"
    else:
        return False