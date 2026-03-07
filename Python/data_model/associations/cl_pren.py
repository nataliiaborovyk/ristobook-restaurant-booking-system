
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from data_model.classes.Cliente import Cliente
    from data_model.classes.Prenotazione import Prenotazione

class cl_pren:

    class _link:

        _cliente: Cliente
        _prenotazione: Prenotazione

        def __init__(self, 
                     cliente: Cliente, 
                     prenotazione: Prenotazione
                     ) -> None:
            self._cliente = cliente
            self._prenotazione = prenotazione

        def cliente(self) -> Cliente:
            return self._cliente
        
        def prenotazione(self) -> Prenotazione:
            return self._prenotazione
        
        def __hash__(self) -> int:
            return hash((self.cliente(), self.prenotazione()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.cliente() == other.cliente() and self.prenotazione() == other.prenotazione()
        
        def __str__(self) -> str:
            return f"Cliente {self.cliente()} ha fatto la prenotazione {self.prenotazione()}"
        
        def __repr__(self) -> str:
            # return f"cl_pren({self.cliente()} - {self.prenotazione()})"
            return f"cl_pren(cliente_id={self.cliente().id()}, prenotazione_id={self.prenotazione().id()})"
