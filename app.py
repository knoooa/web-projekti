from flask import Flask
from os import getenv
import secrets

app = Flask(__name__)

#app.secret_key = getenv("SECRET_KEY")
app.secret_key = secrets.token_hex(16)

import routes
    
#test
