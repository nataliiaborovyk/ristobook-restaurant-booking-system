from __future__ import annotations

import os
import json
from typing import Any

from data_model.classes.Nazione import Nazione
from data_model.classes.Regione import Regione
from data_model.classes.Citta import Citta


# CURRENT_DIR = os.path.curdir  # cartella db/
# MOCKUP_DB_JSON_FILENAME = os.path.join(CURRENT_DIR, "db", "mockup_db_ristobook.json")

CURRENT_DIR = os.path.dirname(__file__)   # cartella db/
MOCKUP_DB_JSON_FILENAME = os.path.join(CURRENT_DIR, "mockup_db_ristobook.json")


def leggi_db_da_json() -> dict[str, Any]:
    with open(MOCKUP_DB_JSON_FILENAME, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    return data

def scrivi_db_nel_json(data: dict[str, Any]) -> None:
    with open(MOCKUP_DB_JSON_FILENAME, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        # json.dump scrive il dict sul file come JSON
        # indent=4 rende il file leggibile
        # ensure_ascii=False mantiene caratteri tipo à, è, ecc.

# ============== Nazione ==================================

def load_nazioni_da_json() -> dict[str, Nazione]:
    data = leggi_db_da_json()
    nazioni_dict: dict[str, Any] = data["Nazione"]
    result: dict[str, Nazione] = dict()

    for valore_dict in nazioni_dict.values():
        nome: str = valore_dict["nome"]
        nazione_creata: Nazione = Nazione(nome, salva_nel_json=False) 
        # mentre carico nel db non voglio attivare store_nazione... che sta nel __init__
        result[nome] = nazione_creata
    return result

def store_nazione_nel_json(nazione_nuova: Nazione) -> None:
    data: dict[str, Any] = leggi_db_da_json()
    nazioni_dict: dict[str, dict[str, str]] = data['Nazione']  # nazioni_dict è solo un riferimento verso data
    nazione_nuova_info: dict[str, str] = nazione_nuova.info()
    key: str = nazione_nuova.nome()
    nazioni_dict[key] = nazione_nuova_info  
    # modifico nazioni_dict ma sicome è solo riferimento su data -> modifico anche data
    # data['Nazione'][key] = nazione_nuova
    scrivi_db_nel_json(data)

def rename_nazione_nel_json(nome_vecchio:str, nome_nuovo: str) -> None:
    data: dict[str, Any] = leggi_db_da_json()
    nazioni_dict: dict[str, Any] = data['Nazione']
    if nome_vecchio in nazioni_dict:
        nazioni_dict.pop(nome_vecchio)
    nazioni_dict[nome_nuovo] = {'nome': nome_nuovo}
    scrivi_db_nel_json(data)

def delete_nazione_da_json(nome:str) -> None:    # rimuovo da json
    data: dict[str, Any] = leggi_db_da_json()
    nazioni_dict: dict[str, Any] = data['Nazione']
    nazioni_dict.pop(nome, None)  # None serve per non restituire errore se non c'è la chiave nel dizionario
    scrivi_db_nel_json(data)
     
def nazioni_info_per_response(nazioni: dict[str, Nazione]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = dict()
    for nazione in nazioni.values():
        result[nazione.nome()] = nazione.info()
    return result

# ============== Regione ========================

def load_regioni_da_json(nazioni: dict[str, Nazione]) -> dict[int, Regione]:  
    data = leggi_db_da_json()
    regioni_dict: dict[str, Any] = data["Regione"]
    # dobbiamo ordinare per poi creare regioni in ordine di id (0,1,2...) per avere id coerenti
    lista_regioni_ordinate:list[tuple[str, dict[str, Any]]] = sorted(regioni_dict.items(), 
                                                                     key=lambda coppia_k_v: int(coppia_k_v[0]))
    result: dict[int, Regione] = dict()

    for chiave, valore_dict in lista_regioni_ordinate:
        id_regione_json: int = valore_dict["id"]
        nome_regione: str = valore_dict["nome"]
        nome_nazione: str = valore_dict["nazione"]

        nazione: Nazione = nazioni[nome_nazione]
        regione_creata: Regione = Regione(nome_regione, nazione, salva_nel_json=False)

        # Controllo se sto creando le regioni nello stesso ordine in cui sono state salvate nel JSON
        if regione_creata.id() != id_regione_json:
            raise ValueError(f"ID Regione non coincide: JSON={id_regione_json}, creato={regione_creata.id()}.")
        
        result[id_regione_json] = regione_creata
    return result

def store_regione_nel_json(regione_nuova: Regione) -> None:
    data: dict[str, Any] = leggi_db_da_json()
    # trasformo oggeto in forma adatta per json
    regione_nuova_info: dict = regione_nuova.info()
    data['Regione'][str(regione_nuova.id())] = regione_nuova_info
    scrivi_db_nel_json(data) 



def regioni_info_per_response(regioni: dict[int, Regione]) -> dict[str, dict[str, int|str]]:
    result: dict[str, dict[str, int|str]] = dict()
    for regione in regioni.values():
        id_key: str = str(regione.id())
        result[id_key] = regione.info()
    return result

def delete_regione_da_json(id: int) -> None:
    data: dict[str, Any] = leggi_db_da_json()
    regioni_dict: dict[str, Any] = data['Regione']
    regioni_dict.pop(str(id), None)
    scrivi_db_nel_json(data)


# ================== Citta =====================

def load_citta_da_json(regioni: dict[int, Regione]) -> dict[int, Citta]:
    data = leggi_db_da_json()
    citta_dict: dict[str, Any] = data["Citta"]
    lista_citta_ordinate: list[tuple[str, dict[str, Any]]] = sorted(citta_dict.items(), 
                                                                    key=lambda coppia_k_v: int(coppia_k_v[0]))
    result: dict[int, Citta] = dict()

    for chiave, valore_dict in lista_citta_ordinate:
        id_citta_json: int = valore_dict["id"]
        nome_citta: str = valore_dict["nome"]
        regione_id: int = valore_dict["regione_id"]

        regione: Regione = regioni[regione_id]
        citta_creata: Citta = Citta(nome_citta, regione, salva_nel_json=False)

        # Controllo se sto creando le citta nello stesso ordine in cui sono state salvate nel JSON
        if citta_creata.id() != id_citta_json:
            raise ValueError(f"ID Citta non coincide: JSON={id_citta_json}, creato={citta_creata.id()}. ")
        
        result[id_citta_json] = citta_creata
    return result

def store_citta_nel_json(citta: Citta) -> None:
    data: dict = leggi_db_da_json()
    data['Citta'][str(citta.id())] = citta.info()
    scrivi_db_nel_json(data)




def citta_info_per_response(citta: dict[int, Citta]) -> dict[str, dict[str, int | str]]:
    result: dict[str, dict[str, int | str]] = dict()
    for cit in citta.values():
        id_key: str = str(cit.id())
        result[id_key] = cit.info()
    return result














def load_all() -> tuple[dict[str, Nazione], dict[int, Regione], dict[int, Citta]]:
    nazioni: dict = load_nazioni_da_json()
    print("DEBUG nazioni:", list(Nazione.tutte_nazioni()))
    regioni: dict = load_regioni_da_json(nazioni)
    citta: dict = load_citta_da_json(regioni)
    return nazioni, regioni, citta







