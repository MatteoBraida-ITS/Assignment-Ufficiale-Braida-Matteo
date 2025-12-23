import json
from datetime import datetime, timedelta
import os
import re
import csv

contatore_matricola = 0
contatore_task = 0
cartella = 'backup_dati_alunni'
cartella_csv = 'backup_dati_csv'

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

def sincronizza_contatori(dati):
    """Aggiorna i contatori globali basandosi sui dati caricati"""
    global contatore_matricola, contatore_task
    
    alunni = dati.get("alunni", {})
    compiti = dati.get("compiti", {})

    matricole = [int(k[3:]) for k in alunni.keys() if k.startswith("MAT") and k[3:].isdigit()]
    if matricole:
        contatore_matricola = max(matricole)
    else:
        contatore_matricola = 0

    tasks = [int(k[4:]) for k in compiti.keys() if k.startswith("TASK") and k[4:].isdigit()]
    if tasks:
        contatore_task = max(tasks)
    else:
        contatore_task = 0

def carica_database():
    """Carica la lista degli alunni del file JSON, se esiste"""
    if not os.path.exists("lista_alunni.json"):
        return{"alunni": {}, "compiti": {}}
    
    try:
        with open("lista_alunni.json", "r", encoding="utf-8") as file:
            dati = json.load(file)
            if "alunni" not in dati: dati["alunni"] = {}
            if "compiti" not in dati: dati["compiti"] = {}
            return dati
    except (json.JSONDecodeError, IOError):
        print("\n Errore nel caricamento del database. File corrotto o illegibile.")
        return {"alunni": {}, "compiti": {}}
    
    
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
    alunni = dati.get("alunni", {})

    if alunni:
        for matricola, alunno in alunni.items():
            if matricola.startswith("MAT"):
                print(f"\n{matricola}:\n -Nome:{alunno['nome']}\n -Cognome:{alunno['cognome']}\n -E-mail:{alunno['email']}")
    else:
        print("\nNessun alunno presente.")

def valida_email(email: str) -> bool:
    """Valida un indirizzo email"""

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False

def email_esistente(email:str, dati: dict, matricola_da_escludere: str = None) -> bool:
    """Controlla se l'email è già in uso da un altro alunno"""

    alunni = dati.get("alunni", {})

    for matricola, alunno in alunni.items():
        if matricola_da_escludere and matricola == matricola_da_escludere:
            continue

        if alunno.get("email", "").lower() == email.lower():
            return True
        
    return False

def richiesta_email_valida(dati: dict, matricola_da_escludere: str = None) -> str:
    """Richiede una email all'utente fino a che questa non è considerata valida"""

    while True:
        email = input("\ninserisci la e-mail: ").strip()

        if not email:
            print("\n❌ Errore: L'email non può essere vuota.")
            continue
        
        if not valida_email(email):
            print("\n❌ Errore: L'email inserita non è valida.")
            print("   Formato corretto: esempio@dominio.com")
            continue
        
        if email_esistente(email, dati, matricola_da_escludere):
            print("\n❌ Errore: Questa email è già utilizzata da un altro alunno.")
            continue
        
        return email

def aggiungi_alunno():
    """Acquisisce i dati di un nuovo alunno""" 
    dati = carica_database()

    if "alunni" not in dati:
        dati["alunni"] = {}
    if "compiti" not in dati:
        dati["compiti"] = {}

    matricola = crea_matricola()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    while True:
        nome = input("\nInserisci il nome del nuovo alunno:").strip()
        if nome:
            break
        print("\n❌ Non puoi lasciare il campo vuoto.")
    
    while True:
        cognome = input("\nInserisci il cognome del nuovo alunno:").strip()
        if cognome:
            break
        print("\n❌ Non puoi lasciare il campo vuoto.")

    print("\n")
    email = richiesta_email_valida(dati)

    dati["alunni"][matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "matricola": matricola,
        "data creazione": timestamp,
        "data modifica": timestamp
    }

    salva_alunni(dati)
    print(f"\n✅ Alunno registrato con successo!")

