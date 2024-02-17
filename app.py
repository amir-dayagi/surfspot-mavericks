import os

# App initialization
from surfspot import create_app

app = create_app(os.getenv('CONFIG_MODE'))
