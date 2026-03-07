from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from data_model.classes.Ristorante import Ristorante
    from data_model.classes.TipoCucina import TipoCucina

class ris_tip:

    class _link:
        
        _ristorante: Ristorante
        _tipo_cucina: TipoCucina

        def __init__(self, 
                     ristorante: Ristorante,
                     tipo_cucina: TipoCucina
            ) -> None:
            self._ristorante = ristorante
            self._tipo_cucina = tipo_cucina

        def ristorante(self) -> Ristorante:
            return self._ristorante
        
        def tipo_cucina(self) -> TipoCucina:
            return self._tipo_cucina
        
        def __hash__(self) -> int:
            return hash((self.ristorante(), self.tipo_cucina()))
        
        def __eq__(self, other: Any) -> bool:
            if type(self) != type(other) or hash(self) != hash(other):
                return False
            return self.ristorante() == other.ristorante() and self.tipo_cucina() == other.tipo_cucina()
        
        def __str__(self) -> str:
            return f"Ristorante {self.ristorante()} è {self.tipo_cucina()} "
        
        def __repr__(self) -> str:
            return f"ris_tip({self.ristorante()}-{self.tipo_cucina()})"
            
        