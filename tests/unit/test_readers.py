import pytest
from app.core.exceptions import DataFormatError
from app.io.readers import CSVReader, JSONReader, get_reader


# --- Тесты для CSVReader ---

def test_csv_reader_success(tmp_path):
    """Успешное чтение валидного CSV файла."""
    d = tmp_path / "inputs"
    d.mkdir()
    p = d / "finances.csv"  # Реалистичное имя файла
    p.write_text("id,amount,category,date\n1,100,IT,2023-01-01", encoding="utf-8")

    reader = CSVReader()
    data = reader.read(p)
    assert len(data) == 1
    assert data[0]["id"] == "1"


def test_csv_reader_general_error(tmp_path):
    """Имитация системной ошибки при чтении CSV (передаем папку вместо файла)."""
    d = tmp_path / "inputs"
    d.mkdir()
    reader = CSVReader()
    with pytest.raises(DataFormatError, match="Ошибка чтения CSV"):
        reader.read(d)


# --- Тесты для JSONReader ---

def test_json_reader_success(tmp_path):
    """Успешное чтение валидного JSON файла."""
    d = tmp_path / "inputs"
    d.mkdir()
    p = d / "records.json"
    p.write_text('[{"id": "1", "amount": 200}]', encoding="utf-8")

    reader = JSONReader()
    data = reader.read(p)
    assert len(data) == 1
    assert data[0]["amount"] == 200


@pytest.mark.parametrize("file_content, expected_error_match", [
    ('{"id": "1"}', "должен содержать список"),  # Валидный JSON, но словарь
    ('{invalid_json]', "Ошибка парсинга JSON"),   # Синтаксическая ошибка JSON
])
def test_json_reader_format_errors(tmp_path, file_content, expected_error_match):
    """Проверка различных ошибок форматирования JSON."""
    d = tmp_path / "inputs"
    d.mkdir()
    p = d / "bad_data.json"
    p.write_text(file_content, encoding="utf-8")

    reader = JSONReader()
    with pytest.raises(DataFormatError, match=expected_error_match):
        reader.read(p)


def test_json_reader_general_error(tmp_path):
    """Имитация системной ошибки при чтении JSON (передаем папку)."""
    d = tmp_path / "inputs"
    d.mkdir()
    reader = JSONReader()
    with pytest.raises(DataFormatError, match="Ошибка чтения JSON"):
        reader.read(d)


# --- Тесты для паттерна Registry ---

@pytest.mark.parametrize("extension, expected_class", [
    (".csv", CSVReader),
    (".json", JSONReader),
    (".CSV", CSVReader),  # Проверка нечувствительности к регистру
])
def test_get_reader_success(extension, expected_class):
    """Проверка корректного выбора класса-чтеца."""
    reader = get_reader(extension)
    assert isinstance(reader, expected_class)


def test_get_reader_unsupported():
    """Проверка реакции фабрики на неизвестный формат."""
    with pytest.raises(DataFormatError, match="Неподдерживаемый формат"):
        get_reader(".xml")
