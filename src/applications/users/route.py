from fastapi import APIRouter

from src.applications.users.model import Payload, PayloadInsert
from src.applications.users.resolver import Resolver

# initate route prefix
router = APIRouter(
    prefix = "/users",
    tags = ["masters.users"]
)

# your route here
@router.get("/")
async def list(page: int = 1, limit: int = 10, keywords: str = None):
    return await Resolver().find_all(page, limit, keywords)

@router.get("/{id}")
async def detail(id):
    return await Resolver().find_one(id)

@router.post("/")
async def create(payload: PayloadInsert):
   return await Resolver().create(payload)

@router.put("/{id}")
async def update(id, payload: Payload,):
    return await Resolver().update(id, payload)

@router.delete("/{id}")
async def remove(id):
    return await Resolver().remove(id)
