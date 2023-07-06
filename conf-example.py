class BaseConfig(object):

    SECRET_KEY = 'Testing-Key1234ChangeMe'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_ENGINE_OPTIONS = { "pool_pre_ping": True, }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConf(BaseConfig):
    DEBUG=False
    

class DevConf(BaseConfig):
    DEBUG=True
    