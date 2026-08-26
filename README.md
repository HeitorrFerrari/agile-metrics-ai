# agile-metrics-ai

Puxa o quadro de uma metodologia ágil (Azure DevOps primeiro) e avalia **o quão bem o Kanban está sendo aplicado de verdade** — não só os gráficos de sempre, mas um diagnóstico opinativo com recomendações.

## Como funciona

```
Conector (Azure DevOps)  ->  Modelo normalizado  ->  Métricas de fluxo  ->  Regras / scoring  ->  Resumo (Claude)
```

- **Conector** — lê work items + histórico de transição de coluna via REST + Analytics API.
- **Modelo normalizado** (`Board`, `Column`, `Card`, `Transition`) — as métricas não conhecem o Azure, só esse modelo. Nova ferramenta = novo conector, resto intacto.
- **Métricas** — cycle/lead time (percentis), WIP vs limite, throughput, aging WIP, CFD, Little's Law.
- **Regras** — geram findings determinísticos ("coluna X sem limite de WIP", "limite furado 40% dos dias").
- **Resumo** — Claude transforma os findings em recomendação priorizada. A matemática nunca passa pelo LLM.

## Estrutura

```
src/agile_metrics/
  config.py              # carrega .env
  cli.py                 # comandos: analyze, snapshot
  models/board.py        # modelo normalizado (Board/Column/Card/Transition)
  connectors/
    base.py              # interface Connector
    azure/               # cliente REST/Analytics + mapeamento -> modelo normalizado
  metrics/               # flow, aging, cfd, littles_law
  analysis/              # findings, engine de regras, regras
  llm/client.py          # wrapper da Anthropic API
  report/                # narrative (Claude) + render (markdown/terminal)
tests/                   # fixtures sintéticas + testes de métricas/regras
data/snapshots/          # estado do quadro capturado dia a dia
```

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env                              # PAT do Azure + chave Anthropic
cp board_config.example.yaml board_config.yaml    # mapear as colunas do seu quadro
```

## Uso

```bash
agile-metrics analyze                 # métricas + findings
agile-metrics analyze --narrative     # + resumo do Claude
agile-metrics snapshot                # salva o estado do dia (constrói histórico)
```

## Estado — MVP em construção

Pronto:
- Modelo normalizado + métricas de fluxo core (cycle time, WIP, throughput, aging)
- Engine de regras + regras de limite de WIP (ausente / furado)
- CLI e camada de relatório

TODO:
- `AzureConnector.fetch_board` — WIQL + work item updates + Analytics snapshots
- CFD, backward-movement e Little's Law como regras
- Comando `snapshot`
- Resumo do Claude conectado ao `analyze --narrative`
