from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = ''
    GOOGLE_TOKEN_URL: str = 'https://oauth2.googleapis.com/token' #'https://accounts.google.com/o/oauth/token'

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self):
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"