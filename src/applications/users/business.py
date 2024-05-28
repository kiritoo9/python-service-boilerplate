import math
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.configs.database import DB_SESSION

from src.applications.users.model import Users

class Business:

    # init core connection
    def __init__(self):
        db: Session = DB_SESSION()
        self.db = db

    def __del__(self):
        self.db.close()

    # custom functions
    async def get_user_list(
        self,
        page: int,
        limit: int,
        keywords: str,
    ) -> list:

        # prepare filters
        filters = [Users.deleted == False]
        if keywords != "" and keywords is not None:
            filters.append(Users.fullname.ilike(f'%{keywords}%'))

        offset = 0
        if limit > 0 and page > 0:
            offset = (limit * page) - limit

        # getting data
        result = self.db.query(Users.id, Users.email, Users.fullname, Users.status, Users.created_at)\
            .filter(*filters)\
            .limit(limit)\
            .offset(offset)\
            .all()

        # preparing for response
        data = []
        for v in result:
            data.append({
                "id": v.id,
                "email": v.email,
                "fullname": v.fullname,
                "status": v.status,
                "created_at": v.created_at,
            })
        return data

    async def get_user_count(self, limit: int, keywords: str = None) -> int:
        # prepare filters
        filters = [Users.deleted == False]
        if keywords != "" and keywords is not None:
            filters.append(Users.fullname.ilike(f'%{keywords}%'))

        # getting data
        totalPage: int = 1
        count = self.db.query(Users)\
            .filter(*filters)\
            .count()
        if count > 0 and limit > 0:
            totalPage = math.ceil(count / limit)
        return totalPage

    async def get_user_by_id(self, id: str) -> dict:
        result = self.db.query(Users)\
            .filter(Users.deleted == False)\
            .filter(Users.id == str(id))\
            .first()

        if result is None:
            return None
        return result

    async def get_user_by_email(self, email: str, id: str = None) -> dict:
        filters = [Users.deleted == False, Users.email == email]
        if id is not None:
            filters.append(Users.id == id)

        result = self.db.query(Users.id, Users.email, Users.fullname, Users.password, Users.status, Users.created_at)\
            .filter(*filters)\
            .first()

        if result is None:
            return None
        return {
            "id": result.id,
            "email": result.email,
            "fullname": result.fullname,
            "password": result.password,
            "status": result.status,
            "created_at": result.created_at,
        }

    async def create_user(self, data: dict) -> dict:
        try:
            trx = Users(**data)
            self.db.add(trx)
            self.db.commit()
            self.db.refresh(trx)
            return {"success": True}
        except SQLAlchemyError as err:
            self.db.rollback()
            errorMessage = str(err.__dict__['orig'])
            return {"success": False, "error": errorMessage}

    async def update_user(self, data) -> dict:
        try:
            self.db.merge(data)
            self.db.commit()
            return {"success": True}
        except SQLAlchemyError as err:
            self.db.rollback()
            errorMessage = str(err.__dict__['orig'])
            return {"success": False, "error": errorMessage}
