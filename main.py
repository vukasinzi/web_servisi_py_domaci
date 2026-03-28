from flask import Flask
from routes.izvodjac import izvodjac_bp
from routes.album import album_bp
from routes.pesma import pesma_bp
from routes.korisnik import korisnik_bp
from routes.recenzija import recenzija_bp

blueprints = [
    (izvodjac_bp, "/api/izvodjac"),
    (album_bp, "/api/album"),
    (pesma_bp, "/api/pesma"),
    (korisnik_bp, "/api/korisnik"),
    (recenzija_bp, "/api/recenzija"),
]

app = Flask(__name__)

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

if __name__ == "__main__":
    app.run(debug=True)