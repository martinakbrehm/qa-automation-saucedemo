import json
import logging
from pathlib import Path

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

logger = logging.getLogger(__name__)

_DATA_FILE = Path("data/usuarios.json")

with open(_DATA_FILE, encoding="utf-8") as _f:
    _USUARIOS = [u for u in json.load(_f) if u["deve_logar"]]


@pytest.mark.login
class TestLoginValido:
    @pytest.mark.parametrize(
        "credencial",
        _USUARIOS,
        ids=[u["perfil"] for u in _USUARIOS],
    )
    def test_login_valido(self, driver, credencial):
        """Deve redirecionar para o inventário após login com credenciais válidas."""
        logger.info(f"Login com perfil: {credencial['perfil']}")
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.fazer_login(credencial["usuario"], credencial["senha"])
        home_page.verificar_login_com_sucesso()