def modifica_dati_alunno():
    """Modica i dati degli studenti contenuti nel file JSON"""
    dati = carica_database()
    
    if not dati or "alunni" not in dati or not dati["alunni"]:
        print("\nNessun alunno presente nel database")
        return
    
    alunni = dati["alunni"]

    matricola = input("\nSeleziona l'alunno di qui vuoi modificare i dati digitando la sua matricola (es.MAT001): ").strip().upper()

    if matricola in alunni:    
        alunno = alunni[matricola]
        print(f"\nDati attuali di {alunno['nome']} {alunno['cognome']}")
        print(f"\n1) Nome: {alunno['nome']}")
        print(f"\n2) Cognome: {alunno['cognome']}")
        print(f"\n3) E-mail: {alunno['email']}")

        campo = input(f"\nQuale dato dell'alunno {alunno['nome']} {alunno['cognome']} vuoi modificare? (1-3): ").strip()

        modificato = True

        if campo == '1':
            alunno['nome'] = input("\nInserisci il nuovo nome: ").strip()
            if not alunno['nome']:
                print("\n❌ Il nome non può essere vuoto.")
                modificato = False
            else:
                print(f"\n✅ Nome cambiato con {alunno['nome']}!")
        elif campo == '2':
            alunno['cognome'] = input("\nInserisci il nuovo cognome: ").strip()
            if not alunno['cognome']:
                print("\n❌ Il cognome non può essere vuoto.")
                modificato = False
            else:
                print(f"\n✅ Cognome cambiato con {alunno['cognome']}!")
        elif campo == '3':
            nuova_email = richiesta_email_valida(dati, matricola)
            alunno['email'] = nuova_email
            print(f"\n✅ E-mail cambiata con {nuova_email}!")
        else:
            print("\n❌ Errore: Dato non presente nel registro.")
            modificato = False
        if modificato:
            alunno['data modifica'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salva_alunni(dati)
            print("\n✅ Dati aggiornati!")
    else:
        print("\n❌ Errore: Matricola non presente nel database.")

def elimina_alunno():
    """Elimina i dati relativi all'alunno selezionato"""
    dati = carica_database()

    if not dati:
          print("\n❌ Nessun alunno presente nel database")
          return
    
    alunni = dati["alunni"]
    compiti = dati["compiti"]
    
    matricola = input("\nSeleziona l'alunno di qui vuoi eliminare i dati digitando la sua matricola (es.MAT001): ").strip().upper()

    if matricola not in alunni:
          print("\n❌ La matricola digitata non corrisponde a nessun alunno presente nel database.")
          return

    alunno = alunni[matricola]
    print(f"\n⚠️ L'alunno selezionato è {alunno['nome']} {alunno['cognome']}.")

    compiti_associati = sum(1 for task_data in compiti.values() if  task_data["matricola"] == matricola)
    if compiti_associati > 0:
        print(f"\n⚠️  ATTENZIONE: Questo alunno ha {compiti_associati} compiti associati che verranno eliminati!")

    conferma = input(f"\n⚠️ Sei sicuro di voler eliminare i dati di {alunno['nome']} {alunno['cognome']}? (y/n): ").strip().lower()

    if conferma == 'y':
        alunni.pop(matricola)

        task_da_eliminare = []

        for task_id, task_data in compiti.items():
            if task_data["matricola"] == matricola:
                task_da_eliminare.append(task_id)
    
        for task_id in task_da_eliminare:
            compiti.pop(task_id)

        print(f"\n✅ L'alunno {alunno['nome']} {alunno['cognome']} con matricola {matricola} è stato rimosso dal database.")
        if task_da_eliminare:
            print(f"\n✅ {len(task_da_eliminare)} compiti associati sono stati eliminati.")
            salva_alunni(dati)
    elif conferma == 'n':
        print("\n⚠️ Operazione annullata.")
        return
    else:
        print("\n❌ Comando non valido.")
        return

def assegna_compito():
    """Assegna un compito ad un alunno"""
    dati = carica_database()

    if not dati or not dati.get("alunni"):
        print("\n❌ Nessun alunno presente nel database")
        return

    matricola = input("\nSeleziona l'alunno a cui assegnare il compito digitando la sua matricola (es.MAT001):").strip().upper()

    if matricola not in dati["alunni"]:
        print("\n❌ Errore: Matricola non presente nel database.")
        return

    alunno = dati["alunni"][matricola]
    print(f"\n✅ Alunno selezionato: {alunno['nome']} {alunno['cognome']}")

    while True:
        compito_da_assegnare = input(f"Quale compito vuoi assegnare?: ").strip()
        if compito_da_assegnare:
            break
        print("\n❌ Errore: La descrizione del compito non può essere vuota.")

    task = crea_task()

    nuovo_compito = {
        task: {
           "id": task,
           "descrizione": compito_da_assegnare,
           "matricola": matricola,
           "stato": "assegnato",
           "data assegnazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "voto": None
        }
    }

    dati["compiti"].update(nuovo_compito)
    salva_alunni(dati)
    print(f"\n✅ Compito assegnato con successo a {matricola}")

def visualizza_compiti():
    """Visualizza i compiti di uno studente"""
    dati = carica_database()

    if not dati or not dati.get("compiti"):
        print("\nNessun compito presente nel database.")
        return
    
    if not dati.get("alunni"):
        print("\nNessun alunno presente nel database.")

    compiti = dati["compiti"]
    alunni = dati["alunni"]

    matricola = input("\nDi quale studente vuoi visualizzare i compiti? (es.MAT001): ").strip().upper()

    if matricola not in alunni:
        print(f"\n❌ Errore: La matricola {matricola} non esiste nel database.")
        return
    
    alunno = alunni[matricola]
    print(f"\n📚 Compiti di {alunno['nome']} {alunno['cognome']} ({matricola}):\n")

    compiti_studente = { task_id: task_data for task_id, task_data in compiti.items()
                        if task_data["matricola"] == matricola }
    
    if not compiti_studente:
        print("\n⚠️ Nessun compito assegnato a questo studente.")
        return
    
    for task, compito in compiti_studente.items():
        stato_emoji = "✅" if compito["voto"] is not None else "⏳"
        voto_str = compito["voto"] if compito["voto"] is not None else "Non valutato"
        print(f"{stato_emoji} {task}")
        print(f"  -Descrizione: {compito['descrizione']}")
        print(f"  -Stato: {compito['stato']}")
        print(f"  -Voto: {voto_str}")
        print(f"  -Data assegnazione: {compito['data assegnazione']}\n")


def assegna_voto():
    """Assegna il voto ad un task"""
    dati = carica_database()

    if not dati or not dati.get("compiti"):
         print("\n❌ Nessun compito presente nel database.")
         return

    compiti = dati["compiti"]

    print("\n📝 Compiti disponibili:\n")
    for task, compito in compiti.items():
        voto_str = compito["voto"] if compito["voto"] is not None else "Non valutato"
        stato_emoji = "✅" if compito["voto"] is not None else "⏳"
        print(f"{stato_emoji} {task}:")
        print(f"   Descrizione: {compito['descrizione']}")
        print(f"   Matricola: {compito['matricola']}")
        print(f"   Voto: {voto_str}\n")

    task = input("A quale compito vuoi assegnare la valutazione? (es.TASK001):").strip().upper()

    if task not in compiti:
        print("\nErrore: il compito selezionato non esiste.")
        return
    
    compito = compiti[task]

    if compito["voto"] is not None:
        conferma = input(f"\n⚠️  Questo compito ha già un voto ({compito['voto']}). Vuoi sovrascriverlo? (y/n): ").strip().lower()
        if conferma == 'y':
            pass
        elif conferma == 'n':
            print("\n⚠️ Operazione annullata.")
            return

    while True:
        try:

            voto_input = input(f"\nAssegna un voto al compito (da 0 a 10):").strip()

            if not voto_input:
                print("\n❌ Errore: Il voto non può essere vuoto.")
                continue

            voto = float(voto_input.replace(',', '.'))

            if voto < 0 or voto > 10:
                print("\n❌ Voto non valido. Deve essere tra 0 e 10.")
                continue
            
            compito["voto"] = voto
            compito["stato"] = "registrato"
            compito["data valutazione"] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salva_alunni(dati)
            print(f"\n✅ Voto {voto} assegnato con successo al compito {task}!")
            break
        except ValueError:
            print("\n❌ Errore: Inserisci un numero valido.")
            continue

    salva_alunni(dati)

def visualizza_statistiche():
    """Visualizza le statistiche di un alunno"""
    dati = carica_database()

    if not dati or not dati.get("compiti"):
       print("\n❌ Nessun compito presente nel database.")
       return     
 
    compiti = dati["compiti"]
    voti = []
 
    matricola = input("Di quale alunno vuoi visualizzare le statisitiche? (es.MAT001):").strip().upper()

    if matricola not in dati.get("alunni", {}):
        print("\n❌ Errore: Matricola non presente nel database.")
        return
 
    conto_compiti_assegnati = 0 
    conto_compiti_completati = 0

    for task_id, task_data in compiti.items():
        if task_data["matricola"] == matricola:
            voto = task_data["voto"]
            voti.append(voto)
            conto_compiti_assegnati += 1
            if voto is not None:
                conto_compiti_completati += 1

    voti_validi = [voto for voto in voti if voto is not None]

    if not voti_validi:
       print(f"\n⚠️  Nessun voto valido trovato per la matricola {matricola}.")
       print(f"Compiti assegnati: {conto_compiti_assegnati}")
       print(f"Compiti completati: {conto_compiti_completati}")
       return
    
    media = sum(voti_validi) / len(voti_validi)
        
    print(f"\n📊 Statische per matricola {matricola}:")
    print(f"\n📈 Media: {media:.2f}")
    print(f"📚 Compiti assegnati: {conto_compiti_assegnati}")
    print(f"✅ Compiti completati: {conto_compiti_completati}")
    print(f"⏳ Compiti in attesa: {conto_compiti_assegnati - conto_compiti_completati}")
    print(f"🏆 Voto massimo: {max(voti_validi)}")
    print(f"📉 Voto minimo: {min(voti_validi)}")

    print(f"\n📈 Progressione voti nel tempo:") 
    for task_id, task_data in compiti.items():
        if task_data["matricola"] == matricola and task_data["voto"] is not None:
            esercizio = task_data["descrizione"]
            voto = task_data["voto"]
            data_voto = task_data.get("data valutazione", task_data["data assegnazione"])
            print(f"  • {esercizio}: {voto} - conseguito in data {data_voto}")

def ranking_alunni():
    """Ritorna le media dei voti di ogni alunno presente nel database in ordine, dalla più alta alla più bassa."""
    dati = carica_database()

    if not dati or not dati.get("compiti"):
        print("\n❌ Nessun compito presente nel database.")
        return
    
    compiti = dati["compiti"]
    alunni = dati.get("alunni", {})
    voti_per_alunno = {}
    medie = {}

    for task_id, task_data in compiti.items():
        alunno = task_data.get("matricola")
        voto = task_data.get("voto")

        if alunno is None or voto is None:
            continue

        if alunno not in voti_per_alunno:
            voti_per_alunno[alunno] = []

        voti_per_alunno[alunno].append(voto)

    for alunno, voti in voti_per_alunno.items():
        voti_validi = [v for v in voti if v is not None]
        if voti_validi:
            media = sum(voti_validi) / len(voti_validi)
            medie[alunno] = media

    if not medie:
        print("\n❌ Nessun voto disponibile per creare un ranking.")
        return

    ranking_medie = sorted(
        medie.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("\n🏆 Ranking alunni per media voti:\n")
    for posizione, (matricola, media) in enumerate(ranking_medie, 1):
        nome_completo = "Sconosciuto"
        if matricola in alunni:
            alunno = alunni[matricola]
            nome_completo = f"{alunno['nome']} {alunno['cognome']}"

            medaglia = ""
            if posizione == 1:
                medaglia = "🥇"
            elif posizione == 2:
                medaglia = "🥈"
            elif posizione == 3:
                medaglia = "🥉"
            else:
                medaglia = f"{posizione}."

        print(f"{medaglia} {nome_completo} ({matricola}) - Media: {media:.2f}")

def report_compiti():
    """Riporta a terminale i compiti assegnati ma a cui non è ancora stato assegnato un voto."""
    dati = carica_database()

    if not dati or not dati.get("compiti"):
        print("\n❌ Nessun compito presente nel database.")
        return    

    compiti = dati.get("compiti", {})

    compiti_non_completati = {task_id: task_data for task_id, task_data in compiti.items() 
                               if task_data["voto"] is None}
    
    if not compiti_non_completati:
        print("\n✅ Tutti i compiti sono stati completati!")
        return
    
    print("\n⏳ Compiti non completati:\n")
    for task_id, task_data in compiti_non_completati.items():
        print(f"  • {task_id} - {task_data['descrizione']}")
        print(f"    Assegnato a: {task_data['matricola']}")
        print(f"    Data assegnazione: {task_data['data assegnazione']}\n")

def ricerca_studente():
    """Ricerca veloce studenti per nome, cognome, email o matricola."""
    dati = carica_database()
    alunni = dati.get("alunni", {})
    
    if not alunni:
        print("\n❌ Nessun alunno presente nel database.")
        return
    
    print("\n🔍 Ricerca studente")
    print("="*70)
    termine = input("Inserisci nome, cognome, email o matricola (anche parziale): ").strip().lower()
    
    if not termine:
        print("❌ Errore: Inserisci un termine di ricerca.")
        return
    
    risultati = []
    
    for matricola, alunno in alunni.items():
        if (termine in alunno['nome'].lower() or 
            termine in alunno['cognome'].lower() or 
            termine in alunno['email'].lower() or 
            termine in matricola.lower()):
            risultati.append((matricola, alunno))
    
    if not risultati:
        print(f"\n⚠️  Nessun risultato trovato per '{termine}'")
        return
    
    print(f"\n✅ Trovati {len(risultati)} risultato/i:\n")
    print("="*70)
    
    for matricola, alunno in risultati:
        print(f"\n🎓 {matricola}")
        print(f"   Nome completo: {alunno['nome']} {alunno['cognome']}")
        print(f"   Email: {alunno['email']}")
        print(f"   Data iscrizione: {alunno.get('data creazione', 'N/A')}")
        
        compiti = dati.get("compiti", {})
        compiti_studente = [c for c in compiti.values() if c['matricola'] == matricola]
        if compiti_studente:
            voti = [c['voto'] for c in compiti_studente if c['voto'] is not None]
            print(f"   📚 Compiti: {len(compiti_studente)} (completati: {len(voti)})")
            if voti:
                media = sum(voti) / len(voti)
                print(f"   📊 Media voti: {media:.2f}")

def backup_dati_alunni():
    """Crea un backup del file JSON dentro una cartella 'backup'"""
    dati = carica_database()

    if not dati:
        print("\n❌ Nessun dato da salvare.")
        return

    if not os.path.exists(cartella):
        os.makedirs(cartella)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_file = f"backup_dati_alunni_{timestamp}.json"
    percorso_file = os.path.join(cartella, nome_file)
    with open(percorso_file, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)
    print(f"\n✅ Backup creato con successo in 📁 percorso: {percorso_file}")

def carica_dati_backup():
    """Carica i dati da un backup"""
    if not os.path.exists(cartella):
        print("\n❌ Nessun backup presente.")
        return
    
    backup_files = [f for f in os.listdir(cartella) if f.endswith(".json")]
    if not backup_files:
        print("\n❌ Nessun backup presente.")
        return

    print("\n📁 Backup disponibili:")
    for i, file in enumerate(backup_files, 1):
        print(f"{i}. {file}")

    try:
        scelta = int(input("\nQuale backup vuoi caricare? (numero): ")) - 1
        if scelta < 0 or scelta >= len(backup_files):
            print("\n❌ Scelta non valida")
            return
        
        file_selezionato = backup_files[scelta]
        percorso_file = os.path.join(cartella, file_selezionato)

        print(f"\n⚠️  ATTENZIONE: Questa operazione sovrascriverà i dati attuali!")
        conferma = input("\nSei sicuro di voler continuare? (y/n): ").strip().lower()

        if conferma == 'y':
            pass
        else:
            print("\n⚠️ Operazione annullata.")
            return

        with open(percorso_file, "r", encoding="utf-8") as file:
            dati = json.load(file)
            salva_alunni(dati)
            print(f"\n✅ Dati caricati con successo da {file_selezionato}")
    except ValueError:
        print("\n❌ Errore: inserisci un numero valido.")
    except Exception as e:
        print(f"\n❌ Errore durante il caricamento: {e}")

def esportazione_dati_csv():
    """Esporta tutto il database in un UNICO file CSV."""
    try:
        dati = carica_database()
        
        if not dati:
            print("\n❌ Nessun dato da esportare.")
            return
        
        if not os.path.exists(cartella_csv):
            os.makedirs(cartella_csv)
        
        alunni = dati.get("alunni", {})
        compiti = dati.get("compiti", {})
        
        if not alunni:
            print("\n❌ Nessun alunno da esportare.")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_file = f"database_completo_{timestamp}.csv"
        percorso_file = os.path.join(cartella_csv, nome_file)
        with open(percorso_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Nome', 'Cognome', 'Email', 'Matricola', 'Descrizione_Compito', 
                         'ID_Compito', 'Stato', 'Voto', 'Data_Assegnazione']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            righe_scritte = 0
            
            for matricola, alunno in alunni.items():
                compiti_alunno = {tid: tdata for tid, tdata in compiti.items() 
                                 if tdata['matricola'] == matricola}
                
                if compiti_alunno:
                    for task_id, compito in compiti_alunno.items():
                        writer.writerow({
                            'Nome': alunno['nome'],
                            'Cognome': alunno['cognome'],
                            'Email': alunno['email'],
                            'Matricola': matricola,
                            'Descrizione_Compito': compito['descrizione'],
                            'ID_Compito': task_id,
                            'Stato': compito['stato'],
                            'Voto': compito.get('voto', ''),
                            'Data_Assegnazione': compito['data assegnazione']
                        })
                        righe_scritte += 1
                else:
                    writer.writerow({
                        'Nome': alunno['nome'],
                        'Cognome': alunno['cognome'],
                        'Email': alunno['email'],
                        'Matricola': matricola,
                        'Descrizione_Compito': '',
                        'ID_Compito': '',
                        'Stato': '',
                        'Voto': '',
                        'Data_Assegnazione': ''
                    })
                    righe_scritte += 1
        
        print(f"\n✅ Database esportato con successo in {percorso_file}!")
        print(f"📁 File: {nome_file}")
        print(f"📊 Statistiche:")
        print(f"   Alunni: {len(alunni)}")
        print(f"   Compiti: {len(compiti)}")
        print(f"   Righe totali: {righe_scritte}")
        
        dimensione = os.path.getsize(percorso_file)
        print(f"💾 Dimensione: {dimensione:,} bytes")
        
    except Exception as e:
        print(f"❌ Errore durante l'esportazione: {e}")

def importazione_dati_csv():
    """Importa alunni e compiti da file CSV con validazione e prevenzione duplicati."""
    if not os.path.exists(cartella_csv):
        print("\n❌ Cartella backup CSV non trovata.")
        return 
    
    backup_files = [f for f in os.listdir(cartella_csv) if f.endswith(".csv")]
    if not backup_files:
        print("\n❌ Nessun file CSV presente nella cartella di backup.")
        return

    print("\n📁 Backup disponibili:")
    for i, file in enumerate(backup_files, 1):
        print(f"{i}. {file}")

    try:
        scelta_input = input("\nQuale backup vuoi caricare? (numero): ").strip()
        if not scelta_input.isdigit() or int(scelta_input) < 1 or int(scelta_input) > len(backup_files):
            print("\n❌ Scelta non valida.")
            return
        
        file_selezionato = backup_files[int(scelta_input) - 1]
        percorso_file = os.path.join(cartella_csv, file_selezionato)

        dati = carica_database()
        if not dati:
            dati = {"alunni": {}, "compiti": {}}

        alunni_importati = 0
        compiti_importati = 0
        righe_saltate = 0
        
        # Cache locale per gestire duplicati all'interno dello stesso CSV
        alunni_elaborati = {}  
        
        with open(percorso_file, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # --- VALIDAZIONE COLONNE ---
            # Verifichiamo che le colonne minime necessarie esistano
            colonne_presenti = set(reader.fieldnames) if reader.fieldnames else set()
            colonne_minime = {'Nome', 'Cognome', 'Email', 'Descrizione_Compito'}
            
            if not colonne_minime.issubset(colonne_presenti):
                print(f"\n❌ Errore: Il file CSV non ha le colonne corrette.")
                print(f"Mancano: {colonne_minime - colonne_presenti}")
                return

            print(f"\n📥 Inizio importazione da {file_selezionato}...")
            print("="*70)
            
            for num_riga, row in enumerate(reader, start=2):
                nome = row.get('Nome', '').strip()
                cognome = row.get('Cognome', '').strip()
                email = row.get('Email', '').strip()
                descrizione_compito = row.get('Descrizione_Compito', '').strip()
                voto_str = row.get('Voto', '').strip()
                
                # Validazione dati minimi riga
                if not nome or not cognome or not email:
                    righe_saltate += 1
                    continue
                
                if not valida_email(email):
                    print(f"⚠️  Riga {num_riga} saltata: email non valida ({email})")
                    righe_saltate += 1
                    continue

                # --- GESTIONE ALUNNO (Case-Insensitive) ---
                email_lower = email.lower()
                matricola = None
                
                # 1. Cerca nella cache del ciclo corrente
                if email_lower in alunni_elaborati:
                    matricola = alunni_elaborati[email_lower]
                
                # 2. Cerca nel database esistente
                else:
                    for mat, alunno in dati["alunni"].items():
                        if alunno["email"].lower() == email_lower:
                            matricola = mat
                            alunni_elaborati[email_lower] = matricola
                            break
                
                # 3. Se non trovato, crea nuovo alunno
                if not matricola:
                    matricola = crea_matricola()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    dati["alunni"][matricola] = {
                        "nome": nome,
                        "cognome": cognome,
                        "email": email,
                        "matricola": matricola,
                        "data creazione": timestamp,
                        "data modifica": timestamp
                    }
                    
                    alunni_elaborati[email_lower] = matricola
                    alunni_importati += 1
                    print(f"✅ Nuovo alunno: {nome} {cognome} ({matricola})")
                
                # --- GESTIONE COMPITO (Evita Duplicati) ---
                if descrizione_compito:
                    # Controllo se l'alunno ha già un compito identico
                    gia_presente = any(
                        t["matricola"] == matricola and 
                        t["descrizione"].lower() == descrizione_compito.lower()
                        for t in dati["compiti"].values()
                    )
                    
                    if gia_presente:
                        continue

                    # Elaborazione voto e stato
                    voto = None
                    stato = "assegnato"
                    data_val = None
                    
                    if voto_str:
                        try:
                            v_float = float(voto_str.replace(',', '.'))
                            if 0 <= v_float <= 10:
                                voto = v_float
                                stato = "registrato"
                                data_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
                    
                    task_id = crea_task()
                    dati["compiti"][task_id] = {
                        "id": task_id,
                        "descrizione": descrizione_compito,
                        "matricola": matricola,
                        "stato": stato,
                        "data assegnazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "voto": voto
                    }
                    if data_val:
                        dati["compiti"][task_id]["data valutazione"] = data_val
                    
                    compiti_importati += 1
        
        # Salvataggio finale e sincronizzazione
        if alunni_importati > 0 or compiti_importati > 0:
            salva_alunni(dati)
            sincronizza_contatori(dati)
            print(f"\n{'='*70}")
            print(f"✅ IMPORTAZIONE COMPLETATA!")
            print(f"👥 Nuovi alunni: {alunni_importati}")
            print(f"📚 Nuovi compiti: {compiti_importati}")
            print(f"⚠️  Righe saltate/invalide: {righe_saltate}")
            print(f"{'='*70}")
        else:
            print("\nℹ️ Nessun nuovo dato importato (dati già presenti nel database).")
            
    except Exception as e:
        print(f"❌ Errore durante l'importazione: {e}")

def menu():
    """Menù principale con loop"""

    while True:

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
     print("     P)Ricerca veloce studente")
     print("     Q)Esportazione dati in CSV")
     print("     R)Importa dati da file CSV")
     print("     Z)Esci")
     
     scelta_menu = input("\n➤ Seleziona l'opzione: ").strip().lower()
 
     if scelta_menu == 'a':
         print("\n")
         box_testo("INSERISCI NUOVO ALUNNO")
         aggiungi_alunno()
 
     elif scelta_menu == 'b':
         print("\n")
         box_testo("VISUALIZZA ALUNNI REGISTRATI")
         visualizza_alunni()
 
     elif scelta_menu == 'c':
         print("\n")
         box_testo("MODIFICA DATI ALUNNO")
         modifica_dati_alunno()
 
     elif scelta_menu == 'd':
         print("\n")
         box_testo("ELIMINA DATI ALUNNO")
         elimina_alunno()
 
     elif scelta_menu == 'e':
         print("\n")
         box_testo("ASSEGNA COMPITO A STUDENTE")
         assegna_compito()
 
     elif scelta_menu == 'f':
         print("\n")
         box_testo("REGISTRA VALUTAZIONE")
         assegna_voto()
 
     elif scelta_menu == 'g':
         print("\n")
         box_testo("VISUALIZZA COMPITI DI UNO STUDENTE")
         visualizza_compiti()
 
     elif scelta_menu == 'h':
         print("\n")
         box_testo("VISUALIZZA STATISTICHE ALUNNO")
         visualizza_statistiche()
 
     elif scelta_menu == 'i':
         print("\n")
         box_testo("RANKING ALUNNI PER MEDIA VOTI")
         ranking_alunni()
 
     elif scelta_menu == 'l':
         print("\n")
         box_testo("REPORT COMPITI NON COMPLETATI")
         report_compiti()
     
     elif scelta_menu == 'm':
         print("\n")
         box_testo("SALVA DATI (BACKUP)")
         backup_dati_alunni()
 
     elif scelta_menu == 'n':
         print("\n")
         box_testo("CARICA DATI (BACKUP)")
         carica_dati_backup()
 
     elif scelta_menu == 'o':
         continue
     
     elif scelta_menu == 'p':
         print("\n")
         box_testo("RICERCA VELOCE STUDENTE")
         ricerca_studente()

     elif scelta_menu == 'q':
         print("\n")
         box_testo("ESPORTAZIONE DATI IN CSV")
         esportazione_dati_csv()
    
     elif scelta_menu == 'r':
         print("\n")
         box_testo("IMPORTAZIONE DATI DA FILE CSV")
         importazione_dati_csv()
     
     elif scelta_menu == 'z':
         print("\n")
         conferma = input ("Sei sicuro di voler uscire? (y/n):").strip().lower()
         if conferma == 'y':
             print("\n 👋 Grazie per aver utilizzato il sistema di tracciamento alunni!")
             print("      Arrivederci!\n")
             break
         else:
             print("\n⚠️ Operazione annullata.")
             continue
    
     else:
         print("\n❌ Opzione non presente nel menù. Riprova.")

     input("\n[Premi INVIO per continuare...]")

if __name__ == "__main__":

    dati = carica_database()

    sincronizza_contatori(dati)
    
    if not dati["alunni"]:
        dati = {"alunni": {}, "compiti": {}}
        salva_alunni(dati)
    
    menu()