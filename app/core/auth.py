from  datetime import datetime,timedelta
from jose import jwt, JWTError;
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM
from datetime import timezone
from passlib.context import CryptContext
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/auth/token')


def create_access_token(data: dict, expire_delta:timedelta |None=None):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        user=payload.get("sub")
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except JWTError:


        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)