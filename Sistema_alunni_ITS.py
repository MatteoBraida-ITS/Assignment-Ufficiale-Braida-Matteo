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
    
def crea_alunni(lista):
     """Crea la  la lista_alunni.json"""
     with open("lista_alunni.json", "w", encoding="utf-8") as file:
        json.dump(lista, file, indent=4)

def salva_alunni(lista):
    """Salva i dati degli alunni nel file JSON"""
    with open("lista_alunni.json", "w", encoding="utf-8") as file:
        json.dump(lista, file, indent=4)

def visualizza_alunni():
    """Stampa una lista con tutti i dati degli studenti presenti nel file JSON"""
    dati = carica_database()
    alunni = dati["alunni"]

    if alunni:
        for matricola, alunno in alunni.items():
            if matricola.startswith("MAT"):
                print(f"{matricola}:\n -Nome:{alunno["nome"]}\n -Cognome:{alunno["cognome"]}\n -E-mail:{alunno["email"]}")
    else:
        print("Nessun alunno presente.")

def aggiungi_alunno():
    """Acquisisce i dati di un nuovo alunno""" 
    matricola = crea_matricola()
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

    nome = input("Inserisci il nome del nuovo alunno:")
    cognome = input("Inserisci il cognome del nuovo alunno:")
    email = input("Inserisci la e-mail del nuovo alunno:")

    nuovo_alunno = {
        "alunni": {
        matricola: {
           "nome": nome,
           "cognome": cognome,
           "email": email,
           "matricola": matricola,
           "data creazione": timestamp,
           "data modifica": timestamp
        }
    },
        "compiti": {}
}
    
    return matricola, nuovo_alunno

def modifica_dati_alunno():
    """Modica i dati degli studenti contenuti nel file JSON"""
    dati = carica_database()
    
    if not dati:
        print("\nNessun alunno presente nel database")
        return
    
    alunni = dati["alunni"]

    matricola = input("\nSeleziona l'alunno di qui vuoi modificare i dati digitando la sua matricola (es.MAT001):")

    if matricola in alunni:    
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
    else:
        print("Errore: Matricola non presente nel database.")

    alunno['data modifica'] = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    alunni[matricola].update(alunno)
    salva_alunni(dati)

def elimina_alunno():
    """Elimina i dati relativi all'alunno selezionato"""
    dati = carica_database()

    if not dati:
          print("\nNessun alunno presente nel database")
          return
    
    alunni = dati["alunni"]
    compiti = dati["compiti"]
    
    matricola = input("\nSeleziona l'alunno di qui vuoi eliminare i dati digitando la sua matricola (es.MAT001):")

    if matricola not in alunni:
          print("\nLa matricola digitata non corrisponde a nessun alunno presente nel database.")
          return

    alunno = alunni[matricola]
    print(f"\nL'alunno selezionato è {alunno['nome']} {alunno['cognome']}.")

    conferma = input(f"\nSei sicuro di voler eliminare i dati di {alunno['nome']} {alunno['cognome']}? (y/n):").lower()

    if conferma == 'y':
        alunni.pop(matricola)

        task_da_eliminare = []

        for task_id, task_data in compiti.items():
            if task_data["matricola"] == matricola:
                task_da_eliminare.append(task_id)
    
        for task_id in task_da_eliminare:
            compiti.pop(task_id)

        print(f"\nL'alunno {alunno['nome']} {alunno['cognome']} con matricola {matricola} è stato rimosso dal database.")
    elif conferma == 'n':
        print("\nOperazione annullata.")
        return
    else:
        print("\nComando non valido.")

    salva_alunni(dati)

def assegna_compito():
    """Assegna un compito ad un alunno"""
    dati = carica_database()

    matricola = input("Seleziona l'alunno a cui assegnare il compito digitando la sua matricola (es.MAT001):")

    task = crea_task()
    if matricola in dati["alunni"]:
        compito_da_assegnare = input(f"Quale compito vuoi asseganre all'alunno {matricola}?:")
    else:
        print("Errore: Matricola non presente nel database.")

    
    nuovo_compito = {
        task: {
           "id": task,
           "descrizione": compito_da_assegnare,
           "matricola": matricola,
           "stato": "assegnato",
           "data assegnazione": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
           "voto": None
        }
    }

    return matricola, task, nuovo_compito

def visualizza_compiti():
    """Visualizza i compiti degli sudenti"""
    dati = carica_database()

    compiti = dati["compiti"]

    if compiti:
        for task, compito in compiti.items():
            if task.startswith("TASK"):
                print(f"{task}:\n -Descrizione: {compito["descrizione"]}\n -Matricola: {compito["matricola"]}\n -Voto: {compito["voto"]}")

