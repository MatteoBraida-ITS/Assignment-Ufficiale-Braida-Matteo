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
     },
     "compiti":{
         "TASK001": {
             "id": "TASK001",
             "descrizione": "esercizio python",
             "matricola": "MAT001",
             "stato": "assegnato",
             "data assegnazione": "",
             "voto": 8
         }
     }
}

database2 = {
     "alunni": {
         "MAT002": {
             "nome": "Matteo",
             "cognome": "Braida",
             "email": "braida.matteo@its.com",
             "matricola": "MAT002",
             "data creazione": "",
             "data modifica": ""
         },
     },
     "compiti":{
         "TASK002": {
             "id": "TASK002",
             "descrizione": "esercizio python",
             "matricola": "MAT002",
             "stato": "assegnato",
             "data assegnazione": "",
             "voto": 8
         }
     }
}

database["alunni"].update(database2["alunni"])
database["compiti"].update(database2["compiti"])

matricola = input("\nSeleziona l'alunno di qui vuoi eliminare i dati digitando la sua matricola (es.MAT001):")

alunni = database["alunni"]
compiti = database["compiti"]

if matricola not in alunni:
    print("matricola non esistente")
else:
    alunni.pop(matricola)
    
    task_da_eliminare = []

    for task_id, task_data in compiti.items():
        if task_data["matricola"] == matricola:
            task_da_eliminare.append(task_id)
    
    for task_id in task_da_eliminare:
        compiti.pop(task_id)


    

print(database)

    
