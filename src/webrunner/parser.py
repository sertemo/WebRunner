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

import toml

from webrunner.settings import CONFIG_FILE

class Parser:
    """Se ocupa de leer el archivo de configuración
    toml y devolver los parámetros deseados"""

    def __init__(self) -> None:
        self.parsed_toml = toml.loads(CONFIG_FILE)

    def get_user_agent_config(self) -> str:  # Si es random o nada o una predeterminada
        """Devuelve la configuración del user agent."""

    def get_proxy_config(self) -> str | bool:  # Si es random o nada o una predeterminada
        """Devuelve la configuración del proxy."""
        return self.parsed_toml["navconfig"]["proxy"]

    def get_browser_config(self) -> str:  # Si es Chrome o Firefox y las opciones
        """Devuelve la configuración del navegador con todas sus opciones."""

    def get_url_list(self) -> list[str]:
        """Devuelve una lista de URLs a visitar."""
        return self.parsed_toml["navigatorconfig"]["urls"]

    def get_proxy_attempts(self) -> int:
        """Devuelve el numero de intentos de proxy."""
        return self.parsed_toml["proxyconfig"]["attempts"]

    def get_proxy_source(self) -> str:
        """Devuelve la fuente de los proxies."""
        return self.parsed_toml["proxyconfig"]["source"]