import json
import time
from datetime import datetime
import os

timestamp = datetime.now()

def crea_matricola():
    id_matricola = "000"
    id_matricola = '%03d' % (int(id_matricola) + 1)
    return id_matricola

crea_matricola()

lista_alunni = {
    f"MAT{crea_matricola()}":{
        "nome": "Matteo",
        "cognome": "Braida",
        "email": "matteo.braida@its.com",
        "matricola": f"MAT{crea_matricola()}",
        "data_creazione":f"{timestamp}",
        "data_modifica":f"{timestamp}"
    },
}

def crea_json():
    with open("lista_alunni.json", "w") as file:
        json.dump(lista_alunni, file, indent=4)

crea_json()

def aggiunta_alunno():
    nuovo_alunno = {}
    nome_alunno = input("Insersci nome alunno:")
    nuovo_alunno.update({"nome": nome_alunno})
    cognome_alunno = input("Inserisci cognome:")
    nuovo_alunno.update({"cognome": cognome_alunno})
    email_alunno = input("Inserisci e-mail:")
    nuovo_alunno.update({"email": email_alunno})
    nuovo_alunno.update({"data_creazione":f"{timestamp}"})
    nuovo_alunno.update({"data_modifica":f"{timestamp}"})
    

print(lista_alunni)

while True:

    print("\nSISTEMA TRACCIAMENTO ALUNNI")
    print("===========================")
    print("\nSeleziona un'opzione:")
    print("     A)Inserisci nuovo alunno")
    print("     B)Visualizza alunni registrati")
    print("     C)Modifica dati alunno")
    print("     D)Elimina alunno")
    print("     E)Assegna compito a studente")
    print("     F)Registra valutazione")
    print("     G)Visualizza compiti di uno studente")
    print("     H)Visualizza statistiche alunno")
    print("     I)Ranking alunni per media voti")
    print("     L)Report compiti non completati")
    print("     M)Salva dati (backup)")
    print("     N)Carica dati")
    print("     O)Visualizza menù")
    print("     P)Esci")
    
    scelta_menu = input("\nSeleziona l'opzione:").lower()

    if scelta_menu == 'a':
        aggiunta_alunno()