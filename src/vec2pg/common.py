from urllib.parse import urlparse

POSTGRES_CONNECTION_STRING = "POSTGRES_CONNECTION_STRING"


def is_http_url(url: str) -> bool:
    return urlparse(url).scheme in {"https", "http"}
