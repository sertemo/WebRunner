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

from webrunner.navconfig import NavConfig
from webrunner.browserfactory import BrowserFactory
from webrunner.navigator import Navigator
from webrunner.parser import Parser


class WebRunnerApp:
    def __init__(self) -> None:
        self.parser = Parser()
        self.navconfig = NavConfig(self.parser)
        self.browser = BrowserFactory(self.parser)

    def run(self) -> None:
        proxy = self.navconfig.load_proxy()
        user_agent = self.navconfig.load_user_agent()
        driver = self.browser.create_browser(proxy, user_agent)

        nav = Navigator(driver, self.parser)
        nav.kickoff()


if __name__ == "__main__":
    wr = WebRunnerApp()
    wr.run()
