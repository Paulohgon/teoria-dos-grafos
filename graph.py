from Vertex import Vertex
import sys
import itertools

class Graph():

    def __init__(self):
        self.dict = {}
        self.numVertices = 0
        self.vertices = []
        self.arestas = [] # usado no hierholzer

    def __iter__(self):
        return iter(self.dict.values())

    def add_vertex(self, node):
        self.numVertices = self.numVertices + 1
        new_vertex = Vertex(node)
        self.dict[node] = new_vertex
        self.vertices.append(node)
        return new_vertex

    def get_vertex(self, n):
        if n in self.dict:
            return self.dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.dict:
            self.add_vertex(frm)
        if to not in self.dict:
            self.add_vertex(to)
        self.arestas.append((frm,to,0)) # Usado no hierholzer, (vertice, vertice, explorado(1) ou nao(0))
        self.arestas.append((frm,to,0)) # caso for grafo nao direcionado
        self.dict[frm].add_neighbor(self.dict[to], cost)
        self.dict[to].add_neighbor(self.dict[frm], cost)

    def get_vertices(self):
        return self.dict.keys()

    def is_adj(self, node1, node2):
        if node1 in self.dict and node2 in self.dict:
            vertex = self.get_vertex(node1)
            if self.get_vertex(node2) in vertex.adj:
                return True
            else:
                return False

    def bfs(self, node, saida):
        self.dict[node].explored = 1
        q = []
        q.append(node)
        ex = []
        while(len(q) > 0):
            v = q.pop(0)
            for x in self.dict[v].get_connections():
                if(x.explored == 0):
                    x.explored = 1
                    q.append(x.get_id())
                    ex.append(x.get_id())

                    return

    def existe_inexplorados(self):
        for node in self.dict:
            if self.get_vertex(node).explored == 0:
                return True
        return False

    def menor_dist(self):
        min = 999999999

        for d in self.dict:
            if self.get_vertex(d).explored == 0:
                if self.get_vertex(d).dist < min:
                    min = self.get_vertex(d).dist
                    nome_menor = self.get_vertex(d).id
        return nome_menor

    def dijkstra(self, node):
        self.get_vertex(node).dist = 0
        while(self.existe_inexplorados()):
            u = self.menor_dist()
            self.get_vertex(u).explored = 1
            for v in self.dict[u].get_connections():
                if v.explored == 0 and self.dict[u].dist + self.dict[u].get_weight(v) < v.dist:
                    v.dist = self.dict[u].dist + self.dict[u].get_weight(v)
                    v.pred = u

    def BellmanFord(self, node):
        self.get_vertex(node).dist = 0
        x = (self.numVertices)
        i = 1
        for i in range(x-1):
            for u in self.dict.values():
                for v in u.adj:
                    if u.dist != sys.maxsize and u.dist + u.get_weight(v) < v.dist:
                        v.dist = u.dist+(u.dist + u.get_weight(v))

    def FloydWarshall(self):
        n = self.numVertices
        linha = []
        matriz = [] 

        for i in range(0, n):
            linha = []
            for j in range(0, n):
                i1 = self.get_vertex(self.vertices[i])
                j1 = self.get_vertex(self.vertices[j])
                if self.is_adj(self.vertices[i], self.vertices[j]):
                    linha.append (i1.get_weight(j1))
                elif(i == j):
                    linha.append( 0)
                else:
                    linha.append(sys.maxsize)
            matriz.append(linha)
        for k in range(0, n):
            for l in range(0, n):
                for m in range(0, n):

                    matriz[l][m] = min(matriz[l][m], (matriz[l][k]+matriz[k][m]))
        return matriz
    def ehEuleriano(self):
        impares =0
        for i in self.dict.values():
            if (i.grau_vertex()) % 2 != 0:
                 impares += 1
            if impares>2:
                return False
        return True

    def setUnexploredHierholzer(self): 
        for (u,v,w), count in zip(self.arestas, range(len(self.arestas))):
            self.arestas[count] = (u,v,0)

    def hierholzer(self):
            odd = 0
            oddVertex = 0

            for i in self.dict.values():
                if (i.grau_vertex()) % 2 != 0:
                    odd += 1
                    oddVertex = i
        
            if odd == 0:
                return(self.__hierholzerUtil('A'))
            
            elif odd > 0:
                return(self.__hierholzerUtil(oddVertex))

    def __hierholzerUtil(self, v):
        if self.ehEuleriano():
            self.setUnexploredHierholzer()
            cpath = []
            epath = []
            cpath = [v]+cpath

            while len(cpath) != 0:
                aux = True
                u = cpath[0]
                for (a,b,c) in self.arestas:
                    if c == 0 and a == u:
                        aux = False
                        v = b
                        break
                if aux :
                    epath = [u]+epath
                    cpath.remove(u)
                else:
                    cpath = [v]+cpath
                    for (a,b,c), count in zip(self.arestas, range(len(self.arestas))):
                        if self.arestas[count] == (u,v,0):
                            self.arestas[count] = (a,b,1)
                            break

                    for (a,b,c), count in zip(self.arestas, range(len(self.arestas))):
                        if self.arestas[count] == (v,u,0):
                            self.arestas[count] = (a,b,1)
                            break
                            
                            
            return list(reversed(epath))
        else:
            return None
    def subset(self,Grafo):
        return list(itertools.chain.from_iterable(itertools.combinations(Grafo.vertices, r) for r in range(len(Grafo.vertices)+1)))

    def minimum(self,S, j, d, C,Grafo):
        min = sys.maxsize
        for i in S:
            if i != j:
                if C[(S-j, i)] + d[i][j] < min:
                    min = C[(S-j, i) + d[i][j]]
        return min

    def minimum2(self,C, k, d, S,Grafo):
        min = sys.maxsize
        for l in S:
            if l != k:
                if C[(S, l)] + d[l][k] < min:
                    min = C[(S, l)] + d[l][k]
        return min

    def caixeiro_viajante(self,G, k):#k é rótulo
        C = {}
        C[((k), k)] = 0
        sub = self.subset(G)
        d = G.FloydWarshall()

        for s in range(2, G.numVertices):
            for S in sub:
                if len(S) == s and k in S:
                    C[(S, k)] = sys.maxsize
                    for j in S:
                        if j != k:
                            C[(S, j)] = self.minimum(S, j, d, C, G)
        
        return self.minimum2(C, k, d, S, G)
    def ordena(self):
        tuplas = []
        for i in self.dict:
            for j in self.dict:
                if self.get_vertex(j) in self.get_vertex(i).get_connections():
                    tuplas.append((i,j,self.get_vertex(i).adj[self.get_vertex(j)]))

        for i in range(len(tuplas)):
            for j in range(i,len(tuplas)):
                if tuplas[i][2]>tuplas[j][2]:
                    aux = tuplas[j]
                    tuplas[j] = tuplas[i]
                    tuplas[i] = aux

        return tuplas
    def kruskal(self):
        a = []
        s = {}
        for i in self.dict:
            s[i]=[i]
        e = self.ordena()
        for (u,v,k) in e:
            if s[u] != s[v]:
                a.append([u,v,k])
                x = s[u]+s[v]
                for y in x:
                    s[y]=x
        return a