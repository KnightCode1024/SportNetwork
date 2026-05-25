import asyncio

import httpx
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from sport_network_api.config.oauth.google import GoogleOAuthConfig

class GoogleOAuthClient:
    def __init__(self, config: GoogleOAuthConfig):
        self.config = config

    async def exchange_code(self, code: str, redirect_uri: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": self.config.CLIENT_ID,
                    "client_secret": self.config.CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            )
            resp.raise_for_status()
            return resp.json()

    async def verify_id_token(self, token: str) -> dict:
        # google-auth автоматически загрузит публичные ключи и проверит подпись, aud, iss, exp
        loop = asyncio.get_event_loop()
        user_info = await loop.run_in_executor(
            None,
            lambda: google_id_token.verify_oauth2_token(
                token, google_requests.Request(), self.config.CLIENT_ID
            )
        )
        if user_info.get("email_verified") is not True:
            raise ValueError("Email не подтверждён в Google")
        return user_info
