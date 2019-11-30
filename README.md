### How to install dependencies

`pip isntall poetry` 

`poetry install`

### How to generate new migration

`alembic revision --autogenerate --rev-id 1 --message 'init'`

### How to apply migrations

`alembic upgrade head`
