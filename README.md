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
poetry run flask run
```