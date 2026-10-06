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