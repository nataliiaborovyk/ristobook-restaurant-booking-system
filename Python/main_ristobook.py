from collections import namedtuple

from flask import Flask, jsonify, request

import db.utils_ristobook as db_utils


from data_model.classes.Nazione import Nazione
from data_model.classes.Regione import Regione
from data_model.classes.Citta import Citta

app = Flask(__name__)

db = namedtuple("mockup_db_ristobook", "nazioni regioni citta")

app.mockup_db = db

db.nazioni = db_utils.load_nazioni_da_json()
db.regioni = db_utils.load_regioni_da_json(db.nazioni)
db.citta   = db_utils.load_citta_da_json(db.regioni)


@app.route('/')
def initial_message():
    return jsonify({"response":'Questo è il messaggio di benvenuto nel RistoBook'})


# ------------ Nazione ----------------------
# GET +
# POST +
# PATCH +
# PUT uguale a PATCH ??
# DELETE +

@app.route('/nazioni', methods=['GET'])
def get_nazioni():
    nazioni: dict[str, Nazione] = app.mockup_db.nazioni  # recupero nazioni da app.mockup_db
    all_nazioni_info = db_utils.nazioni_info_per_response(nazioni)
    return jsonify(all_nazioni_info), 200

@app.route('/nazioni/<string:nome>')
def get_nazione(nome: str):
    try:
        nazione: Nazione = app.mockup_db.nazioni[nome]
        return jsonify(nazione.as_dict()), 200
    except KeyError:
        return jsonify({'Error': f'La nazione con il nome {nome} non esiste'}), 404

@app.route('/nazioni', methods=['POST'])
def add_nazione():
    # leggo il body della richiesta come json
    new_nazione_dict: dict|None = request.get_json() 
    # controlli
    if new_nazione_dict is None:    # body mancante
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in new_nazione_dict:  # campo nome mancante
        return jsonify({'errore': 'per creare la nazione fornire il campo \'nome\''}), 400
    if not isinstance(new_nazione_dict['nome'], str):   # tipo non str
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    nome_input: str = new_nazione_dict['nome'].strip().capitalize()
    if nome_input == "":
        return jsonify({'errore': 'il nome della nazione non può essere vuoto'}), 400
    if Nazione.nazione_con_nome(nome_input) is not None:    # controllo se esiste dublicato
        return jsonify({'errore': f'esiste gia una nazione con come {nome_input}'}), 400
    # creo ogetto
    try:
        nuova_nazione: Nazione = Nazione(nome_input)
    except ValueError as e:
        return jsonify({'errore': str(e)}), 400
    # aggiorno db
    app.mockup_db.nazioni[nuova_nazione.nome()] =nuova_nazione
    return jsonify(nuova_nazione.info()), 201

@app.route('/nazioni/<string:nome_vecchio>', methods=['PATCH'])
def update_nazione(nome_vecchio: str):
    body: dict|None = request.get_json()
    # controlli
    if body is None:
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in body:
        return jsonify({'errore': 'per creare la nazione fornire il campo \'nome\''}), 400
    if not isinstance(body['nome'], str):
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    # pulisco
    nome_vecchio:str = nome_vecchio.strip().capitalize()
    nome_nuovo: str = body['nome'].strip().capitalize()
    if nome_nuovo == "":
        return jsonify({'errore': 'il nome della nazione non può essere vuoto'}), 400
    
    if nome_vecchio not in app.mockup_db.nazioni:
        return jsonify({'errore': f'non esiste la nazione con nome \'{nome_vecchio}\''}), 404
    
    nazione: Nazione = app.mockup_db.nazioni[nome_vecchio]
    
    # controllo dublicati
    altra_nazione: Nazione|None = Nazione.nazione_con_nome(nome_nuovo)
    if altra_nazione is not None and altra_nazione is not nazione:
        return jsonify({'errore':f'esiste gia la nazione con nome\'{nome_nuovo}\''}), 400
    
    import db.utils_ristobook as db_utils
    try:
        nazione.set_nome(nome_nuovo)
        app.mockup_db.nazioni.pop(nome_vecchio)
        app.mockup_db.nazioni[nome_nuovo] = nazione
        db_utils.rename_nazione_nel_json(nome_vecchio, nome_nuovo)
    except ValueError as e:
        # rollback cancello modifiche
        if nome_nuovo in app.mockup_db.nazioni and app.mockup_db.nazioni[nome_nuovo] is nazione:
            app.mockup_db.nazioni.pop(nome_nuovo)
        # rimetto oggetto con vecchio nome nel db
        if nome_vecchio not in app.mockup_db.nazioni:
            app.mockup_db.nazioni[nome_vecchio] = nazione
        return jsonify({'errore': str(e)}), 400
    app.mockup_db.nazioni[nome_nuovo] = nazione 
    return jsonify(nazione.info()), 200


