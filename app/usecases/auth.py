from app.core.errors import (
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.models import User
from app.repositories.users import UserRepository


class AuthUseCase:
    '''
    Сценарий аутентификации.
    '''
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def register(self, email: str, password: str) -> User:
        '''
        Регистрация пользователя.
        '''
        existing = await self._repo.get_by_email(email)
        if existing:
            raise ConflictError('Данный e-mail уже занят')

        hashed = hash_password(password)
        user = await self._repo.create(email=email, password_hash=hashed)
        return user

    async def login(self, email: str, password: str) -> str:
        '''
        Вход и получение JWT-токена.
        '''
        user = await self._repo.get_by_email(email)
        if not user:
            raise UnauthorizedError('Неверный e-mail или пароль')

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError('Неверный e-mail или пароль')

        token = create_access_token(user_id=user.id, role=user.role)
        return token

    async def get_profile(self, user_id: int) -> User:
        '''
        Получение профиля пользователя по ID.
        '''
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError('Пользователь не найден')
        return user