import secrets

# Генерация короткого кода (упрощенная реализация)
def generate_short_code() -> str:
    return secrets.token_urlsafe(6)