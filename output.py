class OutputData:
    def __init__(self, articles: list):
        self.__articles = articles

    def show(self) -> None:
        if not self.__articles:
            print("Ничего не найдено по вашему запросу")
            return

        number = 1

        for article in self.__articles:
            print(f"\nСтатья №{number}")

            for key, value in article.items():
                match key:
                    case "title":
                        print(f"Название: {value}")
                    case "pageid":
                        print(f"ID страницы: {value}")

            number += 1