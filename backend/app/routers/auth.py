import os
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

import psycopg2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv

# --- load env file ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# --- router ---
router = APIRouter()

# --- config ---
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_secret_key_for_testing")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- pydantic models ---
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

# --- db functions ---
def get_db_connection():
    """establish connection with the NeonDB Postgres DB."""
    if not DATABASE_URL:
        # needs database connection string.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DATABASE_URL environment variable is not set. Please check your server configuration."
        )
    try:
        # psycopg2 can connect directly using the connection URI provided by Neon.
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to the database: {e}"
        )

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_from_db(username: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
            user_record = cur.fetchone()
            if user_record:
                return UserInDB(username=user_record[0], hashed_password=user_record[1])
    finally:
        conn.close()
    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_from_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- api endpoints ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    if get_user_from_db(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(form_data.password)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                (form_data.username, hashed_password)
            )
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}"
        )
    finally:
        conn.close()
    return {"message": f"User '{form_data.username}' created!"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_from_db(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user