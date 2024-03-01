import httpx
import typing as t
import config
import time
from types import TracebackType
import json as js

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

_T = t.TypeVar("_T")


class RequestClient:
    def __init__(
        self,
        cookies: t.Optional[CookieTypes] = None,
        proxies: t.Optional[ProxiesTypes] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        verify: VerifyTypes = True,
        cert: t.Optional[CertTypes] = None,
        trust_env: bool = True,
    ) -> None:

        # proxy = (
        #     httpx.Proxy(config.get("HTTP_PROXY", raise_error=True))
        #     if bool(config.get("HTTP_PROXY", False))
        #     else proxies
        # )

        # self.base_url = "https://dev.iiidevops.org/prod-api"
        self.base_url = config.get("III_BASE_URL")

        # self.base_url = config.get("")
        self.access_token = "1"
        self.expire_at = 0
        self._client = httpx.Client(
            cookies=cookies,
            proxies=None,
            cert=cert,
            verify=verify,
            timeout=timeout,
            trust_env=trust_env,
        )

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def is_base_url_available(self, timeout: TimeoutTypes = 3) -> bool:
        try:
            self._client.get(self.base_url, timeout=timeout)
            return True
        except httpx.ConnectError:
            return False

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def __del__(self) -> None:
        if self.is_closed():
            return

        # logger.debug("HTTPX client is not closed, closing it now...")
        self.close()

    def login(self):
        data = {"username": config.get("USER_NAME"), "password": config.get("PASSWORD")}

        self.access_token = self.post("/user/login", json=data)["data"].get("token")

    def api_request(
        self,
        method: str,
        url: str,
        *,
        params: t.Optional[QueryParamTypes] = None,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ):
        url = "{}{}".format(self.base_url, url)

        # with self._client as client:
        while True:
            if headers:
                headers.update({"Authorization": f"Bearer {self.access_token}"})
            else:
                headers = {"Authorization": f"Bearer {self.access_token}"}

            api_response = self._client.request(
                method=method,
                url=url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                auth=auth,
                follow_redirects=follow_redirects,
            )

            if api_response.status_code // 100 == 2:
                return api_response.json()

            elif (
                api_response.status_code == 401
                and api_response.reason_phrase == "UNAUTHORIZED"
            ):
                self.login()
                continue

            else:
                api_response = js.loads(api_response.content.decode("ascii"))["message"]

                raise Exception(js.dumps(api_response))

    def get(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:

        return self.api_request(
            "GET",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def post(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:

        return self.api_request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def put(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.api_request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def patch(
        self,
        url: URLTypes,
        *,
        content: t.Optional[RequestContent] = None,
        data: t.Optional[RequestData] = None,
        files: t.Optional[RequestFiles] = None,
        json: t.Optional[t.Any] = None,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.api_request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )

    def delete(
        self,
        url: URLTypes,
        *,
        params: t.Optional[QueryParamTypes] = None,
        headers: t.Optional[HeaderTypes] = None,
        auth: t.Optional[AuthTypes] = None,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        return self.api_request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
        )


client_request = RequestClient()
