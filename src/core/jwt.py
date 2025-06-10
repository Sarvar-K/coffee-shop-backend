from datetime import datetime, timedelta
from typing import Optional

import jwt

from exceptions import UnauthorizedError
from . import configs
from models.user import User

TOKEN_TYPE_ACCESS = 'access'
TOKEN_TYPE_REFRESH = 'refresh'
TOKEN_ISSUER = 'CoffeeShopAuth'

JWT_ALGORITHM = 'RS256'

with open("../keys/jwt.key") as key_file:
    JWT_PRIVATE_KEY_STRING = key_file.read()

with open("../keys/jwt.key.pub") as key_file:
    JWT_PUBLIC_KEY_STRING = key_file.read()


def create_access_token(user: User):
    return _create_token(user, type=TOKEN_TYPE_ACCESS, alive_for_minutes=configs.ACCESS_TOKEN_ALIVE_FOR_MINUTES)


def create_refresh_token(user: User, session_id: int):
    return _create_token(
        user,
        type=TOKEN_TYPE_REFRESH,
        alive_for_minutes=configs.REFRESH_TOKEN_ALIVE_FOR_MINUTES,
        session_id=session_id
    )


def decode_refresh_token(token_str):
    token_data = _decode_jwt_token(token_str)

    token_type = token_data['type']
    if token_type != TOKEN_TYPE_REFRESH:
        raise UnauthorizedError(f'Expected authentication token type refresh, but got type={token_type}')

    return token_data


def decode_access_token(token_str):
    token_data = _decode_jwt_token(token_str)

    token_type = token_data['type']
    if token_type != TOKEN_TYPE_ACCESS:
        raise UnauthorizedError(f'Expected authentication token type access, but got type={token_type}')

    return token_data


def _create_token(user: User, type: str, alive_for_minutes: int, session_id: Optional[int]=None):
    issued_at = datetime.utcnow()
    token_data = {
        'iss': TOKEN_ISSUER,
        'iat': issued_at,
        'exp': issued_at + timedelta(minutes=alive_for_minutes),
        'sub': str(user.id),
        'type': type,
        'role': user.role.alias,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'isVerified': user.is_verified,
    }
    if session_id:
        token_data.update(sessionId=session_id)

    return jwt.encode(token_data, JWT_PRIVATE_KEY_STRING, algorithm=JWT_ALGORITHM)


def _decode_jwt_token(token_str):
    try:
        token_payload = jwt.decode(token_str, JWT_PUBLIC_KEY_STRING, issuer=TOKEN_ISSUER, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as e:
        raise UnauthorizedError('Authentication token has expired')
    except jwt.PyJWTError as e:
        raise UnauthorizedError(f'Authentication token is invalid: {e}')

    return token_payload
