import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        p = self._view._txt_n.value
        if p == "":
            self._view.create_alert("Inserisci valore numerico")
            return
        try:
            floatN = float(p)
        except ValueError:
            self._view.create_alert("Inserisci valore numerico")
            return
        self._model.buildGraph(floatN)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nNodes} - Archi: {nEdges}"))
        self._view._dd_album.clean()
        self._view._dd_album2.clean()
        self.fillDDAlbum()
        self._view.update_page()

    def handleBilancio(self, e):
        self._view.txt_result.controls.clear()
        id = self._view._dd_album.value
        if id is None:
            self._view.create_alert("Seleziona un album")
            return
        vicini = self._model.getBilancio(id)
        if vicini == []:
            self._view.txt_result.controls.append(ft.Text("Nessun vicino trovato"))
            self._view.update_page()
            return
        for v, bilancio in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v} - bilancio= {bilancio:.2f}"))
        self._view.update_page()

    def handlePercorso(self, e):
        self._view.txt_result.controls.clear()
        id1 = self._view._dd_album.value
        id2 = self._view._dd_album2.value
        if id1 is None or id2 is None:
            self._view.create_alert("Seleziona entrambi gli album")
            return
        if id1 == id2:
            self._view.create_alert("L'album di partenza e di arrivo devono essere diversi")
            return
        soglia = self._view._txt_soglia.value
        if soglia == "":
            self._view.create_alert("Seleziona soglia")
            return
        try:
            x = float(soglia)
        except ValueError:
            self._view.create_alert("Seleziona soglia numerica")
            return
        path = self._model.getPath(id1, id2, x)
        if path is None or len(path) <= 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Non esiste nessun cammino tra i due album che rispetti i criteri indicati.")
            )
        for a in path:
            self._view.txt_result.controls.append(ft.Text(f"{a}"))
        self._view.update_page()


    def fillDDAlbum(self):
        album = self._model._album
        for a in album:
            self._view._dd_album.options.append(ft.dropdown.Option(key=a.AlbumId, text=a))
            self._view._dd_album2.options.append(ft.dropdown.Option(key=a.AlbumId, text=a))
        self._view.update_page()