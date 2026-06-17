RARIDADES_VALIDAS = {"comum", "rara", "lendaria", "especial"}
POSICOES_VALIDAS = {
    "goleiro", "zagueiro", "lateral", "volante",
    "meia", "atacante", "tecnico"
}


class Figurinha:

    def __init__(self, id: int, nome: str, pais: str,
                 posicao: str, raridade: str) -> None:
        self._validar_id(id)
        self._validar_nome(nome)
        self._validar_pais(pais)
        self._validar_posicao(posicao)
        self._validar_raridade(raridade)

        self.id = id
        self.nome = nome.strip().title()
        self.pais = pais.strip().upper()
        self.posicao = posicao.strip().lower()
        self.raridade = raridade.strip().lower()

    @staticmethod
    def _validar_id(id: int) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError(f"ID inválido: '{id}'. Deve ser um inteiro positivo.")

    @staticmethod
    def _validar_nome(nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O Jogador precisa de um nome")
        if len(nome.strip()) > 60:
            raise ValueError("Nome Longo de mais.")

    @staticmethod
    def _validar_pais(pais: str) -> None:
        if not isinstance(pais, str) or not pais.strip() or (pais == int):
            raise ValueError("País Não Existe")
        codigo = pais.strip().upper()
        if not (2 <= len(codigo) <= 3) or not codigo.isalpha():
            raise ValueError(
                f"Código de seleção inválido: '{pais}'. "
                "Use 2 ou 3 letras (ex: BRA, ARG, FR)."
            )

    @staticmethod
    def _validar_posicao(posicao: str) -> None:
        if posicao.strip().lower() not in POSICOES_VALIDAS:
            raise ValueError(
                f"Posição inválida: '{posicao}'. "
                f"Opções válidas: {', '.join(sorted(POSICOES_VALIDAS))}."
            )

    @staticmethod
    def _validar_raridade(raridade: str) -> None:
        if raridade.strip().lower() not in RARIDADES_VALIDAS:
            raise ValueError(
                f"Raridade inválida: '{raridade}'. "
                f"Opções válidas: {', '.join(sorted(RARIDADES_VALIDAS))}."
            )


    def __str__(self) -> str:
        return (
            f"[#{self.id:04d}] {self.nome} | "
            f"{self.pais} | {self.posicao.capitalize()} | "
            f"Raridade: {self.raridade.capitalize()}"
        )

    def __repr__(self) -> str:
        return (
            f"Figurinha(id={self.id}, nome={self.nome!r}, "
            f"pais={self.pais!r}, posicao={self.posicao!r}, "
            f"raridade={self.raridade!r})"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "pais": self.pais,
            "posicao": self.posicao,
            "raridade": self.raridade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Figurinha":
        try:
            return cls(
                id=int(dados["id"]),
                nome=dados["nome"],
                pais=dados["pais"],
                posicao=dados["posicao"],
                raridade=dados["raridade"],
            )
        except KeyError as e:
            raise ValueError(f"Campo obrigatório ausente no dicionário: {e}")