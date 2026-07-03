"""Service-agnostic HTTP client used across the trading-signal-engine.

Wraps a ``requests.Session`` so callers pick a verb (get/post/put) and pass
params/body. All verbs funnel through ``_request``, which centralizes URL
building, default param/header merging, timeout, and ``raise_for_status``.
Every method returns the raw ``requests.Response``.
"""

import requests

DEFAULT_TIMEOUT = 30


class HttpClientError(Exception):
    """Raised when a request fails. Wraps the underlying transport error."""


class HttpClient:
    def __init__(self, base_url="", default_params=None, default_headers=None, timeout=DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.default_params = default_params or {}
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, path):
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method, path, params=None, json=None, data=None, headers=None):
        try:
            response = self.session.request(
                method=method,
                url=self._build_url(path),
                params={**self.default_params, **(params or {})},
                json=json,
                data=data,
                headers={**self.default_headers, **(headers or {})},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise HttpClientError(str(error)) from error
        return response

    def get(self, path, params=None, headers=None):
        return self._request("GET", path, params=params, headers=headers)

    def post(self, path, json=None, data=None, params=None, headers=None):
        return self._request("POST", path, params=params, json=json, data=data, headers=headers)

    def put(self, path, json=None, data=None, params=None, headers=None):
        return self._request("PUT", path, params=params, json=json, data=data, headers=headers)
