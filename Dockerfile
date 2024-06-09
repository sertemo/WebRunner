# Usa una imagen base de Python
FROM python:3.11-slim

# Instala las dependencias del sistema
RUN apt-get update && \
    apt-get install -y curl gnupg unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Añadir las claves GPG de Chrome
RUN curl -sSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Añadir el repositorio de Chrome
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Instalar Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Instalar ChromeDriver
RUN curl -sS -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Poetry
ENV POETRY_VERSION=1.8.3

# Asegurarse de que el binario de Poetry esté en el PATH
ENV PATH="/root/.poetry/bin:${PATH}"

# Configurar Poetry: no crear un entorno virtual y no preguntar en la instalación
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false && \
    poetry config installer.parallel false

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo archivos necesarios para la instalación de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias de proyecto utilizando Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copia los archivos de la aplicación
COPY . /app

# Establecer variables de entorno necesarias para Selenium y ChromeDriver
ENV PYTHONUNBUFFERED=1 \
    CHROME_DRIVER_PATH=/usr/local/bin/chromedriver \
    CHROME_BIN=/usr/bin/google-chrome \
    PYTHONPATH=/app/src:$PYTHONPATH

# Comando por defecto
CMD ["python", "src/webrunner/main.py"]

