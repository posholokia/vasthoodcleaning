from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class RedisConf(BaseSettings):
    redis_host: str
    redis_user: str
    redis_pass: str
    redis_port: int
    redis_db_code: int
    redis_db_token: int
    redis_db_cache: int
    redis_db_celery: int

    @property
    def broker_url(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                username=self.redis_user,
                password=self.redis_pass,
                host=self.redis_host,
                port=self.redis_port,
                path=str(self.redis_db_celery),
            )
        )

    @property
    def result_backend(self):
        return str(
            RedisDsn.build(
                scheme="redis",
                username=self.redis_user,
                password=self.redis_pass,
                host=self.redis_host,
                port=self.redis_port,
                path=str(self.redis_db_celery),
            )
        )
