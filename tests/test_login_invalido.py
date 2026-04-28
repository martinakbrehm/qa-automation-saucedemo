import json
import logging
from pathlib import Path

import pytest
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

_DATA_FILE = Path("data/cenarios_login_invalido.json")

with open(_DATA_FILE, encoding="utf-8") as _f:
    _CENARIOS = json.load(_f)


@pytest.mark.login
class TestLoginInvalido:
    @pytest.mark.parametrize(
        "cenario",
        _CENARIOS,
        ids=[c["id"] for c in _CENARIOS],
    )
    def test_login_invalido(self, driver, cenario):
        """Deve exibir mensagem de erro correta para cada cenário de login inválido."""
        logger.info(f"Executando cenário: {cenario['id']}")
        login_page = LoginPage(driver)
        login_page.fazer_login(cenario["usuario"], cenario["senha"])
        login_page.verificar_mensagem_erro_login_existe()
        login_page.verificar_texto_mensagem_erro_login(cenario["mensagem_esperada"])