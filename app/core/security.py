from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(raw: str) -> str:
    '''
    Хеширование пароля.
    '''
    return pwd_ctx.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    '''
    Сравнение пароля с хешем.
    '''
    return pwd_ctx.verify(raw, hashed)

def create_access_token(user_id: int, role: str,) -> str:
    '''
    Генерация JWT access-токена.
    '''
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        'sub': str(user_id),
        'role': role,
        'iat': now,
        'exp': expire,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

def decode_access_token(token: str) -> dict:
    '''
    Декодирование и проверка JWT-токена.
    Возвращает payload или пробрасывает JWT-Error.
    '''
    try:
        payload = jwt.decode(
            token, settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
        return payload
    except JWTError:
        raise