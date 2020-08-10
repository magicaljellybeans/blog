from app import login
from flask_login import UserMixin


class User(UserMixin):
    id = 0
    username = 'editor'

@login.user_loader
def load_user(id):
    return User.get(id)