@app.route('/nazioni/<string:nome>', methods=['DELETE'])
def delete_nazione(nome:str):
    nome_clean: str = nome.strip().capitalize()
    if nome_clean not in app.mockup_db.nazioni:
        return jsonify({'errore': f'non esiste la nazione con nome\'{nome}\''}), 400
    nazione: Nazione = app.mockup_db.nazioni[nome_clean]
    if len(nazione.links_reg_naz()) > 0:
        return jsonify({'errore': f'non è possibile cancellare la nazione \'{nome}\' perche ha le regioni colegate '}), 400
    app.mockup_db.nazioni.pop(nome_clean)
    try:
        Nazione._remove_from_index(nome_clean)
    except KeyError:
        pass
    db_utils.delete_nazione_da_json(nome_clean)
    return jsonify({'ok': f'Nazione \'{nome_clean}\' -  cancellata'}), 200


# ------------- Regione -------------------------
# GET +
# POST +
# PATCH +
# PUT -
# DELETE +
@app.route('/regioni', methods=['GET'])
def get_regioni():
    regioni: dict[int, Regione] = app.mockup_db.regioni
    all_regioni_info = db_utils.regioni_info_per_response(regioni)
    return jsonify(all_regioni_info), 200

@app.route("/regioni/<int:id>", methods=['GET'])
def get_regione(id:int):
    try:
        regione: Regione = app.mockup_db.regioni[id]
        return jsonify(regione.as_dict()), 200
    except KeyError:
        return jsonify({'Error': f'La regione con id {id} non esiste'}), 404
    
@app.route('/regioni', methods=['POST'])
def add_reggione():
    new_regione_dict: dict = request.get_json()
    # controlli
    if new_regione_dict is None:    # body mancante
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in new_regione_dict:  # campo nome mancante
        return jsonify({'errore': 'per creare la regione fornire il campo \'nome\''}), 400
    if "nazione" not in new_regione_dict:
        return jsonify({'errore': 'per creare la regione fornire il campo \'nazione\''}), 400
    if not isinstance(new_regione_dict['nome'], str):   # tipo non str
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    if not isinstance(new_regione_dict['nazione'], str):   # tipo non str
        return jsonify({'errore': ' il campo \'nazione\' deve essere una stringa'}), 400
    nome_regione_input: str = new_regione_dict['nome']
    nome_nazione_input: str = new_regione_dict['nazione']
    nome_regione_clean: str = nome_regione_input.strip().capitalize()
    nome_nazione_clean: str = nome_nazione_input.strip().capitalize()
    if nome_regione_clean == "":
        return jsonify({'errore': 'il nome della regione non può essere vuoto'}), 400
    nazione: Nazione|None = Nazione.nazione_con_nome(nome_nazione_clean)    # controllo se nazione esiste
    if nazione is None:
        return jsonify({'errore': f'non esiste una nazione con nome \'{nome_nazione_clean}\''}), 404
    if Regione.regione_con_nomeReg_nomeNaz(nome_regione_clean, nome_nazione_clean) is not None:
        return jsonify({"errore": f"esiste gia la regione '{nome_regione_clean}' nella nazione '{nome_nazione_clean}'"}), 400
    # creo oggetto
    try:
        regione_nuova: Regione = Regione(nome_regione_clean, nazione)
    except ValueError as e:
        return jsonify({'errore': str(e)}), 400
    # salvo nel db
    app.mockup_db.regioni[regione_nuova.id()] = regione_nuova
    return jsonify(regione_nuova.info()), 201


@app.route("/regioni/<int:id>", methods=['PATCH'])
def patch_nome_regione(id: int):
    body: dict|None = request.get_json()
    # controlli
    if body is None:
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in body:
        return jsonify({'errore': 'per cambiare il nome fornire il campo \'nome\''}), 400
    if not isinstance(body['nome'], str):
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    # pulisco
    nome_nuovo: str = body['nome'].strip().capitalize()
    if nome_nuovo == "":
        return jsonify({'errore': 'il nome della regione non può essere vuoto'}), 400
    if id not in app.mockup_db.regioni:
        return jsonify({'errore': f'non esiste la regione con id \'{id}\''}), 404
    regione: Regione = app.mockup_db.regioni[id]
    altra_regione : Regione = Regione.regione_con_nomeReg_nomeNaz(nome_nuovo, regione.nazione().nome())
    if altra_regione is not None and altra_regione is not regione:
        return jsonify({'errore':f'esiste gia la regione con nome\'{nome_nuovo}\' nella nazione {regione.nazione().nome()}'}), 400
    regione.set_nome_univoco(nome_nuovo, regione.nazione())
    return jsonify(regione.info())
    

