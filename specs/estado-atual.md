# agile-metrics-ai — Estado atual do projeto

> Snapshot gerado em 2026-09-15 a partir de inspeção direta do código-fonte (não do histórico de memória, que estava desatualizado em relação ao connector Azure).

## Arquitetura

```
Conector (Azure DevOps) -> Modelo normalizado (Board) -> Métricas de fluxo -> Regras determinísticas -> Narrativa (Claude) -> Report
```

Princípio central: a matemática nunca passa pelo LLM. Regras geram `Finding`s com evidência numérica; a camada de narrativa só reformula o que já foi calculado deterministicamente.

## Pronto e testado (suite passando, 6/6)

- **Models** (`src/agile_metrics/models/board.py`): `Board`, `Column`, `Card`, `Transition`, `ColumnType` — modelo normalizado completo.
- **Config** (`src/agile_metrics/config.py`): carregamento via `pydantic-settings` + `.env`.
- **Flow metrics** (`src/agile_metrics/metrics/flow.py`): cycle time em percentis (p50/p85/p95), throughput semanal, WIP atual por coluna. Completo.
- **Aging WIP** (`src/agile_metrics/metrics/aging.py`): função `aging_wip()` detecta cards parados além de um threshold por coluna. Completo, mas não conectado a nenhuma regra (ver seção "Stub" abaixo).
- **Little's Law** (`src/agile_metrics/metrics/littles_law.py`): `littles_law_check()` calcula o sanity check de estabilidade (`deviation_ratio` entre 0.75 e 1.33 = estável). Completo, mas não usado como regra ainda.
- **Engine de análise** (`src/agile_metrics/analysis/engine.py`): `AnalysisContext` + `run_analysis()` roda todas as regras e ordena findings por severidade. Completo.
- **Regras implementadas** (`src/agile_metrics/analysis/rules.py`):
  - `NoWipLimitsRule` — detecta colunas ativas sem limite de WIP.
  - `WipLimitExceededRule` — detecta colunas com WIP atual acima do limite configurado.
- **Narrativa** (`src/agile_metrics/report/narrative.py`) + **LLM client** (`src/agile_metrics/llm/client.py`): wrapper fino sobre a Anthropic Messages API, com `thinking: adaptive`, prompt em pt-BR que transforma findings em coaching priorizado. Completo.
- **Render** (`src/agile_metrics/report/render.py`): monta o relatório em markdown (métricas de fluxo + WIP + findings + narrativa opcional). Completo.
- **CLI** (`src/agile_metrics/cli.py`): comando `analyze` (com flag `--narrative`) já conecta todo o pipeline ponta a ponta. Completo.
- **Testes**: fixtures sintéticas (`tests/conftest.py`) + testes de métricas de fluxo e de modelos (`tests/test_metrics_flow.py`, `tests/test_models.py`) passando.

## Stub / `NotImplementedError` — bloqueadores reais

Estes pontos impedem rodar `analyze` contra um quadro Azure DevOps real (hoje só funciona com a fixture sintética dos testes):

- **`AzureDevOpsClient`** (`src/agile_metrics/connectors/azure/client.py`): todos os métodos são `raise NotImplementedError`:
  - `query_wiql()` — deveria fazer `POST /{project}/_apis/wit/wiql`.
  - `work_item_updates()` — deveria fazer `GET /{project}/_apis/wit/workItems/{id}/updates`, paginado.
  - `board_columns()` — deveria fazer `GET /{project}/{team}/_apis/work/boards/{board}/columns`.
  - `board_snapshots()` — deveria consultar o OData `WorkItemBoardSnapshot` via Analytics API.
- **`AzureConnector.fetch_board()`** (`src/agile_metrics/connectors/azure/connector.py`): `raise NotImplementedError`. Depende inteiramente do client acima. O plano de implementação já está documentado no docstring do método (WIQL → work item updates → montar `Transition`s → cruzar com board snapshots → mapear via `BoardConfig`).
- **CFD** (`src/agile_metrics/metrics/cfd.py`): `cumulative_flow()` — `raise NotImplementedError`.
- **`AgingWipRule`** e **`BackwardMovementRule`** (`src/agile_metrics/analysis/rules.py`): ambas retornam `[]` sempre. `AgingWipRule` deveria consumir `ctx.extras["aging_items"]` (produzido por `metrics.aging.aging_wip`, que já existe e funciona). `BackwardMovementRule` deveria contar transições em que a `order` da coluna de destino é menor que a de origem.
- **CLI `snapshot`**: `raise typer.Exit("TODO: implementar a captura diária de snapshot")`. Deveria persistir o estado do quadro do dia em `data/snapshots/`.

## Vazio / não iniciado

- `src/evals/` — só `__init__.py`, sem escopo definido ainda.
- `src/rag/` — só `__init__.py`, sem escopo definido ainda.

## Bloqueio prático

`agile-metrics analyze` funciona ponta a ponta apenas contra a fixture sintética usada nos testes. Contra um quadro Azure DevOps real, quebra em `AzureConnector.fetch_board()` porque o client REST/Analytics está 100% stub.

## Ordem recomendada para fechar o MVP

1. **`AzureDevOpsClient`** — implementar os 4 métodos REST/Analytics (endpoints já documentados nos comentários `TODO` do próprio arquivo).
2. **`AzureConnector.fetch_board()`** — WIQL → `work_item_updates` → montar `Transition`s → mapear para `Column` normalizada via `BoardConfig`.
3. **`AgingWipRule` + `BackwardMovementRule`** — ligar em `aging_wip()` (já pronta) e implementar a checagem de retrocesso de coluna nas `Transition`s.
4. **CFD** — implementar `cumulative_flow()` (forward-fill do estado por card, pivot data × coluna, acumular da direita para a esquerda).
5. **Little's Law como regra** — hoje é só uma função solta; falta transformar o resultado em `Finding` dentro do engine.
6. **CLI `snapshot`** — persistir o estado diário do quadro em `data/snapshots/` para construir histórico ao longo do tempo.
7. **Testes de integração para o Azure connector** — hoje a suite cobre só métricas/modelos com dados sintéticos; falta cobertura para o fluxo real de fetch do Azure.

## Observação sobre infraestrutura

Sem pendência de setup: dependências instaladas (`pyproject.toml` completo com `httpx`, `pydantic`, `pandas`, `anthropic`, `typer`, etc.), git limpo, `.gitignore` funcionando corretamente. O `README.md` já reflete esse mesmo estado — a seção "TODO" do README bate com o levantamento feito aqui.
