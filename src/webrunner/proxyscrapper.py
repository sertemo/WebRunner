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

"""Script para la clase proxy scrapper que se dedica a scrapear proxies"""

from typing import Any

import requests
from bs4 import BeautifulSoup

from webrunner.logging_config import logger


class ProxyScrapper:
    """Se encarga de scrappear una lista de proxies
    de distintos sitios y devolverlas"""

    def from_sslproxies(self) -> list[str]:
        """Descarga una lista de proxies de sslproxies

        Returns
        -------
        list[str]
            _description_
        """
        url = "https://www.sslproxies.org/"

        response = requests.get(url)

        # Verificar que la solicitud fue exitosa
        if response.status_code != 200:
            logger.error(
                f"Error: Unable to access {url} with response: {response.status_code}"
            )
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.select_one("#list > div > div:nth-of-type(2) > div > table")

        # Verificar que la tabla existe en la página
        if not table:
            logger.error("Error: Proxy table not found on the page")
            return []

        proxies = []
        for row in table.tbody.find_all("tr"):
            cols = row.find_all("td")
            ip = cols[0].text
            port = cols[1].text
            https = cols[6].text
            if https == "yes":
                proxies.append(f"https://{ip}:{port}")
            else:
                proxies.append(f"http://{ip}:{port}")

        if proxies:
            logger.info(f"Found {len(proxies)} proxies in {url}")
        else:
            logger.error("No proxies found")

        return proxies

    def from_geonode(self) -> list[str]:
        url = (
            "https://proxylist.geonode.com/api/proxy-list?protocols=http&"
            "limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        )
        # Devuelve un json con la lista de proxies con protocolo http
        response = requests.get(url)
        data_proxies: list[dict[str, Any]] = response.json()["data"]
        return [f"http://{proxy['ip']}:{proxy['port']}" for proxy in data_proxies]

    def from_spys(self) -> list[str]:
        url = "https://spys.one/en/free-proxy-list/"
        raise NotImplementedError
