import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'adminkey'
