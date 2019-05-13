

def check_session_for(sessionAttributes, key):
    if key in sessionAttributes:
        return True
    else:
        return False

# returns value to key in session if set
# returns None if not
def session_value_is(sessionAttributes, key, value):
    if key in sessionAttributes and sessionAttributes[key] == value:
        return True
    else:
        return False

def get_session_value(sessionAttributes, key):
    if key in sessionAttributes:
        return sessionAttributes[key]
    else:
        return None
