import json

class Parser:
    def __init__(self, response: str):
        self.__response = response

    def parse(self) -> list:
        data = json.loads(self.__response)
        return data["query"]["search"]