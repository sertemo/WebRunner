# WebRunner
### v0.1.0

![Tests](https://github.com/sertemo/WebRunner/actions/workflows/tests.yml/badge.svg)
![Dependabot](https://img.shields.io/badge/dependabot-enabled-blue.svg?logo=dependabot)
![GitHub](https://img.shields.io/github/license/sertemo/WebRunner)
![Docker](https://img.shields.io/docker/image-size/sertemo/webrunner?color=blue&logo=docker)

## Descripción
Aplicación para crear un bot en mi servidor que periódicamente visite cierta lista de páginas de forma automática y haga acciones generales como scroll o pinchar en algún sitio aleatorio.

Se encapsulará la aplicación en un docker y se usará un cronjob para crear un contenedor periódicamente en el que se ejecutará la aplicación. Al finalizar, el contenedor se borrará automáticamente.

## Uso
Para realizar alguna modificación de los parámetros de la aplicación, basta con cambiar la configuración del archivo `wr_config.toml` que luce así:
```toml
[navconfig]
user-agent = "random"  # random false o un user-agent válido
proxy = "random" # random false o un proxy válido

[proxyconfig]
source = "sslproxies"  # sslproxies o geonode o spys
attempts = 5

[browserconfig]
type = "Chrome"
headless = true
disable-gpu = true
no-sandbox = true
enable-javascript = true
allow-insecure-localhost = true
ignore-certificate-errors = true
enable-automation = true
disable-dev-shm-usage = true
disable-blink-features = true

[navigatorconfig]
max-actions = 4
urls = [
    'https://tutorial-kopuru.streamlit.app/',
    'https://earthquakelocator.streamlit.app/',
    'https://stm-cv.streamlit.app/',
    'https://kopuru-model-eval.streamlit.app/',
    'https://litteragpt.streamlit.app/',
    'https://www.tejedormoreno.com/',
    'https://collatzeral.streamlit.app/',
    'https://graphicator.streamlit.app/',
    'https://talsa-mailing.streamlit.app/'
    ]
```

En este archivo se pueden agregar nuevas urls a visitar periódicamente, configurar el tipo de proxy etc.

Actualmente sólo está habilitado para utilizar el navegador **Chrome** (En el Dockerfile solo instalamos Chrome y Chromedriver.)

## SemVer

## Tests
![Pytest](https://img.shields.io/badge/testing-pytest-blue.svg)
![Black](https://img.shields.io/badge/code%20style-black-blue.svg)
![Flake8](https://img.shields.io/badge/linter-flake8-blue.svg)
![MyPy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)

## Tecnologías
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)


## Licencia
Copyright 2024 Sergio Tejedor Moreno

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

