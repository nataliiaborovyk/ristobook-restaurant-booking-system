
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self, Tuple

if TYPE_CHECKING:
    from data_model.classes.Ristorante import Ristorante
    from data_model.associations.ris_tip import ris_tip

from data_model.classes.Index import Index

class TipoCucina:

    _nome: str      # mutabile, noto alla nascita

    _ris_tip: dict[Ristorante, ris_tip._link]   # mutabile, non noto alla nascita

    _index_nome: Index[str, Self] = Index('TipoCucina') # pk

    def __init__(self, nome:str) -> None:
        self._nome = None
        self.set_nome(nome)
        self._ris_tip: dict[Ristorante, ris_tip._link] = {}

    @classmethod
    def tipo_cucina_con_nome(cls, nome: Any) -> Self|None:
        return cls._index_nome.get(nome)
    
    @classmethod
    def tutti_tipo_cucina(cls):
        return cls._index_nome.all()

    def set_nome(self, nome: str) -> None:
        nome = nome.strip().lower()
        altro: Self|None = self._index_nome.get(nome)
        if altro is not None and altro is not self:
            raise ValueError("Il nome è gia usato")
        if self._nome is not None:
            self._index_nome.remove(self._nome)
        self._nome = nome
        self._index_nome.add(nome, self)

    def _add_link_ris_tip(self, link: ris_tip._link) -> None:
        if link.tipo_cucina() is not self:
            raise ValueError(f"Il link fornito non riguarda tipo cucina {self.nome()}")
        if link.ristorante() in self._ris_tip:
            raise KeyError("Errore, il link gia esiste")
        self._ris_tip[link.ristorante()] = link

    def nome(self) -> str:
        return self._nome
    
    def links_ris_tip(self) -> frozenset[ris_tip._link]:
        return frozenset(self._ris_tip.values())
    
    def __str__(self) -> str:
        return f"Tipo cucina: {self.nome()}"