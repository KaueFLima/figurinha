from figurinha import Figurinha
from nodos import NodoLista
from fifo import Fila

TOTAL_FIGURINHAS_ALBUM = 640


class Album:
    def __init__(self, total: int = TOTAL_FIGURINHAS_ALBUM) -> None:
        if not isinstance(total, int) or total <= 0:
            raise ValueError("Total de figurinhas deve ser um inteiro positivo.")
        self._cabeca: NodoLista | None = None
        self._tamanho: int = 0
        self._total_album: int = total
        self._repetidas: Fila = Fila()

    def _buscar_nodo(self, id: int) -> NodoLista | None:
        """Percorre a lista e retorna o nó com o id informado. O(n)."""
        atual = self._cabeca
        while atual is not None:
            if atual.figurinha.id == id:
                return atual
            atual = atual.proximo
        return None

    def adicionar(self, figurinha: Figurinha) -> str:

        if not isinstance(figurinha, Figurinha):
            raise TypeError("Apenas objetos Figurinha podem ser adicionados.")

        if self._buscar_nodo(figurinha.id) is not None:
            self._repetidas.enqueue(figurinha)
            return (
                f"Figurinha #{figurinha.id} ({figurinha.nome}) já está no álbum. "
                "Enviada para a pilha de repetidas."
            )

        novo = NodoLista(figurinha)

        if self._cabeca is None or figurinha.id < self._cabeca.figurinha.id:
            novo.proximo = self._cabeca
            self._cabeca = novo
        else:
            atual = self._cabeca
            while atual.proximo is not None and atual.proximo.figurinha.id < figurinha.id:
                atual = atual.proximo
            novo.proximo = atual.proximo
            atual.proximo = novo

        self._tamanho += 1
        return f"Figurinha #{figurinha.id} ({figurinha.nome}) adicionada ao álbum com sucesso!"

    def remover(self, id: int) -> Figurinha:
        self._validar_id_param(id)


        if self._cabeca is not None and self._cabeca.figurinha.id == id:
            figurinha = self._cabeca.figurinha
            self._cabeca = self._cabeca.proximo
            self._tamanho -= 1
            return figurinha

        anterior = self._cabeca
        while anterior is not None and anterior.proximo is not None:
            if anterior.proximo.figurinha.id == id:
                figurinha = anterior.proximo.figurinha
                anterior.proximo = anterior.proximo.proximo
                self._tamanho -= 1
                return figurinha
            anterior = anterior.proximo

        raise KeyError(f"Figurinha #{id} não encontrada no álbum.")


    def buscar_por_id(self, id: int) -> Figurinha:
        self._validar_id_param(id)
        nodo = self._buscar_nodo(id)
        if nodo is None:
            raise KeyError(f"Figurinha #{id} não encontrada no álbum.")
        return nodo.figurinha

    def buscar_por_jogador(self, nome: str) -> "Album._ResultadoBusca":
 
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome para busca não pode ser vazio.")
        termo = nome.strip().lower()
        encontradas = []
        atual = self._cabeca
        while atual is not None:
            if termo in atual.figurinha.nome.lower():
                encontradas.append(atual.figurinha)
            atual = atual.proximo
        return encontradas

    def buscar_por_selecao(self, pais: str) -> list:
        if not isinstance(pais, str) or not pais.strip():
            raise ValueError("Código de seleção não pode ser vazio.")
        codigo = pais.strip().upper()
        if not (2 <= len(codigo) <= 3) or not codigo.isalpha():
            raise ValueError(
                f"Código de seleção inválido: '{pais}'. Use 2 ou 3 letras (ex: BRA)."
            )
        encontradas = []
        atual = self._cabeca
        while atual is not None:
            if atual.figurinha.pais == codigo:
                encontradas.append(atual.figurinha)
            atual = atual.proximo
        return encontradas

    def ver_album(self) -> str:
        if self._tamanho == 0:
            return "O álbum está vazio."
        linhas = [f"{'='*55}", f"  ÁLBUM DA COPA 2026  ({self._tamanho}/{self._total_album})", f"{'='*55}"]
        atual = self._cabeca
        while atual is not None:
            linhas.append(str(atual.figurinha))
            atual = atual.proximo
        linhas.append(f"{'='*55}")
        linhas.append(f"  Progresso: {self.porcentagem():.1f}%")
        linhas.append(f"{'='*55}")
        return "\n".join(linhas)

    def porcentagem(self) -> float:
        return (self._tamanho / self._total_album) * 100

    def tamanho(self) -> int:
        return self._tamanho

    def esta_vazio(self) -> bool:
        return self._tamanho == 0

    def ver_repetidas(self) -> str:
        if self._repetidas.esta_vazia():
            return "Nenhuma figurinha repetida."
        linhas = [f"{'='*55}", f"  FIGURINHAS REPETIDAS  ({self._repetidas.tamanho()})", f"{'='*55}"]
        atual = self._repetidas._inicio
        while atual is not None:
            linhas.append(str(atual.figurinha))
            atual = atual.proximo
        linhas.append(f"{'='*55}")
        return "\n".join(linhas)

    def contar_repetidas(self) -> int:
        return self._repetidas.tamanho()

    def fila_repetidas(self) -> Fila:
        return self._repetidas

    def tem_repetida(self, id: int) -> bool:
        atual = self._repetidas._inicio
        while atual is not None:
            if atual.figurinha.id == id:
                return True
            atual = atual.proximo
        return False

    def retirar_repetida(self, id: int) -> Figurinha | None:
        from nodos import NodoFila

        anterior = None
        atual = self._repetidas._inicio
        while atual is not None:
            if atual.figurinha.id == id:
                if anterior is None:
                    self._repetidas._inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual == self._repetidas._fim:
                    self._repetidas._fim = anterior
                self._repetidas._tamanho -= 1
                return atual.figurinha
            anterior = atual
            atual = atual.proximo
        return None


    def para_dict(self) -> dict:
        figurinhas = []
        atual = self._cabeca
        while atual is not None:
            figurinhas.append(atual.figurinha.to_dict())
            atual = atual.proximo
        return {
            "total_album": self._total_album,
            "figurinhas": figurinhas,
            "repetidas": self._repetidas.para_lista_dicts(),
        }

    def carregar_dict(self, dados: dict) -> None:
        self._cabeca = None
        self._tamanho = 0
        self._repetidas.limpar()
        self._total_album = int(dados.get("total_album", TOTAL_FIGURINHAS_ALBUM))

        for d in dados.get("figurinhas", []):
            f = Figurinha.from_dict(d)
            novo = NodoLista(f)
            if self._cabeca is None or f.id < self._cabeca.figurinha.id:
                novo.proximo = self._cabeca
                self._cabeca = novo
            else:
                atual = self._cabeca
                while atual.proximo is not None and atual.proximo.figurinha.id < f.id:
                    atual = atual.proximo
                novo.proximo = atual.proximo
                atual.proximo = novo
            self._tamanho += 1

        for d in dados.get("repetidas", []):
            f = Figurinha.from_dict(d)
            self._repetidas.enqueue(f)

    @staticmethod
    def _validar_id_param(id: int) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError(f"ID inválido: '{id}'. Deve ser um inteiro positivo.")


    def __len__(self) -> int:
        return self._tamanho

    def __repr__(self) -> str:
        return (
            f"Album(figurinhas={self._tamanho}/"
            f"{self._total_album}, repetidas={self._repetidas.tamanho()})"
        )