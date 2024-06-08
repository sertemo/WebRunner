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

import random
from typing import Literal

import requests

from webrunner.logging_config import logger
from webrunner.proxyscrapper import ProxyScrapper

class ProxyManager:
    """Clase que se ocupa de la gestión de los proxies para el navegador.
    En funcion de la configuración escogida por el usuario en wr_config.toml
    el proxymanager puede:
    - Devolver un proxy aleatorio funcional: para eso irá probando una serie de veces
    hasta que uno de los proxies sea funcional."""

    def __init__(self) -> None:
        self.ps = ProxyScrapper()

    def _check_url_status(self, url: str, proxy: str):
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(url, proxies=proxies, timeout=10, verify=False)
            return response.status_code
        except requests.exceptions.ProxyError as e:
            msg = f">>>> ERROR DE PROXY: {e}"
            logger.error(msg)
        except requests.RequestException as e:
            msg = f">>>> ERROR DE CONEXIÓN: {e}"
            logger.error(msg)
            return None


    def get_random_proxy(
            self,
            url: str,
            attempts: int,
            source: Literal['sslproxies', 'geonode', 'spys']
            ) -> str | None:
        """Devuelve un proxy aleatorio funcional. Si ninguno es funcional
        después de varios intentos devuelve None."""

        if source == "sslproxies":
            proxy_list = self.ps.from_sslproxies()
        elif source == "geonode":
            proxy_list = self.ps.from_geonode()
        else:
            proxy_list = self.ps.from_spys()


        if not proxy_list:
            logger.error(f"No proxies found in {source}")
            return None

        c = 1
        while c <= attempts:
            logger.info(f"ATTEMPT {c}: Trying to get a valid proxy.from {source}...")
            proxy = random.choice(proxy_list)

            # Verificar el código de estado HTTP
            status_code = self._check_url_status(url, proxy)
            if status_code == 200:
                logger.info(f"SUCCESS: Proxy {proxy} works! in attempt {c}")
                return proxy
            else:
                logger.info("\tURL returned status code {status_code} with proxy {proxy}. Retrying...")
            c += 1
        return None