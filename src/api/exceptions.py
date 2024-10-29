from fastapi import status
from fastapi.exceptions import HTTPException

"""
En nuestra aplicación, distinguimos entre excepciones internas y externas para agilizar el manejo de errores 
y la gestión de respuestas.

Excepciones Internas: Estas excepciones se utilizan dentro del entorno de ejecución del sistema.
Se emplean principalmente para la toma de decisiones y el control del flujo de la aplicación.
Las excepciones internas suelen representar problemas o condiciones que surgen durante la ejecución de la lógica del sistema 
y no se exponen directamente a los usuarios finales.

Excepciones Externas: Estas excepciones están diseñadas para ser comunicadas como respuestas a las solicitudes de los clientes.
A menudo son generadas por servicios o controladores para señalar condiciones de error específicas que 
afectan la interacción del cliente con la aplicación.
Las excepciones externas están asociadas con códigos de estado HTTP e incluyen mensajes que proporcionan contexto sobre el error.
Esta distinción permite que la aplicación responda a los clientes con información de error significativa y procesable.

Al separar las excepciones internas y externas, nos aseguramos de que los problemas internos del sistema 
se manejen discretamente mientras se proporcionan respuestas de error claras y consistentes a los clientes.
Este enfoque mejora tanto la robustez del sistema como la claridad de la comunicación con los usuarios.
"""


class EntityNotFound(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)


class EntityNotInserted(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)


class InvalidCsv(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)


class InvalidFileType(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail=message, status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )


class Duplicated(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_409_CONFLICT)


class ServerError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
