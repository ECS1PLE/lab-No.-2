from json import JSONDecodeError

from requests.exceptions import RequestException

from browser import Browser
from input import InputData
from output import OutputData
from parser import Parser
from query import QueryUser


def main():
    while True:
        try:
            query = InputData(input("Введите поисковый запрос: "))
            break
        except ValueError as error:
            print(error)

    try:
        response = QueryUser(query.data).send_query()
        articles = Parser(response).parse()
    except RequestException as error:
        print(f"Ошибка обращения к Википедии: {error}")
        return
    except (JSONDecodeError, KeyError, TypeError):
        print("Не удалось разобрать ответ Википедии.")
        return

    OutputData(articles).show()

    article = query.choose_article(articles)

    if article is not None:
        try:
            Browser().open_article(article["pageid"])
        except Exception as error:
            print(f"Не удалось открыть статью: {error}")



if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена.")