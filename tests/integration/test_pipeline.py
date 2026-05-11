import csv
import logging
from unittest.mock import patch

from app.services.processor import DataProcessor
from main import run_pipeline


def test_csv_pipeline_with_mixed_data(tmp_path):
    test_csv = tmp_path / "data.csv"
    with open(test_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "category", "date"])
        writer.writerow(["1", "100", "IT", "2023-10-01"])     # Хорошая
        writer.writerow(["2", "-50", "IT", "2023-10-02"])     # Плохая (amount)
        writer.writerow(["3", "200", "Sales", "bad-date"])    # Плохая (date)

    processor = DataProcessor()
    raw_data = []
    with open(test_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append(row)

    for row in raw_data:
        try:
            processor.validate_and_aggregate([row], "data.csv")
        except Exception:
            pass

    # Assert
    result = processor.get_result()
    assert result == {"IT": 100.0}
    assert "Sales" not in result


@patch("pathlib.Path.replace")
def test_pipeline_disk_write_error(mock_replace, tmp_path, caplog):
    """
    Advanced Mocking: имитация блокировки записи на диск.
    Программа не должна упасть (крашнуться), она должна залогировать ошибку.
    """
    # Arrange: Настройка окружения
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    test_file = data_dir / "valid.csv"
    test_file.write_text("id,amount,category,date\n1,100,IT,2023-01-01")

    result_path = tmp_path / "result.json"

    # Имитируем системную ошибку прав доступа
    mock_replace.side_effect = PermissionError("Диск защищен от записи")

    # Act
    with caplog.at_level(logging.ERROR):
        run_pipeline(data_dir, result_path)

    # Assert: Проверяем, что краша не было, а лог записан
    assert "Ошибка сохранения результатов" in caplog.text
    assert "Диск защищен от записи" in caplog.text
