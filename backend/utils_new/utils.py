import secrets

from urllib.parse import urlparse


# Генерация короткого кода (упрощенная реализация)
def generate_short_code() -> str:
    return secrets.token_urlsafe(6)


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
