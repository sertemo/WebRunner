#!/bin/bash

# Levanta los servicios en segundo plano
docker-compose up -d

# Espera unos segundos para asegurarse de que los servicios estén completamente levantados
sleep 10

# Ejecuta la aplicación en el contenedor
#docker-compose run webrunner
docker-compose run --rm webrunner

# Mostrar los logs del contenedor webrunner
docker-compose logs webrunner

# Apaga los servicios
docker-compose down
