# Usar la imagen base de Python
FROM python:3.13.2-alpine3.20

# Instalar locales
RUN apk update && apk add --no-cache musl-locales musl-locales-lang && pip install --upgrade pip

# Establecer la configuración regional como variable de entorno
ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES:es
ENV LC_ALL=es_ES.UTF-8

# Establecer el directorio de trabajo
WORKDIR /app
# Copiar el resto del código al contenedor
COPY . /app/

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]