

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self, Tuple

if TYPE_CHECKING:
    from data_model.classes.Ristorante import Ristorante
    from data_model.associations.ris_cit import ris_cit
    from data_model.classes.Regione import Regione

from data_model.classes.Index import Index

from data_model.associations.cit_reg import cit_reg


class Citta:

    _id: int     # imm, noto alla nascita
    _nome: str   # mutabile, noto alla nascita

    _link_cit_reg: cit_reg._link                # imm, noto alla nascita
    _ris_cit: dict[Ristorante, ris_cit._link]   # mutabile, non noto alla nascita

    _index_id: Index[int, Self] = Index('Citta') # pk
    _index_nome_in_regione: Index[Tuple[str, int], Self] = Index('Citta') # unique   ?????

    def __init__(self, nome: str, regione: Regione, 
                 salva_nel_json:bool = True) -> None:
        self._nome = None
        self.set_nome_univoco(nome, regione)
        self._set_id()
        self._crea_link_cit_reg(regione)
        self._ris_cit: dict[Ristorante, ris_cit._link] = {}
        
        if salva_nel_json:
            import db.utils_ristobook as db_utils
            db_utils.store_citta_nel_json(self)


    @classmethod
    def citta_con_id(cls, id: Any) -> Self|None:
        return cls._index_id.get(id)
    
    @classmethod
    def citta_con_nomeCit_idReg(cls, nomeCit: str, idReg: int) -> Self|None:
        if not isinstance(nomeCit, str) or not isinstance(idReg, int):
            return None
        nomeCit_clean: str = nomeCit.strip().capitalize()
        key = (nomeCit_clean, idReg)
        return cls._index_nome_in_regione.get(key)

    @classmethod
    def tutte_citta(cls):
        return cls._index_id.all()
    
    def _set_id(self) -> None:
        key_list = list(self._index_id.all_keys())
        if len(key_list) > 0:
            last_id = max(key_list)
            id = last_id + 1
        else:
            id = 0
        self._index_id.add(id, self)
        self._id = id
    

    def set_nome_univoco(self, nome: str, regione: Regione) -> None:
        nome = nome.strip().capitalize()
        if nome == "":
            raise ValueError("Il nome della nazione non può essere vuoto")
        key = (nome, regione.id())
        altra_citta = self._index_nome_in_regione.get(key)
        if altra_citta is not None and altra_citta is not self:
            raise ValueError(f"Esiste già la citta '{nome}' nella regione '{regione.nome()}'")
        if self._nome is not None:
            old_key = (self._nome, regione.id())
            self._index_nome_in_regione.remove(old_key)
        self._nome = nome
        self._index_nome_in_regione.add(key, self)

    def _crea_link_cit_reg(self, regione: Regione) -> None:
        link = cit_reg._link(self, regione)
        self._link_cit_reg = link
        regione._add_link_cit_reg(link)


    def _add_link_ris_cit(self, link:ris_cit._link) -> None:
        if link.citta() is not self:
            raise ValueError(f"Il link fornito non riguarda citta {self.nome()}")
        if link.ristorante() in self._ris_cit:
            raise KeyError("Errore, il link gia esiste")
        self._ris_cit[link.ristorante()] = link

    def nome(self) -> str:
        return self._nome
    
    def id(self) -> int:
        return self._id
    
    def regione(self) -> Regione:
        return self._link_cit_reg.regione()
    
    def link_cit_reg(self) -> cit_reg._link:
        return self._link_cit_reg
    
    def links_ris_cit(self) -> frozenset[ris_cit._link]:
        return frozenset(self._ris_cit.values())
    
    def info(self) -> dict[str, int | str]:
        return {
            'id': self.id(),
            'nome': self.nome(),
            'regione_id': self.regione().id()
        }

    def as_dict(self) -> dict[str, int | str | dict[str, int | str] | dict[str, str] | dict[str, dict[str, str]]]:
        result: dict = dict()
        result['id'] = self.id()
        result['nome'] = self.nome()
        regione_info: dict = {
            'id': self.regione().id(),
            'nome': self.regione().nome(),
            'url': f"/regioni/{self.regione().id()}"
        }
        result['regione'] = regione_info
        nazione_info: dict = {
            'nome': self.regione().nazione().nome(),
            'url': f"/nazioni/{self.regione().nazione().nome()}"
        }
        result['nazione'] = nazione_info
        ristoranti_dict: dict = dict()
        for link in self.links_ris_cit():
            ristorante: Ristorante = link.ristorante()
            id_ristorante: int = ristorante.id()
            id_key: str = str(id_ristorante)
            url: str = f"/ristoranti/{id_ristorante}"
            ristorante_info: dict = {
                'nome': ristorante.nome(),
                'url': url
            }
            ristoranti_dict[id_key] = ristorante_info
        result['ristoranti'] = ristoranti_dict
        return result

    ## prova
    def as_dict2(self) -> dict[str, int | str | dict[str, int | str] | dict[str, str] | dict[str, dict[str, str]]]:
        result: dict = dict()
        dict_info: dict = dict()
        dict_info['id'] = self.id()
        dict_info['nome'] = self.nome()
        regione_info: dict = {
            'id': self.regione().id(),
            'nome': self.regione().nome(),
            'url': f"/regioni/{self.regione().id()}"
        }
        dict_info['regione'] = regione_info
        nazione_info: dict = {
            'nome': self.regione().nazione().nome(),
            'url': f"/nazioni/{self.regione().nazione().nome()}"
        }
        dict_info['nazione'] = nazione_info
        ristoranti_dict: dict = dict()
        for link in self.links_ris_cit():
            ristorante: Ristorante = link.ristorante()
            id_ristorante: int = ristorante.id()
            id_key: str = str(id_ristorante)
            url: str = f"/ristoranti/{id_ristorante}"
            ristorante_info: dict = {
                'nome': ristorante.nome(),
                'url': url
            }
            ristoranti_dict[id_key] = ristorante_info
        dict_info['ristoranti'] = ristoranti_dict
        result[str(self.id())] = dict_info
        return result
    

    def __str__(self) -> str:
        return f"Citta nome: {self.nome()}, id: {self.id()}  in regione {self._link_cit_reg.regione().nome()}"
    
    def __repr__(self) -> str:
        return f"Citta({self.nome()} in {self._link_cit_reg.regione().nome()})"



    
        