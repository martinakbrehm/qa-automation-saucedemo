from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class CarrinhoPage(BasePage):
    """Page Object para a tela de carrinho de compras do SauceDemo."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.item_inventario = (By.XPATH, "//*[@class='inventory_item_name' and text()='{}']")
        self.botao_remover_item = (
            By.XPATH,
            "//*[contains(@class,'cart_item') and .//*[text()='{}']]//button[text()='Remove']",
        )
        self.botao_continuar_comprando = (By.ID, "continue-shopping")
        self.botao_checkout = (By.ID, "checkout")

    def verificar_produto_carrinho_existe(self, nome_item: str):
        """Valida que o produto está presente no carrinho."""
        item = (self.item_inventario[0], self.item_inventario[1].format(nome_item))
        self.verificar_se_elemento_existe(item)

    def verificar_produto_ausente_no_carrinho(self, nome_item: str):
        """Valida que o produto NÃO está no carrinho após remoção."""
        item = (self.item_inventario[0], self.item_inventario[1].format(nome_item))
        self.verificar_elemento_nao_existe(item)

    def remover_produto(self, nome_item: str):
        """Remove um produto específico do carrinho pelo nome."""
        botao = (
            self.botao_remover_item[0],
            self.botao_remover_item[1].format(nome_item),
        )
        self.clicar(botao)

    def clicar_continuar_comprando(self):
        """Retorna à tela de inventário clicando em 'Continue Shopping'."""
        self.clicar(self.botao_continuar_comprando)

    def clicar_checkout(self):
        """Inicia o processo de checkout."""
        self.clicar(self.botao_checkout)