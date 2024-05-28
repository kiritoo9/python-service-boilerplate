from fastapi import APIRouter

from src.applications.auths.model import Payload
from src.applications.auths.resolver import Resolvers

# initate route prefix
router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

# your route here
@router.post("/login")
async def login(payload: Payload):
    return await Resolvers().validate_user_login(payload)