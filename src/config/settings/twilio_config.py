from pydantic_settings import BaseSettings


class SMSTwilioConfig(BaseSettings):
    account_sid: str
    auth_token: str
    from_number: str
