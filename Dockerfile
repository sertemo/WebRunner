# Usa una imagen base de Python
FROM python:3.10-slim

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y curl gnupg unzip

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

# Añadir las claves GPG de Chrome
RUN curl -sSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
    
# Añadir el repositorio de Chrome
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
    
# Instalar Chrome y limpiar
RUN bash -c 'for i in {1..5}; do apt-get update && apt-get install -y google-chrome-stable && break || sleep 15; done' && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verificar la versión actual de Chrome instalada
RUN google-chrome --version

# Capturar y mostrar la versión de Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+') && \
    echo "Chrome version: $CHROME_VERSION" && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1) && \
    echo "Chrome major version: $CHROME_MAJOR_VERSION"

# Separar los pasos para una mejor depuración
#RUN CHROME_MAJOR_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | cut -d '.' -f 1) && \
#    echo "Chrome major version: $CHROME_MAJOR_VERSION" && \
#    CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION) && \
#    echo "ChromeDriver version: $CHROMEDRIVER_VERSION" && \
#    curl -sS -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
#    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
#    rm /tmp/chromedriver.zip

# Copia los archivos de la aplicación
COPY . /app

# Establecer variables de entorno necesarias para Selenium y ChromeDriver
ENV PYTHONUNBUFFERED=1 \
    CHROME_DRIVER_PATH=/usr/local/bin/chromedriver \
    CHROME_BIN=/usr/bin/google-chrome \
    PYTHONPATH=/app/src:$PYTHONPATH

# Comando por defecto
CMD ["python", "src/webrunner/main.py"]











