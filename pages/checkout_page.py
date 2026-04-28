from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object para o fluxo de checkout do SauceDemo (Step 1 e Step 2)."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        # Step 1 — informações do comprador
        self.campo_primeiro_nome = (By.ID, "first-name")
        self.campo_sobrenome = (By.ID, "last-name")
        self.campo_cep = (By.ID, "postal-code")
        self.botao_continuar = (By.ID, "continue")
        self.mensagem_erro = (By.XPATH, "//*[@data-test='error']")

        # Step 2 — resumo do pedido
        self.botao_finalizar = (By.ID, "finish")

        # Confirmação
        self.titulo_pedido_concluido = (By.XPATH, "//*[@class='complete-header']")

    def preencher_informacoes(self, primeiro_nome: str, sobrenome: str, cep: str):
        """Preenche o formulário de endereço no checkout Step 1."""
        self.escrever(self.campo_primeiro_nome, primeiro_nome)
        self.escrever(self.campo_sobrenome, sobrenome)
        self.escrever(self.campo_cep, cep)

    def clicar_continuar(self):
        """Avança para o Step 2 do checkout."""
        self.clicar(self.botao_continuar)

    def finalizar_pedido(self):
        """Confirma e finaliza o pedido no Step 2."""
        self.clicar(self.botao_finalizar)

    def verificar_pedido_concluido(self):
        """Valida que a mensagem de confirmação de pedido está visível."""
        self.verificar_se_elemento_existe(self.titulo_pedido_concluido)
        texto = self.pegar_texto_elemento(self.titulo_pedido_concluido)
        assert texto == "Thank you for your order!", (
            f"Mensagem de confirmação inesperada: '{texto}'"
        )

    def verificar_erro_formulario(self, mensagem_esperada: str):
        """Valida a mensagem de erro exibida ao submeter o formulário incompleto."""
        self.verificar_se_elemento_existe(self.mensagem_erro)
        texto = self.pegar_texto_elemento(self.mensagem_erro)
        assert texto == mensagem_esperada, (
            f"Erro encontrado: '{texto}' | Esperado: '{mensagem_esperada}'"
        )
