# Usa una imagen base de Python
FROM python:3.10-slim

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    wget \
    dpkg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Instalación de Poetry
ENV POETRY_VERSION=1.8.3
# Actualizar pip e instalar Poetry utilizando pip
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"
# Asegurarse de que el binario de Poetry esté en el PATH
ENV PATH="/root/.poetry/bin:${PATH}"
# Configurar Poetry: no crear un entorno virtual y no preguntar en la instalación
RUN poetry config virtualenvs.create false && \
    poetry config installer.parallel false
# Copiar solo archivos necesarios para la instalación de dependencias
COPY pyproject.toml poetry.lock* /app/
# Instalar dependencias de proyecto utilizando Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

ENV CHROME_VERSION="125.0.6422.141"
# Añadir las claves GPG de Chrome
RUN curl -sSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Añadir el repositorio de Chrome
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list    
# Instalar Chrome y limpiar
RUN bash -c 'for i in {1..5}; do apt-get update && apt-get install -y google-chrome-stable && break || sleep 15; done' && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*    
# Obtener la versión actual de Chrome instalada
RUN google-chrome --version

# Install ChromeDriver that matches the Chrome version y limpiamos
RUN curl -sS -o /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    ln -s /usr/local/bin/chromedriver /usr/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/*

# Instalar Chrome Headless Shell
RUN curl -sS -o /tmp/chrome-headless-shell.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-headless-shell-linux64.zip" && \
    unzip /tmp/chrome-headless-shell.zip -d /usr/local/bin/ && \
    rm /tmp/chrome-headless-shell.zip && \
    chmod +x /usr/local/bin/chrome-headless-shell-linux64/chrome-headless-shell && \
    ln -s /usr/local/bin/chrome-headless-shell-linux64/chrome-headless-shell /usr/bin/chrome-headless-shell && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos de la aplicación
COPY . /app

# Establecer variables de entorno necesarias para Selenium y ChromeDriver
ENV PYTHONUNBUFFERED=1 \
    CHROME_DRIVER_PATH=/usr/local/bin/chromedriver \
    CHROME_BIN=/usr/bin/google-chrome \
    HEADLESS_SHELL_BIN=/usr/bin/chrome-headless-shell \
    PYTHONPATH=/app/src:$PYTHONPATH

# Comando por defecto
CMD ["python", "src/webrunner/main.py"]













