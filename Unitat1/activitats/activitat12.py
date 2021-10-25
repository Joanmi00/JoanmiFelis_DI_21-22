import os

ficher = os.path.dirname(__file__)
docu = open(os.path.join(ficher, "op.txt"), "r")

class eNumeric(Exception):
    pass

class eOperacio(Exception):
    pass


try:

    for i in docu:
        espai = i.split(" ")

        if espai[1] == "+":
            resu = int(espai[0]) + int(espai[2])
            print(espai[0], espai[1], int(espai[2]), "=", resu)
                    
        elif espai[1] == "-":
            resu = int(espai[0]) - int(espai[2])
            print(espai[0], espai[1], int(espai[2]), "=", resu)

        elif espai[1] == "*":
            resu = int(espai[0]) * int(espai[2])
            print(espai[0], espai[1], int(espai[2]), "=", resu)
                
        elif espai[1] == "/":
            resu = int(espai[0]) / int(espai[2])
            print(espai[0], espai[1], int(espai[2]), "=", resu)

        elif espai[1] != "+" or espai[1] != "-" or espai[1] != "*" or espai[1] != "/":
            raise eOperacio

        elif espai[0].isalpha() or espai[2].isalpha():
            raise eNumeric
    
except eNumeric:
    print("No hi ha numero")

except eOperacio:
    print("la operació no es correcta")
