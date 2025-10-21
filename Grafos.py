# pylint: disable=missing-class-docstring,missing-function-docstring

import math
import pandas as pd



class Vertice:

    def __init__(self, codigo, aeropuerto, ciudad, pais, latitud, longitud):
        self.codigo = codigo
        self.aeropuerto = aeropuerto
        self.ciudad = ciudad
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud



class Grafo:

    def __init__(self, n, ponderado=False, dirigido=False):
        self.n = n
        self.ponderado = ponderado
        self.dirigido = dirigido
        self.adyacencia = []
        self.vertices = [None] * n

        for _ in range(n):
            lista_vecinos = []
            self.adyacencia.append(lista_vecinos)


    def agregar_vertice(self, indice, vertice):
        if 0 <= indice < self.n:
            self.vertices[indice] = vertice


    def indice_por_codigo(self, codigo):
        for i, vertice in enumerate(self.vertices):
            if vertice and vertice.codigo == codigo:
                return i
        return -1


    def agregar_arista(self, u, v, peso=1):
        if self.ponderado:
            par1 = (v, peso)
            self.adyacencia[u].append(par1)
            if not self.dirigido:
                par2 = (u, peso)
                self.adyacencia[v].append(par2)
        else:
            self.adyacencia[u].append(v)
            if not self.dirigido:
                self.adyacencia[v].append(u)


    def mostrar(self): 
        print("Lista de adyacencia del grafo:")
        for i in range((self.n)):
            vertice = self.vertices[i]
            if vertice:
                nombre_vertice = f"{vertice.codigo}"
            else:
                nombre_vertice = f"Vértice {i}"
           
            if self.ponderado:
                vecinos = []
                for vecino, peso in self.adyacencia[i]:
                    vertice_vecino = self.vertices[vecino]
                    if vertice_vecino:
                        nombre_vecino = f"{vertice_vecino.codigo}"
                    else:
                        nombre_vecino = f"Vértice {vecino}"
                    vecinos.append((nombre_vecino, peso))
                print(f"Vértice {i}: {nombre_vertice} -> {vecinos}")
            else:
                vecinos = []
                for vecino in self.adyacencia[i]:
                    vertice_vecino = self.vertices[vecino]
                    if vertice_vecino:
                        nombre_vecino = f"{vertice_vecino.codigo} ({vertice_vecino.ciudad})"
                    else:
                        nombre_vecino = f"Vértice {vecino}"
                    vecinos.append(nombre_vecino)
                print(f"Vértice {i}: {nombre_vertice} -> {vecinos}")



    # Metodos csv
    def aeropuertos(self, df):
        aeropuertos = []

        for _, fila in df.iterrows():
            origen = (
                fila["Source Airport Code"],
                fila["Source Airport Name"],
                fila["Source Airport City"],
                fila["Source Airport Country"],
                fila["Source Airport Latitude"],
                fila["Source Airport Longitude"]
            )
            destino = (
                fila["Destination Airport Code"],
                fila["Destination Airport Name"],
                fila["Destination Airport City"],
                fila["Destination Airport Country"],
                fila["Destination Airport Latitude"],
                fila["Destination Airport Longitude"]
            )
        
            origen_repetido = False
            for a in aeropuertos:
                if a[0] == origen[0]:
                    origen_repetido = True
                    break

            if not origen_repetido:
                aeropuertos.append(origen)

            destino_repetido = False
            for a in aeropuertos:
                if a[0] == destino[0]:
                    destino_repetido = True
                    break

            if not destino_repetido:
                aeropuertos.append(destino)

        df_aeropuertos = pd.DataFrame(aeropuertos, columns=[
        "CODE", "AIRPORT", "CITY", "COUNTRY", "LAT", "LON"])

        self.n = len(df_aeropuertos)
        self.vertices = [None] * self.n
        self.adyacencia = [[] for _ in range(self.n)]

        for i, fila in df_aeropuertos.iterrows():
            vertice = Vertice(
                fila["CODE"],
                fila["AIRPORT"],
                fila["CITY"],
                fila["COUNTRY"],
                fila["LAT"],
                fila["LON"]
            )
            self.agregar_vertice(i, vertice)


    def haversine(self, df):
        R = 6371.0

        distancias = []
        for _, fila in df.iterrows():
            lat1, lon1 = fila["Source Airport Latitude"], fila["Source Airport Longitude"]
            lat2, lon2 = fila["Destination Airport Latitude"], fila["Destination Airport Longitude"]

            lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
            lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad

            a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distancia = R * c

            distancias.append(distancia)

        df["Haversine"] = distancias
        return df


    def vuelos(self, df, columna_peso=None):
        aristas = []

        for _, fila in df.iterrows():
            u = self.indice_por_codigo(fila["Source Airport Code"])
            v = self.indice_por_codigo(fila["Destination Airport Code"])

            if u == -1 or v == -1:
                continue

            if columna_peso and columna_peso in fila:
                peso = fila[columna_peso]
            else:
                peso = 1

            repetida = False
            for a in aristas:
                if ((a[0] == u and a[1] == v) or (a[0] == v and a[1] == u)):
                    repetida = True
                    break

            if not repetida:
                self.agregar_arista(u, v, peso)
                aristas.append((u, v))
    


    # Punto 1
    def conexidad(self):
        if self.n == 0:
            return True
        
        visitados = [False] * self.n
        componentes = 0
        n_componentes = []
        
        def dfs(vertice):
            visitados[vertice] = True
            vecinos = self.adyacencia[vertice]
            tam = 1
            
            lista_vecinos = []
            for elemento in vecinos:
                if isinstance(elemento, tuple):
                    vertice_vecino, peso = elemento
                    lista_vecinos.append(vertice_vecino)
                else:
                    lista_vecinos.append(elemento)
                
            for vecino in lista_vecinos:
                if not visitados[vecino]:
                    tam += dfs(vecino)

            return tam
        
        for i in range(self.n):
            if not visitados[i]:
                componentes += 1
                tam_componente = dfs(i)
                n_componentes.append(tam_componente)
        
        if componentes == 0:
            componentes = 1
        
        print("\nConexidad: ")
        if componentes == 1:
            print("Grafo conexo")
        else:
            print("Grafo no conexo")
            print(f"\nNumero de componentes: {componentes}")
            for i in range(componentes):
                print (f"Componente {i+1}: {n_componentes[i]} vertices")



    def prim_vertice(self, inicio, visitados):
        aristas_arbol = []
        peso_total = 0
        
        cola = []
        cola.append((0, inicio, -1))
        
        while cola:
            indice_menor = 0
            for i in range(1, len(cola)):
                if cola[i][0] < cola[indice_menor][0]:
                    indice_menor = i
            
            peso, vertice_actual, vertice_padre = cola.pop(indice_menor)
            
            if visitados[vertice_actual]:
                continue
            
            visitados[vertice_actual] = True
            if vertice_padre != -1:
                aristas_arbol.append((peso, vertice_padre, vertice_actual))
                peso_total += peso
            
            for elemento in self.adyacencia[vertice_actual]:
                if self.ponderado:
                    vecino, peso_arista = elemento
                else:
                    vecino, peso_arista = elemento, 1
                
                if not visitados[vecino]:
                    cola.append((peso_arista, vecino, vertice_actual))
        
        return peso_total, aristas_arbol

    

    def prim_grafo(self):
        if self.n == 0:
            return []
        
        visitados = [False] * self.n
        todos_arboles = []
        
        for vertice_inicio in range(self.n):
            if not visitados[vertice_inicio]:
                peso, aristas = self.prim_vertice(vertice_inicio, visitados)
                todos_arboles.append((peso, aristas))
        
        return todos_arboles
    


    def arbol_expasion(self):
        arboles = self.prim_grafo()
        
        print("\nARBOLES DE EXPANSIÓN MÍNIMA")
        
        for i in range(len(arboles)):
            peso_componente, aristas_componente = arboles[i]
             
            print(f"\nComponente {i+1}")
            print(f"Peso total: {peso_componente}")
            print(f"Vértices: {len(aristas_componente) + 1}")
            print("Aristas:")
            
            for arista in aristas_componente:
                peso, u, v = arista
                nombre_u = self.vertices[u].codigo if self.vertices[u] else f"V{u}"
                nombre_v = self.vertices[v].codigo if self.vertices[v] else f"V{v}"
                print(f"  {peso} : {nombre_u} -> {nombre_v}")

        return arboles


