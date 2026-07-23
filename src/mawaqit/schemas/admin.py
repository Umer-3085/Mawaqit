from pydantic import BaseModel

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUpdate(BaseModel):
    username: str | None = None
    password: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"