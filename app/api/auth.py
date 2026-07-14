from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import bcrypt
import jwt

from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.models import User
from app.config import settings

router = APIRouter(prefix='/auth', tags=['Auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def hash_passwords(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    
    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm='HS256')
    return encode_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        email: str = payload.get('sub')
        if not email:
            raise HTTPException(status_code=401, detail='Не удалось валидировать токен')
        
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail='В базе нету такого пользователя')
        
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Невалидный токен авторизации')

@router.post('/register', response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    email_db = result.scalar_one_or_none()
    
    if email_db:
        raise HTTPException(status_code=400, detail='Этот email уже зарегистрирован')
    
    hash_password = hash_passwords(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hash_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post('/login')
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.username)
    result = await db.execute(query)
    user_db = result.scalar_one_or_none()

    if not user_db:
        raise HTTPException(status_code=401, detail='Неверный email или пароль')
    
    check_passwords = bcrypt.checkpw(user_data.password.encode(), user_db.hashed_password.encode())

    if not check_passwords:
        raise HTTPException(status_code=401, detail='Неверный email или пароль')
    
    token = create_access_token(data={'sub': user_db.email})

    return {'access_token': token, 'token_type': 'bearer'}