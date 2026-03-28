from config.db import get_connection
from config.pomoc import sredi_rezultate
from flask import Blueprint, jsonify, request


korisnik_bp = Blueprint("korisnik", __name__)

@korisnik_bp.route("/", methods =["GET"])
def get_korisnik():
    con = get_connection()
    cursor = con.cursor()

    cursor.execute("select * from korisnik")
    rezultati = sredi_rezultate(cursor)
    con.close()
    return jsonify(rezultati)
    

@korisnik_bp.route("/", methods = ["POST"])
def post_korisnik():
    
    con = get_connection()
    cursor = con.cursor()
    try:
        korisnik = request.json
        ime = korisnik["ime"]
        email = korisnik["email"]

        cursor.execute( "INSERT INTO korisnik (ime,email) VALUES (%s, %s)",(ime,email))
        con.commit()
        return jsonify({"Poruka": "Korisnik je uspesno dodat"}),201
    except Exception as x:
        con.rollback()
        return jsonify({"greska": str(x)}), 500
    finally:
        con.close()

@korisnik_bp.route("/<id>", methods = ["PATCH"])
def patch_korisnik(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        body = request.json
        set_deo = ""
        for kljuc in body.keys():
            set_deo += f"{kljuc} = %s,"
        set_deo = set_deo.rstrip(",")
        cursor.execute(f"update korisnik set {set_deo} where id = %s", (*body.values(),int(id))) 
        con.commit()
        return jsonify({"Poruka": "Korisnik je uspesno izmenjen"}),201

    except Exception as x:
         con.rollback()
         return jsonify({"Greska": str(x)}),500
    finally:
        con.close()

@korisnik_bp.route("/<id>", methods = ["DELETE"])
def delete_korisnik(id):
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("delete from korisnik where id = %s",(id))
        con.commit()
        return jsonify({"Poruka": "Korisnik je uspesno uklonjen"}),201

    except Exception as x:
         con.rollback()
         return jsonify({"Greska": str(x)}),500
    finally:
        con.close()
