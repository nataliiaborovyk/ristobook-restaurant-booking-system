
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    pass

from datetime import datetime
from data_model.custom_types.integers import IntGZ

from data_model.classes.Index import Index

from data_model.classes.Cliente import Cliente
from data_model.classes.Ristorante import Ristorante
from data_model.associations.cl_pren import cl_pren
from data_model.associations.pren_ris import pren_ris

class Prenotazione:

    _id: int                        # imm, noto alla nascita
    _istante_creazione: datetime    # imm, noto alla nascita
    _numero_commensali: IntGZ       # imm, noto alla nascita
    _data_ora_prenotata: datetime   # imm, noto alla nascita
    _is_rifiutata: bool|None        # imm, non noto alla nascita
    _is_accettata: bool|None        # imm, non noto alla nascita
    _istante_accettazione: datetime|None    # imm, non noto alla nascita
    _istante_rifiuto: datetime|None         # imm, non noto alla nascita

    _link_cl_pren: cl_pren._link    # imm, noto alla nascita
    _link_pren_ris: pren_ris._link  # imm, noto alla nascita

    _index: Index[int, Self] = Index('Prenotazione')  # pk

    def __init__(self, 
                 *,  
                 numero_commensali: IntGZ,       
                 data_ora_prenotata: datetime,  
                 cliente: Cliente,
                 ristorante: Ristorante 
        ) -> None:      
        self._set_id()
        self._istante_creazione = datetime.now()
        self._numero_commensali = numero_commensali
        # [V.IstanteCreazioneMinoreDataOraPrenotata]  
        if data_ora_prenotata < self._istante_creazione:
            raise ValueError('Data e ora prenotata deve essere maggiore della data di creazione prenotazione')
        self._data_ora_prenotata = data_ora_prenotata
        self._crea_link_cl_pren(cliente)
        # [V.DataOraPrenotataNonInPeriodoChiusura]
        if ristorante.is_in_periodo_chiusura(data_ora_prenotata):
            raise ValueError("Errore: il ristorante è chiuso in quella data/ora, prenotazione non valida")
        self._crea_link_pren_ris(ristorante)
        self._is_rifiutata = None
        self._is_accettata = None
        self._istante_accettazione = None
        self._istante_rifiuto = None

    @classmethod
    def get_prenotazione(cls, id: Any) -> Self|None:
        return cls._index.get(id)

    @classmethod
    def tutte_prenotazioni(cls):
        return cls._index.all()


    def _set_id(self) -> None:
        key_list = list(self._index.all_keys())
        if len(key_list) > 0:
            last_id = max(key_list)
            id = last_id + 1
        else:
            id = 0
        self._index.add(id, self)
        self._id = id


    def _crea_link_cl_pren(self, cliente: Cliente) -> None:
        # if self.link_cl_pren() is not None:
        #     raise ValueError(f"Errore, il link verso {cliente} gia esiste")
        link: cl_pren._link = cl_pren._link(cliente, self)
        self._link_cl_pren = link
        cliente._add_link_cl_pren(link)

    def _crea_link_pren_ris(self, ristorante: Ristorante) -> None:
        # if self.link_pren_ris() is not None:
        #     raise ValueError(f"Errore, il link verso {ristorante} gia esiste")
        link: pren_ris._link = pren_ris._link(self, ristorante)
        self._link_pren_ris = link
        ristorante._add_link_pren_ris(link)

    # da rivedere per il vincolo [Da fusione] !!!!!!!
    # TODO

    def _set_accettata(self, data: datetime) -> None:
        # [V.IstanteCreazioneMinoreDiAccettazione]
        if data < self._istante_creazione:
            raise ValueError('Data e ora di accettazione deve essere maggiore della data di creazione prenotazione')
        if self._is_accettata is None and self._is_rifiutata is None and self._istante_creazione < data:
            self._is_accettata = True
            self._istante_accettazione = data

    def _set_rifiutata(self, data:datetime) -> None:
        # [V.IstanteCreazioneMinoreDiRifiuto]
        if data < self._istante_creazione:
            raise ValueError('Data e ora di rifiuto deve essere maggiore della data di creazione prenotazione')
        if self._is_accettata is None and self._is_rifiutata is None and self._istante_creazione < data:
            self._is_rifiutata = True
            self._istante_rifiuto = data

    def stato(self) -> str:
        if self._is_accettata:
            return f"Accettata {self.istante_accettazione()}"
        elif self._is_rifiutata:
            return f"Rifiutata {self.istante_rifiuto()}"
        else:
            return "Pendente"
        
    def id(self) -> int:
        return  self._id
    
    def istante_creazione(self) -> datetime:
        return self._istante_creazione
    
    def numero_commensali(self) -> IntGZ:
        return self._numero_commensali
    
    def data_ora_prenotata(self) -> datetime:
        return self._data_ora_prenotata
    
    def is_accetta(self) -> bool:
        return self._is_accettata is True
    
    def istante_accettazione(self) -> datetime:
        return self._istante_accettazione
    
    def is_rifiutata(self) -> bool:
        return self._is_rifiutata is True
    
    def istante_rifiuto(self) -> datetime:
        return self._istante_rifiuto
    
    def link_cl_pren(self) -> cl_pren._link:
        return self._link_cl_pren
    
    def link_pren_ris(self) -> pren_ris._link:
        return self._link_pren_ris
    
    def __str__(self) -> str:
        cliente_nome: str = self.link_cl_pren().cliente().nome()
        cliente_cognome: str = self.link_cl_pren().cliente().cognome()
        ristorante_nome: str = self.link_pren_ris().ristorante().nome()
        data = self.data_ora_prenotata()
        return f"Cliente {cliente_nome} {cliente_cognome} ha prenotato {self.numero_commensali()} in ristorante {ristorante_nome} per il {data.date()}"
    
   