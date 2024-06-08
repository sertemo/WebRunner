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
import time

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from webrunner.logging_config import logger
from webrunner.parser import Parser

class WebNavigator(ABC):
    def kickoff(self):
        # TODO : Meter aqui el bucle de las listas
        pass


    def navigate(self, url):
        try:
            self.visit_url(url)
            self.perform_actions()
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
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


class Navigator:
    def __init__(self, driver: Chrome | Firefox, parser: Parser) -> None:
        self.driver = driver
        self.parser = parser

    def visit_url(self, url: str):
        self.driver.get(url)
        logger.info(f"Visiting URL: {url}")
        time.sleep(6)

    def perform_actions(self):
        print("Performing random actions.")

    def close_browser(self):
        self.driver.quit()
        logger.info("Browser closed.")