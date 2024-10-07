# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Copiar el archivo CSV
COPY fondos_pensiones.csv /app/fondos_pensiones.csv

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Ejecutar el script insert_fondos.py antes de iniciar la aplicación
#RUN python3 insert_fondos.py

# Exponer el puerto que usará la aplicación
EXPOSE 8000


# Iniciar FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

