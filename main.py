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
from utils import createTodolist as ct

app = FastAPI()

models.Base.metadata.create_all(engine)
ct.create_todolist()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                reload=True, access_log=False)
