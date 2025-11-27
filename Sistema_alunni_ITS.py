import json
import time
from datetime import datetime
import os

contatore_matricola = 0
contatore_task = 0

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

def crea_task():
     global contatore_task
     contatore_task += 1
     return f"TASK{contatore_task:03d}"

def carica_database():
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

def visualizza_alunni():
    """Stampa una lista con tutti i dati degli studenti presenti nel file JSON"""
    dati = carica_database()
    alunni = dati["alunni"]

    if alunni:
                for mat, dati in alunni.items():
                    print(f"{mat}:\n -Nome:{dati['nome']}\n -Cognome:{dati['cognome']}\n -E-mail:{dati['email']}")
    else:
                print("Nessun alunno presente.")

def aggiungi_alunno():
    """Acquisisce i dati di un nuovo alunno""" 
    matricola = crea_matricola()
    task = crea_task()
    timestamp = datetime.now().isoformat() 

    nome = input("Inserisci il nome del nuovo alunno:")
    cognome = input("Inserisci il cognome del nuovo alunno:")
    email = input("Inserisci la e-mail del nuovo alunno:")

    nuovo_alunno= {
        "alunno": {
        matricola: {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "matricola": matricola,
            "data creazione": timestamp,
            "data modifica": timestamp
        }
    },

    "compiti": {
        task: {
            "id": task,
            "descrizione": "",
            "alunno_matricola": matricola,
            "stato": "",
            "data assegnazione": datetime.now().isoformat(),
            "voto": 0
        }
    }
    }

    return matricola, nuovo_alunno

def modifica_dati_alunno():
    """Modica i dati degli studenti contenuti nel file JSON"""
    alunni = carica_database()

    if not alunni:
        print("\nNessun alunno presente nel database")
        return
    
    matricola = input("\nSeleziona l'alunno di qui vuoi modificare i dati digitando la sua matricola (es.MAT001):")

    if matricola not in alunni["alunno"]:
        print("\nSeleziona l'alunno di qui vuoi eliminare i dati digitando la sua matricola (es.MAT001):")
        return
    
    alunno = alunni[matricola]
    print(f"\nDati attuali di {alunno['nome']} {alunno['cognome']}")
    print(f"1) Nome: {alunno['nome']}")
    print(f"2) Cognome: {alunno['cognome']}")
    print(f"3) E-mail: {alunno['email']}")

    campo = input(f"\nQuale dato dell'alunno {alunno['nome']} {alunno['cognome']} vuoi modificare? (1-3):")

    nuovo_dato = None

    if campo == '1':
        nuovo_dato = input("Inserisci il nuovo nome:")
        alunno['nome'] = nuovo_dato
        print(f"Nome cambiato con {alunno['nome']}!")
        print(alunno)
    elif campo == '2':
        nuovo_dato = input("Inserisci il nuovo cognome:")
        alunno['cognome'] = nuovo_dato
        print(f"Cognome cambiato con {alunno['cognome']}")
    elif campo == '3':
        nuovo_dato = input("Inserisci la nuova E-mail:")
        alunno['email'] = nuovo_dato
        print(f"E-mail cambiata con {alunno['email']}")
    else:
        print("\n Errore: Dato non presente nel registro.")

    alunno['data modifica'] = datetime.now().isoformat()
    alunni[matricola] = alunno
    salva_alunni(alunni)

def elimina_alunno():
    """Elimina i dati relativi all'alunno selezionato"""
    alunni = carica_database()

    if not alunni:
          print("\nNessun alunno presente nel database")
          return
     
    matricola = input("\nSeleziona l'alunno di qui vuoi eliminare i dati digitando la sua matricola (es.MAT001):")

    if matricola not in alunni:
          print("\nLa matricola digitata non corrisponde a nessun alunno presente nel database.")
          return

    alunno = alunni[matricola]
    print(f"\nL'alunno selezionato è {alunno['nome']} {alunno['cognome']}.")

    conferma = input(f"\nSei sicuro di voler eliminare i dati di {alunno['nome']} {alunno['cognome']}? (y/n):").lower()

    if conferma == 'y':
        alunni.pop(matricola)
        print(f"\nL'alunno {alunno['nome']} {alunno['cognome']} con matricola {matricola} è stato rimosso dal database.")
    elif conferma == 'n':
        print("\nOperazione annullata.")
        return
    else:
        print("\nComando non valido.")

    salva_alunni(alunni)

if not os.path.exists("lista_alunni.json"):
    matricola_iniziale = crea_matricola()
    task_iniziale = crea_task()
    timestamp_iniziale = datetime.now().isoformat()

    database = {
    "alunno": {
        matricola_iniziale: {
            "nome": "Matteo",
            "cognome": "Braida",
            "email": "braida.matteo@its.com",
            "matricola": matricola_iniziale,
            "data creazione": timestamp_iniziale,
            "data modifica": timestamp_iniziale
        }
    },

    "compiti": {
        task_iniziale: {
            "id": task_iniziale,
            "descrizione": "esercizio python",
            "alunno_matricola": matricola_iniziale,
            "stato": "assegnato",
            "data assegnazione": datetime.now().isoformat(),
            "voto": 8
        }
    }
}
    
    salva_alunni(database)
    print(f"File 'lista_alunni.json' creato con alunno iniziale {matricola_iniziale}")
else:
    alunni_esistenti = carica_database()
    matricole = [int(key.replace("MAT","")) for key in alunni_esistenti.keys() if key.startswith("MAT")]
    if matricole:
        contatore_matricola = max(matricole)

while True:

    carica_database()
    
    print("\n")
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
        matricola, nuovi_dati_alunno = aggiungi_alunno()
        dati = carica_database()
        dati
        alunni = dati[nuovi_dati_alunno["alunno"]["compiti"]]
        salva_alunni(alunni)
        print(f"\nAlunno aggiunto con successo!")

    if scelta_menu == 'b':
        print("\n")
        box_testo("VISUALIZZA ALUNNI REGISTRATI")
        visualizza_alunni()

    if scelta_menu == 'c':
        print("\n")
        box_testo("MODIFICA DATI ALUNNO")
        modifica_dati_alunno()

    if scelta_menu == 'd':
        print("\n")
        box_testo("ELIMINA DATI ALUNNO")
        elimina_alunno()

