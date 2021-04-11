import os
import uvicorn
import time

from fastapi import FastAPI
from config import config
from handlers import add_all_handler
from routers import include_all_router
# from starlette.middleware.cors import CORSMiddleware

def application() -> FastAPI:
    app = FastAPI()
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    add_all_handler(app)

    include_all_router(app)

    return app


app = application()

if __name__ == "__main__":
    uvicorn.run("xway:app", **config.APP)