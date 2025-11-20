import json
import time
from datetime import datetime
import os

timestamp = datetime.now()
generazione_matricola = f"MAT{}"

lista_alunni = {
    f"{generazione_matricola}":{
        "nome": "Matteo",
        "cognome": "Braida",
        "email": "matteo.braida@its.com",
        "matricola": "MAT001",
        "data_creazione":f"{timestamp}",
        "data_modifica":f"{timestamp}"
    },
}

nuovo_alunno = {}

def creo_json():
    with open("lista_alunni.json", "w") as file:
        json.dump(lista_alunni, file, indent=4)

creo_json()

def aggiunta_alunno():
    matricola = input("Insersci ")



print(lista_alunni)

while True:

    print("\nSISTEMA TRACCIAMENTO ALUNNI")
    print("===========================")
    print("\nSeleziona un'opzione:")
    print("     1)Inserisci nuvo alunno")
    print("     2)Visualizza alunni registrati")
    print("     3)Modifica dati alunno")
    print("     4)Elimina alunno")
    print("     5)Assegna compito a studente")
    print("     6)Registra valutazione")
    print("     7)Visualizza compiti di uno studente")
    print("     8)Visualizza statistiche alunno")
    print("     9)Ranking alunni per media voti")
    print("     10)Report compiti non completati")
    print("     11)Salva dati (backup)")
    print("     12)Carica dati")
    print("     13)Visualizza menù")
    print("     14)Esci")
    
    scelta_menu = input("\nSeleziona l'opzione:")