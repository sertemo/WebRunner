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

from typing import Any, Literal, Union

import toml

from webrunner.settings import CONFIG_FILE


class Parser:
    """Se ocupa de leer el archivo de configuración
    toml y devolver los parámetros deseados"""

    def __init__(self) -> None:
        with open(CONFIG_FILE) as f:
            self.parsed_toml = toml.load(f)

    @property
    def user_agent_config(self) -> str:  # Si es random o nada o una predeterminada
        """Devuelve la configuración del user agent."""
        return self.parsed_toml["navconfig"]["user-agent"]

    @property
    def proxy_config(self) -> str | bool:  # Si es random o nada o una predeterminada
        """Devuelve la configuración del proxy."""
        return self.parsed_toml["navconfig"]["proxy"]

    @property
    def browser_config(self) -> dict[str, Any]:  # Si es Chrome o Firefox y las opciones
        """Devuelve la configuración del navegador con todas sus opciones."""
        return self.parsed_toml["browserconfig"]

    @property
    def url_list(self) -> list[str]:
        """Devuelve una lista de URLs a visitar."""
        return self.parsed_toml["navigatorconfig"]["urls"]

    @property
    def proxy_attempts(self) -> int:
        """Devuelve el numero de intentos de proxy."""
        return self.parsed_toml["proxyconfig"]["attempts"]

    @property
    def proxy_source(self) -> str:
        """Devuelve la fuente de los proxies."""
        return self.parsed_toml["proxyconfig"]["source"]

    @property
    def max_actions(self) -> str:
        """Devuelve el número maximo de acciones a realizar."""
        return self.parsed_toml["navigatorconfig"]["max-random-actions"]
