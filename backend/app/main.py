import os
import httpx
import pprint
from typing import Any
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from keycloak import KeycloakOpenID

load_dotenv()
app = FastAPI()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_ID,
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET)


security = HTTPBearer()

async def verify_access_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict[str, Any]:
    token = credentials.credentials

    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if not kid:
            raise HTTPException(
                status_code=401,
                detail="Invalid toke: No key ID"
            )

        jwks_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
        async with httpx.AsyncClient() as client:
            jwks_response = await client.get(jwks_url)
            jwks = jwks_response.json()

        rsa_key = {}
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = {
                    "kty": key.get("kty"),
                    "kid": key.get("kid"),
                    "use": key.get("use"),
                    "n": key.get("n"),
                    "e": key.get("e")
                }
        pprint.pprint(rsa_key)

        if not rsa_key:
            raise HTTPException(
                status_code=401,
                detail="Public key not found in JWKS"
            )

        # 発行者（Issuer）の設定
        # ここはlocalhost
        issuer = f"http://localhost:8080/realms/{REALM}"

        # トークン検証（署名、audience、発行者、有効期限）
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,  # audience検証を有効に
            issuer=issuer,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "verify_exp": True
            }
        )

        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired token: {e}"
        )


@app.get("/protected")
def get_current_user(payload: dict[str, Any] = Depends(verify_access_token)):
    try:
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: No user ID"
            )
        return {"message": f"succeeded: {user_id}"}
    except HTTPException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid or expired token: {e}"
        )


@app.get("/")
def root():
    return {"message": "Hello World"}
