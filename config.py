import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "annsetu-dev-secret-key-change-in-production"
    )

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:Yogi@localhost/annsetu_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False