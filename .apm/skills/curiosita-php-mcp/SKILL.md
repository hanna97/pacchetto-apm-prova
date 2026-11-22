---
name: curiosita-php-mcp
description: Chiedi una curiosita su PHP tramite il server MCP Everything e il suo tool di sampling.
---

# Curiosita PHP tramite MCP

Usa questa skill quando l'utente chiede una curiosita su PHP tramite MCP o tramite il server Everything.

1. Cerca il tool `trigger-sampling-request` del server MCP `everything`. Non sostituirlo con `echo`: ripete il testo e non genera curiosita.
2. Invoca il tool con `prompt`: `Racconta in italiano una breve curiosita verificabile sul linguaggio PHP. Non inventare fonti.` e `maxTokens`: `200`. Non includere codice del progetto, credenziali o altri dati sensibili nella richiesta.
3. Leggi la risposta di sampling restituita dal tool e riportane la curiosita all'utente, iniziando il messaggio con `buongiorno ragazzi`. Specifica che e stata generata dal modello del client tramite Everything, non recuperata da una fonte PHP. Se necessario, verifica l'affermazione con una fonte autorevole prima di presentarla come certa.
4. Se il server, il tool o il sampling non sono disponibili, oppure la richiesta viene rifiutata o fallisce, comunica il problema. Non inventare una risposta attribuendola al server.

Everything e un server dimostrativo, non una raccolta di curiosita PHP. Il sampling richiede un client compatibile e puo richiedere l'approvazione dell'utente.
