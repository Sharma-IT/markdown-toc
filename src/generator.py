#!/usr/bin/env python3

import re
import argparse
import yaml
from typing import List, Dict, Optional
from pathlib import Path

class MarkdownTOCGenerator:
    def __init__(self, config=None):
        """Initialize TOC generator with optional config."""
        default_config = {
            'header_levels': [2],  # Default to H2 headers only
            'toc_title': '## Table of Contents',
            'indent_style': 'github'  # 'github' or 'nested'
        }
        
        self.config = default_config.copy()
        if config:
            self.config.update(config)

    def _load_config(self, config_path: str):
        """
        Load configuration from a YAML file.
        
        :param config_path: Path to the configuration file
        """
        try:
            with open(config_path, 'r') as config_file:
                user_config = yaml.safe_load(config_file)
                self.config.update(user_config)
        except FileNotFoundError:
            print(f"Warning: Configuration file {config_path} not found. Using default settings.")
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")

    def _convert_to_link(self, header_text: str) -> str:
        """
        Convert header text to GitHub-style markdown link.
        
        :param header_text: Original header text
        :return: Converted link
        """
        # Remove special characters and convert to lowercase
        link = re.sub(r'[^\w\s-]', '', header_text.lower())
        # Replace spaces with hyphens
        link = re.sub(r'\s+', '-', link)
        return link

    def _generate_toc(self, headers):
        """Generate table of contents from headers."""
        toc_lines = [self.config['toc_title']]

        if self.config['indent_style'] == 'github':
            # GitHub-friendly format
            for indent, number, text, link in headers:
                if indent == 0:
                    toc_lines.append(f"{number}. [{text}](#{link})")
                else:
                    toc_lines.append(f"   - [{text}](#{link})")
        else:
            # Nested numbering format
            current_section = [0] * 6  # Track numbering for up to 6 levels
            for indent, _, text, link in headers:
                # Update section numbers
                current_section[indent] += 1
                # Reset all deeper levels
                for i in range(indent + 1, 6):
                    current_section[i] = 0
                
                # Generate section number string (e.g., "1.2.3")
                section_nums = current_section[:indent + 1]
                section_number = '.'.join(str(n) for n in section_nums if n != 0)
                
                # Add indentation
                indent_spaces = '    ' * indent
                toc_lines.append(f"{indent_spaces}{section_number}. [{text}](#{link})")

        return '\n'.join(toc_lines)

    def generate_toc(self, markdown_content: str) -> str:
        """
        Generate Table of Contents for the given markdown content.
        
        :param markdown_content: Full markdown text
        :return: Markdown content with inserted TOC
        """
        # Split the content into lines
        lines = markdown_content.split('\n')
        
        # Find the first H1 header and its index
        h1_index = next((i for i, line in enumerate(lines) 
                         if line.startswith('# ') and not line.startswith('## ')), -1)
        
        if h1_index == -1:
            # If no H1 found, insert at the beginning
            h1_index = 0
            
        # Find all TOC sections and remove them
        i = 0
        while i < len(lines):
            if any(lines[i].strip() == title for title in ['## Table of Contents', '## Contents']):
                # Find the end of TOC (next header or empty line followed by header)
                j = i + 1
                while j < len(lines):
                    if re.match(r'^#+\s', lines[j]) or (j + 1 < len(lines) and lines[j].strip() == '' and re.match(r'^#+\s', lines[j + 1])):
                        break
                    j += 1
                lines = lines[:i] + lines[j:]
                i = 0  # Start over to catch any other TOCs
            else:
                i += 1
        
        # Find the end of the initial description (first header after H1)
        description_end = next((i for i in range(h1_index + 1, len(lines)) 
                                if re.match(r'^#+\s', lines[i])), h1_index + 1)
        
        # Clean up extra blank lines before TOC insertion
        while description_end > 0 and not lines[description_end - 1].strip():
            description_end -= 1

        # Find where to end the TOC (next header)
        content_start = next((i for i in range(description_end + 1, len(lines)) 
                            if re.match(r'^#+\s', lines[i])), len(lines))

        # Collect headers matching the configured levels
        headers = []
        current_h2 = None
        counter = 1
        for i, line in enumerate(lines[description_end:], start=description_end):
            # Check if line is a header and matches configured levels
            match = re.match(r'^(#+)\s(.+)$', line)
            if match:
                header_level = len(match.group(1))
                header_text = match.group(2)
                
                if header_level in self.config['header_levels'] and header_text.strip() != 'Table of Contents' and header_text.strip() != 'Contents':
                    if header_level == 2:
                        current_h2 = (header_text, self._convert_to_link(header_text))
                        headers.append((0, counter, header_text, self._convert_to_link(header_text)))
                        counter += 1
                    elif header_level == 3 and current_h2:
                        headers.append((1, counter, header_text, self._convert_to_link(header_text)))
                        counter += 1
        
        # Generate TOC
        toc_lines = self._generate_toc(headers)
        
        # Combine all sections with exactly one blank line between them
        result = []
        result.extend(lines[:description_end])
        result.append('')  # Single blank line before TOC
        result.extend(toc_lines.split('\n'))
        result.append('')  # Single blank line after TOC
        result.extend(lines[content_start:])
        
        # Remove any consecutive blank lines
        i = 0
        while i < len(result) - 1:
            if not result[i].strip() and not result[i + 1].strip():
                result.pop(i)
            else:
                i += 1
        
        return '\n'.join(result)
