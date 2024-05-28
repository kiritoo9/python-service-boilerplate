import uvicorn
from fastapi import FastAPI, status, Request
from src.configs.config import settings
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.helpers.set_message import set_message
from src.configs.database import Base, engine
from src.middlewares.verify import verify_token

# import transactional routes
import src.applications.auths.route as auth_routes
import src.applications.users.route as user_routes

# config application
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    create_tables()
    return app

app = start_application()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# call middleware
@app.middleware("http")
async def __verifyToken(request: Request, call_next):
    middleware_response = await verify_token(request.headers.get("authroization"), str(request.url))
    if middleware_response.get("code") != 401:
        return await call_next(request)
    else:
        response = {
            "message": middleware_response.get("message"),
            "code": 401
        }
        return JSONResponse(content=response, status_code=401)

# health check route
class HealthCheck(BaseModel):
    status: str = "OK"

@app.get(
    "/health_check",
    tags=["health_check"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

# welcome route
@app.get("/")
async def welcome():
    return set_message(message=f'Welcome to {settings.APP_NAME}', code=200, data={"version": f'{settings.APP_VERSION}'})

# regist transactional routes
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

# run application
def main() -> None:
    uvicorn.run("main:app", host=settings.APP_HOST, port=int(settings.APP_PORT))
    
if __name__ == "__main__":
    main()