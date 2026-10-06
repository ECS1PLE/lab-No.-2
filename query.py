from func import check_str
from requests import get

from const import BASE_URL, SEARCH_PARAMS

class QueryUser:
    def __init__(self, query: str):
        self.__str = query

    @property
    def str(self):
        return self.__str

    @str.setter
    def str(self, new_str: str) -> None:
        check_str(new_str)
        self.__str = new_str.strip()

    def send_query(self) -> dict:
        params = {
            **SEARCH_PARAMS,
            "srsearch": self.__str,
        }

        response = get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        return response.json()