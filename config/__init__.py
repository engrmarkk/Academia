import os
from decouple import config
from datetime import timedelta

# This is the base directory for the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# This is the database name
# db_name = 'academia'
#
# # this is the default uri for the database
# # it uses the database name from above
# default_uri = "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', db_name)
#
# # This is the uri for the database
# # it gets the uri from the environment variable DATABASE_URL
# # if the environment variable is not set, it uses the default uri
# uri = os.getenv('DATABASE_URL', default_uri)
# # if the uri starts with postgres://, replace it with postgresql://
# # this is to make it compatible with sqlalchemy
# if uri.startswith('postgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)


# This is the configuration object that will be used by the application
class Config:
    # This is the secret key for the application
    SECRET_KEY = config("SECRET_KEY", "secretkey")


class DevConfig(Config):
    # This is the debug mode for the application
    DEBUG = True
    # This is the testing mode for the application
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This is the database URI for the application
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "mgt_system.sqlite3")


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)


# This is the dictionary that contains the configuration object
config_object = {"development": DevConfig,
                 "prodcon": ProdConfig}


"""

"""