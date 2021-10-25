import random


class menut(Exception):
    pass


class gran(Exception):
    pass


aleatori= random.randint(0, 100)
num = -8
while num != aleatori:
    try:
        num = int(input("Numero entre 0 i 100: "))
        if num < aleatori:
            raise menut()
        elif num > aleatori:
            raise gran()
        else:
            print("CORRECTE!!!")
            break
    except menut:
        print("es mes alt")
    except gran:
        print("es mes baixet")