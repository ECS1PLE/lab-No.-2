from func import check_str

class InputData:
    def __init__(self, data:str) -> None:
        self.__data = data

    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, new_data:str) -> None:
        check_str(new_data)
        self.__data = new_data

    def choose_article(self, articles: list) -> dict | None:
        if not articles:
            return None

        while True:
            try:
                number = int(input("Введите номер статьи: "))
            except ValueError:
                print("Введите целое число.")
                continue

            if 1 <= number <= len(articles):
                return articles[number - 1]

            print(f"Введите номер от 1 до {len(articles)}.")