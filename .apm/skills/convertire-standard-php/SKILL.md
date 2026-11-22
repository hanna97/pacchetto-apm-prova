---
name: convertire-standard-php
description: Converti codice PHP scritto con altre convenzioni allo standard di variabili con iniziale maiuscola, preservando comportamento e compatibilita.
---

# Convertire codice PHP

Usa questa skill quando l'utente chiede di adattare o migrare codice PHP allo standard del pacchetto.

1. Identifica i file e l'ambito richiesti; esamina il codice, i suoi utilizzi e i test prima di modificare.
2. Individua le variabili da rinominare in ogni ambito e scegli nomi con iniziale maiuscola dopo `$`, mantenendo il resto del nome quando possibile. Controlla prima eventuali collisioni: PHP distingue maiuscole e minuscole.
3. Rinomina dichiarazioni e utilizzi collegati, inclusi parametri, closure, `global`, riferimenti e interpolazioni, senza modificare testi o identificatori non correlati. Preferisci il refactoring consapevole della sintassi agli interventi globali con espressioni regolari.
4. Mantieni `$this`, le superglobali e i nomi imposti da PHP. Valuta prima i parametri usati con argomenti nominali, le API pubbliche, le variabili dinamiche, `compact`, `extract`, `$GLOBALS`, reflection, serializzazione, template e integrazioni esterne. Aggiorna i chiamanti nell'ambito autorizzato solo quando e sicuro; se non puoi garantire la compatibilita, lascia invariati i nomi interessati e segnala il problema.
5. Esegui `php -l` su ogni file PHP modificato e i test pertinenti disponibili. Controlla le modifiche, descrivi le eventuali eccezioni e riferisci esplicitamente le verifiche non eseguibili.

Non cambiare la logica, le proprieta o altri identificatori solo per uniformare lo stile. Non introdurre modifiche non richieste.
