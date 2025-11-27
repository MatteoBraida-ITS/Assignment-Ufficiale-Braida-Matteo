database = {
    "alunni": {
        "MAT001": {
            "nome": "Matteo",
            "cognome": "Braida",
            "email": "braida.matteo@its.com",
            "matricola": "MAT001",
            "data creazione": "",
            "data modifica": ""
        },

        "TASK001": {
            "id": "TASK001",
            "descrizione": "esercizio python",
            "alunno_matricola": "MAT001",
            "stato": "assegnato",
            "data assegnazione": "",
            "voto": 8
        }
    },
}

database_nuovo = {
    "alunni": {
        "MAT002": {
            "nome": "Matteo",
            "cognome": "Braida",
            "email": "braida.matteo@its.com",
            "matricola": "MAT002",
            "data creazione": "",
            "data modifica": ""
        },

        "TASK002": {
            "id": "TASK002",
            "descrizione": "esercizio python",
            "alunno_matricola": "MAT002",
            "stato": "assegnato",
            "data assegnazione": "",
            "voto": 8
        }
    },
}

database["alunni"].update(database_nuovo["alunni"])

print(database)