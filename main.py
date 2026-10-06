
from input import InputData

def main():
    while True:
        try:
            query = InputData(input("Введите поисковый запрос: "))
            break
        except ValueError as error:
            print(error)

if __name__ == "__main__":
    main()