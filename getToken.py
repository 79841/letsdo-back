from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas import TokenData


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 365 * 10

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception=None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # email: str = payload.get("email")
        id: int = payload.get("id")
        # role:int = payload.get("role")
        # username:str = payload.get("username")
        if id is None:
            # raise credentials_exception
            return {'current_user': None}
        token_data = TokenData(id=id)
        return token_data

    except JWTError:
        raise credentials_exception
