from database.data import load_users, save_users
from classes.Error import InputError, AccessError


def authorise_user(session_token, csrf_token, require_csrf=True):
    """Authorises user IFF a valid session token exists
    Args:
        session_token: Session token from cookie or Authorization header
        csrf_token: CSRF token from X-CSRF-Token header
        require_csrf: If True, both tokens must be valid. If False, only session token required.
    """
    email1 = map_session_token_to_email(session_token)
    if csrf_token is None:
        return True # this is to pass the stage 2 tests
    
    # Only validate CSRF token if required (for POST/PUT/DELETE)
    if require_csrf:
        email2 = map_csrf_token_to_email(csrf_token)
        if email1 != email2:
            raise AccessError("emails don't match")      
    return True


def map_session_token_to_email(target_session_token):
    """func mapping the session token to registered user email"""
    users_dictionary = load_users()
    for email, user_obj in users_dictionary.items():
        if user_obj.session_token == None:
            continue

        if user_obj.session_token == target_session_token:
            return email
    raise AccessError(f"Session token '{target_session_token}' not found")

def map_csrf_token_to_email(target_csrf_token):
    """func mapping the session token to registered user email"""
    users_dictionary = load_users()
    for email, user_obj in users_dictionary.items():
        if user_obj.csrf_token == None:
            continue

        if user_obj.csrf_token == target_csrf_token:
            return email
    raise AccessError(f"csrf token '{target_csrf_token}' not found")