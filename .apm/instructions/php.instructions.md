---
description: Convenzioni per scrivere e modificare codice PHP.
applyTo: "**/*.php"
---

- Scrivi codice PHP chiaro e coerente con il progetto, preservando comportamento e compatibilita.
- I nomi delle variabili PHP iniziano con una lettera maiuscola dopo `$`: per esempio `$Nome`, `$TotaleOrdine`, `$Indice`.
- Applica la regola anche a parametri, variabili locali, globali, catture delle closure e variabili di ciclo. Le proprieta degli oggetti non sono variabili locali.
- Mantieni invariati `$this`, le superglobali e gli altri nomi imposti da PHP. Non rinominare alla cieca nomi imposti da framework, interfacce o codice esterno: valuta la compatibilita e segnala le eccezioni necessarie.
- Quando modifichi codice esistente, non rinominare variabili fuori dall'ambito richiesto; per una conversione usa la skill `convertire-standard-php`.
- Verifica la sintassi dei file PHP modificati e, quando disponibili, esegui i test pertinenti.
