
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from data_model.associations.reg_naz import reg_naz
    from data_model.classes.Regione import Regione

from data_model.classes.Index import Index

class Nazione:
    
    _nome: str                              # mutabile, noto alla nascita
    _reg_naz: dict[Regione, reg_naz._link]  # mutabile, non noto alla nascita
    
    _index_nome: Index[str, Self] = Index('Nazione') # pk

    def __init__(self, nome: str, salva_nel_json: bool = True) -> None:
        self._nome = None
        self.set_nome(nome)
        self._reg_naz: dict[Regione, reg_naz._link] = {}
        
        if salva_nel_json:
            import db.utils_ristobook as db_utils
            db_utils.store_nazione_nel_json(self)
    
    @classmethod
    def nazione_con_nome(cls, nome: Any) -> Self|None:
        return cls._index_nome.get(nome)

    @classmethod
    def tutte_nazioni(cls):
        return cls._index_nome.all()
    
    @classmethod
    def _remove_from_index(cls, nome:str) -> None:
        cls._index_nome.remove(nome)

    
    def set_nome(self, nome: str) -> None:
        nome = nome.strip().capitalize()
        if nome == "":
            raise ValueError("Il nome della nazione non puo essere vuoto")
        altra_nazione = self._index_nome.get(nome)
        if altra_nazione is not None and altra_nazione is not self:
            raise ValueError("Il nome è gia usato")
        if self._nome is not None:
            self._index_nome.remove(self._nome)
        self._nome = nome
        self._index_nome.add(nome, self)
    

    def _add_link_reg_naz(self, link: reg_naz._link) -> None:
        if link.nazione() is not self:
            raise ValueError(f"Il link fornito non riguarda nazione {self.nome()}")
        if link.regione() in self._reg_naz:
            raise KeyError("Errore, il link gia esiste")
        self._reg_naz[link.regione()] = link

    def nome(self) -> str:
        return self._nome
    
    def links_reg_naz(self) -> frozenset[reg_naz._link]:
        return frozenset(self._reg_naz.values())
    
    def regioni(self) -> frozenset[Regione]:
        return frozenset(self._reg_naz.keys())

     
    def info(self) -> dict[str, str]:
        return {
                'nome': self.nome()
            }
    
    def as_dict(self) -> dict[str, str | dict[str, dict[str, str]]]:
        result: dict = dict()
        result['nome'] = self.nome()
        regioni_dict: dict = dict()
        for link in self.links_reg_naz():
            regione: Regione = link.regione()
            id_regione: int = regione.id()
            id_key: str = str(id_regione)
            url = f"/regioni/{id_regione}"
            regione_info: dict = {
                'nome': regione.nome(),
                'url': url
            }
            regioni_dict[id_key] = regione_info
        result['regioni'] = regioni_dict
        return result



    
    def __str__(self) -> str:
        return f"Nazione: {self.nome()}"
    
    def __repr__(self) -> str:
        return f"Nazione({self.nome()})"

