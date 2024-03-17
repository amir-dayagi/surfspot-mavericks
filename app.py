import os

# App initialization
from . import create_app
app = create_app(os.getenv('CONFIG_MODE', default="development"))

# Auth Routes
from .auth import urls

# Sessions Routes
from .sessions import urls

if __name__ == '__main__':
    app.run()
    

