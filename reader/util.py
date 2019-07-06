
def check_session_for(sessionAttributes, key):
    """Returns True or False based on wether the variable exists"""
    if key in sessionAttributes:
        return True
    else:
        return False

def session_value_is(sessionAttributes, key, value):
    """Returns True or False based on wether the variable has the expected Value"""
    if key in sessionAttributes and sessionAttributes[key] == value:
        return True
    else:
        return False

def get_session_value(sessionAttributes, key):
    """Returns the Value or None"""
    if key in sessionAttributes:
        return sessionAttributes[key]
    else:
        return None
