from app import login
from flask_login import UserMixin


class User(UserMixin):
    def get_id(self):
        return "editor"

@login.user_loader
def load_user(id):
    return User()
