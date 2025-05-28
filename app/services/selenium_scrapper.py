import logging

logger = logging.getLogger(__name__)


class SeleniumScrapperSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "initialized"):
            return

        self.initialized = True


class SeleniumScrapperService(SeleniumScrapperSingleton):
    def __init__(self):
        super().__init__()
        self.driver = self._get_driver()
        self.options = self._get_options()

    def _get_options(self):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")

        return options

    def _get_driver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        service = Service(ChromeDriverManager().install())
        options = self._get_options()

        return webdriver.Chrome(service=service, options=options)

    def start(self):
        logger.info("Starting selenium scrapper")
        self.driver = self._get_driver()
        logger.info("Started selenium scrapper")

        return self.driver

    def stop(self):
        logger.info("Stopping selenium scrapper")
        self.driver.quit()

    def get_html(self, url: str):
        self.driver.get(url)
        return self.driver.page_source
