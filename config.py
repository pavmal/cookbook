import os


# Для указания пути к файлу БД воспользумся путем до текущего модуля
# - Текущая папка
current_path = os.path.dirname(os.path.realpath(__file__))
# - Путь к файлу БД в данной папке
#db_path = "sqlite:///" + current_path + "\\test.db"
db_path = 'postgresql://postgres:pass@127.0.0.1:5432/test'


class Config:
#    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = db_path
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # USERNAME = "123"
    # PASSWORD = "1234"