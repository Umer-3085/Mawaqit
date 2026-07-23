from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from mawaqit.config import settings
from mawaqit.repositories.admin import AdminRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, repo: AdminRepository):
        self.repo = repo

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def hash_password(self, plain: str) -> str:
        return pwd_context.hash(plain)

    def create_token(self, username: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {"sub": username, "exp": expire}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)