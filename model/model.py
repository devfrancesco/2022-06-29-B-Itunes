import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._album = []
        self._idMapA = {}
        self._path = []

    def getPath(self, id1, id2, soglia):
        album1 = self._idMapA[int(id1)]
        album2 = self._idMapA[int(id2)]
        parziale = [album1]
        bilancio = self.calcolaBilancio(album1)
        self._ricorsione(parziale, album2, bilancio, soglia)
        return self._path

    def _ricorsione(self, parziale, target, bilancio, soglia):
        if parziale[-1] == target:
            if len(parziale) > len(self._path):
                self._path = list(parziale)
        nodo_corrente = parziale[-1]
        for vicino in self._graph.neighbors(nodo_corrente):
            if vicino not in parziale:
                if self._graph[nodo_corrente][vicino]['weight'] >= soglia:
                    if self.calcolaBilancio(vicino) > bilancio:
                        parziale.append(vicino)
                        self._ricorsione(parziale, target, bilancio, soglia)
                        parziale.pop()


    def buildGraph(self, n):
        self._graph.clear()
        self._idMapA = {}
        self._album = DAO.getAllAlbum(n)
        for a in self._album:
            self._idMapA[a.AlbumId] = a
        self._graph.add_nodes_from(self._album)
        allEdges = DAO.getAllEdges(n, self._idMapA)
        for e in allEdges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def calcolaBilancio(self, source):
        in_d = self._graph.in_degree(source, weight='weight')
        out_d = self._graph.out_degree(source, weight='weight')
        bilancio = in_d - out_d
        return bilancio

    def getBilancio(self, id):
        source = self._idMapA[int(id)]
        vicini = self._graph.neighbors(source)
        listaT = []
        for v in vicini:
            listaT.append((v, self.calcolaBilancio(v)))
        return sorted(listaT, key=lambda x: x[1], reverse=True)

