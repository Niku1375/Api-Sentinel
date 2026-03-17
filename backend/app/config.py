from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SMTP_HOST: str = "smtp.mailtrap.io"  # Test SMTP server
    SMTP_PORT: int = 2525                # Mailtrap port
    SMTP_USER: str                        # Mailtrap username
    SMTP_PASSWORD: str                    # Mailtrap password
    EMAIL_FROM: EmailStr                  # From address for alerts

    class Config:
        env_file = ".env"

settings = Settings()