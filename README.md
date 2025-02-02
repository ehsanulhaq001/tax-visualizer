# Tax Visualizer

A Python tool to calculate and visualize different tax slabs using Plotly. This project can compute raw tax amounts and tax percentages, then create an interactive chart for comparison. You can also calculate the tax for a specific income.

## Features
- Compare raw tax vs. tax percentage for multiple slab configurations
- Command-line interface with optional theme selection (`--theme=white` or `--theme=dark`)
- Command-line interface with optional limit selection (`--limi=2500000`)
- Vectorized NumPy operations for efficiency

## Installation

1. Clone or download this repository.
2. `cd tax-visualizer`
3. (Optional) create a virtual environment, e.g. `python -m venv venv && source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Command-Line

```bash
python tax_visualizer.py <tax_slab_file1> [<tax_slab_file2> ...] [--theme=dark] [--limit=2500000]
```

```bash
python main.py <income> <tax_slab_file1>
```