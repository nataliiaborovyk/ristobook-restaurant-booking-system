from db.utils_ristobook import load_all
from data_model.classes.Nazione import Nazione
from data_model.classes.Regione import Regione
from data_model.classes.Citta import Citta


nazioni, regioni, citta = load_all()

print("DEBUG nazioni:", list(Nazione.tutte_nazioni()))
print("nazioni dict:", list(nazioni.keys()))


