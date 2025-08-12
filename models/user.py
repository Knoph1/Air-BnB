#!/usr/bin/python3
"""
User Class from Models Module
"""
from datetime import datetime, timedelta
import hashlib
import jwt
import models
from models import authentication_secret
from models.base_model import BaseModel, Base
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime
from uuid import uuid4
utcnow = datetime.utcnow
STORAGE_TYPE = os.environ.get('BTCPBNB_TYPE_STORAGE')
SECRET_KEY = authentication_secret.SECRET_KEY


class User(BaseModel, Base):
    """
        User class handles all application users
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
            instantiates user object
        """
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
                super().__init__(*args, **kwargs)

    def pass_encryption(pwd):
        """
        encrypts input to encypted string
        """
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexdigest()
        return secure_password

    def __set_password(self, pwd):
        """
            custom setter: encrypts password to MD5
        """
        secure_password = User.pass_encryption(pwd)
        setattr(self, "password", secure_password)

    def encode_auth_token(self, user_id):
        """
        Generates Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': utcnow() + timedelta(days=0, seconds=3600),
                'iat': utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError as e:
            print(e)
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError as e:
            print(e)
            return 'Invalid token. Please log in again.'


class BlacklistToken(BaseModel, Base):
    """
    Token Model for storing JWT tokens
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'blacklist_tokens'
        token = Column(String(500), unique=True, nullable=False)
        blacklisted_on = Column(
            DateTime, nullable=False, default=datetime.utcnow()
        )

        def __init__(self, token):
            """
            instantiates with BaseModel attributes
            """
            self.token = token
            self.blacklisted_on = utcnow()
            super().__init__()

        def __repr__(self):
            return '<id: token: {}'.format(self.token)

        @staticmethod
        def check_blacklist(auth_token):
            """
            check whether auth token has been blacklisted
            """
            all_tokens = models.storage.all('BlacklistToken').values()
            for token_obj in all_tokens:
                if token_obj.token == str(auth_token):
                    return True
            return False
