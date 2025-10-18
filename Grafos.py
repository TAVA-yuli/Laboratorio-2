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
            aeropuertos.append((
                fila["Source Airport Code"],
                fila["Source Airport Name"],
                fila["Source Airport City"],
                fila["Source Airport Country"],
                fila["Source Airport Latitude"],
                fila["Source Airport Longitude"]
            ))
            aeropuertos.append((
                fila["Destination Airport Code"],
                fila["Destination Airport Name"],
                fila["Destination Airport City"],
                fila["Destination Airport Country"],
                fila["Destination Airport Latitude"],
                fila["Destination Airport Longitude"]
            ))

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
        for _, fila in df.iterrows():
            u = self.indice_por_codigo(fila["Source Airport Code"])
            v = self.indice_por_codigo(fila["Destination Airport Code"])

            if u == -1 or v == -1:
                continue

            if columna_peso and columna_peso in fila:
                peso = fila[columna_peso]
            else:
                peso = 1

            self.agregar_arista(u, v, peso)
    


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
        
        if componentes == 1:
            print("Grafo conexo")
        else:
            print("Grafo no conexo")
            print(f"Numero de componentes: {componentes}")
            for i in range(componentes):
                print (f"Componente {i+1}: {n_componentes[i]} vertices")



# Pruebas
grafo = Grafo(4, True, False)
v1 = Vertice("JFK", "Nueva York Airport", "New York", "USA", 40.639751, -73.778925)
v2 = Vertice("LAX", "LA Airport", "Los Ángeles", "USA", 33.942791, -118.410042)
v3 = Vertice("LHR", "Heathrow Airport", "London", "United Kingdom", 51.470020, -0.454295)
v4 = Vertice("HND", "Haneda Airport", "Tokyo", "Japan", 35.549393, 139.779838)
grafo.agregar_vertice(0, v1)
grafo.agregar_vertice(1, v2)
grafo.agregar_vertice(2, v3)
grafo.agregar_vertice(3, v4)
grafo.agregar_arista(0, 1, 500)
grafo.agregar_arista(2, 3, 100)



def detectar_repetidos(df):
    # 1️⃣ Caso 1: repetidos dentro de la misma fila (origen = destino)
    mismos_en_fila = df[df['Source Airport Code'] == df['Destination Airport Code']]

    # 2️⃣ Caso 2: repetidos en distintas filas (aparece más de una vez en total)
    # Unimos todas las apariciones de aeropuertos (origen y destino)
    todos_aeropuertos = pd.concat([df['Source Airport Code'], df['Destination Airport Code']], ignore_index=True)

    # Contamos cuántas veces aparece cada aeropuerto
    conteo = todos_aeropuertos.value_counts()

    # Filtramos los que aparecen más de una vez
    repetidos = conteo[conteo > 1]

    # Mostrar resultados
    if not mismos_en_fila.empty:
        print("✈️ Aeropuertos repetidos dentro de la misma fila (origen = destino):")
        print(mismos_en_fila[['Source Airport Code', 'Destination Airport Code']])
    else:
        print("✅ No hay aeropuertos repetidos dentro de la misma fila")

    if not repetidos.empty:
        print("\n🛫 Aeropuertos que se repiten en distintas filas:")
        print(repetidos)
    else:
        print("✅ No hay aeropuertos repetidos entre filas")

    return mismos_en_fila, repetidos




df = pd.read_csv("flights_final.csv")
df1 = df.head(20)
g1 = Grafo(len(df1), True, False)
g1.aeropuertos(df1)
df1 = g1.haversine(df1)
g1.vuelos(df1, "Haversine")
g1.mostrar()
g1.conexidad()

detectar_repetidos(df1)