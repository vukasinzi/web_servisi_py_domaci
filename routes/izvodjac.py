from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request

izvodjac_bp = Blueprint("izvodjac", __name__)

@izvodjac_bp.route("/", methods=["GET"])
def get_izvodjac():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("select * from izvodjac")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)

@izvodjac_bp.route("/", methods=["POST"])
def post_izvodjac():
    con = get_connection()
    cursor = con.cursor()
    try:
        izvodjac = request.json
        ime = izvodjac["ime"]
        zemlja = izvodjac["zemlja"]
        osnovan = izvodjac["osnovan"]

        cursor.execute("INSERT INTO izvodjac (ime, zemlja, osnovan) VALUES (%s, %s, %s)", (ime, zemlja, osnovan))
        con.commit()
        return jsonify({"Poruka": "Izvodjac je uspesno dodat"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@izvodjac_bp.route("/<id>", methods=["PATCH"])
def patch_izvodjac(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update izvodjac set {set_deo} where id = %s", (*body.values(), int(id)))
        con.commit()
        return jsonify({"Poruka": "Izvodjac je uspesno izmenjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@izvodjac_bp.route("/<id>", methods=["DELETE"])
def delete_izvodjac(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from izvodjac where id = %s", (id))
        con.commit()
        return jsonify({"Poruka": "Izvodjac je uspesno uklonjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()