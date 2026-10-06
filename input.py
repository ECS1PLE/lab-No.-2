class InputData:
    def __init__(self, data):
        self.data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
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

        self.__data = new_data