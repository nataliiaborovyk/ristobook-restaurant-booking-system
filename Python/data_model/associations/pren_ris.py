

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from data_model.classes.Prenotazione import Prenotazione
    from data_model.classes.Ristorante import Ristorante

class pren_ris:

    class _link:

        _prenotazione: Prenotazione
        _ristorante: Ristorante

        def __init__(self, 
                     prenotazione: Prenotazione, 
                     ristorante: Ristorante
                     ) -> None:
            self._prenotazione = prenotazione
            self._ristorante = ristorante

        def prenotazione(self) -> Prenotazione:
            return self._prenotazione
        
        def ristorante(self) -> Ristorante:
            return self._ristorante
        
        def __hash__(self) -> int:
            return hash((self.prenotazione(), self.ristorante()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.prenotazione() == other.prenotazione() and self.ristorante() == other.ristorante()
        
        def __str__(self) -> str:
            return f"prenotazione {self.prenotazione()} riguarda il ristorante {self.ristorante()}"
        
        def __repr__(self) -> str:
            # return f"pren_ris({self.prenotazione()}-{self.ristorante()})"
            return f"pren_ris(prenotazione_id={self.prenotazione().id()}, ristorante_id={self.ristorante().id()})"
