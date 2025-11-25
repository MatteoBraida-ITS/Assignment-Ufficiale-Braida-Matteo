import json
import time
from datetime import datetime
import os

contatore_matricola = 0

def box_testo(titolo: str):
    larghezza = len(titolo) + 4 
    parte_sopra = "╔" + "═" * (larghezza - 2) + "╗"
    parte_di_mezzo = "║ " + titolo.ljust(larghezza - 4) + " ║"
    parte_inferiore = "╚" + "═" * (larghezza - 2) + "╝"

    print(parte_sopra)
    print(parte_di_mezzo)
    print(parte_inferiore)

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
    """Acquisisce i dati di un nuovo alunno""" 
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
    
    box_testo("SISTEMA TRACCIAMENTO ALUNNI")
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
        print("\n")
        box_testo("INSERISCI NUOVO ALUNNO")
        matricola, dati = aggiungi_alunno()
        alunni = carica_alunni()
        alunni[matricola] = dati
        salva_alunni(alunni)
        print(f"\nAlunno aggiunto con successo!")

    if scelta_menu == 'b':
        print("\n")
        box_testo("VISUALIZZA ALUNNI REGISTRATI")
        with open("lista_alunni.json", "r") as file:
            lista_alunni = json.load(file)
            lista_alunni_formattata = json.dumps(lista_alunni, indent=4)
            print(lista_alunni_formattata)