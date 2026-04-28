from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object para a tela de login do SauceDemo."""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message_login = (By.XPATH, "//*[@data-test='error']")

    def fazer_login(self, usuario: str, senha: str):
        """Preenche o formulário e submete o login."""
        self.escrever(self.username_field, usuario)
        self.escrever(self.password_field, senha)
        self.clicar(self.login_button)

    def verificar_mensagem_erro_login_existe(self):
        """Valida que o elemento de erro está visível."""
        self.verificar_se_elemento_existe(self.error_message_login)

    def verificar_texto_mensagem_erro_login(self, texto_esperado: str):
        """Valida o texto exato da mensagem de erro de login."""
        texto_encontrado = self.pegar_texto_elemento(self.error_message_login)
        assert texto_encontrado == texto_esperado, (
            f"Texto encontrado: '{texto_encontrado}' | Texto esperado: '{texto_esperado}'"
        )