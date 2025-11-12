#!/usr/bin/env python3
"""
Helper script to replace ${username} variables in JSON files.
Works on Windows, macOS, and Linux.

Usage:
    python replace_username.py -f input.json -u myusername
    
Output:
    Creates a new file: input_replaced.json
"""

import sys
import argparse
import json
import os


def replace_username_in_json(json_content, username):
    return json_content.replace('${username}', username)


def get_output_filename(input_filename):
    name, ext = os.path.splitext(input_filename)
    return f"{name}_replaced{ext}"


def main():
    parser = argparse.ArgumentParser(
        description='Replace ${username} variables in JSON files'
    )
    
    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Input JSON file',
        type=str
    )
    
    parser.add_argument(
        '-u', '--username',
        required=True,
        help='Username to replace ${username} with',
        type=str
    )
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate JSON syntax before replacement
    try:
        temp_content = content.replace('${username}', 'temp_validation_user')
        json.loads(temp_content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax in '{args.file}'", file=sys.stderr)
        print(f"JSON Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    result = replace_username_in_json(content, args.username)
    
    try:
        json.loads(result)
    except json.JSONDecodeError as e:
        print(f"Error: Result is not valid JSON after replacement", file=sys.stderr)
        print(f"JSON Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    output_file = get_output_filename(args.file)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Success: Created '{output_file}' with username '{args.username}'")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()