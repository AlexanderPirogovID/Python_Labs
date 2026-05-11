import json
import csv
from pathlib import Path


def generate():
    Path("data").mkdir(exist_ok=True)

    # Хороший JSON
    with open("data/good1.json", "w", encoding='utf-8') as f:
        json.dump([
            {"id": "t1", "amount": 100.5, "category": "IT", "date": "2023-10"},
            {"id": "t2", "amount": 500.0, "category": "HR", "date": "2023-10"}
        ], f)

    # Хороший CSV
    with open("data/good2.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "category", "date"])
        writer.writerow(["t3", "150.0", "IT", "2023-10-03"])

    # Ошибка бизнес-логики (отрицательная сумма)
    with open("data/bad_logic.json", "w", encoding='utf-8') as f:
        json.dump([
            {"id": "t4", "amount": -50.0, "category": "Sales", "date": "10-04"}
        ], f)

    # Ошибка структуры (не JSON)
    with open("data/bad_format.json", "w", encoding='utf-8') as f:
        f.write("This is not a JSON file")

    # Дубликат ID
    with open("data/duplicate.json", "w", encoding='utf-8') as f:
        json.dump([
            {"id": "t1", "amount": 200.0, "category": "IT", "date": "10-05"}
        ], f)

    print("Тестовые данные сгенерированы в папке data/")


if __name__ == "__main__":
    generate()
