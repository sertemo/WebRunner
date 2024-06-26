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

from pathlib import Path

# Log
FOLDER_LOGS = Path("logs")
LOG_FILE = "webrunner.log"
LOG_PATH = FOLDER_LOGS / LOG_FILE

# config
CONFIG_FILE = "wr_config.toml"

# user-agents file
USER_AGENTS_FOLDER = Path("assets/agents")
USER_AGENT_FILE = "user_agents.txt"
USER_AGENT_PATH = USER_AGENTS_FOLDER / USER_AGENT_FILE

# browser window
HEIGHT = 800
WIDTH = 800

# Proxy
PROXY_SOURCES = [
    "sslproxies",
    "geonode",
    "spys",
]
