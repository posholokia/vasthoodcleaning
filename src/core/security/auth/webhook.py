import hmac
import hashlib

from config.settings import conf
from ninja.security import APIKeyHeader


class ApiKey(APIKeyHeader):
    """
    Аутентификация для входящих запросов на вебхук из crm.
    """
    param_name = "Api-Signature"

    def authenticate(self, request, key):
        timestamp = request.headers.get("Api-Timestamp")
        body = request.body.decode()
        signature_body = f"{timestamp}.{body}"
        allowed_signature = hmac.new(
            key=conf.house_pro_signin_key.encode(),
            msg=signature_body.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return key == allowed_signature


class ApiKeyLocal(APIKeyHeader):
    """
    Аутентификация для входящих запросов на вебхук из crm.
    Для локальной разработки принимает любой key.
    """
    param_name = "Api-Signature"

    def authenticate(self, request, key):
        return True
