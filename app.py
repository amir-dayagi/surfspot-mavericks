import os

# App initialization
from . import create_app
app = create_app(os.getenv('CONFIG_MODE', default="development"))

# Auth Routes
from .auth import urls

# Users Routes
from .users import urls

# Groups Routes
from .groups import urls

# Spots Routes
from .spots import urls

if __name__ == '__main__':
    app.run()
    

