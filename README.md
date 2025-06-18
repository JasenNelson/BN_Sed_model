# Bayesian Network for Sediment Quality Assessment

This repository contains a proof-of-concept Bayesian Network (BN) model for assessing sediment quality in British Columbia's aquatic ecosystems. The model demonstrates the relationships between sediment contaminants, environmental modifiers, and ecological effects.

## Features

- Probabilistic modeling of sediment contamination impacts
- Forward and backward inference capabilities
- Scenario analysis for different environmental conditions
- Built using Python and pgmpy

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/JasenNelson/BN_Sed_model.git
   cd BN_Sed_model
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the model:
```bash
python BN_Sed_model.py
```

## Project Structure

- `BN_Sed_model.py`: Main script containing the Bayesian Network implementation
- `requirements.txt`: List of Python dependencies
- `.gitignore`: Specifies intentionally untracked files to ignore

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
