import jwt

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings

from app.schemas.auth import AuthSchema

from app.enums.user import UserStatusEnum

from app.utils.hashing import verify_password

from app.repositories.user import UserRepository

from app.exceptions.general import UnauthorizedException


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db=db)

    async def authenticate(self, auth_data: AuthSchema):
        # Currently we use it as admin only auth method
        user = await self.user_repository.find(
            username=auth_data.username,
            status=UserStatusEnum.ADMIN.value,
            get_first=True,
        )

        if not user or not verify_password(auth_data.password, user.password):
            raise UnauthorizedException()

        payload = {
            'sub': str(user.id),
            'username': auth_data.username,
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
        return {'token': token}

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            return payload
        except Exception as e:
            raise UnauthorizedException()

    @classmethod
    def token_required(cls, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict:
        token = credentials.credentials
        return cls.decode_token(token=token)
