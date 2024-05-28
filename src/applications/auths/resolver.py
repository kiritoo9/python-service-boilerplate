import bcrypt
import jwt

from src.configs.config import settings
from src.helpers.set_message import set_message

from src.applications.auths.model import Payload
from src.applications.users.business import Business

class Resolvers:
    def __init__(self):
        self.user_business = Business()

    async def validate_user_login(self, payload: Payload):
        try:
            data = await self.user_business.get_user_by_email(payload.email)
            if data is None:
                return set_message(message="User not found", code=401)

            # validate hash password
            encoded_password = payload.password.encode("utf-8")
            if bcrypt.checkpw(encoded_password, data.get("password").encode("utf-8")) is False:
                return set_message(message="Email and password does not match", code=401)

            # preparing token payloads
            payloads = {
                "id": str(data.get("id")),
                "email": data.get("email"),
                "fullname": data.get("fullname"),
                "role": "admin" # static data
            }
            encoded_jwt = jwt.encode(payloads, settings.SECRET_KEY, algorithm="HS256")
        
            # generate token and send response
            return set_message(message="You are authenticated", code=200, data={"access_token": encoded_jwt})
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))