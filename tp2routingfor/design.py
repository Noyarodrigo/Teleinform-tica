import os


def datain():
    nivel = []
    nivel.append(input("Ingrese la cantidad de niveles(routers): "))
    for i in range(0, nivel[0]):
        nivel.append(input('Ingrese la cantidad de routers del nivel {}: '.format(i+1)))

    os.system("clear")

    for i in range(0, nivel[0]):
        if i == 0:
            print('Nivel: {} (central) ===> Routers: {}').format(i+1, nivel[i+1])
        else:
            print('Nivel: {} ===> Routers: {}').format(i+1, nivel[i+1])
    return nivel
