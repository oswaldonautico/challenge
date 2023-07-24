from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET_STRING = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login") 

crypt = CryptContext(schemes=["bcrypt"])

class Appuser(BaseModel):
  username: str
  full_name: str
  department: str
  disabled: bool

class UserDB(Appuser):
  password: str


users_dic = {
    "sadmin": {
        "username": "sadmin",
        "full_name": "nba commissioner",
        "email": "comm@nba.com",
        "department": "adminsit",
        "disabled": False,
        "password": "$2a$12$QRH4PtDnJQ6Zu64kaf17Xu8NIuTOILDwIxnKCnmAk7iFCI971rmrG"
    },
    "patrice": {
        "username": "patrice",
        "full_name": "Patric Ewing",
        "email": "patric.ewing@knicks.com",
        "department": "analytics",
        "disabled": False,
        "password": "$2a$12$W2VDr62TRlSI3iQcPHMR7OB2R8APQ/kyPfWE0bygzIY1tYU9TbAuS"
    },
    "garyp": {
        "username": "garyp",
        "full_name": "Patric Ewing",
        "email": "patric.ewing@knicks.com",
        "department": "support",
        "disabled": True,
        "password": "$2a$12$jmg1o6BJwzigFp6hkjy1n.mqrnAVMw5U7mgjQq438lpTYbuSdNZAC"
    },
    "alonsom": {
        "username": "alonsom",
        "full_name": "Patric Ewing",
        "email": "patric.ewing@knicks.com",
        "department": "support",
        "disabled": False,
        "password": "$2a$12$U3kIb0e7I6O.f/l3gag2YunB146vAVWGjcp/nj.L22mMBc5B0fJAS"
    }
}


def search_user_db(username: str):
  if username in users_dic:
    return UserDB(**users_dic[username])
  

def search_user(username: str):
  if username in users_dic:
    return Appuser(**users_dic[username]) 
  
  
async def auth_user(received_token: str = Depends(oauth2)):
    
    exception = HTTPException(
                  status_code = status.HTTP_401_UNAUTHORIZED, 
                  detail = "No tiene permisos para acceder", 
                  headers = {"WWW-Authenticate": "Bearer"})
    
    try:
    
      username = jwt.decode(received_token, SECRET_STRING, algorithms = ALGORITHM).get("sub")
      if username is None:
         raise exception

    except JWTError:
       raise exception
  
    return search_user(username)

async def current_user(user: Appuser = Depends(auth_user)): 

  if user.disabled:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Usuario inactivo") 
      #headers = {"WWW-Authenticate": "Bearer"})
  return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_dic.get(form.username)
    if not user_db:
        raise HTTPException(
          status_code = status.HTTP_400_BAD_REQUEST, detail = "nombre de usuario incorrecto") 
  
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta") 
    
    access_token_expiration = timedelta(minutes = ACCESS_TOKEN_DURATION)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET_STRING, algorithm = ALGORITHM), "token_type": "bearer"}


#@router.get("/users/me")
#async def me (user: Appuser = Depends(current_user)):
#  return user.username, user.department
  
async def current_user_dep (user: Appuser = Depends(current_user)):
  return user.department