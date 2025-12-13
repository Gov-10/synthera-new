# from ninja.security import HttpBearer
# import os
# from dotenv import load_dotenv
# from jose import jwk, jwt
# from jose.utils import base64url_decode
# from datetime import datetime 
# import requests

# load_dotenv()
# COGNITO_REGION=os.getenv("COGNITO_REGION")
# USER_POOL_ID= os.getenv("USER_POOL_ID")
# USER_POOL_CLIENT_ID = os.getenv("USER_POOL_CLIENT_ID")
# JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
# JWKS = requests.get(JWKS_URL).json()["keys"]
# def validate_token(token:str):
#     headers = jwt.get_unverified_headers(token)
#     kid = headers["kid"]
#     jwt_key = next((key for key in JWKS if key["kid"] == kid),None)
#     if not jwt_key:
#         raise Exception("Public key not found in JWKS")
#     claims = jwt.get_unverified_claims(token)
#     if unverified["exp"]<datetime.utcnow().timestamp():
#         raise Exception("Token is expired")
#     aud = unverified.get("aud") or unverified.get("client_id")
#     if aud != USER_POOL_CLIENT_ID:
#         raise Exception(f"Invalid audience: expected {USER_POOL_CLIENT_ID}, got {aud}")
#     message, encoded_signature = token.rsplit(".", 1)
#     decoded_signature = base64url_decode(encoded_signature.encode())
#     public_key = jwk.construct(jwt_key)
#     if not public_key.verify(message.encode(), decoded_signature):
#         raise Exception("signature verification failed")
#     return unverified

# class CustomAuth(HttpBearer):
#     def authenticate(self, request, token):
#         try:
#             claims = validate_token(token)
#             print("validated claims: ", claims)
#             return claims
#         except Exception as e:
#             print("Auth error: ", e)
#             return None
    


from ninja.security import HttpBearer
from jose import jwt, jwk
from jose.utils import base64url_decode
from datetime import datetime
import requests
import os

COGNITO_REGION = os.getenv("COGNITO_REGION")
USER_POOL_ID = os.getenv("USER_POOL_ID")
USER_POOL_CLIENT_ID = os.getenv("USER_POOL_CLIENT_ID")

JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
JWKS = requests.get(JWKS_URL).json()["keys"]

def validate_token(token: str):
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]

    jwt_key = next((key for key in JWKS if key["kid"] == kid), None)
    if not jwt_key:
        raise Exception("Public key not found")

    claims = jwt.get_unverified_claims(token)

    if claims["exp"] < datetime.utcnow().timestamp():
        raise Exception("Token expired")

    aud = claims.get("aud") or claims.get("client_id")
    if aud != USER_POOL_CLIENT_ID:
        raise Exception("Invalid audience")

    message, encoded_sig = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode())

    public_key = jwk.construct(jwt_key)
    if not public_key.verify(message.encode(), decoded_sig):
        raise Exception("Invalid signature")

    return claims


class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return validate_token(token)
        except Exception as e:
            print("Auth error:", e)
            return None
