import os
APP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/photohub'
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
SQLALCHEMY_DATABASE_URI='sqlite:///' + APP_PATH + '/tmp/photohub.db'
SECRET_KEY='7c401a1e5fd54c6cd8cd0d5016c2911157a6127815ab7686'
USERNAME='hurteng'
PASSWORD='123456'