# raw_variation

Calcola la variazione percentuale rispetto al valore basale per dati di visita in formato Excel.

## Funzionamento

Per ogni cartella-visita in `Input/`, e per ogni foglio di ogni file `.xlsx`, il modulo:

1. Identifica il valore basale della colonna (il minimo tra i valori positivi)
2. Calcola la variazione percentuale di ogni riga rispetto a quel basale
3. Salva in `Output/` due file per ogni foglio:
   - `*_originale.xlsx` — dati grezzi originali
   - `*_variazione_percentuale.xlsx` — variazioni percentuali

## Struttura

```
raw_variation/
├── raw_variation.py   # script principale
├── config.xml         # parametri di configurazione
├── requirements.txt   # dipendenze Python
├── Input/             # cartelle-visita con file .xlsx
└── Output/            # risultati generati
```

## Configurazione

Modifica `config.xml` per cambiare i percorsi di input/output o i parametri soglia:

```xml
<file_config>
    <input_path>./Input/</input_path>
    <output_path>./Output/</output_path>
</file_config>
```

## Utilizzo

```bash
pip install -r requirements.txt
python raw_variation.py
```

## Requisiti

Vedi `requirements.txt`. Dipendenze principali: `pandas`, `numpy`, `openpyxl`.
