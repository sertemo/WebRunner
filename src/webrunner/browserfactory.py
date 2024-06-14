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


# https://nander.cc/using-selenium-within-a-docker-container

import os

from selenium.webdriver import Chrome, Firefox, Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService

from webrunner.parser import Parser
from webrunner.logging_config import logger


class BrowserFactory:
    def __init__(self, parser: Parser) -> None:
        self.browser_config = parser.browser_config

    def _prepare_chrome_options(
        self, proxy: str | None, user_agent: str | None
    ) -> ChromeOptions:
        """Prepara las opciones del navegador de Chrome."""
        options = ChromeOptions()
        if self.browser_config["headless"]:
            options.add_argument("--headless")  # Para ejecutar en modo headless
        if self.browser_config["disable-gpu"]:
            options.add_argument("--disable-gpu")  # Para sistemas que no tienen GPU
        if self.browser_config["no-sandbox"]:
            options.add_argument("--no-sandbox")
        if self.browser_config["enable-javascript"]:
            options.add_argument("--enable-javascript")
        if self.browser_config["allow-insecure-localhost"]:
            options.add_argument("--allow-insecure-localhost")
        if self.browser_config["ignore-certificate-errors"]:
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
        if self.browser_config["enable-automation"]:
            options.add_argument("--enable-automation")
        if self.browser_config["disable-dev-shm-usage"]:
            options.add_argument("--disable-dev-shm-usage")
        if self.browser_config["disable-blink-features"]:
            options.add_argument("--disable-blink-features=AutomationControlled")

        if proxy is not None:
            options.add_argument(f"--proxy-server={proxy}")
        if user_agent is not None:
            options.add_argument(f"user-agent={user_agent}")
        return options

    def _prepare_firefox_options(
        self, proxy: str | None, user_agent: str | None
    ) -> FirefoxOptions:
        """Prepara las opciones del navegador de Firefox."""
        options = FirefoxOptions()
        # Configuramos la pantalla con una determinada dimensión
        options.add_argument("--width=1500")
        options.add_argument("--height=1000")

        if self.browser_config["headless"]:
            options.add_argument("--headless")  # Para ejecutar en modo headless
        if self.browser_config["disable-gpu"]:
            options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")
        if self.browser_config["no-sandbox"]:
            options.add_argument("--no-sandbox")
        if self.browser_config["enable-javascript"]:
            options.set_preference("javascript.enabled", True)
        if self.browser_config["allow-insecure-localhost"]:
            options.set_preference("network.websocket.allowInsecureFromHTTPS", True)
        if self.browser_config["ignore-certificate-errors"]:
            options.set_preference("network.stricttransportsecurity.preloadlist", False)
        if self.browser_config["enable-automation"]:
            options.set_preference("dom.webdriver.enabled", True)
            options.set_preference("useAutomationExtension", False)
        if self.browser_config["disable-dev-shm-usage"]:
            options.set_preference("browser.cache.disk.enable", False)
            options.set_preference("browser.cache.memory.enable", False)
            options.set_preference("browser.cache.offline.enable", False)
            options.set_preference("network.http.use-cache", False)
        if self.browser_config["disable-blink-features"]:
            options.set_preference("dom.webnotifications.enabled", False)

        if proxy is not None:
            host, port = proxy.split(":")[1].strip("/"), proxy.split(":")[2]
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", host)
            options.set_preference("network.proxy.http_port", int(port))
            options.set_preference("network.proxy.ssl", host)
            options.set_preference("network.proxy.ssl_port", int(port))
            options.set_preference("network.proxy.ftp", host)
            options.set_preference("network.proxy.ftp_port", int(port))
            options.set_preference("network.proxy.socks", host)
            options.set_preference("network.proxy.socks_port", int(port))
            options.set_preference("network.proxy.no_proxies_on", "")
        if user_agent is not None:
            options.set_preference("general.useragent.override", user_agent)

        options.set_capability("moz:firefoxOptions", options.to_capabilities())
        return options

    def create_browser(
        self, proxy: str | None, user_agent: str | None, remote: bool = True
    ) -> Chrome | Firefox | Remote:
        """Devuelve un navegador de Chrome o Firefox con
        las opciones del usuario"""

        if self.browser_config["type"].lower() == "chrome":
            chrome_options = self._prepare_chrome_options(proxy, user_agent)

            if remote:
                # Remote para usar Selenium Grid
                command_executor = f"http://{os.getenv('SELENIUM_HUB_HOST')}:{os.getenv('SELENIUM_HUB_PORT')}/wd/hub"

                logger.info(
                    f"Creating Chrome browser with REMOTE\n"
                    f"\tCOMMAND EXECUTOR: {command_executor}"
                    f"\tUSER AGENT: {user_agent}"
                    f"\tPROXY: {proxy}"
                )
                return Remote(
                    command_executor=command_executor,
                    options=chrome_options,
                )
            else:
                service = ChromeService("/usr/local/bin/chromedriver")
                logger.info(
                    f"Creating Chrome browser\n"
                    f"\tUSER AGENT: {user_agent}"
                    f"\tPROXY: {proxy}"
                    f"\tSERVICE: {service}"
                )
                return Chrome(options=chrome_options, service=service)

        elif self.browser_config["type"].lower() == "firefox":
            firefox_options = self._prepare_firefox_options(proxy, user_agent)
            logger.info(f"Creating FIREFOX browser with options: {firefox_options}")
            if remote:
                return Remote(
                    command_executor="http://selenium-hub:4444/wd/hub",
                    options=firefox_options,
                )
            else:
                return Firefox(options=firefox_options)

        raise ValueError(f"Unsupported browser type: {self.browser_config['browser']}")