def assegna_voto():
    """Assegna il voto ad un task"""
    dati = carica_database()

    compiti = dati["compiti"]

    if compiti:
        for task, compito in compiti.items():
            if task.startswith("TASK"):
                print(f"{task}:\n -Descrizione: {compito["descrizione"]}\n -Matricola: {compito["matricola"]}\n -Voto: {compito["voto"]}")

    task = input("A quale compito vuoi assegnare la valutazione? (es.TASK001):")

    if task in compiti:
        compito = compiti[task]
        voto = int(input(f"Assegna un voto al compito (da 0 a 10):"))
        if  voto < 0 or voto > 10:
            print("Voto non valido.")
        else:
            compito["voto"] = voto

    compito["data modifica"] = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    compiti[task].update(compito)
    salva_alunni(dati)

def visualizza_statistiche():
   """Visualizza le statistiche di un alunno"""
   dati = carica_database()
   compiti = dati["compiti"]
   voti = []

   matricola = input("Di quale alunno vuoi visualizzare le statisitiche? (es.MAT001):")

   conto_compiti_assegnati = 0 
   conto_compiti_completati = 0
   for task_id, task_data in compiti.items():
       if task_data["matricola"] == matricola:
           data_assegnazione = task_data["data assegnazione"]
           voto = task_data["voto"]
           voti.append(voto)
           conto_compiti_assegnati += 1
       
   for task_id, task_data in compiti.items():
       if task_data["matricola"] == matricola:
           voto = task_data["voto"]
           if voto == None:
               continue
           else:
               conto_compiti_completati += 1
           
   voti_validi = [voto for voto in voti if voto is not None]
   if voti_validi:
    media = sum(voti_validi) / len(voti_validi)
   else: 
       print("Nessun voto valido trovato pre la media.")

   print(f"Statische per matricola {matricola}:")
   print(f"Media: {media}")
   print(f"Compiti assegnati: {conto_compiti_assegnati}")
   print(f"Compiti completati: {conto_compiti_completati}")
   print(f"Voto massimo matricola {matricola}: {max(voti_validi)}")
   print(f"Voto minimo matricola {matricola}: {min(voti_validi)}")


if not os.path.exists("lista_alunni.json"):
    matricola_iniziale = crea_matricola()
    task_iniziale = crea_task()
    timestamp_iniziale = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    database = {
     "alunni": {
         matricola_iniziale: {
             "nome": "Matteo",
             "cognome": "Braida",
             "email": "braida.matteo@its.com",
             "matricola": matricola_iniziale,
             "data creazione": timestamp_iniziale,
             "data modifica": timestamp_iniziale
         },
     },
     "compiti":{}
    }
  
    crea_alunni(database)
    print(f"File 'lista_alunni.json' creato con alunno iniziale {matricola_iniziale}")
else:
    alunni_esistenti = carica_database()
    alunni = alunni_esistenti["alunni"]
    compiti = alunni_esistenti["compiti"]


    matricole = [int(key.replace("MAT","")) for key in alunni.keys() if key.startswith("MAT")]
    if matricole:
        contatore_matricola = max(matricole)

    tasks = [int(key.replace("TASK","")) for key in compiti.keys() if key.startswith("TASK")]
    if tasks:
        contatore_task = max(tasks)

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
        matricola, nuovo_alunno = aggiungi_alunno()
        dati = carica_database()
        dati["alunni"].update(nuovo_alunno["alunni"])
        dati["compiti"].update(nuovo_alunno["compiti"])
        salva_alunni(dati)
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

    if scelta_menu == 'e':
        print("\n")
        box_testo("ASSEGNA COMPITO A STUDENTE")
        matricola, task, nuovo_compito = assegna_compito()
        dati = carica_database()
        dati["compiti"].update(nuovo_compito)
        salva_alunni(dati)
        print(f"Compito assegnato con successo a {matricola}")

    if scelta_menu == 'f':
        print("\n")
        box_testo("REGISTRA VALUTAZIONE")
        assegna_voto()

    if scelta_menu == 'g':
        print("\n")
        box_testo("VISUALIZZA COMPITI DI UNO STUDENTE")
        visualizza_compiti()

    if scelta_menu == 'h':
        print("\n")
        box_testo("VISUALIZZA STATISTICHE ALUNNO")
        visualizza_statistiche()