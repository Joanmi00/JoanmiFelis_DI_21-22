import os

ficher = os.path.dirname(__file__)
docu = open(os.path.join(ficher, "op.txt"), "r")



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

