import jwt
import datetime

SECRET_KEY = "961d52cc5a8f81c5ebf1e3774fb6f92e016a209104ae5a63b5da4ef3e5474233"

payload: dict = {
    "username": "johndoe",
    "role": "admin",
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
}

#Crear el token
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Token JWT:", token)

#Decodificar el token
try:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print("Payload decodificado:", decoded_payload)
except jwt.ExpiredSignatureError:
    print("El token ha expirado")
except jwt.InvalidTokenError:
    print("Token inválido")