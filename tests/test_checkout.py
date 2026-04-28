import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.carrinho_page import CarrinhoPage
from pages.checkout_page import CheckoutPage


@pytest.mark.checkout
class TestCheckout:
    def test_finalizar_compra_com_sucesso(self, driver):
        """CT06 - Deve completar o fluxo de checkout e exibir confirmação do pedido."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)
        checkout_page = CheckoutPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")
        home_page.adicionar_ao_carrinho("Sauce Labs Backpack")
        home_page.acessar_carrinho()

        carrinho_page.verificar_produto_carrinho_existe("Sauce Labs Backpack")
        carrinho_page.clicar_checkout()

        checkout_page.preencher_informacoes("Martina", "Brehm", "01310-100")
        checkout_page.clicar_continuar()
        checkout_page.finalizar_pedido()
        checkout_page.verificar_pedido_concluido()

    def test_checkout_sem_preencher_formulario(self, driver):
        """CT07 - Deve exibir erro ao tentar avançar no checkout sem preencher o formulário."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)
        checkout_page = CheckoutPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")
        home_page.adicionar_ao_carrinho("Sauce Labs Backpack")
        home_page.acessar_carrinho()
        carrinho_page.clicar_checkout()

        checkout_page.clicar_continuar()
        checkout_page.verificar_erro_formulario("Error: First Name is required")

    def test_checkout_sem_sobrenome(self, driver):
        """CT08 - Deve exibir erro ao tentar avançar sem preencher o sobrenome."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        carrinho_page = CarrinhoPage(driver)
        checkout_page = CheckoutPage(driver)

        login_page.fazer_login("standard_user", "secret_sauce")
        home_page.adicionar_ao_carrinho("Sauce Labs Backpack")
        home_page.acessar_carrinho()
        carrinho_page.clicar_checkout()

        checkout_page.preencher_informacoes("Martina", "", "")
        checkout_page.clicar_continuar()
        checkout_page.verificar_erro_formulario("Error: Last Name is required")
