import juegos_simplificado as js
import minimax

"""
El estado es una tupla de 64 enteros

Los jugadores son 
Negro = 1
Blanco = -1
Vacio = 0

      0  1  2  3  4  5  6  7     

0    01 02 03 04 05 06 07 08
1    09 10 11 12 13 14 15 16 
2    17 18 19 20 21 22 23 24 
3    25 26 27 28 29 30 31 32 
4    33 34 35 36 37 38 39 40 
5    41 42 43 44 45 46 47 48 
6    49 50 51 52 53 54 55 56
7    57 58 59 60 61 62 63 64

"""

# helpers 

def fichas_a_voltear(s, fila, col, j, direccion):
    """
    En una dirección dada, devuelve lista de índices de fichas enemigas
    que quedarían sandwicheadas. Lista vacía si no hay ninguna.
    """
    raise NotImplementedError

def voltear_fichas(lst, a, j):
    """
    Voltea todas las fichas que correspondan tras colocar en índice a.
    Modifica lst in-place.
    """
    raise NotImplementedError

def legal(s, fila, col, j):
    """
    Una jugada (fila, col) es legal para el jugador j si:
    1. La casilla está vacía (ya se verifica antes de llamar esta función)
    2. Al menos una dirección produce un sandwich de fichas enemigas
    """
    raise NotImplementedError

def indice(fila, columna):
    """
    Convierte coordenadas a un indice plano.
    """
    raise NotImplementedError

def coords(indice):
    """
    Convierte un indice plano a una tupla de coordenadas.
    """      
    raise NotImplementedError
    

# clase del juego

class Othello(js.JuegoZT2):

    def inicializa(self):
        """
        Regresa una tupla de 64 ceros, y pone las fichas iniciales
        correspondientes en el centro.
        """
        s = [0] * 64

        s[3 * 8 + 3] = -1  # (3,3) blanco
        s[4 * 8 + 4] = -1  # (4,4) blanco
        s[3 * 8 + 4] = 1   # (3,4) negro
        s[4 * 8 + 3] = 1   # (4,3) negro
        return tuple(s)
    
    def jugadas_legales(self, s, j):
        jugadas = []
        for f in range(8):
            for c in range(8):
                if s[indice(f, c)] == 0 and legal(s, f, c, j):
                    jugadas.append(indice(f, c))
    
        if not jugadas:
            if 0 not in s:  # tablero lleno
                return []
            else:
                return [None]   # pasar turno
    
        return jugadas
    
    def sucesor(self, s, a, j):
        if a is None:       # jugador pasa su turno
            return s        # el estado no cambia
        lst = list(s[:])
        lst[a] = j
        voltear_fichas(lst, a, j)
        return tuple(lst)

    def terminal(self, s):
        """
        El juego termina si:
        - El tablero está lleno, O
        - Ningún jugador tiene jugadas legales
        """
        # Caso 1: tablero lleno
        if 0 not in s:
            return True
    
        # Caso 2: ninguno de los dos puede jugar
        jugadas1 = self.jugadas_legales(s, 1)
        jugadas2 = self.jugadas_legales(s, -1)
        if jugadas1 == [None] and jugadas2 == [None]:
            return True
    
        return False
    
    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 (negro) en el estado terminal s.
        1 si gana negro, -1 si gana blanco, 0 empate.
        """
        negro = sum(1 for x in s if x == 1)
        blanco = sum(1 for x in s if x == -1)
        if negro > blanco:
            return 1
        elif negro < blanco:
            return -1
        else:
            return 0

    
# clase de la interfaz

class InterfaceOthello(js.JuegoInterface):

    def muestra_estado(self, s, j):
        """
        Muestra el estado del juego
        """
        raise NotImplementedError
    
    def muestra_ganador(self, ganancia):
        """
        Muestra el ganador cuando se acaba el juego
        """
        raise NotImplementedError
            
    def jugador_humano(self, s, j):
        """
        Pide jugada al jugador humano
        """
        raise NotImplementedError
            
    def pide_jugada(self, jugador, s, j):
        """
        Pide al jugador escoger la jugada a realizar, entre las acciones posibles
        """
        raise NotImplementedError

# Ordenamiento y evaluacion

def ordena_jugadas(jugadas, jugador):
    """
    Ordena las jugadas por proximidad al centro del tablero.
    """
    raise NotImplementedError

def evalua_estado(s):
    """
    Evalúa el estado: (fichas negro - fichas blanco) / 64
    """
    raise NotImplementedError

# main

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Humano",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": ordena_jugadas,    #Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_estado    #Puede ser None o una función f(estado) -> número entre -1 y 1
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

    interfaz = InterfaceOthello( Othello(), jugador1=jugador_cfg(cfg["Jugador 1"]), jugador2=jugador_cfg(cfg["Jugador 2"]))

    interfaz.juega()
