from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from data_model.classes.Ristorante import Ristorante
    from data_model.classes.Citta import Citta

class ris_cit:

    class _link:
        
        _ristorante: Ristorante
        _citta: Citta

        def __init__(self, 
                     ristorante: Ristorante,
                     citta: Citta
            ) -> None:
            self._ristorante = ristorante
            self._citta = citta

        def ristorante(self) -> Ristorante:
            return self._ristorante
        
        def citta(self) -> Citta:
            return self._citta
        
        def __hash__(self) -> int:
            return hash((self.ristorante(), self.citta()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.ristorante() == other.ristorante() and self.citta() == other.citta()
        
        def __str__(self) -> str:
            return f"Ristorante {self.ristorante()} si trova nella citta {self.citta()} "
        
        def __repr__(self) -> str:
            return f"ris_cit({self.ristorante()}-{self.citta()})"
        