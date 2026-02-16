#!/usr/bin/env python3
"""
Utility script to locate and load the `Alex_emails_march_04.csv` dataset from the workspace.

Usage examples:
  # Run with defaults (searches for file in current folder and subfolders)
  python load_alex_emails.py

  # Specify a path and print 10 rows
  python load_alex_emails.py --path "./Alex_emails_march_04.csv" --head 10

  # Load with UTF-8 encoding and do not set index
  python load_alex_emails.py --encoding utf-8 --no-index
"""
from pathlib import Path
import argparse
import sys
import pandas as pd


def find_file_by_name(name: str, root: Path = Path('.')) -> Path | None:
    """Return a Path to the file if found by exact name or by pattern match, else None."""
    candidate = Path(name)
    if candidate.exists():
        return candidate
    # Search recursively for exact filename
    for p in root.rglob(name):
        return p
    # Search for files that include the name (case-insensitive)
    lowered = name.lower()
    for p in root.rglob('*.csv'):
        if lowered in p.name.lower():
            return p
    return None


def load_csv(path: Path, encoding: str = 'latin-1', index_col: str | None = 'email_id') -> pd.DataFrame:
    """Load CSV into a pandas DataFrame. Set index if index_col is present and provided."""
    df = pd.read_csv(path, encoding=encoding)
    if index_col and index_col in df.columns:
        df = df.set_index(index_col)
    return df


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Load Alex_emails_march_04 dataset')
    parser.add_argument('--path', '-p', help='Path to CSV file (optional). If omitted, script will search the workspace.')
    parser.add_argument('--encoding', '-e', default='latin-1', help="File encoding (default: latin-1)")
    parser.add_argument('--no-index', action='store_true', help='Do not set an index even if email_id column exists')
    parser.add_argument('--head', '-n', type=int, default=5, help='Show first N rows (default: 5). Use 0 to skip.')
    parser.add_argument('--save-pickle', '-s', help='Optional path to save DataFrame as a pickle file')
    args = parser.parse_args(argv)

    root = Path('.').resolve()
    if args.path:
        file_path = Path(args.path)
        if not file_path.exists():
            print(f"File not found at provided path: {file_path}")
            return 2
    else:
        target_name = 'Alex_emails_march_04.csv'
        found = find_file_by_name(target_name, root=root)
        if not found:
            print(f"Could not find '{target_name}' under {root}. Use --path to specify location.")
            return 3
        file_path = found

    print(f'Loading CSV: {file_path} (encoding={args.encoding})')
    try:
        df = load_csv(file_path, encoding=args.encoding, index_col=None if args.no_index else 'email_id')
    except Exception as exc:
        print('Error loading CSV:', exc)
        return 4

    print('\nDataFrame loaded successfully.')
    print('Shape:', df.shape)
    print('\nColumns:', list(df.columns))
    if args.head:
        print('\nShowing top rows:')
        print(df.head(args.head).to_string())

    if args.save_pickle:
        out = Path(args.save_pickle)
        df.to_pickle(out)
        print(f'Wrote DataFrame pickle to: {out}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
