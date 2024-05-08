from fastapi import FastAPI

from testTask.city import router

app = FastAPI()

app.include_router(router.router)
