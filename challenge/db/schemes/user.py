### User schema ###

def user_schema(user) -> dict:
    return {"_id": user["_id"],
            "fec_alta": user["fec_alta"],
            "user_name": user["user_name"],
            "codigo_zip": user["codigo_zip"],
            "credit_card_num": user["credit_card_num"],
            "credit_card_ccv": user["credit_card_ccv"],
            "cuenta_numero": user["cuenta_numero"],
            "direccion": user["direccion"],
            "geo_latitud": user["geo_latitud"],
            "geo_longitud": user["geo_longitud"],
            "color_favorito": user["color_favorito"],
            "foto_dni": user["foto_dni"],
            "ip": user["ip"],
            "auto": user["auto"],
            "auto_modelo": user["auto_modelo"],
            "auto_tipo": user["auto_tipo"],
            "auto_color": user["auto_color"],
            "cantidad_compras_realizadas": user["cantidad_compras_realizadas"],
            "avatar": user["avatar"],
            "fec_birthday": user["fec_birthday"],
            "id": user["id"]}


def users_list_schema(users) -> list:
    return [user_schema(user) for user in users]