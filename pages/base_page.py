from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys


class BasePage:
    """Classe base com ações genéricas reutilizáveis em todas as páginas."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def encontrar_elemento(self, locator):
        return self.driver.find_element(*locator)

    def encontrar_elementos(self, locator):
        return self.driver.find_elements(*locator)

    def escrever(self, locator, text: str):
        self.encontrar_elemento(locator).send_keys(text)

    def clicar(self, locator):
        self.encontrar_elemento(locator).click()

    def pegar_texto_elemento(self, locator) -> str:
        self.esperar_elemento_aparecer(locator)
        return self.encontrar_elemento(locator).text

    def esperar_elemento_aparecer(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def verificar_se_elemento_existe(self, locator):
        assert self.encontrar_elemento(locator).is_displayed(), (
            f"Elemento '{locator}' não está visível na tela."
        )

    def verificar_elemento_nao_existe(self, locator):
        assert len(self.encontrar_elementos(locator)) == 0, (
            f"Elemento '{locator}' existe na tela, mas não era esperado."
        )

    def clique_duplo(self, locator):
        element = self.esperar_elemento_aparecer(locator)
        ActionChains(self.driver).double_click(element).perform()

    def clique_botao_direito(self, locator):
        element = self.esperar_elemento_aparecer(locator)
        ActionChains(self.driver).context_click(element).perform()

    def pressionar_tecla(self, locator, key: str):
        key_map = {
            "ENTER": Keys.ENTER,
            "ESPACO": Keys.SPACE,
            "F1": Keys.F1,
        }
        if key not in key_map:
            raise ValueError(f"Tecla '{key}' não suportada. Use: {list(key_map.keys())}")
        self.encontrar_elemento(locator).send_keys(key_map[key])


