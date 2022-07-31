from fastapi import FastAPI
from routes import router as router_api


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(router_api)

    return application


app = get_application()
