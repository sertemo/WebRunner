# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod

# from concurrent.futures import ThreadPoolExecutor
import random
import time

from selenium.webdriver import Chrome, Firefox, Remote
from selenium.webdriver.common.action_chains import ActionChains

from webrunner.browserfactory import BrowserFactory
from webrunner.logging_config import logger
from webrunner.parser import Parser
from webrunner.settings import HEIGHT, WIDTH


class WebNavigator(ABC):
    def __init__(self) -> None:
        self.driver: Chrome | Firefox | Remote | None = None

    def navigate(self, url: str):
        try:
            logger.info(f"[{url}] | ABRIENDO EL BROWSER ...")
            self.open_browser()
            logger.info(f"[{url}] | VISITANDO ...")
            self.visit_url(url)
            time.sleep(8)
            logger.info(f"[{url}] | REALIZANDO ACCIONES ...")
            self.perform_actions()
        except Exception as e:
            logger.error(f"[{url}] | ERROR: {e}")
        finally:
            logger.info(f"[{url}] | CERRANDO EL BROWSER ...")
            self.close_browser()

    @abstractmethod
    def open_browser(self):
        pass

    @abstractmethod
    def visit_url(self, url):
        pass

    @abstractmethod
    def perform_actions(self):
        pass

    @abstractmethod
    def close_browser(self):
        pass


class Navigator(WebNavigator):
    def __init__(
        self,
        browser_factory: BrowserFactory,
        parser: Parser,
        proxy: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        super().__init__()
        self.browser_factory = browser_factory
        self.url_list = parser.url_list
        self.max_actions = int(parser.max_actions)
        self.proxy = proxy
        self.user_agent = user_agent

    def kickoff(self):
        """with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(self.navigate, self.url_list)"""
        for url in self.url_list:
            self.navigate(url)

    def open_browser(self) -> None:
        self.driver = self.browser_factory.create_browser(
            self.proxy, self.user_agent, remote=False
        )

    @property
    def n_url(self) -> int:
        """Devuelve el número de urls visitadas"""
        return len(self.url_list)

    def visit_url(self, url: str) -> None:
        """Abre la web indicada"""
        if self.driver is not None:
            self.driver.get(url)

    def perform_actions(self) -> None:
        """Realiza una acción aleatoria en la página."""
        n = random.choice(range(1, self.max_actions))
        count = 1

        if self.driver is None:
            return

        logger.info(f"\t[ACTION] Performing {n} actions:")
        while count <= n:
            # Hacer clic en una posición aleatoria de la página
            x = random.choice(range(0, WIDTH // 2))
            y = random.choice(range(0, HEIGHT // 2))
            action_chains = ActionChains(self.driver)
            try:
                action_chains.move_by_offset(x, y).click().perform()
                logger.info(f"\t[ACTION] Clicking at random position ({x}, {y}).")
            except Exception as e:
                logger.error(f"\t[ACTION] Error clicking at ({x}, {y}): {e}")
            time.sleep(5)
            count += 1

    def close_browser(self) -> None:
        """Cierra el navegador"""
        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
