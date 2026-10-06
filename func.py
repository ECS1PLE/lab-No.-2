def check_str(str: str) -> None:
    match new_data:
        case None:
            raise ValueError(
                "Запрос не может быть пустым. Пожалуйста, введите данные."
            )
        case str():
            new_data = new_data.strip()
            if not new_data:
                raise ValueError(
                    "Запрос не может быть пустым или состоять только из пробелов."
                )
        case _:
            raise TypeError("Запрос должен быть строкой.")