from pydantic import BaseModel
 
class User(BaseModel):
    _id: str 
    fec_alta: str 
    user_name: str
    codigo_zip: str
    credit_card_num: str | None
    cuenta_numero: str
    direccion: str
    geo_latitud: str
    geo_longitud: str
    color_favorito: str | None
    foto_dni: str
    ip: str
    auto: str 
    auto_modelo: str
    auto_tipo: str
    auto_color: str | None
    cantidad_compras_realizadas: int
    avatar: str | None
    fec_birthday: str
    id: str

class User_Support(BaseModel):
    _id: str 
    user_name: str
    codigo_zip: str
    direccion: str
    geo_latitud: str
    geo_longitud: str
    auto: str 
    auto_modelo: str
    auto_tipo: str
    id: str

class User_Analytics(BaseModel):
    _id: str 
    fec_alta: str 
    user_name: str
    codigo_zip: str
    cuenta_numero: str
    direccion: str
    geo_latitud: str
    geo_longitud: str
    color_favorito: str | None
    auto: str 
    auto_modelo: str
    auto_tipo: str
    auto_color: str | None
    cantidad_compras_realizadas: int
    avatar: str | None
    fec_birthday: str
    id: str