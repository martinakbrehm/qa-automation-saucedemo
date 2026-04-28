import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Logging estruturado em JSON
# ---------------------------------------------------------------------------

class _JsonFormatter(logging.Formatter):
    """Formata cada linha de log como um objeto JSON — compatível com Datadog, ELK, etc."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "file": f"{record.filename}:{record.lineno}",
            },
            ensure_ascii=False,
        )


def _configure_logging() -> None:
    log_file = LOGS_DIR / f"test_run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"
    handler_file = logging.FileHandler(log_file, encoding="utf-8")
    handler_file.setFormatter(_JsonFormatter())

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(_JsonFormatter())

    logging.basicConfig(level=logging.INFO, handlers=[handler_file, handler_console])


_configure_logging()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def driver():
    """Cria e encerra o WebDriver para cada teste."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(IMPLICIT_WAIT)
    chrome_driver.maximize_window()
    chrome_driver.get(BASE_URL)
    logger.info(f"WebDriver iniciado | URL: {BASE_URL} | headless: {HEADLESS}")

    yield chrome_driver

    chrome_driver.quit()
    logger.info("WebDriver encerrado")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook que loga o resultado de cada teste no formato estruturado."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        status = report.outcome.upper()
        logger.info(
            f"TESTE {status} | {item.nodeid} | duração: {report.duration:.3f}s"
        )
