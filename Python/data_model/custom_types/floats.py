from typing import Self

class FloatGEZ(float):
    def __new__(cls, v:int|float|Self) -> Self:
        if v < 0:
            raise ValueError(f"Il valore di {v} deve essere >= 0.")
        return float.__new__(cls, v)
    
class FloatGZ(FloatGEZ):
    def __new__(cls, v:int|float|Self) -> Self:
        if v <= 0:
            raise ValueError(f"Il valore di {v} deve essere > 0.")
        return FloatGEZ.__new__(cls, v)