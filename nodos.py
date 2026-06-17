from figurinha import Figurinha


class NodoLista:
    def __init__(self, figurinha: Figurinha) -> None:
        if not isinstance(figurinha, Figurinha):
            raise TypeError("NodoLista aceita apenas objetos do tipo Figurinha.")
        self.figurinha: Figurinha = figurinha
        self.proximo: NodoLista | None = None

    def __repr__(self) -> str:
        return f"NodoLista({self.figurinha!r})"


class NodoFila:
    def __init__(self, figurinha: Figurinha) -> None:
        if not isinstance(figurinha, Figurinha):
            raise TypeError("NodoFila aceita apenas objetos do tipo Figurinha.")
        self.figurinha: Figurinha = figurinha
        self.proximo: NodoFila | None = None

    def __repr__(self) -> str:
        return f"NodoFila({self.figurinha!r})"