import heapq

class ElementoMapa:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node(ElementoMapa):
    def __init__(self, x, y, costo=0, heuristica=0):
        super().__init__(x, y)
        self.costo = costo
        self.heuristica = heuristica
        self.costo_total = costo + heuristica
        self.padre = None 

    def __lt__(self, other):
        return self.costo_total < other.costo_total

class Obstaculo(ElementoMapa):
    def __init__(self, x, y, tipo):
        super().__init__(x, y)
        self.tipo = tipo

class Mapa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.mapa = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, x, y, tipo):
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            self.mapa[x][y] = tipo
        else:
            raise ValueError("Las coordenadas del obstáculo están fuera del rango del mapa.")

    def quitar_obstaculo(self, x, y):
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            self.mapa[x][y] = 0
        else:
            raise ValueError("Las coordenadas del obstáculo están fuera del rango del mapa.")

    def es_accesible(self, x, y):
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            return self.mapa[x][y] != 1  # Sólo las paredes (tipo 1) son intransitables
        return False

    def imprimir_mapa(self, path=None):
        if path is None:
            path = []

        for i in range(self.alto):
            for j in range(self.ancho):
                if (i, j) in path:
                    print('*', end=' ')
                elif self.mapa[i][j] == 0:
                    print('.', end=' ')
                elif self.mapa[i][j] == 1:
                    print('|', end=' ')
                elif self.mapa[i][j] == 2:
                    print('~', end=' ')
                elif self.mapa[i][j] == 3:
                    print('\\', end=' ')
            print()
        print()

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    @staticmethod
    def heuristica(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def busqueda_a_star(self, inicio, fin):
        nodo_inicial = Node(inicio[0], inicio[1])
        nodo_final = Node(fin[0], fin[1])
        lista_abierta = []
        heapq.heappush(lista_abierta, nodo_inicial)
        lista_cerrada = set()
        g_costo = {(nodo_inicial.x, nodo_inicial.y): 0}

        while lista_abierta:
            nodo_actual = heapq.heappop(lista_abierta)
            lista_cerrada.add((nodo_actual.x, nodo_actual.y))

            if (nodo_actual.x, nodo_actual.y) == (nodo_final.x, nodo_final.y):
                path = []
                while nodo_actual:
                    path.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre
                return path[::-1]

            vecinos = [
                (nodo_actual.x - 1, nodo_actual.y),
                (nodo_actual.x + 1, nodo_actual.y),
                (nodo_actual.x, nodo_actual.y - 1),
                (nodo_actual.x, nodo_actual.y + 1)
            ]

            for vx, vy in vecinos:
                if self.mapa.es_accesible(vx, vy) and (vx, vy) not in lista_cerrada:
                    tipo_terreno = self.mapa.mapa[vx][vy]
                    if tipo_terreno == 0:
                        new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 1
                    elif tipo_terreno == 2:
                        new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 5
                    elif tipo_terreno == 3:
                        new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 10

                    if (vx, vy) not in g_costo or new_costo < g_costo[(vx, vy)]:
                        nodo_vecino = Node(vx, vy, new_costo, self.heuristica(Node(vx, vy), nodo_final))
                        nodo_vecino.padre = nodo_actual
                        g_costo[(vx, vy)] = new_costo
                        heapq.heappush(lista_abierta, nodo_vecino)

        return []

    def mostrar_ruta(self, inicio, fin):
        path = self.busqueda_a_star(inicio, fin)
        if path:
            print("Ruta encontrada: ")
            self.mapa.imprimir_mapa(path)
        else:
            print("No se encontró ninguna ruta válida.")

def obtener_coordenadas_validadas(mapa, mensaje):
    while True:
        try:
            x = int(input(f"Ingrese la coordenada X del {mensaje}: "))
            y = int(input(f"Ingrese la coordenada Y del {mensaje}: "))
            if 0 <= x < mapa.alto and 0 <= y < mapa.ancho and mapa.es_accesible(x, y):
                return x, y
            else:
                print("Coordenadas inválidas o ubicadas en un obstáculo. Por favor, ingrese nuevamente.")
        except ValueError:
            print("Formato de coordenadas inválido. Por favor, ingrese nuevamente.")

def main():
    ancho = 5
    alto = 5
    mapa = Mapa(ancho, alto)

    while True:
        print("Mapa Actual: ")
        mapa.imprimir_mapa()

        inicio = obtener_coordenadas_validadas(mapa, f"punto de inicio ({ancho - (ancho)}, {alto - 1})")
        fin = obtener_coordenadas_validadas(mapa, f"punto de fin ({ancho - (ancho)}, {alto - 1})")
        
        calculadora_rutas = CalculadoraRutas(mapa)
        calculadora_rutas.mostrar_ruta(inicio, fin)

        agregar_obstaculo = input("¿Desea agregar algún obstáculo? (s/n): ").strip().lower()
        if agregar_obstaculo == 's':
            try:
                obstaculo_x = int(input("Ingrese la coordenada X del obstáculo: "))
                obstaculo_y = int(input("Ingrese la coordenada Y del obstáculo: "))
                tipo_obstaculo = input("Ingrese el tipo de obstáculo (pared=1, agua=2, árbol=3): ").strip()

                if tipo_obstaculo not in ['1', '2', '3']:
                    print("Tipo de obstáculo inválido. Por favor, ingrese nuevamente.")
                    continue

                mapa.agregar_obstaculo(obstaculo_x, obstaculo_y, int(tipo_obstaculo))
            except ValueError:
                print("Formato de coordenadas inválido. Por favor, ingrese otra vez.")
                continue

        eliminar_obstaculo = input("¿Desea eliminar algún obstáculo? (s/n): ").strip().lower()
        if eliminar_obstaculo == 's':
            try:
                obstaculo_x = int(input("Ingrese la coordenada X del obstáculo a eliminar: "))
                obstaculo_y = int(input("Ingrese la coordenada Y del obstáculo a eliminar: "))
                mapa.quitar_obstaculo(obstaculo_x, obstaculo_y)
            except ValueError:
                print("Formato de coordenadas inválido. Por favor, ingrese otra vez.")
                continue

        continuar = input("¿Desea buscar otra ruta? (s/n): ").strip().lower()
        if continuar != 's':
            break

if __name__ == "__main__":
    main()
