from pydantic_settings import BaseSettings


class HouseProConf(BaseSettings):
    house_pro_token: str
    house_pro_signin_key: str