# Pruebas
grafo = Grafo(5, True, False)
v1 = Vertice("JFK", "Nueva York Airport", "New York", "USA", 40.639751, -73.778925)
v2 = Vertice("LAX", "Los Angeles Airport", "Los Angeles", "USA", 33.942791, -118.410042)
v3 = Vertice("MIA", "Miami International", "Miami", "USA", 25.79325, -80.290556)
v4 = Vertice("JFK", "Nueva York Airport", "New York", "USA", 40.639751, -73.778925)
v5 = Vertice("MIA", "Miami International", "Miami", "USA", 25.79325, -80.290556)
grafo.agregar_vertice(0, v1)
grafo.agregar_vertice(1, v2)
grafo.agregar_vertice(2, v3)
grafo.agregar_vertice(3, v4)
grafo.agregar_vertice(4, v4)
grafo.agregar_arista(0, 1, 500)
grafo.agregar_arista(1, 2, 400)
grafo.agregar_arista(2, 0, 600)
grafo.agregar_arista(0, 1, 500)
grafo.agregar_arista(1, 2, 400)


# Menu
df = pd.read_csv("flights_final.csv")
df1 = df.head(20)
g1 = Grafo(len(df1), True, False)
g1.aeropuertos(df1)
df1 = g1.haversine(df1)

g1.vuelos(df1, "Haversine")

def menu():
    print("\nLAB 2 — Grafos - Rutas Transporte Aereo")
    print("1) Grafo")
    print("2) Conexidad")
    print("3) Arbol de expansion minima")

    print("0) Salir")
    return input("Elige opción: ").strip()

while True:
        op = menu()
        if op == "0":
            break

        elif op == "1":
            g1.mostrar()

        elif op == "2":
            g1.conexidad()
        
        elif op == "3":
            g1.arbol_expasion()