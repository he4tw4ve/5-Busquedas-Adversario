import juegos_simplificado as js
import minimax

"""
El estado va a ser una tupla de 27 elementos

0x  1x   2x

0  | 1  | 2       0y
---|----|---   
3  | 4  | 5       1y   |   0z
---|----|---
6  | 7  | 8       2y

9  | 10 | 11      0y
---|----|---
12 | 13 | 14      1y   |   1z 
---|----|---
15 | 16 | 17      2y  

18 | 19 | 20      0y
---|----|---
21 | 22 | 23      1y   |   2z 
---|----|---
24 | 25 | 26      2y 

Para seleccionar casillas en el gato usamos
indice = z*9 + y*3 + x
z*9 nos mueve a la capa que queremos
y*3 nos desplaza a la fila
x nos mueve a la columna.

"""

# clase del juego

class UltimateTicTacToe(js.JuegoZT2):

    def lineas_ganadoras(self):
        """
        Guarda todas las posibles conexiones de 3 que pueden hacer los jugadores
        """
        lineas = [] # lineas va a ser algo como [ [0,1,2] , [3,4,5] ... ] 

        for z in range(3):
            for y in range(3):
                linea = [z*9 + y*3 + x for x in range(3)] # filas por ejemplo [0,1,2] -> 9 lineas
                lineas.append(linea)
        
        for z in range(3):
            for x in range(3):
                linea = [z*9 + y*3 + x for y in range(3)] # columnas por ejemplo [0,3,6] -> 9 lineas
                lineas.append(linea)
        
        for z in range(3):
            lineas.append([z*9, z*9 + 4, z*9 + 8]) # diagonales cada capa como [0,4,8]  -> 6 lineas
            lineas.append([z*9 + 2, z*9 + 4, z*9 + 6])
            
        for y in range(3):
            for x in range(3):
                linea = [z*9 + y*3 + x for z in range(3)] # verticales entre capas como [0,9,18] -> 9 lineas
                lineas.append(linea)

        lineas.append([0, 13, 26])
        lineas.append([2, 13, 24]) # diagonales entre capas como [0,13,26], manualmente porque no se me ocurrio ciclo 
        lineas.append([6, 13, 20]) # estas son de esquina a esquina
        lineas.append([8, 13, 18])

        lineas.append([1,13,25])
        lineas.append([3,13,23]) # estas son internas, de arista a arista
        lineas.append([7,13,19]) 
        lineas.append([5,13,21])

        lineas.append([0,12,24])
        lineas.append([6,12,18]) # diagonales en las caras de afuera [0,12,24] etc.
        lineas.append([0,10,20])
        lineas.append([2,10,18])
        lineas.append([2,14,24])
        lineas.append([8,14,20])
        lineas.append([6,16,26])
        lineas.append([8,16,24])

        return lineas

    def inicializa(self):
        """
        Crea una lista de 27 elementos
        """
        if not hasattr(self, "lineas"):
            self.lineas = self.lineas_ganadoras()
        return tuple(27 * [0])
    
    def jugadas_legales(self, s, j):
        """
        Regresa las casillas vacias en el estado s
        """
        return [casilla for casilla in range(27) if s[casilla] == 0]
    
    def sucesor(self, s, a, j):
        """
        Estado que resulta de hacer la accion a, en el estado s, jugador j
        """
        s = list(s[:])
        s[a] = j
        return tuple(s)
    
    def terminal(self, s):
        """
        True si el estado es terminal, false de lo contrario
        """
        if 0 not in s or self.ganancia(s) != 0:
            return True
        return False
    
    def ganancia(self, s):
        """
        revisa si alguien conecto 3, si si, regresa el jugador que gano (1 o -1)
        """
        for linea in self.lineas:
            a, b, c = linea
            if s[a] != 0 and s[a] == s[b] == s[c]:
                return s[a]
        return 0
    
# clase de la interfaz

class InterfaceUltimateTicTacToe(js.JuegoInterface):
    def muestra_estado(self, s):
        raise NotImplementedError
    
    def muestra_ganador(self, g):
        raise NotImplementedError
    
    def jugador_humano(self, s, j):
        raise NotImplementedError

# Ordenamiento y evaluacion

def ordena_jugadas(jugadas, jugador):
    raise NotImplementedError

def evalua_estado(s):
    raise NotImplementedError

# main

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 8,
        "tiempo": 10,
        "ordena": ordena_jugadas,    #Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_estado       #Puede ser None o una función f(estado) -> número entre -1 y 1
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

    interfaz = InterfaceUltimateTicTacToe(
        UltimateTicTacToe(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )