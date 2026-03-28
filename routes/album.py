from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request

album_bp = Blueprint("album", __name__)

@album_bp.route("/", methods=["GET"])
def get_album():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("select * from album")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)

@album_bp.route("/", methods=["POST"])
def post_album():
    con = get_connection()
    cursor = con.cursor()
    try:
        album = request.json
        naziv = album["naziv"]
        godina = album["godina"]
        izvodjac_id = album["izvodjac_id"]

        cursor.execute("INSERT INTO album (naziv, godina, izvodjac_id) VALUES (%s, %s, %s)", (naziv, godina, izvodjac_id))
        con.commit()
        return jsonify({"Poruka": "Album je uspesno dodat"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@album_bp.route("/<id>", methods=["PATCH"])
def patch_album(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update album set {set_deo} where id = %s", (*body.values(), int(id)))
        con.commit()
        return jsonify({"Poruka": "Album je uspesno izmenjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()

@album_bp.route("/<id>", methods=["DELETE"])
def delete_album(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from album where id = %s", (id))
        con.commit()
        return jsonify({"Poruka": "Album je uspesno uklonjen"}), 201
    except Exception as x:
        con.rollback()
        return jsonify({"Greska": str(x)}), 500
    finally:
        con.close()