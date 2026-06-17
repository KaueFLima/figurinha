from figurinha import Figurinha
from nodos import NodoFila


class Fila:

    def __init__(self) -> None:
        self._inicio: NodoFila | None = None
        self._fim: NodoFila | None = None
        self._tamanho: int = 0

    # Insere a figurinha no final da fila
    def enqueue(self, figurinha: Figurinha) -> None:
        if not isinstance(figurinha, Figurinha):
            raise TypeError("Apenas objetos Figurinha podem ser enfileirados.")
        novo = NodoFila(figurinha)
        if self._fim is None:           # fila vazia
            self._inicio = novo
            self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo
        self._tamanho += 1

    # Remove e Retorna a figurinha no inicio da fila
    def dequeue(self) -> Figurinha:
        if self.esta_vazia():
            raise IndexError("Dequeue em fila vazia.")
        figurinha = self._inicio.figurinha
        self._inicio = self._inicio.proximo
        if self._inicio is None:        # Fila Vazia
            self._fim = None
        self._tamanho -= 1
        return figurinha

    # Apenas retorna a figurinha para o inicio da fila
    def peek(self) -> Figurinha:
        if self.esta_vazia():
            raise IndexError("Peek em fila vazia.")
        return self._inicio.figurinha

    # Limpa a fila
    def limpar(self) -> None:
        self._inicio = None
        self._fim = None
        self._tamanho = 0



    def esta_vazia(self) -> bool:
        return self._tamanho == 0

    def tamanho(self) -> int:
        return self._tamanho


    def para_lista_dicts(self) -> list:
        resultado = []
        atual = self._inicio
        while atual is not None:
            resultado.append(atual.figurinha.to_dict())
            atual = atual.proximo
        return resultado

    def __len__(self) -> int:
        return self._tamanho

    def __str__(self) -> str:
        if self.esta_vazia():
            return "Fila vazia."
        partes = []
        atual = self._inicio
        while atual is not None:
            partes.append(str(atual.figurinha))
            atual = atual.proximo
        return "\n".join(partes)

    def __repr__(self) -> str:
        return f"Fila(tamanho={self._tamanho})"