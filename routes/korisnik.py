from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request


pesma_bp = Blueprint("pesma", __name__)

@pesma_bp.route("/", methods =["GET"])
def get_pesma():
    con = get_connection()
    cursor = con.cursor()

    cursor.execute("select * from korisnik")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)
    

@pesma_bp.route("/", methods = ["POST"])
def post_pesma():
    
    con = get_connection()
    cursor = con.cursor()
    try:
        pesma = request.json
        redni_broj = pesma["redni_broj"]
        naziv = pesma["naziv"]
        trajanje = pesma["trajanje"]
        album_id = pesma["album_id"]

        cursor.execute( "INSERT INTO pesma (redni_broj, naziv, trajanje, album_id) VALUES (%s, %s, %s, %s)",
                    (redni_broj, naziv, trajanje, album_id))
        con.commit()
        return jsonify({"Poruka": "Pesma je uspesno dodata"}),201
    except Exception as x:
        con.rollback()
        return jsonify({"greska": str(x)}), 500
    finally:
        con.close()

@pesma_bp.route("/<id>", methods = ["PATCH"])
def patch_pesma(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update pesma set {set_deo} where id = %s", (*body.values(),int(id))) 
        con.commit()
        return jsonify({"Poruka": "Pesma je uspesno izmenjena"}),201

    except Exception as x:
         con.rollback()
         return jsonify({"Greska": str(x)}),500
    finally:
        con.close()

@pesma_bp.route("/<id>", methods = ["DELETE"])
def delete_pesma(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from pesma where id = %s",(id))
        con.commit()
        return jsonify({"Poruka": "Pesma je uspesno uklonjena"}),201

    except Exception as x:
         con.rollback()
         return jsonify({"Greska": str(x)}),500
    finally:
        con.close()
