from fastapi import FastAPI
import uvicorn
import models
from database import engine
from routers import chatroom, checkList, message, user, authentication, todoList, profile
from fastapi.middleware.cors import CORSMiddleware
from admin.routers import user as admin_route_user
from admin.routers import chatroom as admin_route_chatroom
from admin.routers import message as admin_route_message
from admin.routers import checkList as admin_route_checkList

app = FastAPI()

models.Base.metadata.create_all(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(message.router)
app.include_router(chatroom.router)
app.include_router(profile.router)
app.include_router(admin_route_user.router)
app.include_router(admin_route_chatroom.router)
app.include_router(admin_route_message.router)
app.include_router(admin_route_checkList.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=22222,
                reload=True, access_log=False)
