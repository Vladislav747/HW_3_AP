import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils_new.utils import generate_short_code, is_valid_url, generate_access_token


@pytest.mark.parametrize("url,expected", [
    ("https://example.com", True),
    ("http://test.ru", True),
    ("invalid-url", False),
])
def test_url_validation(url, expected):
    assert is_valid_url(url) == expected


def test_short_code_generation_are_unique():
    code1 = generate_short_code()
    code2 = generate_short_code()
    assert code1 != code2


def test_access_token_length():
    token = generate_access_token()
    # Стандартный размер для token_urlsafe(32) - 43 символа
    assert len(token) == 43
    code1 = generate_access_token()
    code2 = generate_access_token()
    assert code1 != code2


def test_access_token_is_unique():
    token1 = generate_access_token()
    token2 = generate_access_token()
    assert token1 != token2


@pytest.mark.parametrize("url, expected", [
    ("https://example.com", True),
    ("http://example.org/path?query=1", True),
    ("ftp://files.example.com", True),
    ("https://localhost:8000", True),
    ("https://sub.domain.co.uk", True),

    ("example.com", False),  # Нет схемы
    ("http://", False),  # Нет домена
    ("https:/example.com", False),  # Неправильный формат
    ("javascript:alert(1)", False),  # Опасные схемы
    ("", False),  # Пустая строка
    (None, False),  # None вместо строки
])
def test_url_validation(url, expected):
    assert is_valid_url(url) == expected
