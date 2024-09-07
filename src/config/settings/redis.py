from pydantic_settings import BaseSettings


class RedisConf(BaseSettings):
    redis_host: str
    redis_user: str
    redis_pass: str
    redis_port: int
    redis_db_code: int
    redis_db_token: int
    redis_db_cache: int
