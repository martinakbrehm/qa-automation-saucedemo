"""
Script de análise de resultados dos testes com pandas.

Uso:
    python scripts/analyze_results.py

Pré-requisito:
    pytest --json-report --json-report-file=reports/results.json

Dependências:
    pip install pandas pytest-json-report
"""

import json
import sys
from pathlib import Path

import pandas as pd

REPORT_PATH = Path("reports/results.json")


def carregar_relatorio(caminho: Path) -> dict:
    if not caminho.exists():
        print(
            f"[ERRO] Relatório não encontrado em '{caminho}'.\n"
            "Execute: pytest --json-report --json-report-file=reports/results.json"
        )
        sys.exit(1)
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def analisar(data: dict) -> None:
    df = pd.json_normalize(data["tests"])

    # Garante colunas essenciais
    df["outcome"] = df.get("outcome", pd.Series(dtype=str))
    df["duration"] = df.get("call.duration", df.get("duration", 0))

    print("\n" + "=" * 60)
    print("  QUALITY GATE REPORT")
    print("=" * 60)

    # Resumo geral
    resumo = df.groupby("outcome").size().reset_index(name="total")
    print("\n[Resumo por resultado]")
    print(resumo.to_string(index=False))

    # Duração média por marcador (usa o nodeid para inferir o módulo)
    df["modulo"] = df["nodeid"].str.split("::").str[0].str.replace("tests/", "")
    print("\n[Duração média por módulo de teste]")
    duracao = (
        df.groupby("modulo")["duration"]
        .agg(testes="count", media_s="mean", total_s="sum")
        .round(3)
    )
    print(duracao.to_string())

    # Testes mais lentos
    top_lentos = df.nlargest(5, "duration")[["nodeid", "outcome", "duration"]]
    print("\n[Top 5 testes mais lentos]")
    print(top_lentos.to_string(index=False))

    # Falhas detalhadas
    falhas = df[df["outcome"] == "failed"]
    if not falhas.empty:
        print(f"\n[⚠ {len(falhas)} teste(s) falharam]")
        for _, row in falhas.iterrows():
            print(f"  - {row['nodeid']}")
    else:
        print("\n[✓ Todos os testes passaram]")

    # Taxa de sucesso
    total = len(df)
    passou = (df["outcome"] == "passed").sum()
    taxa = round((passou / total) * 100, 1) if total else 0
    print(f"\n[Taxa de sucesso: {taxa}% ({passou}/{total})]")
    print("=" * 60 + "\n")

    # Exporta CSV para auditoria
    csv_path = REPORT_PATH.parent / "results_summary.csv"
    df[["nodeid", "outcome", "duration", "modulo"]].to_csv(csv_path, index=False)
    print(f"CSV de auditoria exportado: {csv_path}")


if __name__ == "__main__":
    data = carregar_relatorio(REPORT_PATH)
    analisar(data)
