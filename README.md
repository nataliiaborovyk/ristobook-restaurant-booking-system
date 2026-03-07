# RistoBook – Sistema di Gestione Prenotazioni Ristoranti

## Overview

RistoBook è un sistema informativo progettato per gestire ristoranti, prenotazioni e informazioni geografiche (nazioni, regioni e città).

Il sistema permette di:

- registrare ristoranti e tipologie di cucina
- gestire clienti e prenotazioni
- organizzare ristoranti per città, regione e nazione
- verificare la disponibilità dei ristoranti
- esporre i dati tramite API REST

Il progetto implementa un modello a oggetti con vincoli di integrità e un semplice database persistente basato su file JSON.

---

# System Architecture

Il progetto è strutturato in diversi moduli principali:

### Data Model
Contiene le classi che rappresentano le entità del dominio:

- `Nazione`
- `Regione`
- `Citta`
- `Ristorante`
- `Cliente`
- `Prenotazione`
- `TipoCucina`

Le relazioni tra le entità sono implementate tramite classi di **associazione**.

### API REST
Il file principale espone diverse API tramite **Flask** per gestire le risorse del sistema. :contentReference[oaicite:2]{index=2}  

Le API permettono operazioni come:

- recupero delle nazioni
- creazione di nuove nazioni
- modifica e cancellazione
- gestione di regioni e città

### Persistence Layer

I dati del sistema vengono salvati in un file JSON che simula un piccolo database.

Il modulo `utils_ristobook` gestisce:

- caricamento dei dati
- salvataggio nel file JSON
- conversione degli oggetti in formato serializzabile. :contentReference[oaicite:3]{index=3}  

---

# Data Model

Il sistema rappresenta il dominio della prenotazione dei ristoranti tramite diverse entità.

## Struttura geografica

- **Nazione → Regione → Città**

Questo permette di organizzare i ristoranti in una gerarchia geografica.

## Ristoranti

Ogni ristorante ha:

- nome
- indirizzo
- partita IVA
- città
- tipologie di cucina
- periodi di chiusura.

Il sistema verifica anche che i periodi di chiusura non si sovrappongano.

## Clienti e prenotazioni

Un cliente può effettuare prenotazioni per un ristorante specifico.

Ogni prenotazione include:

- numero di commensali
- data e ora della prenotazione
- stato della prenotazione (pendente, accettata, rifiutata). :contentReference[oaicite:4]{index=4}  

---

# Key Features

Il sistema supporta diverse funzionalità principali:

### Gestione struttura geografica
- creazione di nazioni
- gestione regioni
- gestione città

### Gestione ristoranti
- registrazione ristoranti
- associazione a città
- gestione tipologie di cucina
- definizione dei periodi di chiusura

### Gestione prenotazioni
- creazione prenotazioni
- accettazione o rifiuto della prenotazione
- controllo della disponibilità del ristorante

### API REST
Il sistema espone endpoint REST per:

- GET
- POST
- PATCH
- DELETE

per gestire le diverse risorse.

---

# Tecnologie utilizzate

- Python
- Flask
- Programmazione Object-Oriented
- JSON come mock database
- Modellazione di sistemi informativi

---

# Contesto del progetto

Progetto sviluppato come esercizio accademico per lo studio di:

- progettazione orientata agli oggetti
- modellazione di sistemi informativi
- sviluppo di API REST in Python.