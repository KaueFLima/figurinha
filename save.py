from __future__ import annotations
import json
import os

ARQUIVO_PADRAO = "copa2026.json"


def salvar(album, historico, caminho: str = ARQUIVO_PADRAO) -> str:
    try:
        dados = {
            "album": album.para_dict(),
            "historico": historico.para_dict(),
        }
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return f"Dados salvos em '{caminho}' com sucesso."
    except OSError as e:
        return f"Erro ao salvar: {e}"
    except Exception as e:
        return f"Erro inesperado ao salvar: {e}"


def carregar(album, historico, caminho: str = ARQUIVO_PADRAO) -> str:
    if not os.path.exists(caminho):
        return f"Arquivo '{caminho}' não encontrado. Iniciando com dados vazios."
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if "album" not in dados or "historico" not in dados:
            return "Arquivo corrompido: estrutura inválida."

        album.carregar_dict(dados["album"])
        historico.carregar_dict(dados["historico"])
        return (
            f"Dados carregados de '{caminho}'.\n"
            f"Álbum: {album.tamanho()} figurinha(s) | "
            f"Repetidas: {album.contar_repetidas()} | "
            f"Trocas: {historico.total_trocas()}"
        )
    except json.JSONDecodeError as e:
        return f"Erro ao decodificar JSON: {e}"
    except ValueError as e:
        return f"Dados inválidos no arquivo: {e}"
    except OSError as e:
        return f"Erro ao ler arquivo: {e}"
    except Exception as e:
        return f"Erro inesperado ao carregar: {e}"