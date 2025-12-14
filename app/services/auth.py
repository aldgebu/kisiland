import jwt

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


from app.settings import settings

from app.schemas.auth import AuthSchema

from app.enums.user import UserStatusEnum

from app.utils.hashing import verify_password

from app.repositories.user import UserRepository

from app.exceptions.general import UnauthorizedException


class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db=db)

    async def authenticate(self, auth_data: AuthSchema):
        # Currently we use it as admin only auth method
        users = await self.user_repository.find(
            username=auth_data.username,
            status=UserStatusEnum.ADMIN.value,
        )

        if not users or not verify_password(auth_data.password, users[0].get('password')):
            raise UnauthorizedException()

        user = users[0]
        payload = {
            'sub': str(user['_id']),
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
