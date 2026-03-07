
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from data_model.associations.cl_pren import cl_pren
    from data_model.classes.Prenotazione import Prenotazione

from data_model.custom_types.strings import Email
from data_model.custom_types.integers import IntGEZ
from datetime import datetime
from data_model.classes.Index import Index


class Cliente:

    _id: int        # imm, noto alla nascita
    _nome: str      # mutabile, noto alla nascita
    _cognome: str   # mutabile, noto alla nascita
    _email: Email   # mutabile, noto alla nascita

    _cl_pren: dict[Prenotazione, cl_pren._link]   # mutabile, non noto alla nascita
    
    _index_id: Index[int, Self] = Index('Cliente') # pk
    _index_email: Index[Email, Self] = Index('Cliente') # unique

    def __init__(self, 
                 *,
                 nome: str,
                 cognome: str,
                 email: Email
        ) -> None:
        self._set_id()
        self.set_nome(nome)
        self.set_cognome(cognome)
        self._email = None
        self.set_email_univoco(email)
        self._cl_pren: dict[Prenotazione, cl_pren._link] = {} 

    @classmethod
    def cliente_con_id(cls, id: Any) -> Self|None:
        return cls._index_id.get(id)
    
    @classmethod
    def cliente_con_email(cls, email: Any) -> Self|None:
        return cls._index_email.get(email)

    @classmethod
    def tutti_clienti(cls):
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

    def set_nome(self, nome: str) -> None:
        nome = nome.strip().capitalize()
        self._nome = nome

    def set_cognome(self, cognome: str) -> None:
        cognome = cognome.strip().capitalize()
        self._cognome = cognome

    def set_email_univoco(self, email: Email) -> None:
        altro = self._index_email.get(email)
        if altro is not None and altro is not self:
            raise ValueError(f"Errore! Email {email} è gia registrato")
        if self._email  is not None:
            self._index_email.remove(self._email)
        self._email = email
        self._index_email.add(email, self)
        
    def _add_link_cl_pren(self, link: cl_pren._link) -> None:
        if link.cliente() is not self:
            raise ValueError(f"Il link fornito non riguarda cliente {self.email()}")
        if link.prenotazione() in self._cl_pren:
            raise KeyError("Errore, il link gia esiste")
        self._cl_pren[link.prenotazione()] = link

    def id(self) -> int:
        return self._id

    def nome(self) -> str:
        return self._nome
    
    def cognome(self) -> str:
        return self._cognome
    
    def email(self) -> Email:
        return self._email
    
    def links_cl_pren(self) -> frozenset[cl_pren._link]:
        return frozenset(self._cl_pren.values())


    def num_prenot_accettate(self, d_iniz: datetime, d_fin: datetime) -> IntGEZ:
        if len(self.links_cl_pren()) == 0:
            return 0
        cont: int = 0
        for link in self.links_cl_pren():
            pren: Prenotazione = link.prenotazione()
            if pren.is_accetta():
                if d_iniz <= pren.istante_accettazione() and d_fin >= pren.istante_accettazione():
                    cont += 1
        return cont


    def num_prenot_rifiutate(self, d_iniz: datetime, d_fin: datetime) -> IntGEZ:
        if len(self.links_cl_pren()) == 0:
            return 0
        cont: int = 0
        for link in self.links_cl_pren():
            pren: Prenotazione = link.prenotazione()
            if pren.is_rifiutata():
                if d_iniz <= pren.istante_rifiuto() and d_fin >= pren.istante_rifiuto():
                    cont += 1
        return cont


    def __str__(self) -> str:
        return f"Nome: {self.nome()}, Cognome: {self.cognome()}, Email: {self.email()}, ID: {self.id()}"
    
    def __repr__(self) -> str:
        return f"Cliente({self.nome()} {self.cognome()}, {self.email()}, ID:{self.id()}"
        

