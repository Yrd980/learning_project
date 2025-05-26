# LangGPT Prompt Generator

A specialized assistant for generating prompts in LangGPT format. This tool helps create structured, effective prompts following the LangGPT methodology.

## Features

- Generate prompts in LangGPT format
- Support for various prompt components (Role, Profile, Rules, etc.)
- Interactive prompt creation
- Export prompts in markdown format

## Installation

1. Clone this repository
2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate.fish (fish)
uv pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python langgpt_generator.py
```

Follow the interactive prompts to create your LangGPT format prompt.

## Project Structure

- `langgpt_generator.py`: Main script for prompt generation
- `prompt_templates/`: Contains template structures for different types of prompts
- `utils/`: Helper functions and utilities
