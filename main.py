from flask import Flask, render_template
from routes.izvodjac import izvodjac_bp
from routes.album import album_bp
from routes.pesma import pesma_bp
from routes.korisnik import korisnik_bp
from routes.recenzija import recenzija_bp
from routes.zanr import zanr_bp

blueprints = [
    (izvodjac_bp, "/api/izvodjac"),
    (album_bp, "/api/album"),
    (pesma_bp, "/api/pesma"),
    (korisnik_bp, "/api/korisnik"),
    (recenzija_bp, "/api/recenzija"),
    (zanr_bp,"/api/zanr"),
]

app = Flask(__name__)

@app.route("/")
def pocetna():
    return render_template("index.html")

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

if __name__ == "__main__":
    app.run(debug=True)