@app.route("/regioni/<int:id>", methods=['DELETE'])
def delete_regione(id: int):
    if id not in app.mockup_db.regioni:
        return jsonify({'errore': f'non esiste la regione con id \'{id}\''}), 404
    regione:Regione = app.mockup_db.regioni[id]
    if len(regione.links_cit_reg()) > 0:
        return jsonify({'errore': f'non è possibile cancellare la regione \'{id}\' perche ha le citta colegate '}), 400
    app.mockup_db.regioni.pop(id)
    try:
        Regione._remove_from_index(id)
    except KeyError:
        pass
    db_utils.delete_regione_da_json(id)
    return jsonify({'ok': f'Regione \'{id}\' -  cancellata'}), 200


# ----------------- Citta ---------------------------
# GET +
# POST +
# PATCH -
# PUT -
# DELETE -
@app.route('/citta', methods=['GET'])
def get_all_citta():
    citta: dict[int, Citta] = app.mockup_db.citta
    all_citta_info: dict = db_utils.citta_info_per_response(citta)
    return jsonify(all_citta_info), 200

@app.route('/citta/<int:id>', methods=['GET'])
def get_citta(id: int):
    try:
        citta: Citta = app.mockup_db.citta[id]
        return jsonify(citta.as_dict()), 200
    except KeyError:
        return jsonify({'Error': f'La citta con id {id} non esiste'}), 404

@app.route('/citta', methods=['POST'])
def add_citta():
    new_citta_dict: dict = request.get_json()
    # controlli
    if new_citta_dict is None:
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in new_citta_dict:
        return jsonify({'errore': 'per creare la citta fornire il campo \'nome\''}), 400
    if 'regione' not in new_citta_dict:
        return jsonify({'errore': 'per creare la citta fornire il campo \'regione\''}), 400
    if not isinstance(new_citta_dict['nome'], str):
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    if not isinstance(new_citta_dict['regione'], int):
        return jsonify({'errore': ' il campo \'regione\' deve essere un intero'}), 400
    nome_citta_input: str = new_citta_dict['nome'].strip().capitalize()
    id_regione_input: int = new_citta_dict['regione']
    if nome_citta_input == "":
        return jsonify({'errore': 'il nome della citta non può essere vuoto'}), 400
    regione: Regione|None = Regione.regione_con_id(id_regione_input) 
    if regione is None:
        return jsonify({'errore': f'non esiste una regione con id \'{id_regione_input}\''}), 404
    if Citta.citta_con_nomeCit_idReg(nome_citta_input,id_regione_input) is not None:
        return jsonify({"errore": f"esiste gia la citta '{nome_citta_input}' nella regione '{id_regione_input}'"}), 400
    try:
        citta: Citta = Citta(nome_citta_input, regione)
    except ValueError as e:
        return jsonify({'errore': str(e)}), 400
    app.mockup_db.citta[citta.id()] = citta
    return jsonify(citta.info()), 201
    
    
@app.route('/citta/<int:id>', methods=['PATCH'])
def patch_nome_citta(id: int):
    body: dict|None = request.get_json()
    #controlli
    if body is None:
        return jsonify({'errore': 'Body json mancante'}), 400
    if 'nome' not in body:
        return jsonify({'errore': 'per cambiare il nome fornire il campo \'nome\''}), 400
    if not isinstance(body['nome'], str):
        return jsonify({'errore': ' il campo \'nome\' deve essere una stringa'}), 400
    # pulisco
    nome_nuovo: str = body['nome'].strip().capitalize()
    if nome_nuovo == "":
        return jsonify({'errore': 'il nome della citta non può essere vuoto'}), 400
    if id not in app.mockup_db.citta:
        return jsonify({'errore': f'non esiste la citta con id \'{id}\''}), 404
    citta: Citta = app.mockup_db.citta[id]
    altra_citta: Citta = Citta.citta_con_nomeCit_idReg(nome_nuovo, citta.regione().nome())
    if altra_citta is not None and altra_citta is not citta:
        return jsonify({'errore':f'esiste gia la citta con nome\'{nome_nuovo}\' nella regione {citta.regione().nome()}'}), 400
    citta.set_nome_univoco(nome_nuovo, citta.regione())
    return jsonify(citta.info())


if __name__ == "__main__":
    app.run(debug=True)