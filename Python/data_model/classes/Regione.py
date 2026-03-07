

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self, Tuple

if TYPE_CHECKING:
    from data_model.classes.Citta import Citta
    from data_model.associations.cit_reg import cit_reg

from data_model.classes.Index import Index

from data_model.classes.Nazione import Nazione
from data_model.associations.reg_naz import reg_naz

class Regione:

    _id: int     # imm, noto alla nascita
    _nome: str   # mutabile, noto alla nascita

    _link_reg_naz: reg_naz._link            # imm, noto alla nascita
    _cit_reg: dict[Citta, cit_reg._link]    # mutabile, non noto alla nascita

    _index_id: Index[int, Self] = Index('Regione') # pk
    _index_nome_in_nazione: Index[Tuple[str, str], Self] = Index('Regione') # unique

    def __init__(self, nome: str, nazione:Nazione, 
                 salva_nel_json:bool = True) -> None:
        self._nome = None
        self.set_nome_univoco(nome, nazione)
        self._set_id()
        self._crea_link_reg_naz(nazione)
        self._cit_reg: dict[Citta, cit_reg._link] = {}
        
        if salva_nel_json:
            import db.utils_ristobook as db_utils
            db_utils.store_regione_nel_json(self)


    @classmethod
    def regione_con_id(cls, id: Any) -> Self|None:
        return cls._index_id.get(id)
    
    @classmethod
    def regione_con_nomeReg_nazione(cls, nome: str, nazione: Nazione) -> Self|None:
        key = (nome, nazione.nome())
        return cls._index_nome_in_nazione.get(key)
    
    @classmethod
    def regione_con_nomeReg_nomeNaz(cls, regione_nome: str, nazione_nome: str) -> Self|None:
        if not isinstance(regione_nome, str) or not isinstance(nazione_nome, str):
            return None
        reg_nom_clean : str = regione_nome.strip().capitalize()
        naz_nom_clean : str = nazione_nome.strip().capitalize()
        key = (reg_nom_clean, naz_nom_clean)
        return cls._index_nome_in_nazione.get(key)
    
    @classmethod
    def tutte_regioni(cls):
        return cls._index_id.all()
    
    @classmethod
    def _remove_from_index(cls, id:int) -> None:
        cls._index_id.remove(id)
    
    def _set_id(self) -> None:
        key_list = list(self._index_id.all_keys())
        if len(key_list) > 0:
            last_id = max(key_list)
            id = last_id + 1
        else:
            id = 0
        self._index_id.add(id, self)
        self._id = id
    

    def set_nome_univoco(self, nome: str, nazione: Nazione) -> None:
        nome = nome.strip().capitalize()
        if nome == "":
            raise ValueError("Il nome della nazione non può essere vuoto")
        key = (nome, nazione.nome())
        altra = self._index_nome_in_nazione.get(key)
        if altra is not None and altra is not self:
            raise ValueError(f"Esiste già la regione '{nome}' nella nazione '{nazione.nome()}'")
        if self._nome is not None:
            old_key = (self._nome, nazione.nome())
            self._index_nome_in_nazione.remove(old_key)
        self._nome = nome
        self._index_nome_in_nazione.add(key, self)

    def _crea_link_reg_naz(self, nazione: Nazione) -> None:
        link = reg_naz._link(self, nazione)
        self._link_reg_naz = link
        nazione._add_link_reg_naz(link)


    def _add_link_cit_reg(self, link:cit_reg._link) -> None:
        if link.regione() is not self:
            raise ValueError(f"Il link fornito non riguarda regione {self.nome()}")
        if link.citta() in self._cit_reg:
            raise KeyError("Errore, il link gia esiste")
        self._cit_reg[link.citta()] = link

    def id(self) -> int:
        return self._id

    def nome(self) -> str:
        return self._nome
    
    def nazione(self) -> Nazione:
        return self._link_reg_naz.nazione()
    
    def link_reg_naz(self) -> reg_naz._link:
        return self._link_reg_naz
    
    def links_cit_reg(self) -> frozenset[cit_reg._link]:
        return frozenset(self._cit_reg.values())
    
    def info(self) -> dict[str, int|str]:
        return {
            'id': self.id(),
            'nome': self.nome(),
            'nazione': self.nazione().nome()
        }
    
    def as_dict(self) -> dict[str, int | str | dict[str, str] | dict[str, dict[str, str]]]:
        result: dict = dict()
        result['id'] = self.id()
        result['nome'] = self.nome()

        nazione_info: dict = {
            'nome': self.nazione().nome(),
            'url': f"/nazioni/{self.nazione().nome()}"
        }
        result['nazione'] = nazione_info
        citta_dict: dict = dict()
        for link in self.links_cit_reg():
            citta: Citta = link.citta()
            id_citta: int = citta.id()
            id_key: str = str(id_citta)
            url: str = f"/citta/{id_citta}"
            citta_info: dict = {
                'nome': citta.nome(),
                'url': url
            }
            citta_dict[id_key] = citta_info
        result['citta'] = citta_dict
        return result
    


    def __str__(self) -> str:
        return f"Regione nome: {self.nome()}, id: {self.id()}  in nazione {self._link_reg_naz.nazione().nome()}"
    
    def __repr__(self) -> str:
        return f"Regione({self.nome()} in {self._link_reg_naz.nazione().nome()})"




    
        