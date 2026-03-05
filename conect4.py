"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que

0  1  2  3  4  5  6
7  8  9  10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

**** la lista realmente se ve como 
[0 1 2 3 4 5 6   7 8 9 10 11 12 13   14 15 16 17 18 19 20 ... ]
entonces para acceder a una casilla usamos 7 * i + a,
i siendo la fila y a la columna.

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax

class Conecta4(js.JuegoZT2):
    def inicializa(self):
        """
        Crea una tupla de 42 ceros que se usara como el estado.
        """
        return tuple([0 for _ in range(6 * 7)])
        
    def jugadas_legales(self, s, j):
        """
        Loop que va de 0 a 6, que son las casillas mas altas de cada columna,
        y devuelve una lista de las columnas que su casilla de hasta arriba
        no tenga ficha.

        Basicamente si la columna no esta llena hasta el tope la mete 
        a una lista y devuelve eso.
        """
        return (columna for columna in range(7) if s[columna] == 0)
    
    def sucesor(self, s, a, j):
        """
        Convierte el estado de una tupla a una lista

        Recibe la accion a, que es la columna en la que el jugador decidio poner ficha,
        y empezando por la fila de hasta abajo, hacia arriba, va checando si las casillas 
        estan vacias. Cuando encuentra una casilla vacia, le asigna j que sera 1 o -1.

        Basicamente simula que las fichas caen por la gravedad, hasta la casilla vacia
        de mas abajo.
        """
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        """
        Checa si algun jugador ganó, primero conectando 4 de forma vertical, luego horizontal,
        y luego en las diagonales.

        El primer loop itera sobre cada columna (range(7)), empezando por la fila de hasta arriba, 
        si hay cuatro piezas iguales conectadas. range(3) es para las filas e itera 
        solo hasta la fila 3 de arriba a abajo, porque a partir de la 4 ya no hay espacio para 4 fichas.

        El segundo loop itera sobre cada fila (range(6)), sobre las primeras 4 columnas de izquierda a derecha,
        si hay 4 fichas iguales conectadas. Del mismo modo solo las primeras 4 columnas porque a partir de la
        5 ya no caben 4 fichas iguales.

        Para la diagonal asi ↘:
        empieza desde la esquina izquierda arriba, y para moverte en diagonal asi ↘ sumas 8 a la posicion en 
        la que estas, ya que sumar 7 te mueve una fila para abajo y sumar 1 mas te mueve a la derecha.
        Itera sobre las primeras 4 columnas, y las primeras 3 filas, ya que despues de eso no hay espacio.

        Para la diagonal asi  ↙:
        Hace lo mismo pero para moverte en diagonal asi ↙, tienes que sumarle 6 al estado, ya que sumar 7 te
        mueve una fila abajo, y restar 1 te mueve a la izquierda. 
        Itera de la columna 4 en adelante, y las primeras 3 filas de arriba a abajo.
        """
        #Verticales
        for i in range(7):       # i es columna
            for j in range(3):   # j es fila
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
                
        #Horizontales
        for i in range(6):       # i es filaa
            for j in range(4):   # j es columna
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
                
        #Diagonales
        for i in range(4):        # i es columna
            for j in range(3):    # j es fila
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        """
        Revisa primero si ya no queda ningun espacio vacio en el tablero, si no queda 
        es terminal.

        Luego llama a ganancia, la cual devuelve 0 solamente si nadie ha ganado.
        Si ganancia devuelve -1 o 1 terminal devuelve True.

        """
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
        for i in range(6):
            print('|'.join(a[7 * i:7 * (i + 1)]))
            print('---+---+---+---+---+---+---\n')
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

# def ordena_jugadas(jugadas, s):
#    """
#    ordena las jugadas posibles para explorar en base a su distancia
#    al centro y si hay fichas adyacentes
#    """
#
#    def puntaje_columna(columna):
#        centro = abs(columna - 3)
#
#        adyacentes = sum(
#            1 for c in [columna - 1, columna + 1]
#            if 0 <= c <= 6
#            for fila in range(6)
#            if s[c + 7 * fila] != 0
#        )
#        return centro - adyacentes
#    
#    return sorted(jugadas, key = puntaje_columna)

