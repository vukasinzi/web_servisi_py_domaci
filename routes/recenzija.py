from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request

recenzija_bp = Blueprint("recenzija", __name__)

@recenzija_bp.route("/", methods=["GET"])
def get_recenzija():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("select * from recenzija")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)

@recenzija_bp.route("/", methods=["POST"])
def post_recenzija():
    con = get_connection()
    cursor = con.cursor()
    try:
        recenzija = request.json
        ocena = recenzija["ocena"]
        komentar = recenzija["komentar"]
        album_id = recenzija["album_id"]
        korisnik_id = recenzija["korisnik_id"]

        cursor.execute("INSERT INTO recenzija (ocena, komentar, album_id, korisnik_id) VALUES (%s, %s, %s, %s)", (ocena, komentar, album_id, korisnik_id))
        con.commit()
        return jsonify({"Poruka": "Recenzija je uspesno dodata"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@recenzija_bp.route("/<id>", methods=["PATCH"])
def patch_recenzija(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update recenzija set {set_deo} where id = %s", (*body.values(), int(id)))
        con.commit()
        return jsonify({"Poruka": "Recenzija je uspesno izmenjena"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@recenzija_bp.route("/<id>", methods=["DELETE"])
def delete_recenzija(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from recenzija where id = %s", (id))
        con.commit()
        return jsonify({"Poruka": "Recenzija je uspesno uklonjena"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()