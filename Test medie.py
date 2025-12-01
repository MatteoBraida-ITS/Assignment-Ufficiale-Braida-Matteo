voti1 = []
voti2 = []
medie = []



compiti = {
    "TASK002": {
            "id": "TASK002",
            "descrizione": "es python",
            "matricola": "MAT001",
            "stato": "assegnato",
            "data assegnazione": "2025-12-01 01-58-53",
            "voto": 8,
            "data modifica": "2025-12-01 16-44-14"
        },
    "TASK003": {
            "id": "TASK003",
            "descrizione": "es python",
            "matricola": "MAT002",
            "stato": "assegnato",
            "data assegnazione": "2025-12-01 16-42-12",
            "voto": 5,
            "data modifica": "2025-12-01 16-45-19"
        },
        "TASK004": {
            "id": "TASK004",
            "descrizione": "es java",
            "matricola": "MAT001",
            "stato": "assegnato",
            "data assegnazione": "2025-12-01 16-43-25",
            "voto": 4,
            "data modifica": "2025-12-01 16-45-48"
        },
        "TASK005": {
            "id": "TASK005",
            "descrizione": "es java",
            "matricola": "MAT002",
            "stato": "assegnato",
            "data assegnazione": "2025-12-01 16-43-35",
            "voto": 9,
            "data modifica": "2025-12-01 16-45-58"
        }

}

for task_id, task_data in compiti.items():
    if task_data["matricola"] == "MAT001":
        voto = task_data["voto"]
        voti1.append(voto)
        media1 = sum(voti1) / len(voti1) 

for task_id, task_data in compiti.items():
    if task_data["matricola"] == "MAT002":
        voto = task_data["voto"]
        voti2.append(voto)
        media2 = sum(voti2) / len(voti2)

medie.append(media1)
medie.append(media2)
medie.sort(reverse=True)
print (medie)