def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    # como primer modificación cambié abs(x - 4) por
    # abs(x - 3) porque el indice de la columna del centro es 
    # 3, no 4.
    return sorted(jugadas, key=lambda x: abs(x - 3))

def evalua_3_2con(s):
    """
    Evalua el estado s para el jugador 1
    """
    # son los mismos ciclos que la funcion de ganancia, solo que para
    # 3 fichas en vez de 4
    conect3 = sum(
        1 for i in range(7) for j in range(4)    # grupos de 3 verticales del jugador 1
        if (s[i + 7 * j] == s[i + 7 * (j + 1)]   # i son columnas, j son filas
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4)    # grupos de 3 verticales
        if (s[i + 7 * j] == s[i + 7 * (j + 1)]   # del jugador -1
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5)    # grupos de 3 horizontales del 
        if (s[7 * i + j] == s[7 * i + j + 1]     # jugador 1
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5)    # grupos de 3 horizontales del 
        if (s[7 * i + j] == s[7 * i + j + 1]     # jugador -1
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4)    # lo mismo para la diagonal ↘
        if (s[i + 7 * j] == s[i + 7 * j + 8]     # j es fila i es columna
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4)    # diagonal ↙
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] # j es fila i es columna
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )

    conect2 = sum(
        1 for columna in range(7) for fila in range(5)                 # conexiones de 2 para el jugador 1, verticales
        if (s[columna + 7 * fila] == s[columna + 7 * (fila + 1)] == 1)
    ) - sum(
        1 for columna in range(7) for fila in range(5)                 # conexiones de 2 para el jugador -1, verticales
        if (s[columna + 7 * fila] == s[columna + 7 * (fila + 1)] == -1)
    ) + sum(
        1 for fila in range(6) for columna in range(6)                 # conexiones de 2 para el jugador 1, horizontales
        if (s[fila * 7 + columna] == s[fila * 7 + (columna + 1)] == 1)
    ) - sum(
        1 for fila in range(6) for columna in range(6)                 # conexiones de 2 para el jugador -1, horizontales
        if (s[fila * 7 + columna] == s[fila * 7 + (columna + 1)] == -1)
    ) + sum(
        1 for columna in range(6) for fila in range(5)                 # conexiones en la diagonal ↘ de 2 para el jugador 1
        if (s[columna + 7 * fila] == s[columna + 7 * fila + 8] == 1)
    ) - sum(
        1 for columna in range(6) for fila in range(5)                 # conexiones en la diagonal↘ de 2 para el jugador -1 
        if (s[columna + 7 * fila] == s[columna + 7 * fila + 8] == -1)
    ) + sum(
        1 for columna in range(1, 7) for fila in range(5)              # conexiones en la diagonal ↙ de 2 para el jugador 1
        if (s[columna + 7 * fila] == s[columna + 7 * fila + 6] == 1)
    ) - sum(
        1 for columna in range(1, 7) for fila in range(5)              # conexiones en la diagonal ↙ de 2 para el jugador -1
        if (s[columna + 7 * fila] == s[columna + 7 * fila + 6] == -1)
    )

    conect3 *= 10
    conect2 *= 5
    puntaje = conect3 + conect2

    total_grupos_3 = (7*4 + 6*5 + 5*4 + 5*4) * 10
    total_grupos_2 = (7*5 + 6*6 + 6*5 + 6*5) * 5
    maximo_grupos = total_grupos_2 + total_grupos_3

    promedio = puntaje / maximo_grupos

    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)

    return promedio

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 8,
        "tiempo": 10,
        "ordena": ordena_centro,    #Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_3_2con       #Puede ser None o una función f(estado) -> número entre -1 y 1
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()
