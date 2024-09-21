import httpx
from loguru import logger

from .decorators import retry
from .exceptions import HttpRequestError


class HttpRequest:
    @retry
    def post(
        self,
        url: str,
        body: dict[str, str] | None = None,
        header: dict[str, str] | None = None,
    ) -> httpx.Response:
        with httpx.Client() as session:
            response = session.post(url=url, json=body, headers=header)
        self._check_error(response, "POST")
        return response

    @retry
    def get(
        self, url: str, header: dict[str, str] | None = None
    ) -> httpx.Response:
        with httpx.Client() as session:
            response = session.get(url=url, headers=header)
        self._check_error(response, "GET")
        return response

    @retry
    def delete(
        self, url: str, header: dict[str, str] | None = None
    ) -> httpx.Response:
        with httpx.Client() as session:
            response = session.delete(url=url, headers=header)
        self._check_error(response, "DELETE")
        return response

    @staticmethod
    def _check_error(response: httpx.Response, method: str) -> None:
        if response.status_code >= 400:
            logger.error(
                "Ошибка при отправке HTTP {} запроса. "
                "url: {}, header: {}, status: {}, response: {}",
                method,
                response.url,
                response.headers,
                response.status_code,
                response.text,
            )
            raise HttpRequestError()
