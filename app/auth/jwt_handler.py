# this file for encoding and decoding and returning jwts
import hashlib
import jwt
import time
from dotenv import load_dotenv
from typing import Dict
import os

use_env = os.environ.get("USE_ENV")

if use_env != "True":
    load_dotenv()
    JWT_SECRET = os.getenv("secret")
    JWT_ALGORITHM = os.getenv("algorithm")
else:
    JWT_SECRET = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

# deez generated tokens (jwts)


def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time()else None
    except:
        return {}
