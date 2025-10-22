# Creativity Score Analyzer

Analyze text characteristics using *wordfreq*: rarity, occurrence count, and a combined **feature score** (rarity × occurrence).
This tool visualizes how unique a piece of writing is through a simple table.

## Dependencies

* Python 3.x
* wordfreq
* tabulate
* regex

Tested on **Windows 11** (should also work on macOS and Linux).

## Setup

1. Install [Python](https://www.python.org/downloads/).
2. Open your terminal or command prompt and install the required packages:

```
pip install wordfreq tabulate regex
```

3. Clone this repository or download the files.

```
git clone https://github.com/AmyJapanese/Creativity-Score-Analyzer
cd Creativity-Score-Analyzer
```

## Usage

1. In the same directory as `creativityscore.py`, create a folder named `txtdata`.
2. Place your `.txt` files (English text only) inside the `txtdata/` folder.
3. Run the tool:

```
python creativityscore.py
```

4. The analysis results will be saved as `rare_words.md`.

## License

MIT License

## Copyright & Text Data

This repository does **not** include any text data.
Please put your own `.txt` files in the `txtdata/` folder before running the tool.
Make sure the texts you use are free of copyright restrictions or belong to you.

## Disclaimer

This tool is provided for educational and research purposes.
The author is **not responsible** for the content of user-provided texts or how the tool is used.
Please comply with copyright laws when analyzing any material.