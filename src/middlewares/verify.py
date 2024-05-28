import os
import jwt
from src.configs.config import settings

from src.applications.users.business import Business

async def verify_token(token: str, url: str):
    # get url request
    requested_url = None
    url = url.split(f':{settings.APP_PORT}')
    if len(url) > 1:
        url = url[1].split("?")
        if len(url) > 0:
            requested_url = url[0]

            # Remove slash in last character
            last = requested_url[len(requested_url)-1:]
            if last == "/":
                requested_url = requested_url[0:len(requested_url)-1]

    # free pass middleware check by route
    free_pass_routes = [
        "",
        "/auth/login"
    ]
    if requested_url is not None:
        if requested_url not in free_pass_routes:
            if token is None:
                return { "message": "Missing authorization header", "code": 401 }

            token = token[7:]
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

                # Check existing user
                user_business = Business()
                user = await user_business.get_user_by_id(decoded.get("id"))
                if user is None:
                    return { "message": "User is not found, probably token is expired already", "code": 401 }
                else:
                    return { "message": "You are authenticated", "code": 200 }
            except Exception as e:
                return { "message": "Token is not valid", "code": 401 }
        else:
            return { "message": "You have route free pass", "code": 200 }

    # allow all
    return { "message": "Invalid access token", "code": 401 }