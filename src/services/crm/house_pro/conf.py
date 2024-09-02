from pydantic import HttpUrl
from config.settings import conf


AUTH_HEADER = {
    "Accept": "application/json",
    "Authorization": f"Token {conf.house_pro_token}"
}

BASE_URL = HttpUrl.build(
    scheme="https",
    host="api.housecallpro.com",
)
