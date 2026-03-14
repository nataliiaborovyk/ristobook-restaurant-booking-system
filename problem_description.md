# Problem Description – RistoBook System

This project was developed as part of a database design exercise based on a textual specification of a coworking management system.

This document contains the original textual description of the problem used as the starting point for the design of the CoLab system.

The text represents the initial specification of the system requirements provided for the database design project.

The following description has been kept unchanged in order to preserve the original problem statement from which the system model, UML diagrams and database schema were developed.

---

## Original Problem Description

Si vuole progettare e realizzare RistoBook, un’applicazione web per creare e gestire prenotazioni per ristoranti.

...

Il sistema deve permettere ai clienti di eﬀettuare prenotazioni presso i ristoranti iscritti, usufruendo, eventualmente, di promozioni. I ristoratori, invece, possono iscriversi per registrare i propri ristoranti e gestire le loro prenotazioni e le loro promozioni.

Dei clienti interessa conoscere il nome e l’indirizzo e-mail, mentre dei ristoranti interessa il nome, la partita IVA (una stringa numerica), l’indirizzo, la città e l’insieme di tipologie di cucina oﬀerte (scelte da una lista tenuta sotto controllo dallo staﬀ di RistoBook).

I clienti possono prenotare presso un ristorante speciﬁcando il giorno, l’ora e il numero di commensali. Le prenotazioni dei clienti devono essere confermate (o riﬁutate) dal personale incaricato dei rispettivi ristoranti, che devono poter accedere ad RistoBook tramite una interfaccia dedicata.

Uno dei punti di forza del modello di business di RistoBook è la possibilità per i ristoranti di oﬀrire e pubblicizzare scontistiche (dette promozioni ). In particolare, i ristoratori devono poter deﬁnire una promozione speciﬁcando una percentuale di sconto sulle prenotazioni consumate in un certo periodo di tempo. Tali promozioni sono valide per al massimo un certo numero di coperti al giorno.

Ad esempio, un ristorante potrebbe deﬁnire la seguente promozione: sconto del 20% sulle prenotazioni dalle 20 alle 22 da martedì 15 giugno 2022 a venerdì 18 giugno 2022, valido per al massimo 10 coperti al giorno. Un altro ristorante potrebbe deﬁnire invece una promozione del tipo: sconto del 25% sulle prenotazioni dalle 18 alle 19 di tutti i martedì e giovedì dal 1 ottobre al 31 dicembre 2022.
Al momento della prenotazione, il cliente può scegliere una delle promozioni ancora disponibili (anche nessuna, se lo desidera). 

Il sistema deve permettere ai ristoratori e ai clienti di gestire lo stato delle prenotazioni. In particolare, quando una prenotazione viene creata, questa è nello stato “pendente”. Il ristoratore può scegliere se accettarla o riﬁutarla. Quando il cliente usufruisce eﬀettivamente della prenotazione, questa viene contrassegnata come “completata”. Se, invece, il cliente non dovesse presentarsi al ristorante, il ristoratore contrassegnerà la prenotazione come “non utilizzata”. Inoltre, in ogni momento (prima del giorno ed ora prenotati) i clienti possono annullare le proprie prenotazioni, anche se già accettate. Inﬁne, in caso di tutto esaurito (o per altre ragioni, ad es. giorni di chiusura), il responsabile di un ristorante deve poter chiudere le prenotazioni per un certo lasso di tempo (ad es., una certa data e fascia oraria, o un’intera settimana): da quel momento in poi, RistoBook non consentirà più ai clienti di richiedere prenotazioni in quel lasso di tempo (a meno che il ristoratore non le riapra).

Il sistema deve oﬀrire, oltre quelle già descritte, le seguenti funzionalità ai suoi attori:
• Il sistema deve permettere ristoratori di RistoBook di calcolare alcune statistiche di utilizzo delle loro promozioni. In particolare, dato un periodo di tempo, RistoBook deve permettere calcolare, per ogni promozione del ristorante considerato, il numero medio di clienti al giorno (dove la media è calcolata sui giorni di validità della promozione) che ha utilizzato quella promozione in una prenotazione.
• Data una città x, un insieme di tipologie di cucina C, un tasso di sconto minimo s ed una data d, i clienti devono poter trovare quali sono i ristoranti nella città x che oﬀrono almeno una delle tipologie di cucina in C e prevedono promozioni con sconti di tasso almeno s nella data d ancora utilizzabili per il numero di coperti che sono interessati a prenotare

