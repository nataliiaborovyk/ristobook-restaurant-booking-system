

from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from data_model.classes.Nazione import Nazione
    from data_model.classes.Regione import Regione

class reg_naz:

    class _link:

        _regione: Regione
        _nazione: Nazione

        def __init__(self, regione: Regione, nazione: Nazione) -> None:

            self._regione = regione
            self._nazione = nazione

        def regione(self) -> Regione:
            return self._regione
        
        def nazione(self) -> Nazione:
            return self._nazione
        
        def __hash__(self) -> int:
            return hash((self.regione(), self.nazione()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.regione() == other.regione() and self.nazione() == other.nazione()
        
        def __str__(self) -> str:
            return f"Regione {self.regione()} si trova nella nazione {self.nazione()}"
        
        def __repr__(self) -> str:
            return f"reg_naz({self.regione()}-{self.nazione()})"