

import requests
import json


BASE_URL = "http://localhost:5000"

headers = {
    "Content-type": "application/json",
    "Accept": "application/json"
}

def _show_response(response: requests.Response) -> None:
    line = '='*10
    print(f"\n\n{line} {response.request.method} {response.url} {line}")
    print(f"\nRESPONSE:\n"
          f"- HTTP Status Code: {response.status_code}\n"
          f"- JSON CONTENT:")
    print(json.dumps(response.json(), indent=4))

# ----------- Nazione -----------------
def test_get_nazioni() -> None:
    response = requests.get(url=f"{BASE_URL}/nazioni", headers=headers)
    _show_response(response)

def test_get_nazione(nome: str) -> None:
    response = requests.get(url=f'{BASE_URL}/nazioni/{nome}', headers=headers)
    _show_response(response)

def test_post_nazione(nome_nazione: str) -> None:
    response = requests.post(url=f'{BASE_URL}/nazioni', headers=headers,
                             json={'nome': nome_nazione})
    response.encoding = 'utf-8'
    _show_response(response)

def test_patch_nazione(nome_vecchio:str, nome_nuovo:str) -> None:
    response = requests.patch(url=f'{BASE_URL}/nazioni/{nome_vecchio}', 
                              headers=headers,
                              json={'nome': nome_nuovo})
    response.encoding = 'utf-8'
    _show_response(response)

def test_delete_nazione(nome:str) -> None:
    response = requests.delete(url=f'{BASE_URL}/nazioni/{nome}', headers=headers)
    response.encoding = 'utf-8'
    _show_response(response)


# ------------ Regione ---------------
def test_get_regioni() -> None:
    response = requests.get(url=f'{BASE_URL}/regioni', headers=headers)
    _show_response(response)

def test_get_regione(id:int) -> None:
    response = requests.get(url=f'{BASE_URL}/regioni/{id}', headers=headers)
    _show_response(response)

def test_post_regione(nomeReg: str, nomeNaz: str) -> None:
    response = requests.post(url=f'{BASE_URL}/regioni', headers=headers,
                             json={'nome': nomeReg, 'nazione': nomeNaz})
    response.encoding = 'utf-8'
    _show_response(response)

def test_patch_regione(id:int, nomeReg) -> None:
    response = requests.patch(url=f'{BASE_URL}/regioni/{id}', headers=headers,
                              json={'nome': nomeReg})
    response.encoding = 'utf-8'
    _show_response(response)

def test_delete_regione(id:int) -> None:
    response = requests.delete(url=f'{BASE_URL}/regioni/{id}', headers=headers)
    _show_response(response)



# ------------ Citta -----------
def test_get_all_citta() -> None:
    response = requests.get(url=f'{BASE_URL}/citta', headers=headers)
    _show_response(response)

def test_get_citta(id: int) -> None:
    response = requests.get(url=f'{BASE_URL}/citta/{id}', headers=headers)
    _show_response(response)


def test_post_citta(nomeCit: str, idReg: int) -> None:
    response = requests.post(url=f'{BASE_URL}/citta', headers=headers,
                             json={'nome': nomeCit, 'regione': idReg})
    response.encoding = 'utf-8'
    _show_response(response)






if __name__ == '__main__':

    # test_get_nazioni()
    # test_get_nazione('Italia')
    # test_get_regioni()
    # test_get_regione(2)
    # test_get_all_citta()
    # test_get_citta(3)

    # test_create_nazione('Germania')
    # test_create_nazione('Germania')
    # test_create_nazione('  ')
    # test_post_regione('Umbria', 'Italia')
    # test_post_regione(' toscana', ' italia   ')
    # test_get_regioni()
    # test_post_citta('Orte', 0)
    # test_get_all_citta()
    # test_post_nazione('Atlantite')
    # test_get_nazioni()
    # test_patch_nazione('Atlantite', 'Atlantide')
    # test_get_nazioni()
    # test_delete_nazione('Atlantide')
    # test_patch_nazione('Atlantite', 'Atlantide')
    # test_get_nazioni()

    # test_get_regioni()
    # test_patch_regione(3, 'Umbriia')
    # test_post_regione('Abruzzo', 'Italia')
    
    # test_patch_regione(4, 'Abruzzzzo')
    # test_delete_regione(4)
    # test_get_regioni()
    # test_post_regione('Abruzzo', 'Italia')
    test_get_regioni()