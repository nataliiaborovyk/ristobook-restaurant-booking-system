from datetime import date, datetime
from data_model.custom_types.other import OrarioGiorno
from data_model.custom_types.enums import Giorno

def non_sovraposti(i1: datetime,
                   f1: datetime,
                   i2: datetime,
                   f2: datetime) -> bool:
    if i1 > f1 or i2 > f2:
        raise ValueError('Inizio deve essere minore di fine')
    return i1 > f2 or i2 > f1

def non_sovraposti_data(i1: date,
                        f1: date,
                        i2: date,
                        f2: date) -> bool:
    if i1 > f1 or i2 > f2:
        raise ValueError('Inizio deve essere minore di fine')
    return i1 > f2 or i2 > f1
    

def non_sovraposti_orariogiorno(og1: OrarioGiorno,
                                og2: OrarioGiorno) -> bool:
    if og1.giorno() != og2.giorno():
        return True
    if og2.ora_fine() <= og1.ora_inizio() or og1.ora_fine() <= og2.ora_inizio():
        return True
    return False

def convert(num: int) -> Giorno:
    if num < 0 or num > 6:
        raise ValueError('Numero deve essere tra 0 e 6')
    match num:
        case 0:
            return Giorno.lunedi
        case 1:
            return Giorno.martedi
        case 2:
            return Giorno.mercoledi
        case 3:
            return Giorno.giovedi
        case 4:
            return Giorno.venerdi
        case 5:
            return Giorno.sabato
        case 6:
            return Giorno.domenica
