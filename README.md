# Sistema de Álbum de Figurinhas — Copa do Mundo 2026 

## Descrição

Sistema de gerenciamento de figurinhas da Copa do Mundo 2026 desenvolvido em Python. Permite colecionarem, trocar e organizar figurinhas de jogadores e seleções, com todas as estruturas de dados implementadas manualmente — sem uso de `list`, `deque` ou qualquer estrutura built-in do Python para listas encadeadas e filas.

---

## Estrutura de Arquivos

```
copa2026/
│
├── figurinha.py      # Entidade principal: dados e validações da figurinha
├── nodos.py          # NodoLista e NodoFila — nós encadeados
├── fila.py           # Fila FIFO própria (enqueue, dequeue, peek, limpar)
├── album.py          # Álbum: lista encadeada + fila de repetidas
├── historico.py      # Trocas: propostas, execução e log de trocas
├── persistencia.py   # Salvar e carregar dados em JSON
├── main.py           # Menu interativo em console
└── copa2026.json     # Arquivo de dados gerado automaticamente
```

---

## Classes Implementadas

### `Figurinha` — `figurinha.py`
Representa uma figurinha individual do álbum.

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `id` | `int` | Número único da figurinha (deve ser positivo) |
| `nome` | `str` | Nome do jogador ou seleção (máx. 60 caracteres) |
| `pais` | `str` | Código da seleção: 2 ou 3 letras (ex: `BRA`, `ARG`, `FR`) |
| `posicao` | `str` | `goleiro`, `zagueiro`, `lateral`, `volante`, `meia`, `atacante`, `tecnico` |
| `raridade` | `str` | `comum`, `rara`, `lendaria`, `especial` |

Todos os campos são **validados no construtor** — entradas inválidas lançam `ValueError` com mensagem descritiva. Inclui métodos `to_dict()` e `from_dict()` para persistência.

---

### `NodoLista` e `NodoFila` — `nodos.py`
Nós de encadeamento simples. Cada nó armazena uma `Figurinha` e um ponteiro `proximo` para o próximo nó. Não utilizam nenhuma estrutura built-in do Python.

---

### `Fila` — `fila.py`
Fila FIFO implementada com `NodoFila`. Mantém ponteiros `_inicio` e `_fim` para operações O(1).

| Método | Complexidade | Descrição |
|--------|-------------|-----------|
| `enqueue(fig)` | O(1) | Insere no final |
| `dequeue()` | O(1) | Remove e retorna do início |
| `peek()` | O(1) | Consulta o início sem remover |
| `limpar()` | O(1) | Esvazia a fila |
| `esta_vazia()` | O(1) | Verifica se vazia |
| `tamanho()` | O(1) | Quantidade de elementos |

---

### `Album` — `album.py`
Álbum da Copa implementado como **lista simplesmente encadeada ordenada por ID**. Figurinhas repetidas são armazenadas em uma `Fila` separada.

**Funcionalidades:**
- Inserir figurinha (duplicatas vão automaticamente para a fila de repetidas)
- Remover figurinha por ID
- Consultar figurinha por ID
- Ver álbum completo com barra de progresso
- Ver porcentagem concluída
- Ver e contar figurinhas repetidas
- Busca por número, por nome do jogador e por seleção

**Constante:** `TOTAL_FIGURINHAS_ALBUM = 640`

---

### `Historico` — `historico.py`
Gerencia propostas e registros de trocas. Utiliza duas estruturas encadeadas internas próprias:

- `_FilaPropostas` — fila FIFO de propostas pendentes (`_NodoProposta`)
- `_FilaRegistros` — fila FIFO de log das trocas realizadas (`_NodoRegistro`)

**Funcionalidades:**
- Registrar proposta de troca (verifica se o solicitante possui a repetida)
- Ver propostas pendentes
- Efetuar troca direta entre dois colecionadores (verifica repetidas de ambos)
- Processar próxima proposta da fila automaticamente
- Ver histórico completo com data e hora de cada troca

---

### `persistencia.py`
Salva e carrega o estado completo do sistema (álbum + histórico) em formato **JSON**.

```python
salvar(album, historico, caminho="copa2026.json")
carregar(album, historico, caminho="copa2026.json")
```

