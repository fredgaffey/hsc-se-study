from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
import re
import html
from classes.Error import InputError, AccessError
import secrets

# TODO: Import password hashing library for secure password storage
# TODO: Import library for secure token generation

class User:
    def __init__(
        self,
        email,
        name,
        password=None,
        password_hash=None,
        session_token=None,
        csrf_token=None,
        # TODO: Add CSRF token parameter
    ):
        """Initialised new user instance."""
        email = User.check_email_is_valid(email)
        name = User.check_name_is_valid(name)
        self.__email = email
        self.__name = name

        # __init__() is used for creating a new User instance via cls(...) or manual instantiation

        if password:
            # TODO: Implement password hashing instead of storing plain text
            password = User.check_is_pwd_valid(password)
            self.__password_hash = generate_password_hash(password)
        elif password_hash:
            self.__password_hash = password_hash
        else:
            raise ValueError("Either password or password_hash must be provided")

        self.__session_token = session_token
        self.__csrf_token = csrf_token
        # TODO: Initialize CSRF token storage
        # tokens are None - iff no user-session

    # private: Generate secure hexadecimal token
    def __generate_token(self):
        # TODO: Implement cryptographically secure token generation
        return secrets.token_urlsafe(64)
        # return "insecure_token_" + self.__email

    # public: Init user session
    def initiate_user_session(self):
        # TODO: Generate CSRF token along with session token
        self.__session_token = self.__generate_token()
        self.__csrf_token = self.__generate_token()
        return self.__session_token, self.__csrf_token  # TODO: Return CSRF token

    # public: Remove user session
    def revoke_user_session(self):
        self.__session_token = None
        self.__csrf_token = None
        # TODO: Clear CSRF token on session revocation

    # public: Verify password input
    def verify_password(self, password_input)-> bool:
        # TODO: Implement secure password verification using hashing
        return check_password_hash(self.__password_hash,password=password_input)
        # return self.__password == password_input

    # public: Session Token Property
    @property
    def session_token(self):
        return self.__session_token

    # TODO: Add CSRF token property getter
    @property
    def csrf_token(self):
        return self.__csrf_token

    # public: mail Property
    @property
    def email(self):
        return self.__email

    # public: Name Property
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = User.check_name_is_valid(new_name)

    @email.setter
    def email(self, new_email):
        self.__email = User.check_email_is_valid(new_email)

    # public: convert fron object -> dict
    def to_dict(self):
        return {
            "email": self.__email,
            "name": self.__name,
            "password_hash": self.__password_hash,
            "session_token": self.__session_token,
            "csrf_token": self.__csrf_token,
            # TODO: Include CSRF token in dictionary
        }

    # public: cls() used in database/data.py to convert JSON -> in-memory user object
    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data["email"],
            name=data["name"],
            password_hash=data["password_hash"],
            session_token=data["session_token"],
            csrf_token=data["csrf_token"],
            # TODO: Load CSRF token from dictionary
        )

    @staticmethod
    def check_email_is_valid(email):
        regex = r"[-A-Za-z0-9!#$%&@'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?" 
        try:
            email = str(email)
            email = email.strip()
            email = email.lower()
        except InputError:
            raise InputError("Email must be a string.")
                
        if email == None:
            raise InputError("Missing required fields: email, password, and name")
        
        if len(email) < 299:
            raise ImportError("The email is to long")    
        
        if not re.fullmatch(regex, email):
            raise InputError("Invalid email")

        email = User.do_XSS_cleaning(email)

        return email

    @staticmethod
    def check_is_pwd_valid(password):
        # regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[#?!@$%^&*-]).{8,}$"
    
        try:
            password = str(password)
        except ValueError:
            raise InputError("Password must be a string.")
        
        if len(password) > 2** 9:
            raise InputError("password to long")
        
        if not re.fullmatch(regex, password):
            # print(f"Failed password check: '{password}'"*10000)
            raise InputError("is not strong enough")
        
        # password = User.do_XSS_cleaning(password)

        return password
    
    @staticmethod
    def check_name_is_valid(name):
        if type(name) == int:
            raise InputError("is a int")
        
        try:
            # name = str(name) comment out to pass tests\test_input_validation.py:392: AssertionError
            name = str(name)
        except InputError:
            print(name,"thi mane has failed")
            raise InputError(f"{name} is not a stringable")
        
        if name == " "*len(name): # name all wite spase
            raise InputError("name is all white space")
        name = name.strip()
        
        if name == None:
                print("Name cannot be empty.")
                print(name)
                raise InputError("Missing required fields: email, password, and name")
            
        if len(name) > 299:
            print("Name cannot exceed 299 characters.")
            print(name)
            raise InputError("Name cannot exceed 299 characters.")
        # Only letters, spaces, hyphens, and apostrophes allowed
        # if not re.fullmatch(r"^[A-Za-z\s'-]+$", name):
            print("Name contains invalid characters.")
            print(name)
            raise InputError("Name contains invalid characters.")
        
        name = User.do_XSS_cleaning(name)
        return name


    @staticmethod
    def do_XSS_cleaning(text)->str:
        text = text.replace("\x00","")
        text = text.replace("javascript","")
        text = text.replace("onclick","")
        text = text.replace("onmouseover","")
        text = text.replace("onfocus","")
        text = text.replace("onload","")
        text = text.replace("onerror","")
        
        return html.escape(text)