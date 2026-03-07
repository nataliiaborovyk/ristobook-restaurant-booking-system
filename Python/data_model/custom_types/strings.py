import re
from typing import Self

# class URL(str):
#     def __new__(cls, v:str|Self) -> Self:
#         if not re.search("(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?", v):
#             raise ValueError(f"{v} non è un URL valido.")
#         return str.__new__(cls, v)
    
class Email(str):

    def __new__(cls, em: str|Self) -> Self:
        em: str = em.strip().lower()
        if not re.fullmatch(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", em):
            raise ValueError(f"Errore! Email {em} non è valida")
        return super().__new__(cls, em)
    
    def __str__(self) -> str:
        return f"Email: {super().__str__()}"
    
    def __repr__(self) -> str:
        return f"Email({super().__str__()})"
    
class CodiceFiscale(str):

    def __new__(cls, cf: str | Self) -> Self:
        cff: str = cf.upper().strip()
        if re.fullmatch(r"[A-Z]{6}[0-9]{2}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}", cf):
            return super().__new__(cls, cff)
        raise ValueError(f"{cff} non è un codice fiscale italiano valido")

class Telefono(str):

    def __new__(cls, tel: str | Self) -> Self:
        if re.fullmatch(r"^\d{10}$", tel):
            return super().__new__(cls, tel)
        raise ValueError(f"{tel} non è un numero di telefono italiano valido")
    
class PartitaIva(str):
    def __new__(cls, p_iva: str) -> "PartitaIva":
        s = p_iva.strip()
        if not (s.isdigit() and len(s) == 11):
            raise ValueError(f"Partita IVA '{s}' non valida: deve contenere 11 cifre.")
        return super().__new__(cls, s)

    def __str__(self) -> str:
        return f"Partita Iva: {super().__str__()}"
    
    def __repr__(self) -> str:
        return f"PartitaIva({super().__str__()})"