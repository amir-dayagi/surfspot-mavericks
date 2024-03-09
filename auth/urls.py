from ..app import app
from . import controllers

@app.route('/login', methods=['POST'])
def login():
    return controllers.login()


@app.route('/signup', methods=['POST'])
def signup():
    return controllers.signup()

    

