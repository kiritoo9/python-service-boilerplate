import datetime
import uuid
import math
import bcrypt

from src.helpers.set_message import set_message
from src.applications.users.model import Payload, PayloadInsert
from src.applications.users.business import Business

class Resolver:
    def __init__(self):
        self.user_business = Business()

    async def find_all(
        self,
        page: int,
        limit: int,
        keywords: str = None
    ):
        try:
            data = await self.user_business.get_user_list(page, limit, keywords)
            totalPage = await self.user_business.get_user_count(limit, keywords)

            # preparing data for response
            data = {
                "limit": limit,
                "currentPage": page,
                "totalPage": totalPage,
                "data": data
            }
            return set_message(message="Request success", code=200, data=data)
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))

    async def find_one(self, id: str):
        try:
            data = await self.user_business.get_user_by_id(id)
            if data is None:
                return set_message(message="Data is not found", code=404)
            return set_message(message="Request success", code=200, data=data)
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))

    async def create(self, payload: PayloadInsert):
        try:
            # check existing email
            user = await self.user_business.get_user_by_email(payload.email)
            if user is not None:
                return set_message(message="Email is already taken, please try another one", code=400)

            # hash password
            encoded_password = payload.password.encode("utf-8")
            payload.password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode("utf-8")

            # preparing and insert data to database
            data = {
                "id": str(uuid.uuid4()),
                "email": payload.email,
                "password": payload.password,
                "fullname": payload.fullname,
                "status": payload.status,
                "created_at": datetime.datetime.now(),
                "created_by": None
            }
            result = await self.user_business.create_user(data)

            # show response
            if result.get("success") == False:
                return set_message(message=result.get("error"), code=400)
            return set_message(message="Data successfully inserted", code=201, data=data)
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))

    async def update(self, id: str, payload: Payload):
        try:
            # check existing data by id
            data = await self.user_business.get_user_by_id(id)
            if data is None:
                return set_message(message="Data is not found", code=404)

            # check existing email
            user = await self.user_business.get_user_by_email(payload.email, id)
            if user is None:
                user = await self.user_business.get_user_by_email(payload.email)
                if user is not None:
                    return set_message(message="Email is already taken, please try another one", error=400)

            # preparing data to update
            data.email = payload.email
            data.fullname = payload.fullname
            data.updated_at = datetime.datetime.now()
            data.update_by = None
            
            # hash password if user filled password in payload
            if payload.password != "" and payload.password is not None:
                encoded_password = payload.password.encode("utf-8")
                data.password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode("utf-8")

            # updating data
            result = await self.user_business.update_user(data)

            # show response
            if result.get("success") == False:
                return set_message(message=result.get("error"), code=400)
            return set_message(message="Data successfully updated", code=201, data=payload)
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))

    async def remove(self, id: str):
        try:
            # check existing data by id
            data = await self.user_business.get_user_by_id(id)
            if data is None:
                return set_message(message="Data is not found", code=404)

            # preparing and updating data
            data.deleted = True
            data.updated_at = datetime.datetime.now()
            data.update_by = None
            result = await self.user_business.update_user(data)

            # show response
            if result.get("success") == False:
                return set_message(message=result.get("error"), code=400)
            return set_message(message="Data successfully deleted", code=201)
        except Exception as e:
            return set_message(message="Something went wrong", code=400, error=str(e))