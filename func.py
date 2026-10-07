def check_str(data: str) -> None:
    if data is None:
        raise ValueError("Запрос не может быть пустым. Пожалуйста, введите данные.")
    if not isinstance(data, str):
        raise TypeError("Запрос должен быть строкой.")
    if not data.strip():
        raise ValueError(
            "Запрос не может быть пустым или состоять только из пробелов."
        )
