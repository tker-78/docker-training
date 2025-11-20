import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError



load_dotenv()
app = FastAPI()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
ALGORITHM = "HS256"

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_ID,
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET)


security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = keycloak_openid.decode_token(
            token
        )
        return decoded_token

    except KeycloakAuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token: {e}",
        )

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": "Access granted", "user": user["preferred_username"]}

@app.get("/")
def root():
    return {"message": "Hello World"}
