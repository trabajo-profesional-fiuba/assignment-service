# Assigment Service API Migrations

Para entender como funcionan, las configuraciones y los archivos es **muy** recomendable leer antes la [documentación](https://alembic.sqlalchemy.org/en/latest/index.html).
Son 15-20min que te van a ahorrar muchos dolores de cabeza

Las migraciones son un proceso en el que se modifican los esquemas (En nuestro caso las clases que estan en los archivos `models.py`) de las tablas actuales de la base de datos.
Estas migraciones se ejecutan basándose en una versión de `revisión` que Alembic utiliza para validar el estado actual del esquema y los cambios que se deben realizar.

## Alembic
Alembic es una herramienta de migración de bases de datos que trabaja con [SQLAlchemy](https://www.sqlalchemy.org/). Alembic te permite gestionar cambios en el esquema de tu base de datos por versiones.

Alembic se puede considerar como **git**; con esta herramienta, podes pensar en las revisiones como commits de git. Así, Alembic puede actualizar, retroceder y crear nuevas revisiones para mantener un control de versiones del esquema de la base de datos.

### Comandos

```
alembic revision -m "Add new table"
```
Este comando genera una nueva migración de base de datos. También podes usar ```alembic revision --autogenerate -m "Agregar nueva tabla"``` después de modificar el archivo de modelos para que Alembic genere automáticamente una revisión predeterminada, es importante revisarla antes de ejecutarla. 

Aveces alembic proporciona cambios de mas porque comenzamos a usar migraciones luego de cierto tiempo y no desde un primer momento.

```
alembic upgrate head
```
Este comando ejecuta la última revisión de la base de datos.

```
alembic downgrade -1.
```
Este comando revierte la última migración aplicada.

```
alembic current
```
Este comando muestra la(s) revisión(es) actual(es) de la base de datos.

```
alembic history
```
Este comando muestra el historial de revisiones.


```
alembic edit
```
Este comando abre el vscode para editar la revision

```
alembic merge r1 r2
```
Este comando mergea dos revisiones en una. En la [documentacion](https://alembic.sqlalchemy.org/en/latest/branches.html) detalla como y cuando trabajar con este caso 

### Configuracion

El archivo alembic.ini tiene la configuracion de las migraciones. Lo mas importante es la URL a la base que apunta y el `Base` que toma para "trackear" los cambios de modelos

##⚠️ Importante ! 
Actualmente, [la autogeneración](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) está habilitada para que los desarrolladores puedan evitar hacer las migraciones manualmente.Igualmente, revisalas para comprobar que esten bien los cambio

Para más información, consulta la documentación sobre [qué puede detectar la autogeneración de Alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).

