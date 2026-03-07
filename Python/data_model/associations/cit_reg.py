


from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from data_model.classes.Regione import Regione
    from data_model.classes.Citta import Citta

class cit_reg:

    class _link:
        
        _citta: Citta
        _regione: Regione

        def __init__(self, citta: Citta, regione: Regione) -> None:
            
            self._citta = citta
            self._regione = regione

        def regione(self) -> Regione:
            return self._regione
        
        def citta(self) -> Citta:
            return self._citta
        
        def __hash__(self) -> int:
            return hash((self.regione(), self.citta()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.regione() == other.regione() and self.citta() == other.citta()
        
        def __str__(self) -> str:
            return f"Citta {self.citta()} si trova nella regione {self.regione()}"
        
        def __repr__(self) -> str:
            return f"cit_reg({self.citta()}-{self.regione()})"