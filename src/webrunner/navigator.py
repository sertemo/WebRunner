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
from concurrent.futures import ThreadPoolExecutor
import random
import time

from selenium.webdriver import Chrome, Firefox

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from webrunner.logging_config import logger
from webrunner.parser import Parser

from webrunner.settings import HEIGHT, WIDTH


class WebNavigator(ABC):

    def navigate(self, url: str):
        try:
            logger.info(f"[{url}] | VISITANDO ...")
            self.visit_url(url)
            logger.info(f"[{url}] | REALIZANDO ACCIONES ...")
            self.perform_actions()
        except Exception as e:
            logger.error(f"[{url}] | ERROR: {e}")
        finally:
            logger.info(f"[{url}] | CERRANDO EL BROWSER ...")
            self.close_browser()

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
    def __init__(self, driver: Chrome | Firefox, parser: Parser) -> None:
        self.driver = driver
        self.url_list = parser.url_list
        self.max_actions = parser.max_actions

    def kickoff(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(self.navigate, self.url_list)

    def visit_url(self, url: str):
        self.driver.get(url)
        time.sleep(6)

    def perform_actions(self):
        """Realiza una acción aleatoria en la página."""
        n = random.choice(range(1, self.max_actions))
        count = 1

        logger.info(f"\t[ACTION] Performing {n} actions:")
        while count <= n:
            action = random.choice(["scroll", "click"])
            if action == "scroll":
                # Scroll hacia abajo
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                logger.info("\t[ACTION] Scrolling down the page.")
                time.sleep(4)
            elif action == "click":
                # Hacer clic en una posición aleatoria de la página
                x = random.choice(range(0, WIDTH // 2))
                y = random.choice(range(0, HEIGHT // 2))
                action_chains = ActionChains(self.driver)
                action_chains.move_by_offset(0, 0).click().perform()
                logger.info(f"\t[ACTION] Clicking at random position ({x}, {y}).")
                time.sleep(4)
            count += 1

    def close_browser(self):
        self.driver.quit()
