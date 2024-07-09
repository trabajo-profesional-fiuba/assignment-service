# Usa una imagen base de Python
FROM python:3.11-slim

# Instala Poetry
RUN pip install poetry

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de Poetry
COPY pyproject.toml poetry.lock ./

# Deshabilita la creación de entorno virtual
RUN poetry config virtualenvs.create false

# Instala las dependencias del proyecto
RUN poetry install --no-root

# Copia todo el código del proyecto
COPY . .

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Define el comando por defecto para ejecutar la aplicación
CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
