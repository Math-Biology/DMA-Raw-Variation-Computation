# raw_variation

**Component Code:** `#L001-U015-P26.0234`

Computes the percentage variation relative to the baseline value for visit data in Excel format.

## How it works

For each visit folder in `Input/`, and for each sheet of every `.xlsx` file, the module:

1. Identifies the baseline value for each column (the minimum among all positive values)
2. Computes the percentage variation of each row relative to that baseline
3. Saves two files per sheet in `Output/`:
   - `*_original.xlsx` — raw original data
   - `*_percentage_variation.xlsx` — percentage variations

## Structure

```
raw_variation/
├── raw_variation.py   # main script
├── config.xml         # configuration parameters
├── requirements.txt   # Python dependencies
├── Input/             # visit folders containing .xlsx files
└── Output/            # generated results
```

## Configuration

Edit `config.xml` to change input/output paths or threshold parameters:

```xml
<file_config>
    <input_path>./Input/</input_path>
    <output_path>./Output/</output_path>
</file_config>
```

## Usage

```bash
pip install -r requirements.txt
python raw_variation.py
```

## Requirements

See `requirements.txt`. Main dependencies: `pandas`, `numpy`, `openpyxl`.
