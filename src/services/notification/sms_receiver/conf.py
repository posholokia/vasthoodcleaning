from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class SMSTwilioConfig(BaseSettings):
    account_sid: str
    auth_token: str
