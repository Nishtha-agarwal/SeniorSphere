from datetime import timedelta


class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'  # Replace with your mail server
    MAIL_PORT = 587  # Port for TLS
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'you-email.com'  # Replace with your email
    MAIL_PASSWORD = 'your-App-password'  # Replace with your email password
    MAIL_DEFAULT_SENDER = 'you-email.com'  # Replace with your sender email

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    EXPORT_FOLDER = "exports"

class LocalDevelopementConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///seniorsphere.sqlite3"
    DEBUG = True
    JWT_SECRET_KEY = 'vu$^rr66r&9tguogugpih;ijno[ej[ogne6478948wg8we4g8wejwobvuw'
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(hours=1)
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'