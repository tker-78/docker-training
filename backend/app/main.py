import logging
import os
import time
from typing import Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBearer
from keycloak import KeycloakOpenID
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

load_dotenv()
logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)

app = FastAPI()
security = HTTPBearer()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "dev-session-secret")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173/")
CALLBACK_URL = os.getenv(
    "BACKEND_CALLBACK_URL",
    "http://localhost:8000/auth/callback",
)

if not all([KEYCLOAK_URL, REALM, CLIENT_ID]):
    raise RuntimeError(
        "Missing Keycloak configuration. Set KEYCLOAK_URL, REALM, and CLIENT_ID."
    )

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_ID,
    realm_name=REALM,
    # client_secret=CLIENT_SECRET,
)


@app.get("/auth/login")
def login(request: Request, redirect: Optional[str] = None) -> RedirectResponse:
    """Keycloakの認証画面へリダイレクトし、state/nonceをセッションに保持する。"""
    state = uuid4().hex
    nonce = uuid4().hex
    redirect_target = redirect or FRONTEND_URL

    request.session["state"] = state
    request.session["nonce"] = nonce
    request.session["redirect_target"] = redirect_target

    auth_url = keycloak_openid.auth_url(
        redirect_uri=CALLBACK_URL,
        scope="openid",
        state=state,
        nonce=nonce,
        response_mode="query",
        response_type="code",
    )

    logger.info(
        "Redirecting to Keycloak login with state=%s, redirect_target=%s",
        state,
        redirect_target,
    )
    return RedirectResponse(auth_url)


@app.get("/auth/callback")
def callback(
        request: Request,
        code: str,
        state: str
     ) -> RedirectResponse:
    """Keycloakの認証コールバックエンドポイント. Keycloakからの認証コードを受け取り, アクセストークンを取得する."""
    try:
        stored_state: Optional[str] = request.session.get("state")
        if stored_state is None or stored_state != state:
            raise HTTPException(
                status_code=400,
                detail="Invalid state"
            )

        # 認可コードを使ってトークンを取得
        tokens = keycloak_openid.token(
                    code=code,
                    grant_type="authorization_code",
                    redirect_uri=CALLBACK_URL
                )

        # nonceの検証
        stored_nonce: Optional[str] = request.session.get("nonce")
        decoded_token = keycloak_openid.decode_token(
            token=tokens["id_token"]
        )
        if stored_nonce is None or stored_nonce != decoded_token["nonce"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid nonce"
            )

        # トークン情報をセッションに保存
        request.session["access_token"] = tokens["access_token"]
        request.session["refresh_token"] = tokens["refresh_token"]

        expires_in: Optional[int] = tokens.get("expires_in")
        if expires_in:
            request.session["token_expires_in"] = time.time() + expires_in

        refresh_expires_in: Optional[int] = tokens.get("refresh_expires_in")
        if refresh_expires_in:
            request.session["refresh_expires_in"] = time.time() + refresh_expires_in

        redirect_target = request.session.pop("redirect_target", FRONTEND_URL)
        response = RedirectResponse(redirect_target)

        # クッキーにアクセストークンを格納する
        for name, value, age in [
            (
                "access_token",
                tokens["access_token"],
                tokens["expires_in"]
            ),
            (
                "refresh_token",
                tokens["refresh_token"],
                tokens.get("refresh_expires_in", 86400)
            ),
        ]:
            response.set_cookie(
                key=name,
                value=value,
                httponly=True,       # JavaScriptからアクセスできない
                secure=False,        # HTTPS 本番ではTrue
                samesite="lax",      # CSRF対策
                max_age=age,         # 有効期限
            )

        logger.info(
            "Auth callback completed; tokens stored. state=%s redirect_target=%s",
            state,
            redirect_target,
        )

        # 一度利用したstate/nonceは削除してCSRFリスクを下げる
        request.session.pop("state", None)
        request.session.pop("nonce", None)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}
