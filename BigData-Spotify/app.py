import os
import secrets
from dotenv import load_dotenv
from flask import Flask

from routes.routes import routes

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar las credenciales de Spotify
os.environ["SPOTIPY_CLIENT_ID"] = os.getenv("SPOTIPY_CLIENT_ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = os.getenv("SPOTIPY_CLIENT_SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = os.getenv("SPOTIPY_REDIRECT_URI")

app = Flask(__name__)
app.config["FLASK_DEBUG"] = True
app.config["SECRET_KEY"] = secrets.token_urlsafe(20)

#Configurar las rutas de la app
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
