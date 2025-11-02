import os
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import HTTPBearer
from fastapi_keycloak_middleware import KeycloakConfiguration, setup_keycloak_middleware, get_user
from typing import Union, Optional
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
ALGORITHM = "HS256"


keycloak_config = KeycloakConfiguration(
    url=KEYCLOAK_URL,
    client_id=CLIENT_ID,
    realm=REALM,
    client_secret=CLIENT_SECRET,
)

setup_keycloak_middleware(
    app,
    keycloak_configuration=keycloak_config,
)

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    roles: Optional[list[str]]


@app.get("/")
async def read_root(user: User = Depends(get_user)):
    return {"message": user.display_name}
