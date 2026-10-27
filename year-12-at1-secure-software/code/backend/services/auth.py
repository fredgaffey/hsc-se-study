from classes.User import User
from classes.Error import InputError, AccessError
from database.data import load_users, save_users

import re
from classes.User import User

def auth_register_user(email, password, name):
    """Service func - registers and stores user on backend"""

    user_dict = load_users()

    email = User.check_email_is_valid(email)
    name = User.check_name_is_valid(name)
    password = User.check_is_pwd_valid(password)
    
    # TODO: Implement input validation for email, password, and name
    
    # Check if email already exists (email is already normalized to lowercase by check_email_is_valid)
    if email in user_dict:
        raise InputError("Email already exists")

    
    # Register the user
    new_user_instance = User(email, name, password)
    user_dict[email] = new_user_instance

    # init user session - this modifies the user object in place
    session_token, csrf_token = new_user_instance.initiate_user_session()
    # TODO: Generate and return CSRF token
    
    # Verify the token is set in the dictionary (should be same object reference)
    # Since Python objects are passed by reference, user_dict[email] should already have the updated tokens
    if user_dict[email].session_token != session_token:
        raise RuntimeError("Token mismatch: user object not updated correctly")
    
    save_users(user_dict)

    return session_token, csrf_token

def auth_login_user(email, password):
    """Service func - logins user if valid email & password"""
    # TODO: Implement input validation for email and password
    
    # Normalize email (same as registration)
    email = User.check_email_is_valid(email)
    
    # validate user if in database
    user_dict = load_users()
    
    if email not in user_dict or not user_dict[email].verify_password(password):
        raise AccessError("Invalid email or password")

    # initiate_user_session modifies the user object in place
    session_token, csrf_token = user_dict[email].initiate_user_session()
    # TODO: Generate and return CSRF token
    
    # Verify the token is set correctly (should be same object reference)
    if user_dict[email].session_token != session_token:
        raise RuntimeError("Token mismatch: user object not updated correctly")
    
    save_users(user_dict)

    return session_token, csrf_token

def auth_logout_user(session_token):
    """Service func - revokes a user session via token"""
    user_dict = load_users()
    for user in user_dict.values():
        if user.session_token == session_token:
            user.revoke_user_session()

    save_users(user_dict)


