class BaseConfig(object):

    dialct = "mysql"
    driver = "pymysql"
    host = ""
    port = "3306"
    user = ""
    password = ""
    database = ""

    SQLALCHEMY_DATABASE_URI = (
        f"{dialct}+{driver}://{user}:{password}@{host}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
