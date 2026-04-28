"""
Pipeline de orquestração da suíte de QA com Prefect.

Funcionalidades:
    - Executa os grupos de testes (marcadores) como tasks independentes
    - Suporta retries automáticos por task
    - Gera relatório JSON e dispara análise com pandas ao final
    - Falha o pipeline (quality gate) se cobertura de sucesso < 100%

Uso local:
    prefect server start          # em outro terminal
    python pipeline/quality_pipeline.py

Uso agendado (registrar no Prefect Cloud / server):
    prefect deploy pipeline/quality_pipeline.py:quality_gate_pipeline
"""

import json
import subprocess
import sys
from pathlib import Path

from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta


REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

MARCADORES = ["login", "carrinho", "checkout"]


@task(
    name="Executar Suite",
    retries=1,
    retry_delay_seconds=10,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(minutes=5),
)
def executar_suite(marcador: str) -> dict:
    """Executa os testes de um marcador específico e retorna o resumo."""
    logger = get_run_logger()
    report_file = REPORTS_DIR / f"results_{marcador}.json"

    logger.info(f"Iniciando suite: @{marcador}")
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "-m", marcador,
            "-v",
            "--tb=short",
            "--json-report",
            f"--json-report-file={report_file}",
        ],
        capture_output=True,
        text=True,
    )

    logger.info(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.stderr:
        logger.warning(result.stderr[-1000:])

    resumo = {"marcador": marcador, "exit_code": result.returncode, "report": str(report_file)}
    if report_file.exists():
        with open(report_file, encoding="utf-8") as f:
            data = json.load(f)
        summary = data.get("summary", {})
        resumo.update({
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
            "total": summary.get("total", 0),
        })
        logger.info(f"Suite '{marcador}': {resumo['passed']}/{resumo['total']} passou")

    return resumo


@task(name="Consolidar Relatórios")
def consolidar_relatorios(resultados: list[dict]) -> Path:
    """Mescla todos os relatórios individuais em um único JSON consolidado."""
    logger = get_run_logger()
    todos_testes = []

    for res in resultados:
        report_path = Path(res["report"])
        if report_path.exists():
            with open(report_path, encoding="utf-8") as f:
                data = json.load(f)
            todos_testes.extend(data.get("tests", []))

    consolidado = {"tests": todos_testes, "suites": resultados}
    output = REPORTS_DIR / "results.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(consolidado, f, indent=2, ensure_ascii=False)

    logger.info(f"Relatório consolidado: {output} ({len(todos_testes)} testes)")
    return output


@task(name="Analisar Resultados")
def analisar_resultados() -> None:
    """Dispara o script de análise pandas."""
    logger = get_run_logger()
    result = subprocess.run(
        [sys.executable, "scripts/analyze_results.py"],
        capture_output=True,
        text=True,
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.warning(f"Análise retornou erros: {result.stderr}")


@task(name="Quality Gate")
def quality_gate(resultados: list[dict]) -> None:
    """Falha o pipeline se qualquer suite tiver testes reprovados."""
    logger = get_run_logger()
    falhas = [r for r in resultados if r.get("failed", 0) > 0 or r["exit_code"] != 0]

    if falhas:
        for f in falhas:
            logger.error(
                f"Suite '{f['marcador']}' FALHOU — "
                f"{f.get('failed', '?')} reprovados de {f.get('total', '?')}"
            )
        raise RuntimeError(
            f"Quality gate falhou em {len(falhas)} suite(s): "
            f"{[f['marcador'] for f in falhas]}"
        )

    total_passou = sum(r.get("passed", 0) for r in resultados)
    total = sum(r.get("total", 0) for r in resultados)
    logger.info(f"✓ Quality gate aprovado — {total_passou}/{total} testes passaram")


@flow(
    name="QA Automation Pipeline — SauceDemo",
    description="Executa a suíte de testes E2E, consolida relatórios e aplica quality gate.",
)
def quality_gate_pipeline():
    # Executa suites sequencialmente (evita conflito de instâncias Chrome)
    resultados = []
    for marcador in MARCADORES:
        resultado = executar_suite(marcador)
        resultados.append(resultado)

    consolidar_relatorios(resultados)
    analisar_resultados()
    quality_gate(resultados)


if __name__ == "__main__":
    quality_gate_pipeline()
