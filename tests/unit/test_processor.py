import pytest
from app.core.exceptions import ValidationError


@pytest.mark.parametrize("amount, expected_valid", [
    (0.01, True),         # Граничное валидное
    (500.0, True),        # Обычное значение
    (0, False),           # Невалидное (0)
    (-100.5, False),      # Невалидное (отрицательное)
    (2e9, False),         # Переполнение (слишком большое число)
    ("invalid", False),   # Строка вместо числа
])
def test_processor_amount_validation(
    processor, valid_transaction, amount, expected_valid
):
    """Тестирование валидации поля amount на граничных значениях."""
    # Arrange
    valid_transaction["amount"] = amount

    # Act & Assert
    if expected_valid:
        processor.validate_and_aggregate([valid_transaction], "test.json")
        assert "Sales" in processor.get_result()
    else:
        with pytest.raises(ValidationError):
            processor.validate_and_aggregate([valid_transaction], "test.json")


@pytest.mark.parametrize("date_str", ["2023/12/01", "01-12-2023", "random"])
def test_processor_invalid_date_format(
    processor, valid_transaction, date_str
):
    """Проверка выброса исключения при некорректном формате даты."""
    valid_transaction["date"] = date_str
    with pytest.raises(ValidationError, match="неверная дата"):
        processor.validate_and_aggregate([valid_transaction], "test.json")


def test_processor_garbage_data(processor):
    """Проверка, что система выбрасывает правильную ошибку на мусор."""
    garbage = [{"foo": "bar", "baz": 123}]
    with pytest.raises(ValidationError, match="нет обязательных полей"):
        processor.validate_and_aggregate(garbage, "garbage.json")


def test_processor_duplicate_ids(processor, valid_transaction):
    """Проверка логики дубликатов."""
    processor.validate_and_aggregate([valid_transaction], "f1.json")
    with pytest.raises(ValidationError, match="Дубликат ID"):
        processor.validate_and_aggregate([valid_transaction], "f2.json")
