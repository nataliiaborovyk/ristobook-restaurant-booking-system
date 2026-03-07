

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self, Tuple

if TYPE_CHECKING:
    from data_model.associations.pren_ris import pren_ris
    from data_model.classes.Prenotazione import Prenotazione

from data_model.classes.Index import Index
from datetime import datetime
from data_model.custom_types.other import *
from data_model.custom_types.strings import PartitaIva

from data_model.classes.TipoCucina import TipoCucina
from data_model.classes.Citta import Citta
from data_model.associations.ris_cit import ris_cit
from data_model.associations.ris_tip import ris_tip
import data_model.utils as utils
from itertools import combinations

class Ristorante:

    _id: int                            # imm, noto alla nascita
    _nome: str                          # mutabile, noto alla nascita
    _indirizzo: Indirizzo               # mutabile, noto alla nascita
    _partita_iva: PartitaIva            # imm, noto alla nascita
    _periodo_chiusura: set[Periodo]     # mutabile, noto alla nascita

    _link_ris_cit: ris_cit._link                    # imm, noto alla nascita
    _pren_ris: dict[Prenotazione, pren_ris._link]   # mutabile, non noto alla nascita
    _ris_tip: dict[TipoCucina, ris_tip._link]       # mutabile, non noto alla nascita

    _index_id: Index[int, Self] = Index('Ristorante') # pk
    _index_nome_in_citta: Index[Tuple[str, int], Self] = Index('Ristorante') # unique

    def __init__(self,
                 *,
                 nome: str,
                 indirizzo: Indirizzo,
                 partita_iva: PartitaIva,
                 periodo_chiusura: set[Periodo],
                 citta: Citta,
                 tipi_cucina: set[TipoCucina] 
    ) -> None:
        self._nome = None
        self.set_nome_univoco(nome, citta)
        self._set_id(self._nome, citta.id())  
        self.set_indirizzo(indirizzo)
        self._partita_iva = partita_iva
        # [v.PeriodoChiusura.NonSovrapposti]
        self.set_periodo_chiusura(periodo_chiusura)
        
        self._pren_ris: dict[Prenotazione, pren_ris._link] = {}
        self._ris_tip: dict[TipoCucina, ris_tip._link] = {}
        self._crea_link_ris_cit(citta)
        self._crea_link_ris_tip(tipi_cucina)    
        

    @classmethod
    def ristorante_con_id(cls, id: Any) -> Self|None:
        return cls._index_id.get(id)
    
    @classmethod
    def tutti_ristoranti(cls):
        return cls._index_id.all()
    

    def _set_id(self, nome: str, id_citta: int) -> None:
        key_list = list(self._index_id.all_keys())
        if len(key_list) > 0:
            last_id = max(key_list)
            id = last_id + 1
        else:
            id = 0
        self._index_id.add(id, self)
        self._id = id

    def set_nome_univoco(self, nome: str, citta: Citta) -> None:
        nome = nome.strip()
        coppia = (nome, citta.id())
        altro_ristorante = self._index_nome_in_citta.get(coppia)
        if altro_ristorante is not None and altro_ristorante is not self:
            raise ValueError(f"Esiste già la ristorante '{nome}' nella citta '{citta.nome()}'")
        if self._nome is not None:
            vecchia_coppia = (self._nome, citta.id())
            self._index_nome_in_citta.remove(vecchia_coppia)
        self._nome = nome
        self._index_nome_in_citta.add(coppia, self)

    def set_indirizzo(self, indirizzo: Indirizzo) -> None:
        self._indirizzo = indirizzo

    # [v.PeriodoChiusura.NonSovrapposti]
    def set_periodo_chiusura(self, periodo_chiusura: set[Periodo]) -> None:
        lista_periodi: list[Periodo] = list(periodo_chiusura)
        for pc1, pc2 in combinations(lista_periodi, 2):
            result: bool = utils.non_sovraposti_data(pc1.data_inizio(), pc1.data_fine(),
                                                     pc2.data_inizio(), pc2.data_fine())
        if not result:
            raise ValueError('Periodi sovraposti')
        for pc in periodo_chiusura:
            self._orari_periodo_non_sovrapposti(pc)
        self._periodo_chiusura = periodo_chiusura

    # [v.OrarioGiorno.NonSovrapposto]
    def _orari_periodo_non_sovrapposti(self, pc: Periodo) -> None:
        lista_orari = list(pc.orari())
        for og1, og2 in combinations(lista_orari, 2):
            if not utils.non_sovraposti_orariogiorno(og1, og2):
                raise ValueError(f"Orari sovraposti")


    def _crea_link_ris_cit(self, citta: Citta) -> None:
        link = ris_cit._link(self, citta)
        self._link_ris_cit = link
        citta._add_link_ris_cit(link)

    def _crea_link_ris_tip(self, tipi_cucina: set[TipoCucina]) -> None:
        for tc in tipi_cucina:
            link = ris_tip._link(self, tc)
            self._ris_tip[tc] = link
            tc._add_link_ris_tip(link)
    

    def _add_link_pren_ris(self, link: pren_ris._link) -> None:
        if link.ristorante() is not self:
            raise ValueError(f"Il link fornito non riguarda ristorante {self.nome()}")
        if link.prenotazione() in self._pren_ris:
            raise KeyError("Errore, il link gia esiste")
        self._pren_ris[link.prenotazione()] = link

    def _add_link_ris_tip(self, link: ris_tip._link) -> None:
        if link.ristorante() is not self:
            raise ValueError(f"Il link fornito non riguarda ristorante {self.nome()}")
        if link.tipo_cucina() in self._ris_tip:
            raise KeyError("Errore, il link gia esiste")
        self._ris_tip[link.tipo_cucina()] = link


    def id(self) -> int:
        return self._id
    
    def nome(self) -> str:
        return self._nome
    
    def periodo_chiusura(self) -> frozenset[Periodo]:
        return frozenset(self._periodo_chiusura)
            
    def link_ris_cit(self) -> ris_cit._link:
        return self._link_ris_cit

    def links_pren_ris(self) -> frozenset[pren_ris._link]:
        return frozenset(self._pren_ris.values())
    
    def links_ris_tip(self) -> frozenset[ris_tip._link]:
        return frozenset(self._ris_tip.values())
    

    def is_in_periodo_chiusura(self, i:datetime) -> bool:
        i_giorno: Giorno = utils.convert(i.weekday())
        for pc in self.periodo_chiusura():
            if i.date() >= pc.data_inizio() and i.date() <= pc.data_fine:
                for og in pc.orari():
                    if og.giorno() == i_giorno and (og.ora_inizio() <= i.time() and og.ora_fine() > i.time()):
                        return True
        return False



    def __str__(self) -> str:
        return f"Ristorante nome: {self.nome()}, id: {self.id()} in citta {self._link_ris_cit.citta().nome()}"
    
    def __repr__(self) -> str:
        return f"Ristorante({self.nome()} in {self._link_ris_cit.citta().nome()})"
    
    

