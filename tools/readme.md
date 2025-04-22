# Read Pickle Tool

A command-line utility for reading and displaying the contents of pickle files.

## Description

This tool reads pickle (.pkl) files and displays their contents. It supports both standard and pretty-printed output formats, and can direct output to either the console or a specified file.

## Usage

```
python tools/read_pickle.py INPUT_FILE [--pretty] [--output_file OUTPUT_FILE]
```

### Arguments

- `INPUT_FILE`: Path to the pickle file to read (must end with .pkl)
- `--pretty`: Enable pretty printing for more readable output
- `--output_file OUTPUT_FILE`: Save output to a file instead of printing to console

## Examples

### Basic usage - display pickle contents to console

```bash
python tools/read_pickle.py example_data/cit1.pkl
```

### Pretty-print the pickle contents to console

```bash
python tools/read_pickle.py example_data/cit1.pkl --pretty
```

### Save pretty-printed output to a file

```bash
python tools/read_pickle.py example_data/cit1.pkl --pretty --output_file output.txt
```