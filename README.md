# Pension Funds Management API
Prueba tecnica para BTG-pactual
Domingo Alberto Utrera Cedeño

## Descripción
API REST para la gestión de fondos de pensiones.
la api esta eche en Fast-Api con MongoDb como base de datos NoSql


## Funcionalidades
1. Suscribirse a un nuevo fondo.
2. Cancelarse de un fondo actual.
3. Ver el historial de últimas transacciones.
4. Envío de notificaciones por email o SMS.


## Cómo ejecutar
1. Clonar el repositorio.
2. Navegar al directorio del proyecto "test-btg/app".
3. Ejecutar `docker-compose up --build`.
4. Acceder a la API en `http://localhost:8000/docs`.
4. terminar el contenedor de docker `docker-compose down`.


### crear la coleccion de tipos de fondos
desde el terminal ejecutar:
    sudo docker exec -it <nombre_del_contenedor> /bin/bash
    python app/insert_fondos.py
estocreara una collecion de Fondos de pensiones, basados en la tabla suministrada en la prueba

