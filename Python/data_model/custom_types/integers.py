from typing import Self, Type

class IntGEZ(int):

    def __new__(cls, v: Self | int | float | str | bool):
        value: int = super().__new__(cls, v)
        if value < 0:
            raise ValueError(f"The value {v} must be greater than zero")
        return value
    

class IntGZ(int):

    def __new__(cls, v: Self | int | float | str | bool):
        value: int = super().__new__(cls, v)
        if value <= 0:
            raise ValueError(f"The value {v} must be greater than zero")
        return value
    
    # Attenzione: in generale la differenza tra interi non dovrebbe essere toccata
    def __sub__(self, other: int | Self) -> Self:
        other_int : int = int(other)
        try:
            res: int = int(self) - other_int
            return IntGZ(res)
        except ValueError:
            raise ValueError(f"The difference between {self} and {other} is not an IntGZ")
        
    def __str__(self) -> str:
        # return super().__str__()            
        return str(int(self))

    def __repr__(self) -> str:
        return f"IntGEZ({super().__str__()})"
    

    
    
class Voto(int):
    def __new__(cls, v:int|float|Self) -> Self:
        if v < 0 or v > 5:
            raise ValueError(f"Il valore di {v} deve essere compreso tra 0 e 5.")
        return int.__new__(cls, v)
    
    
def build_int_GE_class(v: int) -> Type:
    class IntGEV(int):
        def __new__(cls, x:int|float|Self) -> Self:
            if x < v:
                raise ValueError(f"Il valore di {x} deve essere >= {v}.")
            return int.__new__(cls, x)
    return IntGEV
