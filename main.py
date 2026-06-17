from figurinha import Figurinha
from album import Album
from historico import Historico
import save

def _ler_int(prompt: str, minimo: int = 1) -> int | None:
    try:
        valor = int(input(prompt).strip())
        if valor < minimo:
            print(f"Valor deve ser >= {minimo}.")
            return None
        return valor
    except ValueError:
        print("ntrada inválida: digite um número inteiro.")
        return None


def _ler_str(prompt: str) -> str:
    """Lê string não vazia."""
    valor = input(prompt).strip()
    if not valor:
        print("Campo não pode ser vazio.")
    return valor


def _pausar() -> None:
    input("\n  [Enter para continuar...]")


def _cabecalho(titulo: str) -> None:
    print(f"\n{'─'*55}")
    print(f"  {titulo}")
    print(f"{'─'*55}")


def _coletar_dados_figurinha() -> Figurinha | None:
    print()
    id_ = _ler_int("  Número da figurinha (ID): ")
    if id_ is None:
        return None

    nome = _ler_str("  Nome do jogador/seleção: ")
    if not nome:
        return None

    pais = _ler_str("  Código da seleção (ex: BRA, ARG): ")
    if not pais:
        return None

    print("  Posições: goleiro | zagueiro | lateral | volante | meia | atacante | tecnico")
    posicao = _ler_str("  Posição: ")
    if not posicao:
        return None

    print("  Raridades: comum | rara | lendaria | especial")
    raridade = _ler_str("  Raridade: ")
    if not raridade:
        return None

    try:
        return Figurinha(id_, nome, pais, posicao, raridade)
    except ValueError as e:
        print(f"Erro {e}")
        return None


def menu_album(album: Album) -> None:
    while True:
        _cabecalho("ÁLBUM")
        print("  1. Inserir figurinha")
        print("  2. Remover figurinha")
        print("  3. Consultar figurinha por número")
        print("  4. Ver álbum completo")
        print("  5. Ver porcentagem concluída")
        print("  6. Ver figurinhas repetidas")
        print("  7. Contar repetidas")
        print("  0. Voltar")
        opcao = input("\n  Opção: ").strip()

        if opcao == "1":
            _cabecalho("INSERIR FIGURINHA")
            fig = _coletar_dados_figurinha()
            if fig:
                print("\n  " + album.adicionar(fig))
            _pausar()

        elif opcao == "2":
            _cabecalho("REMOVER FIGURINHA")
            id_ = _ler_int("  Número da figurinha a remover: ")
            if id_:
                try:
                    fig = album.remover(id_)
                    print(f"\nRemovida: {fig}")
                except KeyError as e:
                    print(f"\n{e}")
            _pausar()

        elif opcao == "3":
            _cabecalho("CONSULTAR FIGURINHA")
            id_ = _ler_int("Número da figurinha: ")
            if id_:
                try:
                    fig = album.buscar_por_id(id_)
                    print(f"\n{fig}")
                except KeyError as e:
                    print(f"\n{e}")
            _pausar()

        elif opcao == "4":
            _cabecalho("ÁLBUM COMPLETO")
            print(album.ver_album())
            _pausar()

        elif opcao == "5":
            _cabecalho("PROGRESSO DO ÁLBUM")
            pct = album.porcentagem()
            total = album.tamanho()
            barra = int(pct / 2)
            barra_str = "█" * barra + "░" * (50 - barra)
            print(f"\n  [{barra_str}]")
            print(f"  {total}/{album._total_album} figurinhas  →  {pct:.1f}%")
            _pausar()

        elif opcao == "6":
            _cabecalho("FIGURINHAS REPETIDAS")
            print(album.ver_repetidas())
            _pausar()

        elif opcao == "7":
            _cabecalho("CONTAGEM DE REPETIDAS")
            print(f"\n  Total de repetidas: {album.contar_repetidas()}")
            _pausar()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            _pausar()


def menu_busca(album: Album) -> None:
    while True:
        _cabecalho("BUSCAS")
        print("  1. Buscar por número (ID)")
        print("  2. Buscar por nome do jogador")
        print("  3. Buscar por seleção")
        print("  0. Voltar")
        opcao = input("\n  Opção: ").strip()

        if opcao == "1":
            _cabecalho("BUSCA POR NÚMERO")
            id_ = _ler_int("  Número da figurinha: ")
            if id_:
                try:
                    fig = album.buscar_por_id(id_)
                    print(f"\n  Encontrada:\n  {fig}")
                except KeyError as e:
                    print(f"\n{e}")
            _pausar()

        elif opcao == "2":
            _cabecalho("BUSCA POR JOGADOR")
            nome = _ler_str("  Nome (ou parte do nome): ")
            if nome:
                try:
                    resultados = album.buscar_por_jogador(nome)
                    if resultados:
                        print(f"\n  {len(resultados)} resultado(s):")
                        for f in resultados:
                            print(f"  {f}")
                    else:
                        print(f"\n  Nenhuma figurinha encontrada com '{nome}'.")
                except ValueError as e:
                    print(f"\n{e}")
            _pausar()

        elif opcao == "3":
            _cabecalho("BUSCA POR SELEÇÃO")
            pais = _ler_str("  Código da seleção (ex: BRA): ")
            if pais:
                try:
                    resultados = album.buscar_por_selecao(pais)
                    if resultados:
                        print(f"\n  {len(resultados)} figurinha(s) de {pais.upper()}:")
                        for f in resultados:
                            print(f"  {f}")
                    else:
                        print(f"\n  Nenhuma figurinha de '{pais.upper()}' no álbum.")
                except ValueError as e:
                    print(f"\n{e}")
            _pausar()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            _pausar()


