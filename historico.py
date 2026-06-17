from figurinha import Figurinha

class _NodoRegistro:
    __slots__ = ("registro", "proximo")

    def __init__(self, registro: str) -> None:
        self.registro: str = registro
        self.proximo: _NodoRegistro | None = None


class _FilaRegistros:
    def __init__(self) -> None:
        self._inicio: _NodoRegistro | None = None
        self._fim: _NodoRegistro | None = None
        self._tamanho: int = 0

    def enqueue(self, registro: str) -> None:
        novo = _NodoRegistro(registro)
        if self._fim is None:
            self._inicio = novo
            self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo
        self._tamanho += 1

    def esta_vazia(self) -> bool:
        return self._tamanho == 0

    def tamanho(self) -> int:
        return self._tamanho

    def para_lista(self) -> list:
        resultado = []
        atual = self._inicio
        while atual is not None:
            resultado.append(atual.registro)
            atual = atual.proximo
        return resultado

    def carregar_lista(self, registros: list) -> None:
        self._inicio = None
        self._fim = None
        self._tamanho = 0
        for r in registros:
            self.enqueue(str(r))

    def __str__(self) -> str:
        if self.esta_vazia():
            return "Nenhuma troca registrada."
        linhas = []
        atual = self._inicio
        idx = 1
        while atual is not None:
            linhas.append(f"  {idx:>3}. {atual.registro}")
            atual = atual.proximo
            idx += 1
        return "\n".join(linhas)



class _NodoProposta:
    __slots__ = ("id_oferto", "id_desejado", "solicitante", "proximo")

    def __init__(self, id_oferto: int, id_desejado: int, solicitante: str) -> None:
        self.id_oferto: int = id_oferto
        self.id_desejado: int = id_desejado
        self.solicitante: str = solicitante
        self.proximo: _NodoProposta | None = None


class _FilaPropostas:

    def __init__(self) -> None:
        self._inicio: _NodoProposta | None = None
        self._fim: _NodoProposta | None = None
        self._tamanho: int = 0

    def enqueue(self, id_oferto: int, id_desejado: int, solicitante: str) -> None:
        novo = _NodoProposta(id_oferto, id_desejado, solicitante)
        if self._fim is None:
            self._inicio = novo
            self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo
        self._tamanho += 1

    def dequeue(self) -> _NodoProposta:
        if self.esta_vazia():
            raise IndexError("Nenhuma proposta pendente.")
        prop = self._inicio
        self._inicio = self._inicio.proximo
        if self._inicio is None:
            self._fim = None
        self._tamanho -= 1
        return prop

    def peek(self) -> _NodoProposta:
        if self.esta_vazia():
            raise IndexError("Nenhuma proposta pendente.")
        return self._inicio

    def esta_vazia(self) -> bool:
        return self._tamanho == 0

    def tamanho(self) -> int:
        return self._tamanho

    def __str__(self) -> str:
        if self.esta_vazia():
            return "Nenhuma proposta pendente."
        linhas = []
        atual = self._inicio
        idx = 1
        while atual is not None:
            linhas.append(
                f"  {idx}. {atual.solicitante} oferece #{atual.id_oferto} "
                f"e quer #{atual.id_desejado}"
            )
            atual = atual.proximo
            idx += 1
        return "\n".join(linhas)


class Historico:
    def __init__(self) -> None:
        self._propostas: _FilaPropostas = _FilaPropostas()
        self._registros: _FilaRegistros = _FilaRegistros()

    def registrar_proposta(
        self,
        id_oferto: int,
        id_desejado: int,
        solicitante: str,
        album_solicitante,
    ) -> str:
        if not isinstance(id_oferto, int) or id_oferto <= 0:
            raise ValueError(f"ID ofertado inválido: '{id_oferto}'.")
        if not isinstance(id_desejado, int) or id_desejado <= 0:
            raise ValueError(f"ID desejado inválido: '{id_desejado}'.")
        if id_oferto == id_desejado:
            raise ValueError("Não é possível propor troca da mesma figurinha.")
        if not isinstance(solicitante, str) or not solicitante.strip():
            raise ValueError("Nome do solicitante não pode ser vazio.")

        if not album_solicitante.tem_repetida(id_oferto):
            return (
                f"Proposta recusada: {solicitante} não possui a figurinha "
                f"#{id_oferto} como repetida."
            )

        self._propostas.enqueue(id_oferto, id_desejado, solicitante.strip())
        return (
            f"Proposta registrada: {solicitante} oferece #{id_oferto} "
            f"e deseja #{id_desejado}."
        )

    def ver_propostas(self) -> str:
        cabecalho = f"{'='*55}\n  PROPOSTAS PENDENTES ({self._propostas.tamanho()})\n{'='*55}"
        return cabecalho + "\n" + str(self._propostas)


    def efetuar_troca(
        self,
        album_a,        
        id_a: int,      
        nome_a: str,
        album_b,        
        id_b: int,      
        nome_b: str,
    ) -> str:
        import datetime

        for id_val, label in [(id_a, "A"), (id_b, "B")]:
            if not isinstance(id_val, int) or id_val <= 0:
                raise ValueError(f"ID inválido para o usuário {label}: '{id_val}'.")

        erros = []
        if not album_a.tem_repetida(id_a):
            erros.append(f"{nome_a} não possui #{id_a} como repetida.")
        if not album_b.tem_repetida(id_b):
            erros.append(f"{nome_b} não possui #{id_b} como repetida.")
        if erros:
            return "Troca não realizada:\n  - " + "\n  - ".join(erros)

        fig_a = album_a.retirar_repetida(id_a)
        fig_b = album_b.retirar_repetida(id_b)

        msg_a = album_b.adicionar(fig_a)
        msg_b = album_a.adicionar(fig_b)

        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        registro = (
            f"[{timestamp}] {nome_a} (deu #{id_a} '{fig_a.nome}') "
            f"↔ {nome_b} (deu #{id_b} '{fig_b.nome}')"
        )
        self._registros.enqueue(registro)

        return (
            f"Troca realizada com sucesso!\n"
            f"{nome_a} recebeu: {fig_b}\n"
            f"{nome_b} recebeu: {fig_a}\n"
            f"Resultado para {nome_a}: {msg_b}\n"
            f"Resultado para {nome_b}: {msg_a}"
        )


    def processar_proxima_proposta(self, album_solicitante, album_receptor, nome_receptor: str) -> str:
        if self._propostas.esta_vazia():
            return "Nenhuma proposta pendente para processar."

        proposta = self._propostas.dequeue()
        return self.efetuar_troca(
            album_solicitante, proposta.id_oferto, proposta.solicitante,
            album_receptor, proposta.id_desejado, nome_receptor,
        )


    def ver_historico(self) -> str:
        cabecalho = (
            f"{'='*55}\n"
            f"  HISTÓRICO DE TROCAS ({self._registros.tamanho()})\n"
            f"{'='*55}"
        )
        return cabecalho + "\n" + str(self._registros)

    def total_trocas(self) -> int:
        return self._registros.tamanho()


    def para_dict(self) -> dict:
        return {
            "registros": self._registros.para_lista(),
        }

    def carregar_dict(self, dados: dict) -> None:
        self._registros.carregar_lista(dados.get("registros", []))

    def __repr__(self) -> str:
        return (
            f"Historico(propostas_pendentes={self._propostas.tamanho()}, "
            f"trocas_realizadas={self._registros.tamanho()})"
        )