# surfspot

## Setup

This project is built against Python 3.10, which is the latest supported by Databricks 14.x ML.  
We use `Poetry` for managing the build and install of the project.

### Pipx

[pipx](https://github.com/pypa/pipx) is a tool to help you install and run end-user applications written in Python. It's roughly similar to macOS's brew, JavaScript's npx, and Linux's apt.

It's closely related to pip. In fact, it uses pip, but is focused on installing and managing Python packages that can be run from the command line directly as applications.

Install pipx ([instructions](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)):

```
brew install pipx
pipx ensurepath
```
### Poetry

[Poetry](https://python-poetry.org/) is a tool for **dependency management** and **packaging** in Python. It allows you to declare the libraries your project 
depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.
To get started you will need to install `poetry` locally (recommended is to install using `pipx`)

Install Poetry ([instructions](https://python-poetry.org/docs/#installing-with-pipx))

```
pipx install poetry
```

Ensure version of Poetry is >1.8
```
poetry --version
```

### PostgreSQL

PostgreSQL is a relational database. We use it to persist our data.

Install PostgreSQL ([instructions](https://www.postgresql.org/download))

```
brew install postgresql@16
```

To run PostgreSQL, run the following command:

```
brew services start postgresql@16
```

To stop running PostgreSQL, run the following command:

```
brew services stop postgresql@16
```

#### Database Setup

After running a PostgreSQL server, we need to create a database.

Create a database ([instructions](https://www.postgresql.org/docs/current/app-createdb.html))

```
createdb surfspot
```

Use Migrate to initialize database ([instructions](https://www.postgresql.org/docs/current/app-createdb.html))

**Don't forget to use poetry to run your commands so all required dependencies are installed!**

```
poetry run flask db init
```


```
poetry run flask db migrate -m "Initial migration."
```


```
poetry run flask db upgrade
```

#### Database Migration

Each time the database models change, repeat the `migrate` and `upgrade` commands.

<!--TODO fill in according to migration-->

## Build and Run

To add dependencies:
```
poetry add <dependencies>
```

To install dependencies:
```
poetry lock --no-update
poetry install
```

To run:
```
CONFIG_MODE=<DESIRED_CONFIG_MODE> SECRET_KEY=<YOUR_SECRET_KEY>  poetry run flask run 
```