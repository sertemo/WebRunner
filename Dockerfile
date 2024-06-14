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

# Copia los archivos de la aplicación
COPY . /app

# Establecer variables de entorno necesarias para Selenium y Firefox
ENV PYTHONUNBUFFERED=1 \
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver \
CHROME_BIN=/usr/bin/google-chrome \
PYTHONPATH=/app/src:$PYTHONPATH

# Comando por defecto
CMD ["python", "src/webrunner/main.py"]


