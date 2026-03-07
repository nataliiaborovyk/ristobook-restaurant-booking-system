
from datetime import datetime, timedelta
from classes.Cliente import Cliente
from classes.Prenotazione import Prenotazione
from classes.Ristorante import Ristorante
from classes.TipoCucina import TipoCucina
from classes.Nazione import Nazione
from classes.Regione import Regione
from classes.Citta import Citta
from custom_types.other import Indirizzo, Periodo
from custom_types.strings import Email, PartitaIva
from custom_types.integers import IntGZ




italia: Nazione = Nazione('Italia')
print(italia)

lazio: Regione = Regione('Lazio', italia)
print(lazio)

roma: Citta = Citta('Roma', lazio)
print(roma)

print("GET:", Nazione.nazione_con_nome("Italia"))
print("GET:", Regione.regione_con_id(0))
print("GET:", Citta.citta_con_id(0))

try:
    lazio2 = Regione("Lazio", italia)   # stesso nome nella stessa nazione
except Exception as e:
    print("OK vincolo Regione:", e)

try:
    roma2 = Citta("Roma", lazio)       # stesso nome nella stessa regione
except Exception as e:
    print("OK vincolo Citta:", e)


c_italiana = TipoCucina("italiana")
print(c_italiana)
c_giaponese = TipoCucina("giapponese")
print(c_giaponese)

r1 = Ristorante(
    nome="Da Mario",
    indirizzo=Indirizzo("Via Roma", "10", "00100"),
    partita_iva=PartitaIva("12345678901"),
    periodo_chiusura=set(),
    citta=roma,
    tipi_cucina={c_italiana, c_giaponese}
)

print(r1)
print("Citta -> ristoranti:", list(roma.links_ris_cit()))
print("Ristorante -> tipi:", list(r1.links_ris_tip()))
print("TipoCucina italiana -> ristoranti:", list(c_italiana.links_ris_tip()))


try:
    r2 = Ristorante(
        nome="Da Mario",
        indirizzo=Indirizzo("Via Milano", "5", "00100"),
        partita_iva=PartitaIva("10987654321"),
        periodo_chiusura=set(),
        citta=roma,
        tipi_cucina={c_italiana}
    )
except Exception as e:
    print("OK vincolo Ristorante:", e)

ostia = Citta("Ostia", lazio) 
r3 = Ristorante(
    nome="Da Mario",
    indirizzo=Indirizzo("Via Roma", "1", "20100"),
    partita_iva=PartitaIva("22222222222"),
    periodo_chiusura=set(),
    citta=ostia,
    tipi_cucina={c_italiana}
)
print("OK stesso nome altra città:", r3)




alice: Cliente = Cliente(nome="Alice", cognome="Bella", email=Email("alice@mail.com"))
print(alice)


p = Prenotazione(
    numero_commensali=IntGZ(2),
    data_ora_prenotata=datetime.now() + timedelta(days=1),
    cliente=alice,
    ristorante=r1
)
print(p)


print("Cliente -> prenotazioni:", list(alice.links_cl_pren()))
print("Ristorante -> prenotazioni:", list(r1.links_pren_ris()))
print("Navigazione:", list(alice.links_cl_pren())[0].prenotazione().link_pren_ris().ristorante())