Formato do arquivo:
```json
{
  "album": {
    "total_album": 640,
    "figurinhas": [ { "id": 1, "nome": "Vinicius Jr", ... } ],
    "repetidas":  [ { "id": 1, "nome": "Vinicius Jr", ... } ]
  },
  "historico": {
    "registros": [ "[17/06/2026 14:30] João (deu #10) ↔ Maria (deu #42)" ]
  }
}
```

---

## Como Executar

**Pré-requisito:** Python 3.10 ou superior (uso de `X | Y` para type hints).

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd copa2026

# Execute o sistema
python main.py
```

O sistema carrega automaticamente os dados de `copa2026.json` ao iniciar (se o arquivo existir) e salva ao sair.

---

## 🖥️ Menu do Sistema

```
═══════════════════════════════════════════════════════
  ⚽  ÁLBUM DA COPA DO MUNDO 2026  ⚽
═══════════════════════════════════════════════════════
  Figurinhas: 3/640 (0.5%)  |  Repetidas: 1
───────────────────────────────────────────────────────
  1. Álbum (inserir, remover, ver, progresso)
  2. Buscas
  3. Trocas e Histórico
  4. Salvar / Carregar dados
  0. Sair
───────────────────────────────────────────────────────
```

---

## Requisitos Técnicos Atendidos

| Requisito | Status | Detalhe |
|-----------|--------|---------|
| Classe `Figurinha` | `figurinha.py` — com validações completas |
| Classes `NodoLista` e `NodoFila` | `nodos.py` — nós encadeados independentes |
| Classe `Album` (lista encadeada) | `album.py` — sem estruturas built-in |
| Classe `Fila` FIFO própria | `fila.py` — enqueue/dequeue O(1) |
| Classe `Historico` | `historico.py` — filas internas próprias |
| Sem `list`, `deque` ou built-ins | Todas as estruturas implementadas com nós |
| Tratamento de entradas inválidas | `ValueError` descritivo em todos os campos |
| Persistência (JSON) | `persistencia.py` — salvar e carregar |
| Figurinhas repetidas | Fila FIFO separada dentro do `Album` |
| Buscas | Por ID, por nome do jogador, por seleção |
| Trocas | Propostas, verificação e troca automática |

---

## Diagrama de Classes (simplificado)

```
┌─────────────────┐        ┌─────────────────┐
│   Figurinha     │◄───────│   NodoLista     │
│─────────────────│        │─────────────────│
│ id: int         │        │ figurinha       │
│ nome: str       │        │ proximo         │
│ pais: str       │        └────────┬────────┘
│ posicao: str    │                 │ compõe
│ raridade: str   │        ┌────────▼────────┐
│─────────────────│        │     Album       │
│ to_dict()       │        │─────────────────│
│ from_dict()     │        │ _cabeca         │
└─────────────────┘        │ _tamanho        │
                           │ _total_album    │
         ┌──────────────── │ _repetidas:Fila │
         │                 └─────────────────┘
         ▼
┌─────────────────┐        ┌─────────────────┐
│   NodoFila      │◄───────│     Fila        │
│─────────────────│        │─────────────────│
│ figurinha       │        │ _inicio         │
│ proximo         │        │ _fim            │
└─────────────────┘        │ _tamanho        │
                           │─────────────────│
                           │ enqueue()       │
                           │ dequeue()       │
                           │ peek()          │
                           └─────────────────┘

┌──────────────────────────────────────────┐
│              Historico                   │
│──────────────────────────────────────────│
│ _propostas: _FilaPropostas               │
│ _registros: _FilaRegistros               │
│──────────────────────────────────────────│
│ registrar_proposta()                     │
│ efetuar_troca()                          │
│ processar_proxima_proposta()             │
│ ver_historico()                          │
└──────────────────────────────────────────┘
```

---

## Validações Implementadas

- **ID:** deve ser inteiro positivo
- **Nome:** não pode ser vazio; máximo 60 caracteres
- **País:** código de 2 ou 3 letras (`BRA`, `ARG`, `FR`, etc.)
- **Posição:** apenas valores do conjunto `{goleiro, zagueiro, lateral, volante, meia, atacante, tecnico}`
- **Raridade:** apenas `{comum, rara, lendaria, especial}`
- **Trocas:** verifica se ambos os colecionadores possuem as figurinhas como repetidas antes de executar
- **Propostas:** verifica existência da repetida do solicitante antes de enfileirar

---
