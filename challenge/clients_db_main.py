from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from challenge.db.models.user import User, User_Support, User_Analytics
from challenge.db.schemes.user import user_schema, users_list_schema
from challenge.db.client import db_client
from bson import ObjectId
from challenge import jwt_authe_users
from challenge.jwt_authe_users import current_user_dep

app = FastAPI()

user_list = []

# Routers
app.include_router(jwt_authe_users.router)


#1. CONSULTAR CLIENTE EN LA DB

#1.1 Colsultar todos los clientes

@app.get("/allusersdb", response_model= list[User])
async def get_all_users(dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
        return users_list_schema(db_client.Challenge.personaldata.find())
    else:
      raise HTTPException(
         status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")

#1.2 Consultar un cliente mediante el _id

@app.get("/userquery_id")  # Query
async def get_user_by_mongo_id(_id: str, dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
      return search_user("_id", ObjectId(_id))  
    else: 
      raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")       

#1.3 Consultar un cliente mediante el id original

@app.get("/userqueryid")  # Query
async def get_user_by_id(id: str, dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
      return search_user("id", id)
    elif dep == "support":
      return search_user_support("id", id)
    elif dep == "analytics":
      return search_user_analytics("id", id)
    else: 
      raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")   

#1.5 Consultar un cliente por user_name

@app.get("/querybyusername")  # Query
async def get_user_by_user_name(user_name: str, dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
      return search_user("user_name", user_name)
    elif dep == "support":
      return search_user_support("user_name", user_name)
    elif dep == "analytics":
      return search_user_analytics("user_name", user_name)
    else: 
      raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")


#2. CREAR UN CLIENTE EN LA DB

@app.post("/adduserdb", response_model=User, status_code=status.HTTP_201_CREATED)
async def new_user(user: User, dep: str = Depends(current_user_dep)):
  if dep == "adminsit":

    if type(search_user("user_name", user.user_name)) == User:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
        
    user_dict = dict(user) #transforma los datos de entrada del usuario en el diccionario "user_dict"
  
    _id = db_client.Challenge.personaldata.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.Challenge.personaldata.find_one({"_id":_id}))

    return User(**new_user)
  
  else:
      raise HTTPException(
         status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")


#3. EDITAR UN CLIENTE EN LA DB

@app.put("/edituser", response_model= User)
async def edit_user(user: User, dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
    
        user_dict = dict(user)
    
        try:
            db_client.Challenge.personaldata.find_one_and_replace(
            {"user_name": user.user_name}, user_dict)
            return search_user("user_name", user.user_name)
        except:    
            return {"error": "No se ha actualizado el usuario"}
    
    else:
      raise HTTPException(
         status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")



#4. BORRAR UN CLIENTE EN LA DB

@app.delete("/deleteuser/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_name: str, dep: str = Depends(current_user_dep)):
    if dep == "adminsit":
    
        found =  db_client.Challenge.personaldata.find_one_and_delete(
            {"user_name": user_name})

        if not found:
            return {"error": "No se ha eliminado el usuario"}
    
    else:
      raise HTTPException(
         status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuario no tiene permisos")

# FUNCIONES INDEPENDIENTES PARA BUSCAR USUARIOS

#Entrega información requerida por ITadmins
def search_user(field: str, key):

    try:
        user = db_client.Challenge.personaldata.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    
#Entrega información requerida por Support
def search_user_support(field: str, key):

    try:
        user = db_client.Challenge.personaldata.find_one({field: key})
        return User_Support(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    
#Entrega información requerida por Analytics
def search_user_analytics(field: str, key):

    try:
        user = db_client.Challenge.personaldata.find_one({field: key})
        return User_Analytics(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}