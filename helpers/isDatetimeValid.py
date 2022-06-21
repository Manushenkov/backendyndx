from datetime import datetime


def isDatetimeValid(dateString):
    try:
        datetime.fromisoformat(dateString.replace('Z', '+00:00'))
    except:
        return False
    return True
