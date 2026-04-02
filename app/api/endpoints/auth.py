from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.models.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginJSONRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(request: SignupRequest):
    db: Session = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            email=request.email,
            hashed_password=hash_password(request.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User created successfully",
            "user_id": new_user.id,
            "email": new_user.email
        }
    finally:
        db.close()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()

    try:
        email = form_data.username
        password = form_data.password

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email
        }
    finally:
        db.close()


@router.post("/login-json")
def login_json(request: LoginJSONRequest):
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email
        }
    finally:
        db.close()