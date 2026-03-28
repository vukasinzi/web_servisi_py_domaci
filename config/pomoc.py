
from flask import jsonify

def sredi_rezultate(cursor):
    kolone = []
    for red in cursor.description:
        kolone.append(red[0])
    
    lista = []
    for red in cursor.fetchall():
        objekat = {}
        for i in range(len(kolone)):
            objekat[kolone[i]] = red[i]
        lista.append(objekat)
    
    return lista