"""
Data migration script for DecentraNode platform
"""

import sqlite3
import csv
import os

# Database configuration
DB_FILE = "decentranode.db"
CSV_EXPORT_DIR = "exports"
CSV_IMPORT_FILE = "imports/nodes.csv"

def export_to_csv(table_name):
    """
    Export table data to a CSV file.
    :param table_name: The name of the database table to export.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Fetch table data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        # Create export directory if it doesn't exist
        if not os.path.exists(CSV_EXPORT_DIR):
            os.makedirs(CSV_EXPORT_DIR)

        # Write data to CSV
        csv_file_path = os.path.join(CSV_EXPORT_DIR, f"{table_name}.csv")
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write column headers
            writer.writerows(rows)  # Write rows

        print(f"Exported {table_name} to {csv_file_path}")
    except sqlite3.Error as e:
        print(f"Error exporting {table_name}: {e}")
    finally:
        conn.close()

def import_from_csv(table_name):
    """
    Import data from a CSV file into a database table.
    :param table_name: The name of the database table to populate.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Read data from CSV
        with open(CSV_IMPORT_FILE, mode="r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            columns = next(reader)  # Read the header row
            rows = [tuple(row) for row in reader]

        # Insert data into the database
        placeholders = ", ".join(["?"] * len(columns))
        cursor.executemany(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", rows)
        conn.commit()

        print(f"Imported data into {table_name} from {CSV_IMPORT_FILE}")
    except sqlite3.Error as e:
        print(f"Error importing data into {table_name}: {e}")
    except FileNotFoundError:
        print(f"File {CSV_IMPORT_FILE} not found.")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Data Migration Tool")
    print("1. Export data to CSV")
    print("2. Import data from CSV")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        table = input("Enter the table name to export: ")
        export_to_csv(table)
    elif choice == "2":
        table = input("Enter the table name to import into: ")
        import_from_csv(table)
    else:
        print("Invalid choice. Exiting.")
