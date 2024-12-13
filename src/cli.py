#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from .generator import MarkdownTOCGenerator

def find_readme() -> Path:
    """Find the README.md file in the current directory."""
    current_dir = Path.cwd()
    readme_candidates = list(current_dir.glob('README.md')) + list(current_dir.glob('readme.md'))
    if readme_candidates:
        return readme_candidates[0]
    return None

def main():
    parser = argparse.ArgumentParser(
        description='Generate Table of Contents for Markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate TOC for a specific file
  markdown-toc path/to/your/README.md

  # Generate TOC with custom configuration
  markdown-toc path/to/your/README.md -c config.yaml

  # Save output to a different file
  markdown-toc path/to/your/README.md -o output.md

  # Auto-detect and process README.md in current directory
  markdown-toc

  # Show this help message
  markdown-toc --help
        """
    )
    
    parser.add_argument(
        'input_file', 
        nargs='?', 
        help='Input markdown file (defaults to README.md in current directory)',
        default=None
    )
    parser.add_argument(
        '-c', '--config', 
        help='Path to configuration file (YAML format)',
        default=None
    )
    parser.add_argument(
        '-o', '--output', 
        help='Output markdown file (defaults to input file)',
        default=None
    )
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # If no input file is specified, try to find README.md
    if args.input_file is None:
        readme_path = find_readme()
        if readme_path is None:
            print("Error: No README.md found in current directory and no input file specified.")
            print("Please specify a markdown file or run from a directory containing README.md")
            sys.exit(1)
        args.input_file = readme_path
    else:
        args.input_file = Path(args.input_file)

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Read input file
    try:
        with open(args.input_file, 'r') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Generate TOC
    try:
        toc_generator = MarkdownTOCGenerator(args.config)
        updated_content = toc_generator.generate_toc(markdown_content)
    except Exception as e:
        print(f"Error generating TOC: {e}")
        sys.exit(1)
    
    # Write output
    try:
        output_file = Path(args.output) if args.output else args.input_file
        with open(output_file, 'w') as f:
            f.write(updated_content)
        print(f"Table of Contents generated in {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
