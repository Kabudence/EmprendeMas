import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:gitano200J@@J@@@localhost/emprende_mas")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