def menu_trocas(album: Album, historico: Historico) -> None:
    while True:
        _cabecalho("TROCAS")
        print("  1. Registrar proposta de troca")
        print("  2. Ver propostas pendentes")
        print("  3. Efetuar troca direta (entre dois álbuns na sessão)")
        print("  4. Ver histórico de trocas")
        print("  0. Voltar")
        opcao = input("\n  Opção: ").strip()

        if opcao == "1":
            _cabecalho("REGISTRAR PROPOSTA")
            solicitante = _ler_str("  Seu nome: ")
            if not solicitante:
                _pausar()
                continue
            id_oferto = _ler_int("  ID da figurinha que você oferece (deve ser sua repetida): ")
            if not id_oferto:
                _pausar()
                continue
            id_desejado = _ler_int("  ID da figurinha que você deseja: ")
            if not id_desejado:
                _pausar()
                continue
            try:
                msg = historico.registrar_proposta(
                    id_oferto, id_desejado, solicitante, album
                )
                print(f"\n  {msg}")
            except ValueError as e:
                print(f"\n{e}")
            _pausar()

        elif opcao == "2":
            _cabecalho("PROPOSTAS PENDENTES")
            print(historico.ver_propostas())
            _pausar()

        elif opcao == "3":
            _cabecalho("TROCA DIRETA")
            print("  (Simula troca entre dois colecionadores nesta sessão)")
            nome_a = _ler_str("  Nome do colecionador A: ")
            if not nome_a:
                _pausar()
                continue
            id_a = _ler_int("  ID que A vai dar (repetida de A): ")
            if not id_a:
                _pausar()
                continue

            nome_b = _ler_str("  Nome do colecionador B: ")
            if not nome_b:
                _pausar()
                continue
            id_b = _ler_int("  ID que B vai dar (repetida de B no álbum atual): ")
            if not id_b:
                _pausar()
                continue

            try:
                msg = historico.efetuar_troca(
                    album, id_a, nome_a,
                    album, id_b, nome_b,
                )
                print(f"\n  {msg}")
            except ValueError as e:
                print(f"\n{e}")
            _pausar()

        elif opcao == "4":
            _cabecalho("HISTÓRICO DE TROCAS")
            print(historico.ver_historico())
            _pausar()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            _pausar()


def menu_dados(album: Album, historico: Historico) -> None:
    while True:
        _cabecalho("SALVAR / CARREGAR")
        print("  1. Salvar dados (JSON)")
        print("  2. Carregar dados (JSON)")
        print("  3. Informar caminho personalizado")
        print("  0. Voltar")
        opcao = input("\n  Opção: ").strip()

        if opcao == "1":
            print("\n  " + save.salvar(album, historico))
            _pausar()

        elif opcao == "2":
            print("\n  " + save.carregar(album, historico))
            _pausar()

        elif opcao == "3":
            caminho = _ler_str("  Caminho do arquivo (ex: meu_album.json): ")
            if caminho:
                print("\n  1. Salvar  2. Carregar")
                sub = input("  Opção: ").strip()
                if sub == "1":
                    print("\n  " + save.salvar(album, historico, caminho))
                elif sub == "2":
                    print("\n  " + save.carregar(album, historico, caminho))
                else:
                    print("Opção inválida.")
            _pausar()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            _pausar()



def menu_principal() -> None:
    album = Album()
    historico = Historico()

    print(save.carregar(album, historico))

    while True:
        print(f"\n{'═'*55}")
        print("ÁLBUM DA COPA DO MUNDO 2026")
        print(f"{'═'*55}")
        print(f"  Figurinhas: {album.tamanho()}/{album._total_album}  "
              f"({album.porcentagem():.1f}%)  |  "
              f"Repetidas: {album.contar_repetidas()}")
        print(f"{'─'*55}")
        print("  1. Álbum (inserir, remover, ver, progresso)")
        print("  2. Buscas")
        print("  3. Trocas e Histórico")
        print("  4. Salvar / Carregar dados")
        print("  0. Sair")
        print(f"{'─'*55}")
        opcao = input("  Opção: ").strip()

        if opcao == "1":
            menu_album(album)
        elif opcao == "2":
            menu_busca(album)
        elif opcao == "3":
            menu_trocas(album, historico)
        elif opcao == "4":
            menu_dados(album, historico)
        elif opcao == "0":
            print("\n  " + save.salvar(album, historico))
            print("\n  Até a próxima, colecionador! ⚽\n")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()