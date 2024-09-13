# Assigment Service API Migrations

Read the [documentation](https://alembic.sqlalchemy.org/en/latest/index.html)!!!

Migrations are process where the schemas of the current database tables are modified. This migrations are run based on a `revision` version which alembic takes to validate the current state of the schema and the changes that needs to do.

## Alembic
Alembic is a database migration tool that works with SQLAlchemy, a popular Python library for interacting with relational databases. Alembic allows you to manage changes to your database schema in a version-controlled way, keeping it in sync with your application code. It is particularly useful for developing applications that use SQLAlchemy models to define the database structure.

Alembic can be though as git, with this tool you can think revisions as git commits. Then, alembic can upgrade, downgrade and create new revisions to keep a version control of the database schema.

### Commands

```
alembic revision -m "Add new table"
```
This command generates a new database migration. You can also use ```alembic revision --autogenerate -m "Add new table"``` after modifying models file to autogenerate a default revision by alembic, which can be customized.

```
alembic upgrate head
```
This command executes the latest database revision.

```
alembic downgrade -1.
```
This command rolls back the last applied migration.

```
alembic current
```
This command shows the current revision(s) of the database.

```
alembic history
```
This command shows the revision history.

```
alembic edit
```
This command opens the current revision script in an editor.

```
alembic merge
```
This command creates a new migration script by merging two or more revisions.

### Configuration

The alembic.ini file contains various configuration options such as the database URL, migration script location, and other settings. These options can be customized according to your project requirements.

Currently, [autogenerating](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) is enabled so that devs can avoid doing the migrations manually. For more info read the documentation of [what alembic autogeneration can detect](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)
