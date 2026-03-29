from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request

zanr_bp = Blueprint("zanr", __name__)

@zanr_bp.route("/", methods=["GET"])
def get_zanr():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("select * from zanr")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)

@zanr_bp.route("/", methods=["POST"])
def post_zanr():
    con = get_connection()
    cursor = con.cursor()
    try:
        zanr = request.json
        naziv = zanr["naziv"]

        cursor.execute("INSERT INTO zanr (naziv) VALUES (%s)", (naziv,))
        con.commit()
        return jsonify({"Poruka": "Zanr je uspesno dodat"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@zanr_bp.route("/<id>", methods=["PATCH"])
def patch_zanr(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update zanr set {set_deo} where id = %s", (*body.values(), int(id)))
        con.commit()
        return jsonify({"Poruka": "Zanr je uspesno izmenjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@zanr_bp.route("/<id>", methods=["DELETE"])
def delete_zanr(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from zanr where id = %s", (id,))
        con.commit()
        return jsonify({"Poruka": "Zanr je uspesno uklonjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()
