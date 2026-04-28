import json
import logging
from pathlib import Path

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.carrinho_page import CarrinhoPage

logger = logging.getLogger(__name__)

_DATA_FILE = Path("data/produtos.json")

with open(_DATA_FILE, encoding="utf-8") as _f:
    _PRODUTOS = json.load(_f)

_PRODUTO_1 = _PRODUTOS[0]["nome"]
_PRODUTO_2 = _PRODUTOS[1]["nome"]


@pytest.mark.carrinho
class TestAdicionarProdutosCarrinho:
    def test_ct01_adicionar_produtos_carrinho(self, driver):
        """CT01 - Deve adicionar dois produtos ao carrinho e validar persistência e badge."""
        logger.info(f"Adicionando produtos: '{_PRODUTO_1}' e '{_PRODUTO_2}'")
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")

        home_page.adicionar_ao_carrinho(_PRODUTO_1)
        home_page.verificar_contador_carrinho(1)

        home_page.acessar_carrinho()
        carrinho_page.verificar_produto_carrinho_existe(_PRODUTO_1)

        carrinho_page.clicar_continuar_comprando()
        home_page.adicionar_ao_carrinho(_PRODUTO_2)
        home_page.verificar_contador_carrinho(2)

        home_page.acessar_carrinho()
        carrinho_page.verificar_produto_carrinho_existe(_PRODUTO_1)
        carrinho_page.verificar_produto_carrinho_existe(_PRODUTO_2)