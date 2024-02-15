import os

# App initialization
from . import create_app
app = create_app(os.getenv('CONFIG_MODE'))

# Users Routes
from .users import urls


if __name__ == '__main__':
    app.run()

