import json
import time
from datetime import datetime
import os

contatore_matricola = 0

def crea_matricola():
    global contatore_matricola
    contatore_matricola += 1
    return f"MAT{contatore_matricola:03d}"

def carica_alunni():
    """Carica la lista degli alunni del file JSON, se esiste"""
    if os.path.exists("lista_alunni.json"):
        with open("lista_alunni.json", "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}

def salva_alunni(lista):
    """Salva i dati degli alunni nel file JSON"""
    with open("lista_alunni.json", "w", encoding="utf-8") as file:
        json.dump(lista, file, indent=4)

def aggiungi_alunno():
    """Crea un nuovo alunno e lo aggiunge al dizionario""" 
    matricola = crea_matricola()
    timestamp = datetime.now().isoformat() 

    nome = input("Inserisci il nome del nuovo alunno:")
    cognome = input("Inserisci il cognome del nuovo alunno:")
    email = input("Inserisci la e-mail del nuovo alunno:")

    nuovo_alunno= {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "matricola": matricola,
        "data creazione": timestamp,
        "data modifica": timestamp
    }

    return matricola, nuovo_alunno

if not os.path.exists("lista_alunni.json"):
    matricola_iniziale = crea_matricola()
    timestamp_iniziale = datetime.now().isoformat()
    lista_iniziale = {
        matricola_iniziale: {
        "nome": "Matteo",
        "cognome": "Braida",
        "email": "braida.matteo@its.com",
        "matricola": matricola_iniziale,
        "data creazione": timestamp_iniziale,
        "data modifica": timestamp_iniziale
        }
    }

    salva_alunni(lista_iniziale)
    print(f"File 'lista_alunni.json' creato con alunno iniziale {matricola_iniziale}")
else:
    alunni_esistenti = carica_alunni()
    matricole = [int(key.replace("MAT","")) for key in alunni_esistenti.keys() if key.startswith("MAT")]
    if matricole:
        contatore_matricola = max(matricole)


while True:

    carica_alunni()
    
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
        matricola, dati = aggiungi_alunno()
        alunni = carica_alunni()
        alunni[matricola] = dati
        salva_alunni(alunni)
        print(f"\nAlunno aggiunto con successo!")