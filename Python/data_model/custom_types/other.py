
from typing import *
from datetime import *
from data_model.custom_types.enums import Giorno


class Indirizzo:
    def __init__(self, via: str, civico: str, cap: str) -> None:
        if not via or not civico:
            raise ValueError("Via e civico non possono essere vuoti.")
        if not (cap.isdigit() and len(cap) == 5):
            raise ValueError(f"CAP '{cap}' non valido: deve essere una stringa di 5 cifre.")
        self._via = via
        self._civico = civico
        self._cap = cap

    def via(self) -> str:
        return self._via

    def civico(self) -> str:
        return self._civico

    def cap(self) -> str:
        return self._cap

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Indirizzo) and (self.via(), self.civico(), self.cap()) == (other.via(), other.civico(), other.cap())

    def __hash__(self) -> int:
        return hash((self.via(), self.civico(), self.cap()))

    def __str__(self) -> str:
        return f"{self.via()}, {self.civico()}, {self.cap()}"
    

class OrarioGiorno:

    def __init__(self, ora_inizio: time, ora_fine: time, giorno: Giorno) -> None:
        if ora_inizio >= ora_fine:
            raise ValueError("ora_inizio deve essere < ora_fine")
        self._ora_inizio = ora_inizio
        self._ora_fine = ora_fine
        self._giorno = giorno

    def ora_inizio(self) -> time:    
        return self._ora_inizio

    def ora_fine(self) -> time: 
        return self._ora_fine

    def giorno(self) -> Giorno: 
        return self._giorno

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, OrarioGiorno) and \
               (self.ora_inizio(), self.ora_fine(), self.giorno()) == (other.ora_inizio(), other.ora_fine(), other.giorno())

    def __hash__(self) -> int:
        return hash((self.ora_inizio(), self.ora_fine(), self.giorno()))

    def __str__(self) -> str:
        return f"{self.giorno()}: {self.ora_inizio()}-{self.ora_fine()}"
    

class Periodo:

    def __init__(self, data_inizio: date, data_fine: date, orari: set[OrarioGiorno]) -> None:
        if data_inizio > data_fine:
            raise ValueError("data_inizio deve essere <= data_fine")
        self._data_inizio = data_inizio
        self._data_fine = data_fine
        self._orari = orari

    def data_inizio(self) -> date:  
        return self._data_inizio

    def data_fine(self) -> date: 
        return self._data_fine

    def orari(self) -> FrozenSet[OrarioGiorno]: 
        return FrozenSet(self._orari)

    def __eq__(self, other):
        return isinstance(other, Periodo) and \
               (self.data_inizio(), self.data_fine(), self.orari()) == (other.data_inizio(), other.data_fine(), other.orari())

    def __hash__(self):
        return hash((self.data_inizio(), self.data_fine(), self.orari()))

    def __str__(self):
        return f"{self.data_inizio()}, {self.data_fine()}, {self.orari()}"