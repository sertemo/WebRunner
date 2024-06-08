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

"""Script para configurar el navconfigo que se encarga de gestionar los
user-agents y el proxymanager."""

import random

from webrunner.parser import Parser
from webrunner.proxymanager import ProxyManager
from webrunner.settings import USER_AGENT_PATH

class NavConfig:
    def __init__(self, proxy_manager: ProxyManager, parser: Parser) -> None:
        self.pm = proxy_manager
        self.parser = parser
        self.url_list = self.parser.get_url_list()
    
    def load_proxy(self) -> str | None:
        """Devuelve un proxy aleatorio funcional, o
        un proxy determinado por el usuario o None
        """
        proxy_config = self.parser.get_proxy_config()
        n_attemps = self.parser.get_proxy_attempts()
        source = self.parser.get_proxy_source()

        if proxy_config == "random":
            return self.pm.get_random_proxy(self.url_list[0], n_attemps, source)
        elif proxy_config == False:
            return None
        else:
            return str(proxy_config)

    def load_user_agent(self) -> str:
        """Devuelve un user-agent aleatorio o una predeterminada."""
        user_agent_config = self.parser.get_user_agent_config()
        if user_agent_config == "random":
            with open(USER_AGENT_PATH) as f:
                user_agents = [line.strip() for line in f]
            return random.choice(user_agents)
        elif user_agent_config == False:
            return None
        else:
            return user_agent_config

