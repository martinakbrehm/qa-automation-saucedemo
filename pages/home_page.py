from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object para a tela de inventário (home) do SauceDemo."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.titulo_pagina = (By.XPATH, "//span[@class='title']")
        self.item_inventario = (By.XPATH, "//*[@class='inventory_item_name' and text()='{}']")
        self.botao_adicionar_carrinho = (By.XPATH, "//*[text()='Add to cart']")
        self.icone_carrinho = (By.XPATH, "//*[@class='shopping_cart_link']")
        self.badge_contador_carrinho = (By.XPATH, "//span[@class='shopping_cart_badge']")

    def verificar_login_com_sucesso(self):
        """Valida que o título da página de inventário está visível."""
        self.verificar_se_elemento_existe(self.titulo_pagina)

    def adicionar_ao_carrinho(self, nome_item: str):
        """Clica no produto pelo nome e adiciona ao carrinho."""
        item = (self.item_inventario[0], self.item_inventario[1].format(nome_item))
        self.clicar(item)
        self.clicar(self.botao_adicionar_carrinho)

    def verificar_contador_carrinho(self, quantidade_esperada: int):
        """Valida que o badge do carrinho exibe o número correto de itens."""
        texto = self.pegar_texto_elemento(self.badge_contador_carrinho)
        assert int(texto) == quantidade_esperada, (
            f"Contador do carrinho: '{texto}' | Esperado: '{quantidade_esperada}'"
        )

    def acessar_carrinho(self):
        """Clica no ícone do carrinho para acessar a página do carrinho."""
        self.clicar(self.icone_carrinho)