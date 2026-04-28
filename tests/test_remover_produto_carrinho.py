import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.carrinho_page import CarrinhoPage


@pytest.mark.carrinho
class TestRemoverProdutoCarrinho:
    def test_remover_unico_produto_do_carrinho(self, driver):
        """CT04 - Deve remover um produto do carrinho e validar que ele não aparece mais."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")

        home_page.adicionar_ao_carrinho("Sauce Labs Backpack")
        home_page.verificar_contador_carrinho(1)
        home_page.acessar_carrinho()

        carrinho_page.verificar_produto_carrinho_existe("Sauce Labs Backpack")
        carrinho_page.remover_produto("Sauce Labs Backpack")
        carrinho_page.verificar_produto_ausente_no_carrinho("Sauce Labs Backpack")

    def test_remover_um_de_dois_produtos_do_carrinho(self, driver):
        """CT05 - Deve remover apenas um produto quando há dois no carrinho."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")

        home_page.adicionar_ao_carrinho("Sauce Labs Backpack")
        home_page.acessar_carrinho()
        carrinho_page.clicar_continuar_comprando()

        home_page.adicionar_ao_carrinho("Sauce Labs Bike Light")
        home_page.verificar_contador_carrinho(2)
        home_page.acessar_carrinho()

        carrinho_page.remover_produto("Sauce Labs Backpack")
        carrinho_page.verificar_produto_ausente_no_carrinho("Sauce Labs Backpack")
        carrinho_page.verificar_produto_carrinho_existe("Sauce Labs Bike Light")
