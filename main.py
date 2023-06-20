from fastapi import FastAPI
import uvicorn
import models
from database import engine
from routers import checkList, user, authentication, todoList, exception
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import status, Request

app = FastAPI()

models.Base.metadata.create_all(engine)

# app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.exception_handler(exception.AuthException)
# async def authentication_exception_handler(request: Request, exc: exception.AuthException):
#     return RedirectResponse(
#         '/auth',
#         status_code=status.HTTP_303_SEE_OTHER
#     )

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(todoList.router)
app.include_router(checkList.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=False)
