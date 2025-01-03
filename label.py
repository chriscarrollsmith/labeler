#!/usr/bin/env python3

import csv
import argparse
import sys

def fill_csv(csv_file_path):
    """
    Reads a CSV with one text column (assumed to be the first column) and
    any number of potentially empty columns. For each row that isn't fully
    populated, prompts the user to fill in missing values, then writes
    updated data back to the file.
    """
    # Read the CSV into memory.
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        data = list(reader)

    # Iterate over rows, asking for missing data.
    for row_index, row in enumerate(data):
        # Identify columns (besides the text column) that are missing data.
        missing_cols = [col for col in fieldnames[1:] if not row[col]]

        # If nothing is missing, skip this row.
        if not missing_cols:
            continue

        # Print the text column (assumed to be fieldnames[0]).
        text_value = row[fieldnames[0]]
        print(f"\nRow {row_index + 1} — Text: {text_value}")

        # For each missing column, prompt the user for input.
        for col in missing_cols:
            user_input = input(f"  Enter value for '{col}' (or 'q' to quit): ").strip()
            if user_input.lower() in ('q', 'quit'):
                print("Quitting early...")
                # Write all collected data so far back to the CSV, then exit.
                _write_csv(csv_file_path, fieldnames, data)
                sys.exit(0)
            # Fill in the value provided by the user.
            row[col] = user_input

    # If we finish filling everything without quitting, write to file.
    _write_csv(csv_file_path, fieldnames, data)
    print("\nAll missing fields have been filled.")


def _write_csv(csv_file_path, fieldnames, data):
    """
    Helper function to write data back into the CSV.
    """
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    parser = argparse.ArgumentParser(description="Fill empty CSV columns interactively.")
    parser.add_argument("csv_file", help="Path to the CSV file to fill.")
    args = parser.parse_args()

    fill_csv(args.csv_file)


if __name__ == "__main__":
    main()

