# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.auth import create_access_token, verify_password
from app.schemas.auth import LoginRequest
from app.schemas.user import Token
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(payload: LoginRequest, db: Session = Depends(get_db)):
    user: User = db.query(User).filter(User.email == payload.email).first()
    if not user or not hasattr(user, 'hashed_password'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    hashed_password: str = str(user.hashed_password)
    if not verify_password(payload.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token_expire = timedelta(minutes=30)
    token = create_access_token(
        data={"sub": str(user.id)},  
        expire_delta=access_token_expire
    )
    return {"access_token": token, "token_type": "bearer"}
