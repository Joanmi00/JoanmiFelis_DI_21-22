
llista = [1, 5, 4, 6, 8, 11, 3, 12]

nova_llista = list(filter(lambda x: x % 2 == 0, llista))

print(nova_llista)