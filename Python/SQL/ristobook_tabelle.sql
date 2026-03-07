-- Tipi di dato 

create type giorno as 
    enum ('Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica');

create type stato as 
    enum ('Pendente', 'Accettata', 'Rifiutata');

create domain string100_not_null as varchar(100)
    check (value is not null);

create domain int_gz_not_null as integer
    check (value is not null and value > 0);

create type indirizzo as (
    via string100_not_null,
    civico int_gz_not_null
);

create domain partitaiva as char(11)
    check (value ~ '[0-9]{11}'); 

create domain email as varchar(100)
    check (value ~ '^[a-z0-9!#$%&''*+/=?^_`{|}~-]+(\.[a-z0-9!#$%&''*+/=?^_`{|}~-]+)*@([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z0-9]([a-z0-9-]*[a-z0-9])?$');
   
create domain intgez as integer
    check (value >= 0);

-- tabelle

-- classe Nazione
create table nazione (
	nome varchar(100) primary key
);

-- classe Regione
create table regione (
	id integer primary key,
	nome varchar(100) not null,
	nazione varchar(100) not null,   -- accorpa reg_naz
	unique(nome, nazione),
	foreign key (nazione) 
        references nazione(nome)
);

-- classe Citta
create table citta (
	id integer primary key,
	nome varchar(100) not null,
	regione integer not null,   -- accorpa cit_reg
	unique (nome, regione),
	foreign key (regione) 
        references Regione(id)
);

-- classe OrarioGiorno
create table orariogiorno (
    id integer primary key,
    ora_inizio time not null,
    ora_fine time not null,
    giorno_settimana giorno not null,
    check (ora_inizio < ora_fine)    
    -- v.inclusione: OrariGiorno(id) occorre in orari(orario_giorno)  
); 

-- classe PeriodoChiusura
create table periodochiusura (
    id integer primary key,
    data_inizio date not null,    
    data_fine date not null,
    check (data_inizio < data_fine)
    -- v.inclusione: PeriodoChiusura(id) occorre in period_chius(periodo_chiusura)    
    -- v.inclusione: PeriodoChiusura(id) occorre in orari(periodo_chiusura)    
);

-- associazione og_pc,  tra OrarioGiorno - PeriodoChiusura
create table og_pc (
	orario_giorno integer not null,
	periodo_chiusura integer not null,
	primary key (orario_giorno, periodo_chiusura),
	foreign key (orario_giorno) 
        references OrarioGiorno(id),
	foreign key (periodo_chiusura) 
        references PeriodoChiusura(id)
);

-- classe TipoCucina
create table tipocucina (
    nome varchar(100) primary key
);

-- classe Ristorante
create table ristorante (
    id integer primary key,
    nome varchar(100) not null,
    citta integer not null,    -- accorpa ris_cit
    indirizzo indirizzo not null,
    partita_iva partitaIva not null,
    unique (nome, citta),
    foreiGn key (citta) 
        references citta(id)
    -- VINCOLI DI INCLUSIONE 
    -- v.inclusione: Ristorante(id) occorre in ris_tip(ristorante)     
    -- v.inclusione: Ristorante(id) occorre in period_chius(ristorante)
    -- v.inclusione: Ristorante(id) occorre in ris_citt(ristorante) 
);

-- associazione ris_pc,  tra PeriodoChiusura - Ristorante
create table ris_pc (
    ristorante integer not null,
    periodo_chiusura integer not null,
    primary key (ristorante, periodo_chiusura),
    foreign key (ristorante) 
        references ristorante(id),
    foreign key (periodo_chiusura) 
        references periodochiusura(id)
);

-- associazione ris_tip,  tra Ristoranta - TipoCucina
create table ris_tip (
    ristorante integer not null,
    tipo_cucina varchar(100) not null,
    primary key (ristorante, tipo_cucina),
    foreign key (ristorante) 
        references ristorante(id),
    foreign key (tipo_cucina) 
        references tipocucina(nome)
);

-- classe Cliente
create table cliente (
	email email primary key,
	nome varchar(100) not null,
	cognome varchar(100) not null
);

-- classe Prenotazione
create table prenotazione (
	id integer primary key,
	istante_creazione timestamp not null,
    numero_commensali intgez not null,
	data_ora_prenotata timestamp not null,
	stato stato not null default 'Pendente',
    istante_rifiuto timestamp,
    istante_accettazione timestamp,
    ristorante integer not null,  -- accorpa pren_ris 
    cliente email not null,   -- accorpa cl_pren
    check (istante_creazione < data_ora_prenotata),
    check (istante_rifiuto is null or (istante_creazione < istante_rifiuto)),   -- servono parentesi ?
    check (istante_accettazione is null or (istante_creazione < istante_accettazione)),
    -- vincoli esterni
    check ((stato = 'Pendente') = 
        (istante_rifiuto is null and istante_accettazione is null)
        ), 
    check ((stato = 'Accettata') =
        (istante_accettazione is not null and istante_rifiuto is null)
        ),
    check ((stato = 'Rifiutata') =
        (istante_rifiuto is not null and istante_accettazione is null)
        ),
    foreign key (ristorante) 
        references ristorante(id),
    foreign key (cliente) 
        references cliente(email)
);
