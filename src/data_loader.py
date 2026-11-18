import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "student-por.csv")

def load_data(filepath=None):
    if filepath is None:
        filepath = CSV_PATH
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found at {filepath}")
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        data = list(reader)
    print(f"[SUCCESS] Loaded {len(data)} records across {len(data[0])} columns.")
    return data

if __name__ == "__main__":
    d = load_data()
    print("Columns:", list(d[0].keys()))
