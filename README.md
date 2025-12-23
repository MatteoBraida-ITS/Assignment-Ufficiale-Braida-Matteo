# 📚 Sistema di Tracciamento Alunni ITS

Un sistema completo per la gestione degli studenti e dei compiti, progettato per gli Istituti Tecnici Superiori (ITS). Il programma offre funzionalità avanzate per registrare studenti, assegnare compiti, gestire valutazioni e generare statistiche dettagliate.

## ✨ Caratteristiche Principali

- **Gestione Studenti**: Registrazione completa con nome, cognome, email e matricola univoca
- **Sistema di Compiti**: Assegnazione, tracciamento e valutazione dei compiti
- **Validazione Email**: Controllo formato e univocità delle email
- **Statistiche Avanzate**: Medie voti, ranking studenti, report compiti
- **Backup e Restore**: Salvataggio automatico con timestamp
- **Import/Export CSV**: Compatibilità con Excel e fogli di calcolo
- **Ricerca Veloce**: Trova rapidamente studenti per nome, cognome o email
- **Persistenza Dati**: Salvataggio automatico in formato JSON

## 🚀 Requisiti

- Python 3.6 o superiore
- Nessuna dipendenza esterna (utilizza solo librerie standard)

## 📦 Installazione

1. Clona il repository:
```bash
git clone https://github.com/tuo-username/sistema-alunni-its.git
cd sistema-alunni-its
```

2. Esegui il programma:
```bash
python Sistema_alunni_ITS.py
```

## 💻 Utilizzo

Al primo avvio, il programma creerà automaticamente il database `lista_alunni.json`. Il menu principale offre le seguenti opzioni:

### Menu Principale

```
╔═════════════════════════════════════╗
║ SISTEMA TRACCIAMENTO ALUNNI         ║
╚═════════════════════════════════════╝
A) Inserisci nuovo alunno
B) Visualizza alunni registrati
C) Modifica dati alunno
D) Elimina alunno
E) Assegna compito a studente
F) Registra valutazione
G) Visualizza compiti di uno studente
H) Visualizza statistiche alunno
I) Ranking alunni per media voti
L) Report compiti non completati
M) Salva dati (backup)
N) Carica dati
O) Visualizza menù
P) Ricerca veloce studente
Q) Esportazione dati in CSV
R) Importa dati da file CSV
Z) Esci
```

### Esempi d'uso

#### Aggiungere un nuovo studente
```
➤ Seleziona l'opzione: a

Inserisci il nome del nuovo alunno: Mario
Inserisci il cognome del nuovo alunno: Rossi
Inserisci la e-mail: mario.rossi@example.com

✅ Alunno registrato con successo!
```

#### Assegnare un compito
```
➤ Seleziona l'opzione: e

Seleziona l'alunno digitando la matricola (es.MAT001): MAT001
Inserisci la descrizione del compito: Progetto Python - Sistema Gestionale

✅ Compito assegnato con successo!
```

#### Visualizzare statistiche
```
➤ Seleziona l'opzione: h

Inserisci la matricola dello studente: MAT001

STATISTICHE STUDENTE
Nome: Mario Rossi
Media voti: 8.5
Compiti completati: 12/15
Percentuale completamento: 80%
```

## 📁 Struttura dei File

```
sistema-alunni-its/
│
├── Sistema_alunni_ITS.py      # File principale del programma
├── lista_alunni.json           # Database principale (generato automaticamente)
├── backup_dati_alunni/         # Cartella backup (generata automaticamente)
└── backup_dati_csv/            # Cartella esportazioni CSV (generata automaticamente)
```

## 🗂️ Formato Dati

### Struttura JSON
```json
{
  "alunni": {
    "MAT001": {
      "nome": "Mario",
      "cognome": "Rossi",
      "email": "mario.rossi@example.com",
      "matricola": "MAT001",
      "data creazione": "2024-01-15 10:30:00",
      "data modifica": "2024-01-15 10:30:00"
    }
  },
  "compiti": {
    "TASK001": {
      "id": "TASK001",
      "descrizione": "Progetto Python",
      "matricola": "MAT001",
      "stato": "registrato",
      "data assegnazione": "2024-01-15 10:30:00",
      "data valutazione": "2024-01-20 14:00:00",
      "voto": 8.5
    }
  }
}
```

### Formato CSV per Import
Il file CSV deve avere le seguenti colonne:
```csv
Nome,Cognome,Email,Descrizione Compito,Voto
Mario,Rossi,mario.rossi@example.com,Progetto Python,8.5
Laura,Bianchi,laura.bianchi@example.com,Esercizi Java,9.0
```

**Note importanti:**
- L'intestazione è obbligatoria
- L'email deve essere valida e univoca
- Il voto è opzionale (range 0-10)
- Se l'alunno esiste già, viene associato al compito esistente

## 🔧 Funzionalità Dettagliate

### Gestione Studenti
- ✅ Aggiunta con validazione email
- ✅ Modifica dati (nome, cognome, email)
- ✅ Eliminazione con conferma
- ✅ Ricerca per nome, cognome o email
- ✅ Matricola univoca generata automaticamente (MAT001, MAT002, ...)

### Gestione Compiti
- ✅ Assegnazione a studente specifico
- ✅ Stati: assegnato, registrato
- ✅ Valutazione con voto (0-10)
- ✅ ID univoco generato automaticamente (TASK001, TASK002, ...)
- ✅ Timestamp di assegnazione e valutazione

### Report e Statistiche
- 📊 Media voti per studente
- 📈 Ranking studenti per performance
- 📋 Compiti non completati
- 🔍 Ricerca avanzata studenti
- 📊 Statistiche dettagliate individuali

### Backup e Persistenza
- 💾 Salvataggio automatico con timestamp
- 📂 Cartella backup organizzata per data
- ⚡ Ripristino dati da backup
- 🔄 Import/Export CSV per integrazioni esterne

## 🛡️ Sicurezza e Validazione

- **Validazione Email**: Controllo formato con regex
- **Unicità Email**: Prevenzione duplicati
- **Conferme Eliminazione**: Protezione da cancellazioni accidentali
- **Gestione Errori**: Try-catch per operazioni critiche
- **Campi Obbligatori**: Validazione input utente

## 🎨 Caratteristiche UX

- 🎨 Interfaccia ASCII con box decorati
- ✅ Messaggi di conferma colorati
- ❌ Messaggi di errore chiari
- ⚠️ Warning per operazioni critiche
- 📝 Prompt intuitivi

---

**Nota**: Alcune funzioni sono state implementate con aiuto da intelligenza artificiale, come l'importazione da file CSV e la validazione delle e-mail.