from pydantic import BaseModel

class UserSchema(BaseModel):
    user: str
    password: str
