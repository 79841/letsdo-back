import todolist
import user
import chatroom
import profile
import message

if __name__ == "__main__":
    todolist.create_todolist()
    user.create_admin()
    user.create_users()
    profile.create_profile_images()
    chatroom.create_chatrooms()
    message.create_messages()
