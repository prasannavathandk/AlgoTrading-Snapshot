from datetime import datetime
import re

def currentDate() -> str:
    return datetime.today().strftime('%Y-%m-%d')

def simpleString(inputString: str) -> str:
    simpleString = re.sub(r'[^a-zA-Z0-9\s]', '', inputString)
    return simpleString.lower()