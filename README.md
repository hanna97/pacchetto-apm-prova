# Standard personali

Pacchetto APM per GitHub Copilot con convenzioni per PHP, comunicazione e commit.

## Contenuto

- `.apm/instructions/`: istruzioni generali e per i file PHP.
- `.apm/skills/convertire-standard-php/`: conversione guidata di codice PHP esistente.
- `.apm/skills/lettera-php-ascii/`: genera un file ASCII art per ogni file PHP richiesto.
- `.apm/skills/curiosita-php-mcp/`: richiede una curiosita PHP tramite MCP.
- `.apm/agents/standard-php.agent.md`: agente specializzato in PHP.
- `.apm/prompts/convertire-php.prompt.md`: prompt per avviare la conversione.
- `.apm/hooks/standard.json`: promemoria Copilot all'avvio della sessione; richiede PHP nel PATH.
- `.apm/git-hooks/commit-msg`: controllo Git opzionale per questo repository.
- `apm.yml`: dichiara il server MCP dimostrativo Everything.
- `.mcp.json`: configura Everything per il Copilot di questo progetto.

Le variabili PHP iniziano con una maiuscola dopo `$`, per esempio `$Nome`. Restano invariati i nomi obbligatori come `$this` e le superglobali; i nomi legati a interfacce esterne o a usi dinamici richiedono una valutazione di compatibilita.

## Utilizzo

Distribuisci il pacchetto APM da un repository Git accessibile e installalo nel progetto destinatario:

```sh
apm install <proprietario>/<repository> --target copilot
apm compile --target copilot --force-instructions
```

In alternativa, per provarlo prima della pubblicazione, usa `apm install ../percorso-del-pacchetto --target copilot` da un progetto separato, seguito dallo stesso comando `apm compile`. APM distribuisce istruzioni, skill, agente, prompt e hook alle posizioni supportate dal target `copilot`. La compilazione con `--force-instructions` include anche le regole generali nel contesto del progetto, per le richieste in chat senza file associati. Riavvia la sessione Copilot e richiedi, per esempio, la conversione di un file PHP allo standard.

Il prompt e disponibile nelle sessioni Local di VS Code; nelle sessioni Copilot usa la skill tramite una richiesta in linguaggio naturale. Le istruzioni e il promemoria dell'hook guidano l'agente, ma non garantiscono da soli il rispetto delle regole. Gli hook dipendono anche dalle impostazioni e dalle autorizzazioni dell'ambiente.

Le regole generali valgono anche per codice, esempi e messaggi di commit generati in chat, pur senza modificare file o selezionare l'agente personalizzato. Il supporto dipende dal client e dalla modalita: per esempio, le istruzioni della chat non si applicano automaticamente ai suggerimenti inline dell'editor. Per la generazione dedicata dei messaggi di commit puo servire una configurazione specifica del client. Un modello o servizio esterno che non riceve queste istruzioni non le applichera automaticamente.

### ASCII art dei file PHP

Chiedi a Copilot di generare l'ASCII art dei file PHP desiderati, oppure esegui lo script della skill installata con Python 3:

```sh
python3 .agents/skills/lettera-php-ascii/scripts/genera_ascii.py percorso/file.php percorso/directory
```

Le directory vengono esplorate ricorsivamente, incluse quelle nascoste; le directory simboliche non vengono seguite e sono segnalate. Ogni file PHP UTF-8 produce accanto un file `<nome>.php.ascii.txt`: vengono contate solo le lettere ASCII `A-Z` e `a-z` nell'intero contenuto, inclusi commenti e stringhe; maiuscole e minuscole sono distinte e, in caso di parita, vince la prima lettera incontrata. Lo script non modifica i PHP, non sovrascrive i risultati esistenti e segnala eventuali errori.

### Curiosita PHP con MCP

Il pacchetto dichiara il server ufficiale di test `@modelcontextprotocol/server-everything` versione `2.3.1`. Occorrono Node.js 24 o superiore e `npx` nel PATH dell'ambiente che esegue il server; al primo avvio `npx` puo scaricare il pacchetto. Il server viene eseguito localmente e mette a disposizione strumenti dimostrativi: esamina e approva solo le operazioni desiderate. Tra questi, `get-env` puo esporre variabili d'ambiente al modello; non usarlo per condividere credenziali.

Questo progetto include `.mcp.json` per il Copilot di VS Code. In un progetto destinatario, APM 0.36.0 con target `copilot` genera `.github/mcp.json`; se Everything non compare nella sessione VS Code, aggiungi nel progetto destinatario questa configurazione nativa `.mcp.json`, unendola agli eventuali server gia presenti senza sovrascriverli:

```json
{
  "mcpServers": {
    "everything": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything@2.3.1"],
      "tools": ["*"]
    }
  }
}
```

Dopo l'installazione e l'eventuale approvazione del server in Copilot, chiedi: «Usa Everything per raccontarmi una curiosita su PHP». La skill usa `trigger-sampling-request`: Everything chiede una risposta al modello del client, non dispone di una propria fonte di curiosita PHP. Il sampling e deprecato nel protocollo MCP e richiede un client compatibile e l'eventuale approvazione per il server; se non e disponibile, la skill segnala il problema.

Il server e dichiarato direttamente nel pacchetto con `registry: false`. APM puo escluderlo quando il pacchetto e una dipendenza transitiva: in tal caso il progetto destinatario deve dichiararlo direttamente o valutare esplicitamente l'opzione di fiducia `--trust-transitive-mcp`.

Per verificare le definizioni del pacchetto:

```sh
apm compile --validate
apm compile --dry-run
```

Per verificare la distribuzione di tutte le primitive, installa il pacchetto in un progetto di prova separato: `apm install` in questo repository installa le sue dipendenze, non il pacchetto stesso.

## Controllo dei commit

Per attivare il controllo Git **in questo repository**, assicurati prima che `git config --get core.hooksPath` non indichi hook che vuoi mantenere, poi esegui:

```sh
chmod +x .apm/git-hooks/commit-msg
git config --local core.hooksPath .apm/git-hooks
```

L'hook rifiuta i messaggi la cui prima riga non inizia esattamente con `ragazzi buongiorno`. Git deve poter eseguire il file `.apm/git-hooks/commit-msg`. Se il filesystem non conserva il bit eseguibile, dopo aver aggiunto il file all'indice usa `git update-index --chmod=+x .apm/git-hooks/commit-msg` per registrarlo nel repository.

Questo hook Git non viene attivato o distribuito automaticamente da APM: nei progetti destinatari serve un controllo Git equivalente configurato separatamente. La configurazione e locale al repository e `git commit --no-verify` puo aggirare il controllo.
