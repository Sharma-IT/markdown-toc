# Markdown TOC Generator

A powerful and flexible command-line tool for automatically generating Tables of Contents in markdown files. The generator supports customisable header parsing and TOC formatting.

## Contents
1. [Features](#features)
    2. [Header Parsing](#header-parsing)
    3. [Link Generation](#link-generation)
    4. [Configuration](#configuration)
2. [Installation](#installation)
3. [Usage](#usage)
    4. [Basic Usage](#basic-usage)
    5. [With Configuration](#with-configuration)
    6. [Output Options](#output-options)
4. [Configuration Options](#configuration-options)
5. [Contributing](#contributing)
6. [License](#license)

## Features

### Header Parsing
- Automatic detection of markdown headers (H1-H6)
- Configurable header level inclusion
- Smart placement after H1 title and description
- Nested header support with proper indentation

### Link Generation
- GitHub-style markdown link generation
- Automatic handling of special characters
- Case-insensitive link formatting
- Space-to-hyphen conversion

### Configuration
- YAML-based configuration
- Customisable TOC title
- Flexible header level selection
- Extensible formatting options

## Installation

You can install the package directly from source:

```bash
pip install git+https://github.com/Sharma-IT/markdown-toc.git
```

Or install in development mode:

```bash
git clone https://github.com/Sharma-IT/markdown-toc.git
cd markdown-toc
pip install -e .
```

## Usage

### Basic Usage
Generate a TOC for README.md in current directory:
```bash
markdown-toc
```

Generate a TOC for a specific file:
```bash
markdown-toc path/to/your/README.md
```

Show help and examples:
```bash
markdown-toc --help
```

### With Configuration
Use a custom configuration file:
```bash
markdown-toc path/to/your/README.md -c config.yaml
```

Example configuration file (config.yaml):
```yaml
# Header levels to include (1-6)
header_levels: [2, 3]

# Title for the Table of Contents section
toc_title: '## Contents'

# Numbering style (currently only 'numeric' supported)
numbering_style: 'numeric'

# Link formatting style (currently only 'github' supported)
link_formatting: 'github'
```

### Output Options
Save to a different file:
```bash
markdown-toc path/to/your/README.md -o output.md
```

Check version:
```bash
markdown-toc --version
```

## Configuration Options

| Option | Description | Default | Values |
|--------|-------------|---------|---------|
| header_levels | Header levels to include | [2, 3] | List of integers 1-6 |
| toc_title | Title of TOC section | "## Table of Contents" | Any markdown header |
| numbering_style | Style of TOC numbering | "numeric" | "numeric" |
| link_formatting | Link format style | "github" | "github" |

## Contributing
Contributions are welcome. Please feel free to submit a Pull Request.

## License
MIT License, for more details see [LICENSE](LICENSE).
